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
Classes for drawing graphics items on QGraphicsScene.

:authors: M. Marin (KTH), P. Savolainen (VTT)
:date:    4.4.2018
"""

from math import atan2, sin, cos, pi
from PySide2.QtCore import Qt, Slot, QPointF, QLineF, QRectF, QVariantAnimation
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsTextItem,
    QGraphicsEllipseItem,
    QStyle,
    QToolTip,
)
from PySide2.QtGui import QColor, QPen, QBrush, QPainterPath, QLinearGradient, QFont
from PySide2.QtSvg import QGraphicsSvgItem, QSvgRenderer
from spinetoolbox.mvcmodels.resource_filter_model import ResourceFilterModel
from spinetoolbox.helpers import busy_effect
from .project_item_icon import ConnectorButton


class LinkBase(QGraphicsPathItem):
    """Base class for Link and LinkDrawer.

    Mainly provides the ``update_geometry`` method for 'drawing' the link on the scene.
    """

    def __init__(self, toolbox, src_connector, dst_connector):
        """
        Args:
            toolbox (ToolboxUI): main UI class instance
            src_connector (ConnectorButton, optional): Source connector button
            dst_connector (ConnectorButton): Destination connector button
        """
        super().__init__()
        self._toolbox = toolbox
        self.src_connector = src_connector
        self.dst_connector = dst_connector
        self.arrow_angle = pi / 4
        self.setCursor(Qt.PointingHandCursor)

    @property
    def magic_number(self):
        return 0.625 * self.src_rect.width()

    @property
    def src_rect(self):
        """Returns the scene rectangle of the source connector."""
        return self.src_connector.sceneBoundingRect()

    @property
    def src_center(self):
        """Returns the center point of the source rectangle."""
        return self.src_rect.center()

    @property
    def dst_rect(self):
        """Returns the scene rectangle of the destination connector."""
        return self.dst_connector.sceneBoundingRect()

    @property
    def dst_center(self):
        """Returns the center point of the destination rectangle."""
        return self.dst_rect.center()

    def moveBy(self, _dx, _dy):
        """Does nothing. This item is not moved the regular way, but follows the ConnectorButtons it connects."""

    def update_geometry(self, curved_links=None):
        """Updates geometry."""
        self.prepareGeometryChange()
        if curved_links is None:
            qsettings = self._toolbox.qsettings()
            curved_links = qsettings.value("appSettings/curvedLinks", defaultValue="false") == "true"
        guide_path = self._make_guide_path(curved_links)
        self.do_update_geometry(guide_path)

    def do_update_geometry(self, guide_path):
        """Sets the path for this item.

        Args:
            guide_path (QPainterPath)
        """
        ellipse_path = self._make_ellipse_path()
        connecting_path = self._make_connecting_path(guide_path)
        arrow_path = self._make_arrow_path(guide_path)
        path = ellipse_path + connecting_path + arrow_path
        self.setPath(path.simplified())

    def _make_ellipse_path(self):
        """Returns an ellipse path for the link's base.

        Returns:
            QPainterPath
        """
        ellipse_path = QPainterPath()
        rect = QRectF(0, 0, 1.6 * self.magic_number, 1.6 * self.magic_number)
        rect.moveCenter(self.src_center)
        ellipse_path.addEllipse(rect)
        return ellipse_path

    def _get_src_offset(self):
        return {"left": QPointF(-1, 0), "bottom": QPointF(0, 1), "right": QPointF(1, 0)}[self.src_connector.position]

    def _get_dst_offset(self, c1):
        if not self.dst_connector:
            guide_path = QPainterPath(self.src_center)
            guide_path.quadTo(c1, self.dst_center)
            line = self._get_joint_line(guide_path).unitVector()
            return QPointF(-line.dx(), -line.dy())
        return {"left": QPointF(-1, 0), "bottom": QPointF(0, 1), "right": QPointF(1, 0)}[self.dst_connector.position]

    def _make_guide_path(self, curved_links):
        """Returns a 'narrow' path connecting this item's source and destination.

        Args:
            curved_links (bool): Whether the path should follow a curved line or just a straight line

        Returns:
            QPainterPath
        """
        path = QPainterPath(self.src_center)
        if not curved_links:
            path.lineTo(self.dst_center)
            return path
        c_min = 2 * self.magic_number
        c_max = 8 * self.magic_number
        c_factor = QLineF(self.src_center, self.dst_center).length() / 2
        c_factor = min(c_factor, c_max)
        c_factor = max(c_factor, c_min)
        c1 = self.src_center + c_factor * self._get_src_offset()
        c2 = self.dst_center + c_factor * self._get_dst_offset(c1)
        path.cubicTo(c1, c2, self.dst_center)
        return path

    def _points_and_angles_from_path(self, path):
        """Returns a list of representative points and angles from given path.

        Args:
            path (QPainterPath)

        Returns:
            list(QPointF): points
            list(float): angles
        """
        count = min(int(100 * (1.0 - path.percentAtLength(self.src_rect.width() / 2))) + 2, 100)
        percents = [k / 100 for k in range(count)]
        points = list(map(path.pointAtPercent, percents))
        angles = list(map(path.angleAtPercent, percents))
        return points, angles

    def _make_connecting_path(self, guide_path):
        """Returns a 'thick' path connecting source and destination, by following the given 'guide' path.

        Args:
            guide_path (QPainterPath)

        Returns:
            QPainterPath
        """
        points, angles = self._points_and_angles_from_path(guide_path)
        outgoing_points = []
        incoming_points = []
        for point, angle in zip(points, angles):
            off = self._radius_from_point_and_angle(point, angle)
            outgoing_points.append(point + off)
            incoming_points.insert(0, point - off)
        p0 = guide_path.pointAtPercent(0)
        a0 = guide_path.angleAtPercent(0)
        off0 = self._radius_from_point_and_angle(p0, a0)
        curve_path = QPainterPath(p0 + off0)
        self._follow_points(curve_path, outgoing_points)
        curve_path.lineTo(incoming_points[0])
        self._follow_points(curve_path, incoming_points)
        curve_path.lineTo(p0 - off0)
        curve_path.closeSubpath()
        curve_path.setFillRule(Qt.WindingFill)
        return curve_path.simplified()

    @staticmethod
    def _follow_points(curve_path, points):
        points = iter(points)
        for p0 in points:
            p1 = next(points, None)
            if p1 is None:
                break
            curve_path.quadTo(p0, p1)

    def _radius_from_point_and_angle(self, point, angle):
        line = QLineF()
        line.setP1(point)
        line.setAngle(angle)
        normal = line.normalVector()
        normal.setLength(self.magic_number / 2)
        return QPointF(normal.dx(), normal.dy())

    def _make_arrow_path(self, guide_path):
        """Returns an arrow path for the link's tip.

        Args:
            guide_path (QPainterPath): A narrow path connecting source and destination,
                used to determine the arrow orientation.

        Returns:
            QPainterPath
        """
        angle = self._get_joint_angle(guide_path)
        arrow_p0 = self.dst_center
        d1 = QPointF(sin(angle + self.arrow_angle), cos(angle + self.arrow_angle))
        d2 = QPointF(sin(angle + (pi - self.arrow_angle)), cos(angle + (pi - self.arrow_angle)))
        arrow_diag = self.magic_number / sin(self.arrow_angle)
        arrow_p1 = arrow_p0 - d1 * arrow_diag
        arrow_p2 = arrow_p0 - d2 * arrow_diag
        arrow_path = QPainterPath(arrow_p1)
        arrow_path.lineTo(arrow_p0)
        arrow_path.lineTo(arrow_p2)
        arrow_path.closeSubpath()
        return arrow_path

    def _get_joint_line(self, guide_path):
        t = 1.0 - guide_path.percentAtLength(self.src_rect.width() / 2)
        t = max(t, 0.01)
        src = guide_path.pointAtPercent(t - 0.01)
        dst = guide_path.pointAtPercent(t)
        return QLineF(src, dst)

    def _get_joint_angle(self, guide_path):
        line = self._get_joint_line(guide_path)
        return atan2(-line.dy(), line.dx())


class _LinkIcon(QGraphicsEllipseItem):
    """An icon to show over a Link."""

    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h, parent)
        self._parent = parent
        color = QColor("slateblue")
        self.setBrush(qApp.palette().window())  # pylint: disable=undefined-variable
        self._text_item = QGraphicsTextItem(self)
        font = QFont('Font Awesome 5 Free Solid')
        self._text_item.setFont(font)
        self._text_item.setDefaultTextColor(color)
        self._svg_item = QGraphicsSvgItem(self)
        self._datapkg_renderer = QSvgRenderer()
        self._datapkg_renderer.load(":/icons/datapkg.svg")
        self.setFlag(QGraphicsItem.ItemIsSelectable, enabled=False)

    def update_icon(self):
        """Sets the icon (filter, datapkg, or none), depending on Connection state."""
        connection = self._parent.connection
        if connection.use_datapackage:
            self.setVisible(True)
            self._svg_item.setVisible(True)
            self._svg_item.setSharedRenderer(self._datapkg_renderer)
            scale = 0.8 * self.rect().width() / self._datapkg_renderer.defaultSize().width()
            self._svg_item.setScale(scale)
            self._svg_item.setPos(0, 0)
            self._svg_item.setPos(self.sceneBoundingRect().center() - self._svg_item.sceneBoundingRect().center())
            self._text_item.setVisible(False)
            return
        if connection.has_filters():
            self.setVisible(True)
            self._text_item.setVisible(True)
            self._text_item.setPlainText("\uf0b0")
            self._text_item.setPos(self.sceneBoundingRect().center() - self._text_item.sceneBoundingRect().center())
            self._svg_item.setVisible(False)
            return
        self.setVisible(False)
        self._text_item.setVisible(False)
        self._svg_item.setVisible(False)

    def wipe_out(self):
        """Cleans up icon's resources."""
        self._text_item.deleteLater()
        self._svg_item.deleteLater()
        self._datapkg_renderer.deleteLater()


