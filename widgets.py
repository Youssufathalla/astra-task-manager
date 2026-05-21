"""Reusable custom Tkinter widgets used by Astra.

The classes here are mostly visual building blocks:
rounded frames, rounded buttons, custom entries, dropdowns, checkboxes, scrollbars,
and the progress bar.
"""

import tkinter as tk

from config import *
from utils import draw_rounded_rectangle

class RoundedFrame(tk.Canvas):
    """A Canvas that draws a rounded rectangle and places a normal Frame inside it."""

    def __init__(
        self,
        parent,
        bg,
        fill,
        radius=20,
        padding=14,
        width=100,
        height=100,
        outline=BORDER_GLOW,
        shadow=True
    ):
        super().__init__(parent, bg=bg, highlightthickness=0, bd=0, width=width, height=height)

        self.fill = fill
        self.radius = radius
        self.padding = padding
        self.outline = outline
        self.shadow = shadow

        self.inner = tk.Frame(self, bg=fill)
        self.window_id = self.create_window(padding, padding, window=self.inner, anchor="nw")

        self.bind("<Configure>", self.redraw)

    def redraw(self, event=None):
        self.delete("background")

        width = self.winfo_width()
        height = self.winfo_height()

        if self.shadow:
            draw_rounded_rectangle(
                self,
                4,
                5,
                width - 1,
                height - 1,
                self.radius,
                fill=SOFT_SHADOW,
                outline=SOFT_SHADOW,
                tags="background"
            )

        draw_rounded_rectangle(
            self,
            1,
            1,
            width - 4,
            height - 4,
            self.radius,
            fill=self.fill,
            outline=self.outline,
            tags="background"
        )

        self.tag_lower("background")
        self.itemconfig(
            self.window_id,
            width=max(1, width - self.padding * 2),
            height=max(1, height - self.padding * 2)
        )


class RoundedButton(tk.Canvas):
    """A rounded button made with Canvas so it looks modern in Tkinter."""

    def __init__(
        self,
        parent,
        text,
        command,
        bg=BLUE,
        hover_bg=BLUE_HOVER,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        width=110,
        height=42,
        radius=16
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )

        self.text = text
        self.command = command
        self.normal_bg = bg
        self.hover_bg = hover_bg
        self.current_bg = bg
        self.fg = fg
        self.font = font
        self.radius = radius
        self.disabled = False
        self.disabled_bg = DISABLED_BUTTON_BG
        self.disabled_fg = "#b8c7d9"

        self.draw()
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def draw(self):
        self.delete("all")

        width = int(self.cget("width"))
        height = int(self.cget("height"))
        fill = self.disabled_bg if self.disabled else self.current_bg
        fg = self.disabled_fg if self.disabled else self.fg

        draw_rounded_rectangle(self, 0, 0, width, height, self.radius, fill=fill, outline=fill)
        self.create_text(width // 2, height // 2, text=self.text, fill=fg, font=self.font)

    def on_enter(self, event=None):
        if not self.disabled:
            self.current_bg = self.hover_bg
            self.draw()

    def on_leave(self, event=None):
        if not self.disabled:
            self.current_bg = self.normal_bg
            self.draw()

    def on_click(self, event=None):
        if not self.disabled and self.command:
            self.command()

    def set_text(self, text):
        self.text = text
        self.draw()

    def set_colors(self, bg, hover_bg):
        self.normal_bg = bg
        self.hover_bg = hover_bg
        self.current_bg = bg
        self.draw()

    def set_disabled(self, disabled):
        self.disabled = disabled
        self.draw()


class RoundedEntry(tk.Canvas):
    """A rounded text input with placeholder behavior."""

    def __init__(self, parent, placeholder, font, width=170, height=42, radius=16):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0
        )

        self.placeholder = placeholder
        self.placeholder_visible = False
        self.font = font
        self.radius = radius
        self.enabled = True
        self.normal_bg = INPUT_BG
        self.disabled_bg = DISABLED_BG

        self.entry = tk.Entry(
            self,
            font=font,
            bg=self.normal_bg,
            fg=TEXT_MUTED,
            insertbackground=WHITE,
            disabledbackground=self.disabled_bg,
            disabledforeground=TEXT_FADED,
            relief="flat",
            bd=0
        )

        self.entry_window = self.create_window(14, height // 2, window=self.entry, anchor="w")
        self.show_placeholder()

        self.entry.bind("<FocusIn>", self.hide_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.bind("<KeyPress>", self.prepare_for_typing)
        self.bind("<Button-1>", lambda event: self.entry.focus_set())
        self.bind("<Configure>", self.redraw)

    def redraw(self, event=None):
        self.delete("background")

        width = self.winfo_width()
        height = self.winfo_height()
        fill = self.normal_bg if self.enabled else self.disabled_bg

        draw_rounded_rectangle(
            self,
            0,
            0,
            width,
            height,
            self.radius,
            fill=fill,
            outline=fill,
            tags="background"
        )

        self.tag_lower("background")
        self.itemconfig(self.entry_window, width=max(1, width - 28), height=max(1, height - 10))
        self.entry.config(bg=fill)

    def show_placeholder(self):
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=TEXT_MUTED)
        self.placeholder_visible = True

        if not self.enabled:
            self.entry.config(state="disabled")

    def hide_placeholder(self, event=None):
        if self.placeholder_visible and self.enabled:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=WHITE)
            self.placeholder_visible = False

    def prepare_for_typing(self, event=None):
        if self.placeholder_visible:
            self.hide_placeholder()

    def restore_placeholder(self, event=None):
        if self.enabled and self.entry.get().strip() == "":
            self.show_placeholder()

    def get_value(self):
        if self.placeholder_visible:
            return ""
        return self.entry.get().strip()

    def set_value(self, value):
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)

        if value:
            self.entry.insert(0, value)
            self.entry.config(fg=WHITE)
            self.placeholder_visible = False
        else:
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=TEXT_MUTED)
            self.placeholder_visible = True

        if not self.enabled:
            self.entry.config(state="disabled")

    def clear(self):
        self.set_value("")

    def set_enabled(self, enabled):
        self.enabled = enabled

        if enabled:
            self.entry.config(state="normal")
            self.entry.config(fg=TEXT_MUTED if self.placeholder_visible else WHITE)
        else:
            self.entry.config(state="disabled")

        self.redraw()

    def bind_key(self, sequence, function):
        self.entry.bind(sequence, function)


