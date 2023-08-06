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
QUndoCommand subclasses for modifying the project.

:authors: M. Marin (KTH)
:date:   12.2.2020
"""
from enum import IntEnum, unique
from PySide2.QtWidgets import QUndoCommand
from spine_engine.project_item.connection import Connection, Jump


@unique
class Id(IntEnum):
    """Id numbers for project commands."""

    JUMP_CONDITION = 1


class SpineToolboxCommand(QUndoCommand):
    successfully_undone = False
    """Flag to register the outcome of undoing a critical command, so toolbox can react afterwards."""

    @staticmethod
    def is_critical():
        """Returns True if this command needs to be undone before
        closing the project without saving changes.
        """
        return False


class SetItemSpecificationCommand(SpineToolboxCommand):
    def __init__(self, item, spec, old_spec):
        """Command to set the specification for a Tool.

        Args:
            item (ProjectItem): the Item
            spec (ProjectItemSpecification): the new spec
            old_spec (ProjectItemSpecification): the old spec
        """
        super().__init__()
        self.item = item
        self.spec = spec
        self.old_spec = old_spec
        self.setText(f"set specification of {item.name}")

    def redo(self):
        self.item.do_set_specification(self.spec)

    def undo(self):
        self.item.do_set_specification(self.old_spec)


class MoveIconCommand(SpineToolboxCommand):
    def __init__(self, icon, project):
        """Command to move icons in the Design view.

        Args:
            icon (ProjectItemIcon): the icon
            project (SpineToolboxProject): project
        """
        super().__init__()
        self._project = project
        self._previous_pos = {x.name(): x.previous_pos for x in icon.icon_group}
        self._current_pos = {x.name(): x.current_pos for x in icon.icon_group}
        if len(icon.icon_group) == 1:
            self.setText(f"move {next(iter(icon.icon_group)).name()}")
        else:
            self.setText("move multiple items")

    def redo(self):
        self._move_to(self._current_pos)

    def undo(self):
        self._move_to(self._previous_pos)

    def _move_to(self, positions):
        icon_group = set()
        for item_name, position in positions.items():
            icon = self._project.get_item(item_name).get_icon()
            icon.setPos(position)
            icon_group.add(icon)
        for icon in icon_group:
            icon.icon_group = icon_group
        representative = next(iter(icon_group))
        representative.update_links_geometry()
        representative.notify_item_move()


class SetProjectNameCommand(SpineToolboxCommand):
    def __init__(self, project, name):
        """Command to set the project name.

        Args:
            project (SpineToolboxProject): the project
            name (str): The new name
        """
        super().__init__()
        self.project = project
        self.redo_name = name
        self.undo_name = self.project.name
        self.setText("rename project")

    def redo(self):
        self.project.set_name(self.redo_name)

    def undo(self):
        self.project.set_name(self.undo_name)


class SetProjectDescriptionCommand(SpineToolboxCommand):
    def __init__(self, project, description):
        """Command to set the project description.

        Args:
            project (SpineToolboxProject): the project
            description (str): The new description
        """
        super().__init__()
        self.project = project
        self.redo_description = description
        self.undo_description = self.project.description
        self.setText("change project description")

    def redo(self):
        self.project.set_description(self.redo_description)

    def undo(self):
        self.project.set_description(self.undo_description)


class AddProjectItemsCommand(SpineToolboxCommand):
    def __init__(self, project, items_dict, item_factories, silent=True):
        """Command to add items.

        Args:
            project (SpineToolboxProject): the project
            items_dict (dict): a mapping from item name to item dict
            item_factories (dict): a mapping from item type to ProjectItemFactory
            silent (bool): If True, suppress messages
        """
        super().__init__()
        self._project = project
        self._items_dict = items_dict
        self._item_factories = item_factories
        self._silent = silent
        if not items_dict:
            self.setObsolete(True)
        elif len(items_dict) == 1:
            self.setText(f"add {next(iter(items_dict))}")
        else:
            self.setText("add multiple items")

    def redo(self):
        self._project.restore_project_items(self._items_dict, self._item_factories, self._silent)

    def undo(self):
        for item_name in self._items_dict:
            self._project.remove_item_by_name(item_name, delete_data=True)


class RemoveAllProjectItemsCommand(SpineToolboxCommand):
    def __init__(self, project, item_factories, delete_data=False):
        """Command to remove all items from project.

        Args:
            project (SpineToolboxProject): the project
            item_factories (dict): a mapping from item type to ProjectItemFactory
            delete_data (bool): If True, deletes the directories and data associated with the items
        """
        super().__init__()
        self._project = project
        self._item_factories = item_factories
        self._items_dict = {i.name: i.item_dict() for i in self._project.get_items()}
        self._connection_dicts = [c.to_dict() for c in self._project.connections]
        self._delete_data = delete_data
        self.setText("remove all items")

    def redo(self):
        for name in self._items_dict:
            self._project.remove_item_by_name(name, self._delete_data)

    def undo(self):
        self._project.restore_project_items(self._items_dict, self._item_factories, silent=True)
        for connection_dict in self._connection_dicts:
            self._project.add_connection(Connection.from_dict(connection_dict), silent=True)


class RemoveProjectItemsCommand(SpineToolboxCommand):
    def __init__(self, project, item_factories, item_names, delete_data=False):
        """Command to remove items.

        Args:
            project (SpineToolboxProject): The project
            item_factories (dict): a mapping from item type to ProjectItemFactory
            item_names (list of str): Item names
            delete_data (bool): If True, deletes the directories and data associated with the item
        """
        super().__init__()
        self._project = project
        self._item_factories = item_factories
        items = [self._project.get_item(name) for name in item_names]
        self._items_dict = {i.name: i.item_dict() for i in items}
        self._delete_data = delete_data
        connections = sum((self._project.connections_for_item(name) for name in item_names), [])
        unique_connections = {(c.source, c.destination): c for c in connections}.values()
        self._connection_dicts = [c.to_dict() for c in unique_connections]
        if not item_names:
            self.setObsolete(True)
        elif len(item_names) == 1:
            self.setText(f"remove {item_names[0]}")
        else:
            self.setText("remove multiple items")

    def redo(self):
        for name in self._items_dict:
            self._project.remove_item_by_name(name, self._delete_data)

    def undo(self):
        self._project.restore_project_items(self._items_dict, self._item_factories, silent=True)
        for connection_dict in self._connection_dicts:
            self._project.add_connection(Connection.from_dict(connection_dict), silent=True)


class RenameProjectItemCommand(SpineToolboxCommand):
    def __init__(self, project, previous_name, new_name):
        """Command to rename project items.

        Args:
            project (SpineToolboxProject): the project
            previous_name (str): item's previous name
            new_name (str): the new name
        """
        super().__init__()
        self._project = project
        self._previous_name = previous_name
        self._new_name = new_name
        self.setText(f"rename {self._previous_name} to {self._new_name}")

    def redo(self):
        box_title = f"Doing '{self.text()}'"
        if not self._project.rename_item(self._previous_name, self._new_name, box_title):
            self.setObsolete(True)

    def undo(self):
        box_title = f"Undoing '{self.text()}'"
        self.successfully_undone = self._project.rename_item(self._new_name, self._previous_name, box_title)

    @staticmethod
    def is_critical():
        return True


class AddConnectionCommand(SpineToolboxCommand):
    def __init__(self, project, source_name, source_position, destination_name, destination_position):
        """Command to add connection between project items.

        Args:
            project (SpineToolboxProject): project
            source_name (str): source item's name
            source_position (str): link's position on source item's icon
            destination_name (str): destination item's name
            destination_position (str): link's position on destination item's icon
        """
        super().__init__()
        self._project = project
        self._source_name = source_name
        self._destination_name = destination_name
        self._connection_dict = Connection(
            source_name, source_position, destination_name, destination_position
        ).to_dict()
        replaced_connection = self._project.find_connection(source_name, destination_name)
        self._replaced_connection_dict = replaced_connection.to_dict() if replaced_connection is not None else None
        self._connection_name = f"link from {source_name} to {destination_name}"

    def redo(self):
        if self._replaced_connection_dict is None:
            success = self._project.add_connection(Connection.from_dict(self._connection_dict))
            if not success:
                self.setObsolete(True)
        else:
            self._project.replace_connection(
                Connection.from_dict(self._replaced_connection_dict), Connection.from_dict(self._connection_dict)
            )
        action = "add" if self._replaced_connection_dict is None else "replace"
        self.setText(f"{action} {self._connection_name}")

    def undo(self):
        if self._replaced_connection_dict is None:
            connection = self._project.find_connection(self._source_name, self._destination_name)
            self._project.remove_connection(connection)
        else:
            connection = self._project.find_connection(self._source_name, self._destination_name)
            self._project.replace_connection(connection, Connection.from_dict(self._replaced_connection_dict))


class RemoveConnectionsCommand(SpineToolboxCommand):
    def __init__(self, project, connections):
        """Command to remove links.

        Args:
            project (SpineToolboxProject): project
            connections (list of Connection): the connections
        """
        super().__init__()
        self._project = project
        self._connections_dict = {(c.source, c.destination): c.to_dict() for c in connections}
        if not connections:
            self.setObsolete(True)
        elif len(connections) == 1:
            c = connections[0]
            self.setText(f"remove link from {c.source} to {c.destination}")
        else:
            self.setText("remove multiple links")

    def redo(self):
        for source, destination in self._connections_dict:
            connection = self._project.find_connection(source, destination)
            self._project.remove_connection(connection)

    def undo(self):
        for connection_dict in self._connections_dict.values():
            self._project.add_connection(Connection.from_dict(connection_dict), silent=True)


class AddJumpCommand(SpineToolboxCommand):
    def __init__(self, project, source_name, source_position, destination_name, destination_position):
        """Command to add a jump between project items.

        Args:
            project (SpineToolboxProject): project
            source_name (str): source item's name
            source_position (str): link's position on source item's icon
            destination_name (str): destination item's name
            destination_position (str): link's position on destination item's icon
        """
        super().__init__()
        self._project = project
        self._source_name = source_name
        self._destination_name = destination_name
        self._jump_dict = Jump(source_name, source_position, destination_name, destination_position).to_dict()
        replaced_jump = self._project.find_jump(source_name, destination_name)
        self._replaced_jump_dict = replaced_jump.to_dict() if replaced_jump is not None else None
        self._jump_name = f"jump from {source_name} to {destination_name}"

    def redo(self):
        if self._replaced_jump_dict is None:
            success = self._project.add_jump(Jump.from_dict(self._jump_dict))
            if not success:
                self.setObsolete(True)
        else:
            self._project.replace_jump(Jump.from_dict(self._replaced_jump_dict), Jump.from_dict(self._jump_dict))
        action = "add" if self._replaced_jump_dict is None else "replace"
        self.setText(f"{action} {self._jump_name}")

    def undo(self):
        if self._replaced_jump_dict is None:
            jump = self._project.find_jump(self._source_name, self._destination_name)
            self._project.remove_jump(jump)
        else:
            jump = self._project.find_jump(self._source_name, self._destination_name)
            self._project.replace_jump(jump, Jump.from_dict(self._replaced_jump_dict))


class RemoveJumpsCommand(SpineToolboxCommand):
    """Command to remove jumps."""

    def __init__(self, project, jumps):
        """
        Args:
            project (SpineToolboxProject): project
            jumps (list of Jump): the jumps
        """
        super().__init__()
        self._project = project
        self._jump_dicts = {(j.source, j.destination): j.to_dict() for j in jumps}
        if not jumps:
            self.setObsolete(True)
        elif len(jumps) == 1:
            j = jumps[0]
            self.setText(f"remove loop from {j.source} to {j.destination}")
        else:
            self.setText("remove multiple loops")

    def redo(self):
        for source, destination in self._jump_dicts:
            jump = self._project.find_jump(source, destination)
            self._project.remove_jump(jump)

    def undo(self):
        for jump_dict in self._jump_dicts.values():
            self._project.add_jump(Jump.from_dict(jump_dict), silent=True)


class SetJumpConditionCommand(SpineToolboxCommand):
    """Command to set jump condition."""

    def __init__(self, jump_properties, jump, condition):
        """
        Args:
            jump_properties (JumpPropertiesWidget): jump's properties tab
            jump (Jump): target jump
            condition (str): jump condition
        """
        super().__init__()
        self._jump_properties = jump_properties
        self._jump = jump
        self._condition = condition
        self._previous_condition = jump.condition
        self.setText("change loop condition")

    def id(self):
        return Id.JUMP_CONDITION

    def mergeWith(self, other):
        if not isinstance(other, SetJumpConditionCommand) or self._jump is not other._jump:
            return False
        self._condition = other._condition
        return True

    def redo(self):
        self._jump_properties.set_condition(self._jump, self._condition)

    def undo(self):
        self._jump_properties.set_condition(self._jump, self._previous_condition)


class SetFiltersOnlineCommand(SpineToolboxCommand):
    def __init__(self, resource_filter_model, resource, filter_type, online):
        """Command to toggle filter value.

        Args:
            resource_filter_model (ResourceFilterModel): filter model
            resource (str): resource label
            filter_type (str): filter type identifier
            online (dict): mapping from scenario/tool id to online flag
        """
        super().__init__()
        self._resource_filter_model = resource_filter_model
        self._resource = resource
        self._filter_type = filter_type
        self._online = online
        source_name = self._resource_filter_model.connection.source
        destination_name = self._resource_filter_model.connection.destination
        self.setText(f"change {filter_type} for {resource} at link from {source_name} to {destination_name}")

    def redo(self):
        self._resource_filter_model.set_online(self._resource, self._filter_type, self._online)

    def undo(self):
        negated_online = {id_: not online for id_, online in self._online.items()}
        self._resource_filter_model.set_online(self._resource, self._filter_type, negated_online)


class SetConnectionOptionsCommand(SpineToolboxCommand):
    def __init__(self, link, options):
        """Command to set connection options.

        Args:
            link (Link)
            options (dict): containing options to be set
        """
        super().__init__()
        self._link = link
        self._new_options = link.connection.options.copy()
        self._new_options.update(options)
        self._old_options = link.connection.options.copy()
        self.setText(f"change options in link {link.name}")

    def redo(self):
        self._link.set_connection_options(self._new_options)

    def undo(self):
        self._link.set_connection_options(self._old_options)


class AddSpecificationCommand(SpineToolboxCommand):
    def __init__(self, project, specification, save_to_disk):
        """Command to add item specification to a project.

        Args:
            project (ToolboxUI): the toolbox
            specification (ProjectItemSpecification): the spec
            save_to_disk (bool): If True, save the specification to disk
        """
        super().__init__()
        self._project = project
        self._specification = specification
        self._save_to_disk = save_to_disk
        self._spec_id = None
        self.setText(f"add specification {specification.name}")

    def redo(self):
        self._spec_id = self._project.add_specification(self._specification, save_to_disk=self._save_to_disk)
        if self._spec_id is None:
            self.setObsolete(True)
        else:
            self._save_to_disk = False

    def undo(self):
        self._project.remove_specification(self._spec_id)


class ReplaceSpecificationCommand(SpineToolboxCommand):
    def __init__(self, project, name, specification):
        """Command to replace item specification in project.

        Args:
            project (ToolboxUI): the toolbox
            name (str): the name of the spec to be replaced
            specification (ProjectItemSpecification): the new spec
        """
        super().__init__()
        self._project = project
        self._name = name
        self._specification = specification
        self._undo_name = specification.name
        self._undo_specification = self._project.get_specification(name)
        self.setText(f"replace specification {name} by {specification.name}")

    def redo(self):
        if not self._project.replace_specification(self._name, self._specification):
            self.setObsolete(True)

    def undo(self):
        self.successfully_undone = self._project.replace_specification(self._undo_name, self._undo_specification)

    @staticmethod
    def is_critical():
        return True


class RemoveSpecificationCommand(SpineToolboxCommand):
    def __init__(self, project, name):
        """Command to remove specs from a project.

        Args:
            project (SpineToolboxProject): the project
            name (str): specification's name
        """
        super().__init__()
        self._project = project
        self._specification = self._project.get_specification(name)
        self._spec_id = self._project.specification_name_to_id(name)
        self.setText(f"remove specification {self._specification.name}")

    def redo(self):
        self._project.remove_specification(self._spec_id)

    def undo(self):
        self._spec_id = self._project.add_specification(self._specification, save_to_disk=False)


class SaveSpecificationAsCommand(SpineToolboxCommand):
    def __init__(self, project, name, path):
        """Command to remove item specs from a project.

        Args:
            project (SpineToolboxProject): the project
            name (str): specification's name
            path (str): new specification file location
        """
        super().__init__()
        self._project = project
        self._path = path
        self._spec_id = self._project.specification_name_to_id(name)
        specification = self._project.get_specification(self._spec_id)
        self._previous_path = specification.definition_file_path
        self.setText(f"save specification {name} as")

    def redo(self):
        specification = self._project.get_specification(self._spec_id)
        specification.definition_file_path = self._path
        self._project.save_specification_file(specification)

    def undo(self):
        specification = self._project.get_specification(self._spec_id)
        specification.definition_file_path = self._previous_path
        self._project.save_specification_file(specification)