class _JumpIcon(QGraphicsEllipseItem):
    """An icon to show over a JumpLink."""

    _NORMAL_COLOR = QColor("black")
    _ISSUE_COLOR = QColor("red")

    def __init__(self, x, y, w, h, jump_link):
        super().__init__(x, y, w, h, jump_link)
        self._jump_link = jump_link
        self.setBrush(qApp.palette().window())  # pylint: disable=undefined-variable
        self._text_item = QGraphicsTextItem(self)
        font = QFont('Font Awesome 5 Free Solid')
        self._text_item.setFont(font)
        self.setFlag(QGraphicsItem.ItemIsSelectable, enabled=False)
        self.setAcceptHoverEvents(True)

    def update_icon(self):
        """Sets the icon depending on Jump state."""
        issues = self._jump_link.issues()
        if issues:
            self._text_item.setDefaultTextColor(self._ISSUE_COLOR)
            self._text_item.setPlainText("\uf06a")
            self._text_item.setPos(
                self.sceneBoundingRect().center() - self._text_item.sceneBoundingRect().center() + QPointF(0.0, 0.5)
            )
            self.setToolTip(issues[0])
        else:
            self._text_item.setDefaultTextColor(self._NORMAL_COLOR)
            self._text_item.setPlainText("\uf1ce")
            self._text_item.setPos(
                self.sceneBoundingRect().center() - self._text_item.sceneBoundingRect().center() + QPointF(0.0, 0.5)
            )
            self.setToolTip("")

    def wipe_out(self):
        """Cleans up icon's resources."""
        self._text_item.deleteLater()
        self._renderer.deleteLater()

    def hoverEnterEvent(self, event):
        QToolTip.showText(event.screenPos(), self.toolTip())

    def hoverLeaveEvent(self, event):
        QToolTip.hideText()