class ModernDropdown:
    """A custom dropdown made from a RoundedButton and a popup menu."""

    def __init__(self, parent, values, font, width=150):
        self.parent = parent
        self.values = values
        self.selected_value = values[0] if values else ""
        self.font = font
        self.width = width
        self.popup = None

        self.button = RoundedButton(
            parent,
            text=self.selected_value + "  ▾",
            command=self.open_menu,
            bg=INPUT_BG,
            hover_bg=GRAY_BUTTON,
            fg=WHITE,
            font=font,
            width=width,
            height=42,
            radius=16
        )

    def grid(self, **kwargs):
        self.button.grid(**kwargs)

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def get(self):
        return self.selected_value

    def set(self, value):
        self.selected_value = value
        self.button.set_text(value + "  ▾")

    def update_values(self, values):
        self.values = values

        if self.selected_value not in values and values:
            self.set(values[0])

    def set_enabled(self, enabled):
        self.button.set_disabled(not enabled)

    def open_menu(self):
        if self.button.disabled:
            return

        if self.popup:
            self.popup.destroy()

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height() + 4
        item_height = 38
        popup_height = min(len(self.values) * item_height + 14, 330)
        popup_width = self.width + 24

        self.popup = tk.Toplevel(self.button)
        self.popup.overrideredirect(True)
        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        self.popup.configure(bg=APP_BG)
        self.popup.attributes("-topmost", True)

        shell = RoundedFrame(
            self.popup,
            bg=APP_BG,
            fill=CATEGORY_PANEL_BG,
            radius=18,
            padding=7,
            width=popup_width,
            height=popup_height
        )
        shell.pack(fill="both", expand=True)

        for value in self.values:
            item = tk.Label(
                shell.inner,
                text=value,
                font=self.font,
                bg=CATEGORY_PANEL_BG,
                fg="#e2e8f0",
                padx=14,
                pady=8,
                anchor="w"
            )
            item.pack(fill="x")
            item.bind("<Enter>", lambda event, label=item: label.config(bg=BLUE, fg=WHITE))
            item.bind("<Leave>", lambda event, label=item: label.config(bg=CATEGORY_PANEL_BG, fg="#e2e8f0"))
            item.bind("<Button-1>", lambda event, selected=value: self.select_value(selected))

        self.popup.focus_force()
        self.popup.bind("<FocusOut>", lambda event: self.close_menu())

    def select_value(self, value):
        self.set(value)
        self.close_menu()

    def close_menu(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None


class ModernCheckbox(tk.Canvas):
    """A small rounded checkbox with a label."""

    def __init__(self, parent, text, font, command=None, checked=False, width=130, height=32, box_size=24):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )

        self.text = text
        self.font = font
        self.command = command
        self.checked = checked
        self.box_size = box_size

        self.draw()
        self.bind("<Button-1>", self.toggle)

    def draw(self):
        self.delete("all")

        height = int(self.cget("height"))
        box_size = self.box_size
        box_top = (height - box_size) // 2
        box_bottom = box_top + box_size
        box_radius = max(6, box_size // 3)
        box_center = box_top + box_size // 2

        box_fill = GREEN if self.checked else INPUT_BG
        outline = GREEN if self.checked else GRAY_BUTTON_HOVER

        draw_rounded_rectangle(
            self,
            0,
            box_top,
            box_size,
            box_bottom,
            box_radius,
            fill=box_fill,
            outline=outline
        )

        if self.checked:
            self.create_text(
                box_size // 2,
                box_center,
                text="✓",
                fill=WHITE,
                font=(self.font[0], 11, "bold")
            )

        self.create_text(
            box_size + 12,
            height // 2,
            text=self.text,
            fill=TEXT_LIGHT,
            font=self.font,
            anchor="w"
        )

    def toggle(self, event=None):
        self.checked = not self.checked
        self.draw()

        if self.command:
            self.command(self.checked)

    def set_checked(self, value, call_command=False):
        self.checked = value
        self.draw()

        if call_command and self.command:
            self.command(self.checked)

    def get(self):
        return self.checked


class ModernScrollbar(tk.Canvas):
    """A custom scrollbar that controls the task table."""

    def __init__(self, parent, command):
        super().__init__(
            parent,
            width=12,
            bg=TABLE_BG,
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )

        self.command = command
        self.first = 0
        self.last = 1

        self.bind("<Configure>", self.draw)
        self.bind("<Button-1>", self.move_to)
        self.bind("<B1-Motion>", self.move_to)

    def set(self, first, last):
        self.first = float(first)
        self.last = float(last)
        self.draw()

    def draw(self, event=None):
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        draw_rounded_rectangle(self, 3, 0, width - 3, height, 8, fill=INPUT_BG, outline=INPUT_BG)

        thumb_top = int(self.first * height)
        thumb_bottom = int(self.last * height)

        if thumb_bottom - thumb_top < 38:
            thumb_bottom = thumb_top + 38

        draw_rounded_rectangle(
            self,
            3,
            thumb_top,
            width - 3,
            min(thumb_bottom, height),
            8,
            fill=TEXT_FADED,
            outline=TEXT_FADED
        )

    def move_to(self, event):
        height = max(1, self.winfo_height())
        fraction = event.y / height
        fraction = max(0, min(1, fraction))
        self.command(fraction)


class RoundedProgressBar(tk.Canvas):
    """A pill-shaped progress bar."""

    def __init__(self, parent, height=18):
        super().__init__(parent, height=height, bg=parent.cget("bg"), highlightthickness=0, bd=0)

        self.progress = 0
        self.track_color = INPUT_BG
        self.fill_color = EMERALD
        self.bind("<Configure>", self.draw)

    def set_progress(self, percentage):
        self.progress = max(0, min(100, percentage))
        self.draw()

    def draw(self, event=None):
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 2 or height <= 2:
            return

        line_width = max(8, height - 2)
        y = height // 2
        x_start = line_width // 2
        x_end = max(x_start, width - line_width // 2)

        self.create_line(x_start, y, x_end, y, fill=self.track_color, width=line_width, capstyle="round")

        if self.progress > 0:
            fill_end = x_start + ((x_end - x_start) * (self.progress / 100))
            self.create_line(x_start, y, fill_end, y, fill=self.fill_color, width=line_width, capstyle="round")
