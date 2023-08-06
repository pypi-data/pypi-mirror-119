"""
pytermgui.widget.base
---------------------
author: bczsalba


This submodule the basic elements this library provides.
"""

# These classes will have to have more than 7 attributes mostly.
# pylint: disable=too-many-instance-attributes

from __future__ import annotations

from copy import deepcopy
from inspect import signature
from dataclasses import dataclass, field
from typing import Callable, Optional, Type, Union, Iterator, Any

from ..input import keys
from ..parser import markup
from ..context_managers import cursor_at
from ..helpers import real_length, break_line
from ..exceptions import WidthExceededError, LineLengthError
from ..ansi_interface import terminal, clear, MouseEvent, MouseAction
from .styles import (
    CharType,
    StyleType,
    StyleCall,
    apply_markup,
    DepthlessStyleType,
    overrideable_style,
)


__all__ = ["MouseTarget", "MouseCallback", "Widget", "Container", "Label"]

MouseCallback = Callable[["MouseTarget", "Widget"], Any]
BoundCallback = Callable[["Widget", str], Any]


def _set_obj_or_cls_style(
    obj_or_cls: Union[Type[Widget], Widget], key: str, value: StyleType
) -> Union[Type[Widget], Widget]:
    """Set the style of an object or class"""

    if not key in obj_or_cls.styles.keys():
        raise KeyError(f"Style {key} is not valid for {obj_or_cls}!")

    if not callable(value):
        raise ValueError(f"Style {key} for {type(obj_or_cls)} has to be a callable.")

    obj_or_cls.styles[key] = value

    return obj_or_cls


def _set_obj_or_cls_char(
    obj_or_cls: Union[Type[Widget], Widget], key: str, value: CharType
) -> Union[Type[Widget], Widget]:
    """Set a char of an object or class"""

    if not key in obj_or_cls.chars.keys():
        raise KeyError(f"Char {key} is not valid for {obj_or_cls}!")

    obj_or_cls.chars[key] = value

    return obj_or_cls


@dataclass
class MouseTarget:
    """A target for mouse events."""

    # TODO: Support MouseTargets in nested contexts

    parent: Widget
    left: int
    right: int
    height: int
    top: int = 0

    _start: tuple[int, int] = field(init=False)
    _end: tuple[int, int] = field(init=False)

    onclick: Optional[MouseCallback] = None

    @property
    def start(self) -> tuple[int, int]:
        """Get object start"""

        return self._start

    @property
    def end(self) -> tuple[int, int]:
        """Get object end"""

        return self._end

    def adjust(self) -> None:
        """Adjust target positions to fit in whatever new positions we have"""

        pos = self.parent.pos
        self._start = (pos[0] + self.left - 1, pos[1] + 1 + self.top)
        self._end = (
            pos[0] + self.parent.width - 1 - self.right,
            pos[1] + self.top + self.height,
        )

    def contains(self, pos: tuple[int, int]) -> bool:
        """Check if button area contains pos"""

        start = self._start
        end = self._end

        return start[0] <= pos[0] <= end[0] and start[1] <= pos[1] <= end[1]

    def click(self, caller: Widget) -> None:
        """Execute callback with caller as the argument"""

        if self.onclick is None:
            return

        self.onclick(self, caller)

    def show(self, color: Optional[int] = None) -> None:
        """Print coordinates"""

        if color is None:
            color = 210

        for y_pos in range(self._start[1], self._end[1] + 1):
            with cursor_at((self._start[0], y_pos)) as print_here:
                length = self._end[0] - self._start[0]
                print_here(markup.parse(f"[@{color}]" + " " * length))


