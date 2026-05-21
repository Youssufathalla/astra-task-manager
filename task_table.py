"""Custom Canvas-based task table for Astra.

Tkinter's default Treeview cannot easily draw rounded badges, so this table is
drawn manually on a Canvas. It still behaves like a simple table: click rows to
select, double-click to edit, and click headers to sort.
"""

import tkinter as tk

from config import *
from utils import draw_rounded_rectangle

class ModernTaskTable(tk.Canvas):
    """A custom table drawn on Canvas so badges, spacing, hover and selection look premium."""

    def __init__(self, parent, columns, normal_font, heading_font):
        super().__init__(
            parent,
            bg=TABLE_BG,
            highlightthickness=0,
            bd=0,
            cursor="arrow"
        )

        self.columns = columns
        self.normal_font = normal_font
        self.heading_font = heading_font
        self.tasks = []
        self.selected_id = None
        self.hovered_id = None
        self.y_offset = 0
        self.yscrollcommand = None
        self.sort_callback = None
        self.select_callback = None
        self.double_click_callback = None

        self.header_height = 36
        self.row_height = 50
        self.left_padding = 12
        self.right_padding = 12

        self.bind("<Configure>", lambda event: self.redraw())
        self.bind("<Motion>", self.on_motion)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Double-1>", self.on_double_click)
        self.bind("<MouseWheel>", self.on_mousewheel)

    def configure(self, cnf=None, **kwargs):
        if "yscrollcommand" in kwargs:
            self.yscrollcommand = kwargs.pop("yscrollcommand")
        return super().configure(cnf or {}, **kwargs)

    config = configure

    def set_sort_callback(self, callback):
        self.sort_callback = callback

    def set_select_callback(self, callback):
        self.select_callback = callback

    def set_double_click_callback(self, callback):
        self.double_click_callback = callback

    def load_tasks(self, tasks):
        self.tasks = list(tasks)
        available_ids = {str(task["id"]) for task in self.tasks}

        if self.selected_id not in available_ids:
            self.selected_id = None

        self.hovered_id = None
        self.limit_scroll()
        self.redraw()
        self.call_select_callback()

    def get_children(self):
        return tuple(str(task["id"]) for task in self.tasks)

    def selection(self):
        if self.selected_id is None:
            return ()
        return (self.selected_id,)

    def selection_remove(self, items):
        self.selected_id = None
        self.redraw()
        self.call_select_callback()

    def clear_selection(self):
        self.selection_remove(())

    def yview_moveto(self, fraction):
        max_offset = self.get_max_offset()
        self.y_offset = int(max_offset * max(0, min(1, float(fraction))))
        self.limit_scroll()
        self.redraw()

    def yview_scroll(self, number, what):
        step = self.row_height if what == "units" else self.winfo_height()
        self.y_offset += int(number) * step
        self.limit_scroll()
        self.redraw()

    def get_content_height(self):
        return self.header_height + len(self.tasks) * self.row_height

    def get_max_offset(self):
        return max(0, self.get_content_height() - max(1, self.winfo_height()))

    def limit_scroll(self):
        self.y_offset = max(0, min(self.y_offset, self.get_max_offset()))
        self.update_scrollbar()

    def update_scrollbar(self):
        if not self.yscrollcommand:
            return

        content_height = max(1, self.get_content_height())
        visible_height = max(1, self.winfo_height())

        if content_height <= visible_height:
            first, last = 0, 1
        else:
            first = self.y_offset / content_height
            last = min(1, (self.y_offset + visible_height) / content_height)

        self.yscrollcommand(first, last)

    def get_column_positions(self):
        width = max(1, self.winfo_width())
        usable_width = max(1, width - self.left_padding - self.right_padding)
        total_weight = sum(column[2] for column in self.columns)
        positions = []
        x = self.left_padding

        for index, column in enumerate(self.columns):
            if index == len(self.columns) - 1:
                column_width = self.left_padding + usable_width - x
            else:
                column_width = int(usable_width * (column[2] / total_weight))

            positions.append((column[0], column[1], x, x + column_width, column[4]))
            x += column_width

        return positions

    def redraw(self):
        self.delete("all")
        self.limit_scroll()
        self.draw_rows()
        self.draw_header()
        self.update_scrollbar()

    def draw_header(self):
        width = self.winfo_width()
        positions = self.get_column_positions()

        self.create_rectangle(0, 0, width, self.header_height, fill=INPUT_BG, outline=INPUT_BG)
        self.create_line(0, self.header_height - 1, width, self.header_height - 1, fill="#334155")

        for column_id, heading, x1, x2, anchor in positions:
            text_x = (x1 + x2) // 2 if anchor == "center" else x1 + 8
            text_anchor = "center" if anchor == "center" else "w"
            self.create_text(
                text_x,
                self.header_height // 2,
                text=heading,
                fill=SILVER,
                font=self.heading_font,
                anchor=text_anchor
            )

    def draw_rows(self):
        positions = self.get_column_positions()
        visible_top = self.y_offset
        visible_bottom = self.y_offset + self.winfo_height()

        for index, task in enumerate(self.tasks):
            row_y = self.header_height + index * self.row_height
            screen_y = row_y - self.y_offset

            if row_y + self.row_height < visible_top or row_y > visible_bottom:
                continue

            row_id = str(task["id"])
            selected = row_id == self.selected_id
            hovered = row_id == self.hovered_id and not selected
            bg = SELECTED_ROW_BG if selected else HOVER_ROW_BG if hovered else TABLE_BG

            self.create_rectangle(0, screen_y, self.winfo_width(), screen_y + self.row_height, fill=bg, outline=bg)
            self.create_line(
                self.left_padding,
                screen_y + self.row_height - 1,
                self.winfo_width() - self.right_padding,
                screen_y + self.row_height - 1,
                fill="#172033"
            )

            for column_id, heading, x1, x2, anchor in positions:
                self.draw_cell(task, column_id, x1, x2, screen_y, selected)

    def draw_cell(self, task, column_id, x1, x2, row_y, selected):
        center_y = row_y + self.row_height // 2
        value = self.get_cell_value(task, column_id)

        if column_id in ("priority", "status", "due_state"):
            self.draw_badge(x1, x2, center_y, value)
            return

        if column_id == "title":
            text_color = self.get_title_color(task)
            self.create_text(
                x1 + 8,
                center_y,
                text=value,
                fill=text_color,
                font=self.normal_font,
                anchor="w"
            )
            return

        color = self.get_cell_color(task, column_id)
        self.create_text(
            (x1 + x2) // 2,
            center_y,
            text=value,
            fill=WHITE if selected else color,
            font=self.normal_font,
            anchor="center"
        )

    def draw_badge(self, x1, x2, center_y, text):
        bg, fg = BADGE_COLORS.get(text, ("#172033", SILVER))
        badge_width = min(max(72, len(text) * 9 + 26), max(70, x2 - x1 - 16))
        badge_height = 26
        badge_x1 = (x1 + x2 - badge_width) // 2
        badge_y1 = center_y - badge_height // 2
        badge_x2 = badge_x1 + badge_width
        badge_y2 = badge_y1 + badge_height

        draw_rounded_rectangle(
            self,
            badge_x1,
            badge_y1,
            badge_x2,
            badge_y2,
            13,
            fill=bg,
            outline=fg
        )
        self.create_text(
            (badge_x1 + badge_x2) // 2,
            center_y,
            text=text,
            fill=fg,
            font=self.normal_font,
            anchor="center"
        )

    def get_title_color(self, task):
        due_state = task.get("due_state", "Upcoming")

        if due_state == "Overdue":
            return ROSE
        if task["status"] == "Completed":
            return "#86efac"
        if task["status"] == "In Progress":
            return VIOLET
        return SILVER

    def get_cell_color(self, task, column_id):
        if column_id == "category":
            return CYAN
        if column_id == "due_date":
            due_state = task.get("due_state", "Upcoming")
            return BADGE_COLORS.get(due_state, (None, TEXT_LIGHT))[1]
        if column_id == "due_time":
            return TEXT_LIGHT if task["due_time"] != "No time" else TEXT_MUTED
        return TEXT_LIGHT

    def get_cell_value(self, task, column_id):
        if column_id == "due_state":
            return task.get("due_state", "Upcoming")
        return str(task.get(column_id, ""))

    def get_row_id_at_y(self, y):
        table_y = y + self.y_offset
        if table_y < self.header_height:
            return None

        index = int((table_y - self.header_height) // self.row_height)
        if 0 <= index < len(self.tasks):
            return str(self.tasks[index]["id"])
        return None

    def get_column_id_at_x(self, x):
        for column_id, heading, x1, x2, anchor in self.get_column_positions():
            if x1 <= x <= x2:
                return column_id
        return None

    def on_motion(self, event):
        row_id = self.get_row_id_at_y(event.y)
        if row_id == self.hovered_id:
            return

        self.hovered_id = None if row_id == self.selected_id else row_id
        self.redraw()

    def on_leave(self, event=None):
        if self.hovered_id is not None:
            self.hovered_id = None
            self.redraw()

    def on_click(self, event):
        if event.y <= self.header_height:
            column_id = self.get_column_id_at_x(event.x)
            if column_id and self.sort_callback:
                self.sort_callback(column_id)
            return

        row_id = self.get_row_id_at_y(event.y)
        self.selected_id = row_id
        self.hovered_id = None
        self.redraw()
        self.call_select_callback()

    def on_double_click(self, event):
        row_id = self.get_row_id_at_y(event.y)
        if row_id:
            self.selected_id = row_id
            self.redraw()
            self.call_select_callback()
            if self.double_click_callback:
                self.double_click_callback()

    def on_mousewheel(self, event):
        self.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def call_select_callback(self):
        if self.select_callback:
            self.select_callback()
