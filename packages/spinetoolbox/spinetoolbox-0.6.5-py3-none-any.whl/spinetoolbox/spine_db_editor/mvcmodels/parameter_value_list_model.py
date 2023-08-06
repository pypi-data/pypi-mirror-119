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
A tree model for parameter_value lists.

:authors: M. Marin (KTH)
:date:   28.6.2019
"""

import json
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QIcon
from spinedb_api import to_database
from spinetoolbox.mvcmodels.shared import PARSED_ROLE
from .tree_model_base import TreeModelBase
from .tree_item_utility import (
    EmptyChildMixin,
    LastGrayMixin,
    AllBoldMixin,
    EditableMixin,
    NonLazyTreeItem,
    NonLazyDBItem,
)
from ...helpers import CharIconEngine


class DBItem(EmptyChildMixin, NonLazyDBItem):
    """An item representing a db."""

    def empty_child(self):
        return ListItem()


class ListItem(LastGrayMixin, AllBoldMixin, EditableMixin, NonLazyTreeItem):
    """A list item."""

    def __init__(self, identifier=None):
        super().__init__()
        self.id = identifier
        self._name = "Type new list name here..."

    @property
    def db_map(self):
        return self.parent_item.db_map

    @property
    def item_type(self):
        return "list"

    @property
    def name(self):
        if not self.id:
            return self._name
        try:
            return self.db_mngr.get_item(self.db_map, "parameter_value_list", self.id)["name"]
        except KeyError:
            return "<removed>"

    @property
    def value_list(self):
        if not self.id:
            return [child.value for child in self.children[:-1]]
        return self.db_mngr.get_parameter_value_list(self.db_map, self.id, role=Qt.EditRole)

    def fetch_more(self):
        self.db_mngr.fetch_more(self.db_map, "parameter_value_list")
        children = [ValueItem() for _ in self.value_list]
        self.append_children(children)
        if self.id:
            self.append_children([self.empty_child()])

    # pylint: disable=no-self-use
    def empty_child(self):
        return ValueItem(is_empty=True)

    def data(self, column, role=Qt.DisplayRole):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self.name
        if role == Qt.DecorationRole:
            engine = CharIconEngine("\uf022", 0)
            return QIcon(engine.pixmap())
        return super().data(column, role)

    def set_data(self, column, value, role=Qt.EditRole):
        if role != Qt.EditRole or value == self.name:
            return False
        if self.id:
            self.update_name_in_db(value)
            return True
        self._name = value
        self.parent_item.append_empty_child(self.child_number())
        self.append_children([self.empty_child()])
        return True

    def set_child_data(self, child, value):
        if value == child.value:
            return False
        if self.id:
            self.update_value_list_in_db(child, value)
        else:
            self.add_to_db(child, value)
        return True

    def update_name_in_db(self, name):
        db_item = dict(id=self.id, name=name)
        self.db_mngr.update_parameter_value_lists({self.db_map: [db_item]})

    def _new_value_list(self, child_number, value):
        value_list = self.value_list.copy()
        try:
            value_list[child_number] = value
        except IndexError:
            value_list.append(value)
        return value_list

    def update_value_list_in_db(self, child, value):
        value_list = self._new_value_list(child.child_number(), value)
        data = [(self.name, json.loads(value)) for value in value_list]
        self.db_mngr.import_data({self.db_map: {"parameter_value_lists": data}})

    def add_to_db(self, child, value):
        """Add item to db."""
        value_list = self._new_value_list(child.child_number(), value)
        db_item = dict(name=self.name, value_list=value_list)
        self.db_mngr.add_parameter_value_lists({self.db_map: [db_item]})

    def handle_updated_in_db(self):
        """Runs when an item with this id has been updated in the db."""
        self.update_value_list()

    def handle_added_to_db(self, identifier):
        """Runs when the item with this name has been added to the db."""
        self.id = identifier
        self.update_value_list()

    def update_value_list(self):
        value_count = len(self.value_list)
        curr_value_count = self.child_count() - 1
        if value_count > curr_value_count:
            added_count = value_count - curr_value_count
            children = [ValueItem() for _ in range(added_count)]
            self.insert_children(curr_value_count, children)
        elif curr_value_count > value_count:
            removed_count = curr_value_count - value_count
            self.remove_children(value_count, removed_count)


class ValueItem(LastGrayMixin, EditableMixin, NonLazyTreeItem):
    """A value item."""

    def __init__(self, is_empty=False):
        super().__init__()
        self._is_empty = is_empty
        self._fetched = True

    @property
    def item_type(self):
        return "value"

    @property
    def db_map(self):
        return self.parent_item.db_map

    @property
    def value(self):
        return self.db_mngr.get_value_list_item(self.db_map, self.parent_item.id, self.child_number(), Qt.EditRole)

    def data(self, column, role=Qt.DisplayRole):
        if role in (Qt.DisplayRole, Qt.EditRole, Qt.ToolTipRole, PARSED_ROLE):
            if self._is_empty:
                if role == PARSED_ROLE:
                    return None
                return "Enter new list value here..."
            return self.db_mngr.get_value_list_item(self.db_map, self.parent_item.id, self.child_number(), role)
        return super().data(column, role)

    def set_data(self, column, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        db_value, _ = to_database(value)
        return self.set_data_in_db(db_value)

    def set_data_in_db(self, db_value):
        return self.parent_item.set_child_data(self, db_value)


class ParameterValueListModel(TreeModelBase):
    """A model to display parameter_value_list data in a tree view."""

    def add_parameter_value_lists(self, db_map_data):
        for db_item, items in self._items_per_db_item(db_map_data).items():
            # First realize the ones added locally
            ids = {x["name"]: x["id"] for x in items}
            for list_item in db_item.children[:-1]:
                id_ = ids.pop(list_item.name, None)
                if not id_:
                    continue
                list_item.handle_added_to_db(identifier=id_)
            children = [ListItem(id_) for id_ in ids.values()]
            db_item.insert_children(db_item.child_count() - 1, children)

    def update_parameter_value_lists(self, db_map_data):
        for root_item, items in self._items_per_db_item(db_map_data).items():
            self._update_leaf_items(root_item, {x["id"] for x in items})

    def remove_parameter_value_lists(self, db_map_data):
        for root_item, items in self._items_per_db_item(db_map_data).items():
            self._remove_leaf_items(root_item, {x["id"] for x in items})

    @staticmethod
    def _make_db_item(db_map):
        return DBItem(db_map)

    @staticmethod
    def _top_children():
        return []

    def columnCount(self, parent=QModelIndex()):
        """Returns the number of columns under the given parent. Always 1.
        """
        return 1

    def index_name(self, index):
        return self.data(index.parent(), role=Qt.DisplayRole)

    def get_set_data_delayed(self, index):
        """Returns a function that ParameterValueEditor can call to set data for the given index at any later time,
        even if the model changes.

        Args:
            index (QModelIndex)

        Returns:
            Callable
        """
        item = self.item_from_index(index)
        return lambda value, item=item: item.set_data_in_db(value[0])
