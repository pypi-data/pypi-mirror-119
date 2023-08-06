######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
SpineDBFetcher class.

:authors: M. Marin (KTH)
:date:   13.3.2020
"""

import itertools
from collections import OrderedDict
from PySide2.QtCore import Signal, Slot, QObject
from spinetoolbox.helpers import busy_effect, signal_waiter, CacheItem

# FIXME: We need to invalidate cache here as user makes changes (update, remove)


class SpineDBFetcher(QObject):
    """Fetches content from a Spine database."""

    _fetch_more_requested = Signal(str, object, int)
    _fetch_all_requested = Signal(set, int)
    _fetch_all_finished = Signal()

    def __init__(self, db_mngr, db_map):
        """Initializes the fetcher object.

        Args:
            db_mngr (SpineDBManager): used for fetching
            db_map (DiffDatabaseMapping): The db to fetch
        """
        super().__init__()
        self._db_mngr = db_mngr
        self._db_map = db_map
        self._getters = {
            "object_class": self._db_mngr.get_object_classes,
            "relationship_class": self._db_mngr.get_relationship_classes,
            "parameter_definition": self._db_mngr.get_parameter_definitions,
            "object": self._db_mngr.get_objects,
            "relationship": self._db_mngr.get_relationships,
            "entity_group": self._db_mngr.get_entity_groups,
            "parameter_value": self._db_mngr.get_parameter_values,
            "parameter_value_list": self._db_mngr.get_parameter_value_lists,
            "alternative": self._db_mngr.get_alternatives,
            "scenario": self._db_mngr.get_scenarios,
            "scenario_alternative": self._db_mngr.get_scenario_alternatives,
            "feature": self._db_mngr.get_features,
            "tool": self._db_mngr.get_tools,
            "tool_feature": self._db_mngr.get_tool_features,
            "tool_feature_method": self._db_mngr.get_tool_feature_methods,
        }
        self._iterators = {item_type: getter(self._db_map) for item_type, getter in self._getters.items()}
        self.cache = {}
        self._fetched = {item_type: False for item_type in self._getters}
        self._can_fetch_more_cache = {}
        self.moveToThread(db_mngr.worker_thread)
        self._fetch_more_requested.connect(self._fetch_more)
        self._fetch_all_requested.connect(self._fetch_all)

    def cache_items(self, item_type, items):
        # NOTE: OrderedDict is so we can call `reversed()` in Python 3.7
        self.cache.setdefault(item_type, OrderedDict()).update({x["id"]: CacheItem(**x) for x in items})

    def get_item(self, item_type, id_):
        return self.cache.get(item_type, {}).get(id_, {})

    def _make_fetch_successful(self, parent):
        try:
            fetch_successful = parent.fetch_successful
        except AttributeError:
            return lambda _: True
        return lambda item: fetch_successful(self._db_map, item)

    def can_fetch_more(self, item_type, parent=None):
        if not self._fetched[item_type]:
            return True
        fetch_successful = self._make_fetch_successful(parent)
        items = self.cache.get(item_type, OrderedDict())
        try:
            key = (next(reversed(items), None), len(items))
            try:
                fetch_id = parent.fetch_id()
            except AttributeError:
                fetch_id = parent
            cache_key, cache_result = self._can_fetch_more_cache.get((item_type, fetch_id), (None, None))
            if key == cache_key:
                return cache_result
            result = any(fetch_successful(x) for x in items.values())
            self._can_fetch_more_cache[item_type, fetch_id] = (key, result)
            return result
        except RuntimeError:
            # OrderedDict mutated during iteration
            # This means the fetcher thread did something, and we need to start over
            return self.can_fetch_more(item_type, parent=parent)

    @busy_effect
    def fetch_more(self, item_type, parent=None, iter_chunk_size=1000):
        """Fetches items from the database.

        Args:
            item_type (str): the type of items to fetch, e.g. "object_class"
        """
        self._fetch_more_requested.emit(item_type, parent, iter_chunk_size)

    @Slot(str, object, int)
    def _fetch_more(self, item_type, parent, iter_chunk_size):
        self._do_fetch_more(item_type, parent, iter_chunk_size)

    @busy_effect
    def _do_fetch_more(self, item_type, parent, iter_chunk_size):
        iterator = self._iterators.get(item_type)
        if iterator is None:
            return
        fetch_successful = self._make_fetch_successful(parent)
        items = self.cache.get(item_type, {})
        args = [iter(items)] * iter_chunk_size
        for keys in itertools.zip_longest(*args):
            keys = set(keys) - {None}  # Remove fillvalues
            chunk = [items[k] for k in keys]
            if any(fetch_successful(x) for x in chunk):
                for k in keys:
                    del items[k]
                signal = self._db_mngr.added_signals[item_type]
                signal.emit({self._db_map: chunk})
                return
        while True:
            chunk = next(iterator, [])
            if not chunk:
                self._fetched[item_type] = True
                break
            if any(fetch_successful(x) for x in chunk):
                signal = self._db_mngr.added_signals[item_type]
                signal.emit({self._db_map: chunk})
                return
            self.cache_items(item_type, chunk)
        try:
            parent.fully_fetched.emit()
        except AttributeError:
            pass

    def fetch_all(self, item_types=None, only_descendants=False, include_ancestors=False, iter_chunk_size=1000):
        if item_types is None:
            item_types = set(self._getters)
        if only_descendants:
            item_types = {
                descendant
                for item_type in item_types
                for descendant in self._db_map.descendant_tablenames.get(item_type, ())
            }
        if include_ancestors:
            item_types |= {
                ancestor for item_type in item_types for ancestor in self._db_map.ancestor_tablenames.get(item_type, ())
            }
        if not any(self.can_fetch_more(item_type) for item_type in item_types):
            return
        with signal_waiter(self._fetch_all_finished) as waiter:
            self._fetch_all_requested.emit(item_types, iter_chunk_size)
            waiter.wait()

    @Slot(set, int)
    def _fetch_all(self, item_types, iter_chunk_size):
        self._do_fetch_all(item_types, iter_chunk_size)

    @busy_effect
    def _do_fetch_all(self, item_types, iter_chunk_size):
        class _Parent:
            def fetch_successful(self, *args):
                return False

        parent = _Parent()
        for item_type in item_types:
            self._do_fetch_more(item_type, parent, iter_chunk_size)
        self._fetch_all_finished.emit()