class Link(LinkBase):
    """A graphics item to represent the connection between two project items."""

    _COLOR = QColor(255, 255, 0, 200)

    def __init__(self, toolbox, src_connector, dst_connector, connection):
        """
        Args:
            toolbox (ToolboxUI): main UI class instance
            src_connector (ConnectorButton): Source connector button
            dst_connector (ConnectorButton): Destination connector button
            connection (spine_engine.project_item.connection.Connection): connection this link represents
        """
        super().__init__(toolbox, src_connector, dst_connector)
        self._connection = connection
        self.selected_pen = QPen(Qt.black, 1, Qt.DashLine)
        self.normal_pen = QPen(Qt.black, 0.5)
        self._link_icon_extent = 4 * self.magic_number
        self._link_icon = _LinkIcon(0, 0, self._link_icon_extent, self._link_icon_extent, self)
        self._link_icon.setPen(self.normal_pen)
        self._link_icon.update_icon()
        self.setBrush(QBrush(self._COLOR))
        self.parallel_link = None
        self.setFlag(QGraphicsItem.ItemIsSelectable, enabled=True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, enabled=True)
        self.setZValue(0.5)  # This makes links appear on top of items because item zValue == 0.0
        self.update_geometry()
        self._exec_color = None
        self.resource_filter_model = ResourceFilterModel(self._connection, toolbox.undo_stack, toolbox)

    def refresh_resource_filter_model(self):
        """Makes resource filter mode fetch filter data from database."""
        self.resource_filter_model.build_tree()

    @busy_effect
    def set_connection_options(self, options):
        if options == self.connection.options:
            return
        self.connection.options = options
        self._link_icon.update_icon()
        item = self._toolbox.project_item_model.get_item(self.connection.source).project_item
        self._toolbox.project().notify_resource_changes_to_successors(item)
        if self is self._toolbox.active_link:
            self._toolbox.link_properties_widgets[Link].load_connection_options()

    @property
    def name(self):
        return self._connection.name

    @property
    def connection(self):
        return self._connection

    def do_update_geometry(self, guide_path):
        """See base class."""
        super().do_update_geometry(guide_path)
        center = guide_path.pointAtPercent(0.5)
        self._link_icon.setPos(center - 0.5 * QPointF(self._link_icon_extent, self._link_icon_extent))

    def make_execution_animation(self, excluded):
        """Returns an animation to play when execution 'passes' through this link.

        Returns:
            QVariantAnimation
        """
        colorname = "lightGray" if excluded else "red"
        self._exec_color = QColor(colorname)
        qsettings = self._toolbox.qsettings()
        duration = int(qsettings.value("appSettings/dataFlowAnimationDuration", defaultValue="100"))
        animation = QVariantAnimation()
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setDuration(duration)
        animation.valueChanged.connect(self._handle_execution_animation_value_changed)
        animation.finished.connect(lambda: self.setBrush(self._COLOR))
        animation.finished.connect(animation.deleteLater)
        return animation

    @Slot(object)
    def _handle_execution_animation_value_changed(self, step):
        gradient = QLinearGradient(self.src_center, self.dst_center)
        delta = 8 * self.magic_number / QLineF(self.src_center, self.dst_center).length()
        gradient.setColorAt(0, self._COLOR)
        gradient.setColorAt(max(0.0, step - delta), self._COLOR)
        gradient.setColorAt(step, self._exec_color)
        gradient.setColorAt(min(1.0, step + delta), self._COLOR)
        gradient.setColorAt(1.0, self._COLOR)
        self.setBrush(gradient)

    def mousePressEvent(self, e):
        """Ignores event if there's a connector button underneath,
        to allow creation of new links.

        Args:
            e (QGraphicsSceneMouseEvent): Mouse event
        """
        if any(isinstance(x, ConnectorButton) for x in self.scene().items(e.scenePos())):
            e.ignore()

    def contextMenuEvent(self, e):
        """Selects the link and shows context menu.

        Args:
            e (QGraphicsSceneMouseEvent): Mouse event
        """
        self.setSelected(True)
        self._toolbox.show_link_context_menu(e.screenPos(), self)

    def paint(self, painter, option, widget=None):
        """Sets a dashed pen if selected."""
        if option.state & QStyle.State_Selected:
            option.state &= ~QStyle.State_Selected
            self.setPen(self.selected_pen)
            self._link_icon.setPen(self.selected_pen)
        else:
            self.setPen(self.normal_pen)
            self._link_icon.setPen(self.normal_pen)
        super().paint(painter, option, widget)

    def shape(self):
        shape = super().shape()
        if self._link_icon.isVisible():
            shape.addEllipse(self._link_icon.sceneBoundingRect())
        return shape

    def itemChange(self, change, value):
        """Brings selected link to top."""
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange and value == 1:
            for item in self.collidingItems():  # TODO: try using scene().collidingItems() which is ordered
                if not isinstance(item, Link):
                    continue
                item.stackBefore(self)
            return value
        return super().itemChange(change, value)

    def wipe_out(self):
        """Removes any trace of this item from the system."""
        self._link_icon.wipe_out()
        self.src_connector.links.remove(self)
        self.dst_connector.links.remove(self)
        scene = self.scene()
        if scene:
            scene.removeItem(self)