class Widget:
    """The widget from which all UI classes derive from"""

    set_style = classmethod(_set_obj_or_cls_style)
    set_char = classmethod(_set_obj_or_cls_char)

    OVERRIDE: StyleType = overrideable_style
    styles: dict[str, StyleType] = {}
    chars: dict[str, CharType] = {}
    keys: dict[str, set[str]] = {}

    serialized: list[str] = [
        "id",
        "pos",
        "depth",
        "width",
        "height",
        "forced_width",
        "forced_height",
        "selected_index",
        "selectables_length",
    ]

    # Alignment policies
    PARENT_LEFT = 0
    PARENT_CENTER = 1
    PARENT_RIGHT = 2
    DEFAULT_PARENT_ALIGN = PARENT_CENTER

    # Size policies
    SIZE_STATIC = 3
    SIZE_FILL = 4
    DEFAULT_SIZE_POLICY = SIZE_FILL

    # This class is loaded after this module,
    # and thus mypy doesn't see its existence.
    _id_manager: Optional["_IDManager"] = None  # type: ignore

    is_bindable = False
    size_policy = SIZE_FILL
    parent_align = PARENT_CENTER

    def __init__(self, **attrs: Any) -> None:
        """Initialize universal data for objects"""

        self.set_style = lambda key, value: _set_obj_or_cls_style(self, key, value)
        self.set_char = lambda key, value: _set_obj_or_cls_char(self, key, value)

        self.forced_width: Optional[int] = None
        self.forced_height: Optional[int] = None

        self._width: int = 0
        self.height = 1

        self.pos: tuple[int, int] = (1, 1)

        self.depth = 0

        self.selected_index: Optional[int] = None
        self.mouse_targets: list[MouseTarget] = []
        self.styles = type(self).styles.copy()
        self.chars = type(self).chars.copy()
        self.onclick: Optional[MouseCallback] = None

        self._serialized_fields = type(self).serialized
        self._selectables_length = 0
        self._id: Optional[str] = None

        self._bindings: dict[str, tuple[BoundCallback, str]] = {}

        for attr, value in attrs.items():
            setattr(self, attr, value)

    def __repr__(self) -> str:
        """Print self.debug() by default"""

        return self.debug()

    def __iter__(self) -> Iterator[Widget]:
        """Return self for iteration"""

        yield self

    @property
    def bindings(self) -> dict[str, tuple[BoundCallback, str]]:
        """Return copy of bindings dictionary"""

        return self._bindings.copy()

    @property
    def id(self) -> Optional[str]:  # pylint: disable=invalid-name
        """Getter for id property

        There is no better name for this."""

        return self._id

    @id.setter
    def id(self, value: str) -> None:  # pylint: disable=invalid-name
        """Register widget to idmanager

        There is no better name for this."""

        if self._id == value:
            return

        manager = Widget._id_manager
        assert manager is not None

        old = manager.get_id(self)
        if old is not None:
            manager.deregister(old)

        self._id = value
        manager.register(self)

    @property
    def width(self) -> int:
        """Getter for width property"""

        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Setter for width property"""

        if self.forced_width is not None and value is not self.forced_width:
            raise TypeError(
                "It is impossible to manually set the width "
                + "of an object with a `forced_width` attribute."
            )

        self._width = value

    @property
    def posx(self) -> int:
        """Return x position of object"""

        return self.pos[0]

    @posx.setter
    def posx(self, value: int) -> None:
        """Set x position of object"""

        if not isinstance(value, int):
            raise NotImplementedError("You can only set integers as object positions.")

        self.pos = (value, self.posy)

    @property
    def posy(self) -> int:
        """Return y position of object"""

        return self.pos[1]

    @posy.setter
    def posy(self, value: int) -> None:
        """Set y position of object"""

        if not isinstance(value, int):
            raise NotImplementedError("You can only set integers as object positions.")

        self.pos = (self.posx, value)

    @property
    def selectables_length(self) -> int:
        """Override this to return count of selectables of an object,
        defaults to attribute _selectables_length"""

        return self._selectables_length

    @property
    def is_selectable(self) -> bool:
        """Determine if this widget has any selectables.

        Shorthand for `Widget.selectables_length != 0`"""

        return self.selectables_length != 0

    @property
    def forced_width(self) -> Optional[int]:
        """Return forced/static width of object"""

        return self._forced_width

    @forced_width.setter
    def forced_width(self, value: Optional[int]) -> None:
        """Set forced width"""

        self._forced_width = value

        if value is not None:
            self.width = value

    def define_mouse_target(
        self, left: int, right: int, height: int, top: int = 0
    ) -> MouseTarget:
        """Define a mouse target, return it for method assignments"""

        target = MouseTarget(self, left, right, height, top)

        target.adjust()
        self.mouse_targets.insert(0, target)

        return target

    def get_target(self, pos: tuple[int, int]) -> Optional[MouseTarget]:
        """Get MouseTarget for a position"""

        for target in self.mouse_targets:
            if target.contains(pos):
                return target

        return None

    def handle_mouse(
        self, event: MouseEvent, target: MouseTarget | None = None
    ) -> bool:
        """Handle a mouse event, return True if success"""

        action, pos = event
        target = target or self.get_target(pos)

        if action is MouseAction.LEFT_CLICK:
            if target is None:
                return False

            target.click(self)
            return True

        return False

    def handle_key(self, key: str) -> bool:
        """Handle a keystroke, return True if success"""

        return not bool(key)

    def serialize(self) -> dict[str, Any]:
        """Serialize object based on type(object).serialized"""

        fields = self._serialized_fields

        out: dict[str, Any] = {"type": type(self).__name__}
        for key in fields:
            # Detect styled values
            if key.startswith("*"):
                style = True
                key = key[1:]
            else:
                style = False

            value = getattr(self, key)

            # Convert styled value into markup
            if style:
                style_call = self.get_style(key)
                if isinstance(value, list):
                    out[key] = [markup.get_markup(style_call(char)) for char in value]
                else:
                    out[key] = markup.get_markup(style_call(value))

                continue

            out[key] = value

        # The chars need to be handled separately
        out["chars"] = {}
        for key, value in self.chars.items():
            style_call = self.get_style(key)

            if isinstance(value, list):
                out["chars"][key] = [
                    markup.get_markup(style_call(char)) for char in value
                ]
            else:
                out["chars"][key] = markup.get_markup(style_call(value))

        return out

    def copy(self) -> Widget:
        """Copy widget into a new object"""

        return deepcopy(self)

    def get_style(self, key: str) -> DepthlessStyleType:
        """Try to get style"""

        style_method = self.styles[key]

        return StyleCall(self, style_method)

    def get_char(self, key: str) -> CharType:
        """Try to get char"""

        chars = self.chars[key]
        if isinstance(chars, str):
            return chars

        return chars.copy()

    def get_lines(self) -> list[str]:
        """Stub for widget.get_lines"""

        raise NotImplementedError(f"get_lines() is not defined for type {type(self)}.")

    def bind(
        self, key: str, action: BoundCallback, description: Optional[str] = None
    ) -> None:
        """Bind a key to a callable"""

        if not self.is_bindable:
            raise TypeError(f"Widget of type {type(self)} does not accept bindings.")

        if description is None:
            description = f"Binding of {key} to {action}"

        self._bindings[key] = (action, description)

    def execute_binding(self, key: str) -> bool:
        """Execute a binding if this widget is bindable

        True: binding found & execute
        False: binding not found"""

        # Execute special binding
        if keys.ANY_KEY in self._bindings:
            method, _ = self._bindings[keys.ANY_KEY]
            method(self, key)

        if key in self._bindings:
            method, _ = self._bindings[key]
            method(self, key)

            return True

        return False

    def select(self, index: int | None = None) -> None:
        """Select part of self"""

        if not self.is_selectable:
            raise TypeError(f"Object of type {type(self)} has no selectables.")

        if index is not None:
            index = min(max(0, index), self.selectables_length - 1)
        self.selected_index = index

    def get_container(self) -> Container:
        """Return Container including self"""

        container = Container() + self
        return container

    def show_targets(self, color: Optional[int] = None) -> None:
        """Show all mouse targets of this Widget"""

        for target in self.mouse_targets:
            target.show(color)

    def print(self) -> None:
        """Print object within a Container
        Overwrite this for Container-like widgets."""

        self.get_container().print()

    def debug(self) -> str:
        """Debug identifiable information about object"""

        constructor = "("
        for name in signature(getattr(self, "__init__")).parameters:
            current = ""
            if name == "attrs":
                current += "**attrs"
                continue

            if len(constructor) > 1:
                current += ", "

            current += name

            attr = getattr(self, name, None)
            if attr is None:
                continue

            current += "="

            if isinstance(attr, str):
                current += f'"{attr}"'
            else:
                current += str(attr)

            constructor += current

        constructor += ")"

        return type(self).__name__ + constructor


class Container(Widget):
    """The widget that serves as the outer parent to all other widgets"""

    # Centering policies
    CENTER_X = 6
    CENTER_Y = 7
    CENTER_BOTH = 8

    chars = {"border": ["| ", "-", " |", "-"], "corner": [""] * 4}
    styles = {"border": apply_markup, "corner": apply_markup}

    keys = {
        "navigation_up": {keys.UP, keys.CTRL_P, "k"},
        "navigation_down": {keys.DOWN, keys.CTRL_N, "j"},
    }

    serialized = Widget.serialized + ["_centered_axis"]

    def __init__(self, *widgets: Widget, **attrs: Any) -> None:
        """Initialize Container data"""

        super().__init__(**attrs)
        self._widgets: list[Widget] = []
        self._centered_axis: Optional[int] = None

        self._prev_screen: tuple[int, int] = (0, 0)

        self.styles = type(self).styles.copy()
        self.chars = type(self).chars.copy()

        for widget in widgets:
            self._add_widget(widget)

        self._drag_target: Widget | None = None

    @property
    def sidelength(self) -> int:
        """Returns length of left+right borders"""

        chars = self.get_char("border")
        style = self.get_style("border")
        if not isinstance(chars, list):
            return 0

        left_border, _, right_border, _ = chars
        return real_length(style(left_border) + style(right_border))

    @property
    def selectables(self) -> list[tuple[Widget, i]]:
        """Get all selectable widgets and their inner indexes"""

        _selectables: list[tuple[Widget, int]] = []
        for i, widget in enumerate(self._widgets):
            if not widget.is_selectable:
                continue

            _selectables.append((widget, i))

        return _selectables

    @property
    def selectables_length(self) -> int:
        """Get len(_selectables)"""

        return len(self.selectables)

    @property
    def selected(self) -> Optional[Widget]:
        """Return selected object"""

        # TODO: Add deeper selection

        if self.selected_index is None:
            return None

        if self.selected_index >= len(self.selectables):
            return None

        return self.selectables[self.selected_index][0]

    def __iadd__(self, other: object) -> Container:
        """Call self._add_widget(other) and return self"""

        self._add_widget(other)
        return self

    def __add__(self, other: object) -> Container:
        """Call self._add_widget(other)"""

        self.__iadd__(other)
        return self

    def __iter__(self) -> Iterator[Widget]:
        """Iterate through self._widgets"""

        for widget in self._widgets:
            yield widget

    def __len__(self) -> int:
        """Get length of widgets"""

        return len(self._widgets)

    def __getitem__(self, sli: Union[int, slice]) -> Union[Widget, list[Widget]]:
        """Index in self._widget"""

        return self._widgets[sli]

    def __setitem__(self, index: int, value: Any) -> None:
        """Set item in self._widgets"""

        self._widgets[index] = value

    def __contains__(self, other: object) -> bool:
        """Find if Container contains other"""

        return other in self._widgets

    def _add_widget(self, other: object, run_get_lines: bool = True) -> None:
        """Add other to self._widgets, convert using auto() if necessary"""

        if not isinstance(other, Widget):
            to_widget = Widget.from_data(other)
            if to_widget is None:
                raise ValueError(
                    f"Could not convert {other} of type {type(other)} to a Widget!"
                )

            other = to_widget

        if self.forced_width is not None and other.forced_width is not None:
            if self.forced_width < other.forced_width:
                raise ValueError(
                    "Object being added has a forced width that is larger than self."
                    + f" ({other.forced_width} > {self.forced_width})"
                )

        other.parent = self
        if other.forced_height is not None:
            other.height = other.forced_height

        # This is safe to do, as it would've raised an exception above already
        assert isinstance(other, Widget)

        self._widgets.append(other)
        if isinstance(other, Container):
            other.set_recursive_depth(self.depth + 2)
        else:
            other.depth = self.depth + 1

        other.get_lines()
        other.parent = self

        self.height += other.height

        if run_get_lines:
            self.get_lines()

    def _get_aligners(
        self, widget: Widget, borders: tuple[str, str]
    ) -> tuple[Callable[[str], str], int]:
        """Get aligner method & offset for alignment value"""

        left, right = borders

        def _align_left(text: str) -> str:
            """Align line left"""

            padding = self.width - real_length(left + right) - real_length(text)
            return left + text + padding * " " + right

        def _align_center(text: str) -> str:
            """Align line center"""

            total = self.width - real_length(left + right) - real_length(text)
            padding, offset = divmod(total, 2)
            return left + (padding + offset) * " " + text + padding * " " + right

        def _align_right(text: str) -> str:
            """Align line right"""

            padding = self.width - real_length(left + right) - real_length(text)
            return left + padding * " " + text + right

        if widget.parent_align is Widget.PARENT_CENTER:
            total = self.width - real_length(left + right) - widget.width
            padding, offset = divmod(total, 2)
            return _align_center, real_length(left) + padding + offset

        if widget.parent_align is Widget.PARENT_RIGHT:
            return _align_right, self.width - real_length(left) - widget.width

        # Default to left-aligned
        return _align_left, real_length(left)

    def _update_width(self, widget: Widget) -> None:
        """Update width of widget & self"""

        if widget.forced_width is not None and self.forced_width is not None:
            if widget.forced_width + self.sidelength > self.forced_width:
                raise WidthExceededError(
                    f"Widget {widget}'s forced_width value"
                    + f" ({widget.forced_width + self.sidelength})"
                    + f" is higher than its parent Container's ({self.forced_width})"
                )

        elif widget.forced_width is not None and self.forced_width is None:
            if widget.forced_width + self.sidelength > self.width:
                self.width = widget.forced_width + self.sidelength

        elif self.forced_width is None:
            self.width = max(self.width, widget.width + self.sidelength + 1)

    def get_lines(self) -> list[str]:  # pylint: disable=too-many-locals
        """Get lines of all widgets

        Note about pylint: Having less locals in this method would ruin readability."""

        def _apply_style(style: DepthlessStyleType, target: list[str]) -> list[str]:
            """Apply style to target list elements"""

            for i, char in enumerate(target):
                target[i] = style(char)

            return target

        # Get chars & styles
        corner_style = self.get_style("corner")
        border_style = self.get_style("border")

        border_char = self.get_char("border")
        assert isinstance(border_char, list)
        corner_char = self.get_char("corner")
        assert isinstance(corner_char, list)

        left, top, right, bottom = _apply_style(border_style, border_char)
        t_left, t_right, b_right, b_left = _apply_style(corner_style, corner_char)

        def _get_border(left: str, char: str, right: str) -> str:
            """Get a border line"""

            offset = real_length(left + right)
            return left + char * (self.width - offset) + right

        # Set up lines list
        lines: list[str] = []
        self.mouse_targets = []

        align, offset = self._get_aligners(self, (left, right))

        # Go through widgets
        for widget in self._widgets:
            # Update width
            if self.width == 0:
                self.width = widget.width

            # Fill container
            if (
                widget.size_policy == Widget.SIZE_FILL
                and widget.width < self.width
                and widget.forced_width is None
            ):
                widget.width = self.width - self.sidelength - 1

            self._update_width(widget)

            align, offset = self._get_aligners(widget, (left, right))
            widget.parent_offset = offset

            # TODO: This is ugly, and should be avoided.
            # For now, only Container has a top offset, but this should be
            # opened up as some kind of API for custom widgets.
            if type(widget).__name__ == "Container":
                container_vertical_offset = 1
            else:
                container_vertical_offset = 0

            widget.pos = (
                self.pos[0] + offset,
                self.pos[1] + len(lines) + container_vertical_offset,
            )

            widget_lines: list[str] = []

            for i, line in enumerate(widget.get_lines()):
                # Pad horizontally
                aligned = align(line)
                new = real_length(aligned)

                # Assert well formed lines
                if not new == self.width:
                    raise LineLengthError(
                        f"Widget {widget} returned a line of invalid length at index {i}:"
                        + f" ({new} != {self.width}): {aligned}"
                    )

                widget_lines.append(aligned)

            # Update height
            if widget.forced_height is None:
                widget.height = len(widget_lines)

            # Add to lines
            lines += widget_lines

            self.mouse_targets += widget.mouse_targets

        # Update height
        if self.forced_height is not None:
            for _ in range(self.forced_height - len(lines)):
                lines.append(align(""))
        else:
            self.height = len(lines) + 2

        # Add capping lines
        if real_length(top):
            lines.insert(0, _get_border(t_left, top, t_right))

        if real_length(bottom):
            lines.append(_get_border(b_left, bottom, b_right))

        for target in self.mouse_targets:
            target.adjust()

        # Return
        return lines

    def set_widgets(self, new: list[Widget]) -> None:
        """Set self._widgets to a new list"""

        self._widgets = []
        for widget in new:
            self._add_widget(widget)

    def serialize(self) -> dict[str, Any]:
        """Serialize object"""

        out = super().serialize()
        out["_widgets"] = []

        for widget in self._widgets:
            out["_widgets"].append(widget.serialize())

        return out

    def pop(self, index: int) -> Widget:
        """Pop widget from self._widgets"""

        return self._widgets.pop(index)

    def remove(self, other: Widget) -> None:
        """Remove widget from self._widgets"""

        return self._widgets.remove(other)

    def set_recursive_depth(self, value: int) -> None:
        """Set depth for all children, recursively"""

        self.depth = value
        for widget in self._widgets:
            if isinstance(widget, Container):
                widget.set_recursive_depth(value + 1)
            else:
                widget.depth = value

    def select(self, index: int | None = None) -> None:
        """Select inner object"""

        widget = None

        # Unselect all sub-elements
        for other in self._widgets:
            if other.selectables_length > 0:
                other.select(None)

                if isinstance(other, Container):
                    for sub in other:
                        if sub.selectables_length > 0:
                            sub.select(None)

        if index is not None:
            selectables = []
            for widget in self._widgets:
                for i in range(widget.selectables_length):
                    selectables.append((widget, i))

            index = min(max(0, index), len(selectables) - 1)

            data = selectables[index]
            if data is None:
                raise IndexError("Container selection index out of range")

            widget, inner_index = data
            widget.select(inner_index)

        self.selected_index = index

    def center(
        self, where: Optional[int] = CENTER_BOTH, store: bool = True
    ) -> Container:
        """Center object on given axis, store & reapply if `store`"""

        # Refresh in case changes happened
        self.get_lines()

        centerx = where in [Container.CENTER_X, Container.CENTER_BOTH]
        centery = where in [Container.CENTER_Y, Container.CENTER_BOTH]

        if centerx:
            self.posx = (terminal.width - self.width + 2) // 2

        if centery:
            self.posy = (terminal.height - self.height + 2) // 2

        if store:
            self._centered_axis = where

        self._prev_screen = terminal.size

        return self

    def handle_mouse(
        self, event: MouseEvent, target: MouseTarget | None = None
    ) -> bool:
        """Handle mouse event on our children"""

        def _get_widget(target: MouseTarget) -> Widget | None:
            """Try to get widget from its mouse target"""

            for widget in self._widgets:
                if target in widget.mouse_targets:
                    return widget

            return None

        action, pos = event
        target = target or self.get_target(pos)
        target_widget = self._drag_target or _get_widget(target)

        if action is MouseAction.LEFT_CLICK:
            self._drag_target = target_widget

        elif action is MouseAction.RELEASE:
            self._drag_target = None

        if target_widget is None:
            return False

        handled = target_widget.handle_mouse(event, target)
        if handled:
            for i, widget in enumerate(self.selectables):
                if target_widget is widget or target_widget in widget:
                    self.select(i)

        return handled

    def handle_key(self, key: str) -> bool:
        """Handle a keypress, return True if success"""

        def _is_nav(key: str) -> bool:
            """Determine if a key is in the navigation sets"""

            return key in self.keys["navigation_up"] | self.keys["navigation_down"]

        if self.selected is not None and self.selected.handle_key(key):
            return True

        # Only use navigation when there is more than one selectable
        if self.selectables_length > 1 and _is_nav(key):
            if self.selected_index is None:
                self.select(0)
                return True

            if key in self.keys["navigation_up"]:
                # No more selectables left, user wants to exit Container
                # upwards.
                if self.selected_index == 0:
                    return False

                self.select(self.selected_index - 1)
                return True

            if key in self.keys["navigation_down"]:
                self.select(self.selected_index + 1)
                return True

        if key == keys.ENTER and self.selected is not None:
            if self.selected.selected_index is not None:
                self.selected.mouse_targets[self.selected.selected_index].click(self)
                return True

        return False

    def wipe(self) -> None:
        """Wipe characters occupied by the object"""

        with cursor_at(self.pos) as print_here:
            for line in self.get_lines():
                print_here(real_length(line) * " ")

    def show_targets(self, color: Optional[int] = None) -> None:
        """Show all mouse targets of this Widget"""

        super().show_targets(color)

        for widget in self._widgets:
            widget.show_targets(color)

    def print(self) -> None:
        """Print object"""

        if not terminal.size == self._prev_screen:
            clear()
            self.center(self._centered_axis)

        self._prev_screen = terminal.size

        with cursor_at(self.pos) as print_here:
            for line in self.get_lines():
                print_here(line)

    def debug(self) -> str:
        """Return debug information about this object's widgets"""

        out = "Container("
        for widget in self._widgets:
            out += widget.debug() + ", "

        out = out.strip(", ")
        out += ", **attrs)"

        return out


class Label(Widget):
    """Unselectable text object"""

    styles: dict[str, StyleType] = {"value": apply_markup}

    serialized = Widget.serialized + ["*value", "align", "padding"]

    def __init__(self, value: str = "", padding: int = 0, **attrs: Any) -> None:
        """Set up object"""

        super().__init__(**attrs)

        self.value = value
        self.padding = padding
        self.width = real_length(value) + self.padding

    def get_lines(self) -> list[str]:
        """Get lines of object"""

        value_style = self.get_style("value")
        lines = break_line(value_style(self.padding * " " + self.value), self.width)

        return list(lines) or [""]