class JumpLink(LinkBase):
    """A graphics icon to represent a jump connection between items."""

    def __init__(self, toolbox, src_connector, dst_connector, jump):
        """
        Args:
            toolbox (ToolboxUI): main UI class instance
            src_connector (ConnectorButton): Source connector button
            dst_connector (ConnectorButton): Destination connector button
            jump (spine_engine.project_item.connection.Jump): connection this link represents
        """
        super().__init__(toolbox, src_connector, dst_connector)
        self._jump = jump
        self.selected_pen = QPen(Qt.black, 1, Qt.DashLine)
        self.normal_pen = QPen(Qt.black, 0.5)
        self._icon_extent = 2.5 * self.magic_number
        self._icon = _JumpIcon(0, 0, self._icon_extent, self._icon_extent, self)
        self._icon.setPen(self.normal_pen)
        self._icon.update_icon()
        self._color = QColor(128, 0, 255, 200)
        brush = QBrush(self._color)
        self.setBrush(brush)
        self.setFlag(QGraphicsItem.ItemIsSelectable, enabled=True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, enabled=True)
        self.setZValue(0.6)
        self.update_geometry()
        self._exec_color = None

    @property
    def jump(self):
        return self._jump

    def issues(self):
        """Checks if jump is well-defined.

        Returns:
            list of str: issues regarding the jump
        """
        return self._toolbox.project().jump_issues(self.jump)

    def wipe_out(self):
        """Removes any trace of this item from the system."""
        self.src_connector.links.remove(self)
        self.dst_connector.links.remove(self)
        scene = self.scene()
        if scene:
            scene.removeItem(self)

    def do_update_geometry(self, guide_path):
        """See base class."""
        super().do_update_geometry(guide_path)
        center = guide_path.pointAtPercent(0.5)
        self._icon.setPos(center - 0.5 * QPointF(self._icon_extent, self._icon_extent))

    def contextMenuEvent(self, e):
        """Selects the link and shows context menu.

        Args:
            e (QGraphicsSceneMouseEvent): Mouse event
        """
        self.setSelected(True)
        self._toolbox.show_link_context_menu(e.screenPos(), self)

    def mousePressEvent(self, e):
        """Ignores event if there's a connector button underneath,
        to allow creation of new links.

        Args:
            e (QGraphicsSceneMouseEvent): Mouse event
        """
        if any(isinstance(x, ConnectorButton) for x in self.scene().items(e.scenePos())):
            e.ignore()

    def paint(self, painter, option, widget=None):
        """Sets a dashed pen if selected."""
        if option.state & QStyle.State_Selected:
            option.state &= ~QStyle.State_Selected
            self.setPen(self.selected_pen)
        else:
            self.setPen(self.normal_pen)
        super().paint(painter, option, widget)

    def make_execution_animation(self, excluded):
        """Returns an animation to play when execution 'passes' through this link.

        Returns:
            QVariantAnimation
        """
        animation = QVariantAnimation()
        animation.finished.connect(animation.deleteLater())
        return animation

    def update_geometry(self, curved_links=None):
        """Forces curved links."""
        super().update_geometry(curved_links=True)


class LinkDrawerBase(LinkBase):
    """A base class for items intended for drawing links between project items."""

    def __init__(self, toolbox):
        """
        Args:
            toolbox (ToolboxUI): main UI class instance
        """
        super().__init__(toolbox, None, None)
        self.tip = None
        self.setPen(QPen(Qt.black, 0.5))
        self.setZValue(1)  # A drawer should be on top of every other item.

    @property
    def src_rect(self):
        if not self.src_connector:
            return QRectF()
        return self.src_connector.sceneBoundingRect()

    @property
    def dst_rect(self):
        if not self.dst_connector:
            return QRectF()
        return self.dst_connector.sceneBoundingRect()

    @property
    def dst_center(self):
        if not self.dst_connector:
            return self.tip
        # If link drawer tip is on a connector button, this makes
        # the tip 'snap' to the center of the connector button
        return self.dst_rect.center()

    def add_link(self):
        """Makes link between source and destination connectors."""
        raise NotImplementedError()

    def wake_up(self, src_connector):
        """Sets the source connector, shows this item and adds it to the scene.
        After calling this, the scene is in link drawing mode.

        Args:
            src_connector (ConnectorButton): source connector
        """
        src_connector.scene().addItem(self)
        self.src_connector = src_connector
        self.tip = src_connector.sceneBoundingRect().center()
        self.update_geometry()
        self.show()

    def sleep(self):
        """Removes this drawer from the scene, clears its source and destination connectors, and hides it.
        After calling this, the scene is no longer in link drawing mode.
        """
        scene = self.scene()
        scene.removeItem(self)
        scene.link_drawer = self.src_connector = self.dst_connector = self.tip = None
        self.hide()


class ConnectionLinkDrawer(LinkDrawerBase):
    """An item for drawing connection links between project items."""

    def __init__(self, toolbox):
        """
        Args:
            toolbox (ToolboxUI): main UI class instance
        """
        super().__init__(toolbox)
        self.setBrush(QBrush(QColor(255, 255, 0, 100)))

    def add_link(self):
        self._toolbox.ui.graphicsView.add_link(self.src_connector, self.dst_connector)
        self.sleep()

    def wake_up(self, src_connector):
        super().wake_up(src_connector)
        self.src_connector.set_friend_connectors_enabled(False)

    def sleep(self):
        self.src_connector.set_friend_connectors_enabled(True)
        super().sleep()


class JumpLinkDrawer(LinkDrawerBase):
    """An item for drawing jump connections between project items."""

    def __init__(self, toolbox):
        """
        Args:
            toolbox (ToolboxUI): main UI class instance
        """
        super().__init__(toolbox)
        self.setBrush(QBrush(QColor(128, 0, 255, 100)))

    def add_link(self):
        self._toolbox.ui.graphicsView.add_jump(self.src_connector, self.dst_connector)
        self.sleep()
