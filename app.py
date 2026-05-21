"""Main application class for the Astra task manager."""

import json
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from datetime import datetime, date, timedelta

from config import *
from utils import make_label, add_accent_line
from widgets import (
    RoundedFrame,
    RoundedButton,
    RoundedEntry,
    ModernDropdown,
    ModernCheckbox,
    ModernScrollbar,
    RoundedProgressBar,
)
from task_table import ModernTaskTable

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_fonts()

        self.months = MONTHS.copy()
        self.next_task_id = 1
        self.categories = STARTING_CATEGORIES.copy()
        self.tasks = []
        self.load_data()

        self.sort_column = None
        self.sort_reverse = False
        self.selected_period = "AM"
        self.active_filter = "All"
        self.selection_buttons = []
        self.filter_buttons = {}

        self.setup_styles()
        self.create_widgets()
        self.set_time_enabled(False)
        self.refresh_table()
        self.update_dashboard()
        self.update_action_buttons()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # -------------------------------------------------------------------------
    # Setup and data storage
    # -------------------------------------------------------------------------

    def setup_window(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        self.root.configure(bg=APP_BG)
        self.root.resizable(True, True)
        self.root.tk.call("tk", "scaling", TK_SCALING)

        try:
            self.root.state("zoomed")
        except Exception:
            pass

    def setup_fonts(self):
        available_fonts = set(tkfont.families())

        def choose_font(options):
            for font_name in options:
                if font_name in available_fonts:
                    return font_name
            return "Segoe UI"

        display_font = choose_font(["Segoe UI Variable Display", "Bahnschrift SemiBold", "Aptos Display", "Segoe UI"])
        body_font = choose_font(["Segoe UI Variable Text", "Bahnschrift SemiBold", "Aptos", "Segoe UI"])

        self.FONT_TITLE = (display_font, 29, "bold")
        self.FONT_SUBTITLE = (body_font, 12, "bold")
        self.FONT_SECTION = (display_font, 18, "bold")
        self.FONT_LABEL = (body_font, 11, "bold")
        self.FONT_NORMAL = (body_font, 11, "bold")
        self.FONT_CARD = (display_font, 28, "bold")
        self.FONT_BUTTON = (body_font, 10, "bold")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.create_starting_data()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.categories = data.get("categories", STARTING_CATEGORIES.copy())
            self.tasks = []
            self.next_task_id = 1

            for task_data in data.get("tasks", []):
                task = self.normalize_loaded_task(task_data)
                self.tasks.append(task)
                self.next_task_id = max(self.next_task_id, task["id"] + 1)

            if not self.categories:
                self.categories = STARTING_CATEGORIES.copy()

        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            self.create_starting_data()

    def create_starting_data(self):
        self.categories = STARTING_CATEGORIES.copy()
        self.tasks = [self.create_task_record(*task_data) for task_data in STARTING_TASKS]
        self.save_data()

    def normalize_loaded_task(self, task_data):
        task_id = int(task_data.get("id", self.next_task_id))
        task = {
            "id": task_id,
            "title": str(task_data.get("title", "Untitled Task")),
            "category": str(task_data.get("category", self.categories[0] if self.categories else "Personal")),
            "priority": str(task_data.get("priority", "Low")),
            "due_date": str(task_data.get("due_date", date.today().isoformat())),
            "due_time": str(task_data.get("due_time", "No time")),
            "status": str(task_data.get("status", "Pending")),
            "notes": str(task_data.get("notes", "")),
        }

        if task["category"] not in self.categories:
            self.categories.append(task["category"])

        if task["priority"] not in ["Low", "Medium", "High"]:
            task["priority"] = "Low"

        if task["status"] not in ["Pending", "In Progress", "Completed"]:
            task["status"] = "Pending"

        return task

    def save_data(self):
        data = {
            "categories": self.categories,
            "tasks": self.tasks,
        }

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError:
            pass

    def on_close(self):
        self.save_data()
        self.root.destroy()

    def create_task_record(self, title, category, priority, due_date, due_time, status, notes=""):
        task = {
            "id": self.next_task_id,
            "title": title,
            "category": category,
            "priority": priority,
            "due_date": due_date,
            "due_time": due_time,
            "status": status,
            "notes": notes,
        }
        self.next_task_id += 1
        return task

    # -------------------------------------------------------------------------
    # UI creation
    # -------------------------------------------------------------------------

    def create_widgets(self):
        self.create_header()
        self.create_dashboard()
        self.create_control_area()
        self.create_task_board()

    def create_header(self):
        header = tk.Frame(self.root, bg=APP_BG)
        header.pack(fill="x", padx=28, pady=(18, 6))

        header_content = tk.Frame(header, bg=APP_BG)
        header_content.pack(anchor="w")

        self.logo_image = tk.PhotoImage(data=LOGO_IMAGE_BASE64)

        try:
            self.root.iconphoto(True, self.logo_image)
        except Exception:
            pass

        logo_label = tk.Label(header_content, image=self.logo_image, bg=APP_BG, bd=0)
        logo_label.pack(side="left", padx=(0, 14))

        text_box = tk.Frame(header_content, bg=APP_BG)
        text_box.pack(side="left", fill="both")

        title = make_label(text_box, APP_TITLE, self.FONT_TITLE, WHITE, APP_BG)
        title.pack(anchor="w")

        subtitle = make_label(text_box, APP_SUBTITLE, self.FONT_SUBTITLE, TEXT_MUTED, APP_BG)
        subtitle.pack(anchor="w", pady=(2, 0))

    def create_dashboard(self):
        dashboard = tk.Frame(self.root, bg=APP_BG)
        dashboard.pack(fill="x", padx=28, pady=(10, 8))

        self.card_labels = {}

        for index, (title, key, color) in enumerate(DASHBOARD_CARDS):
            dashboard.grid_columnconfigure(index, weight=1)
            card = RoundedFrame(dashboard, bg=APP_BG, fill=PANEL_BG, radius=22, padding=12, height=110)
            card.grid(row=0, column=index, sticky="ew", padx=(0, 14 if index < len(DASHBOARD_CARDS) - 1 else 0))

            line = tk.Frame(card.inner, bg=color, width=6)
            line.pack(side="left", fill="y", padx=(0, 12))

            content = tk.Frame(card.inner, bg=PANEL_BG)
            content.pack(side="left", fill="both", expand=True)

            value_label = make_label(content, "0", self.FONT_CARD, color, PANEL_BG)
            value_label.pack(anchor="w")

            title_label = make_label(content, title, self.FONT_LABEL, TEXT_LIGHT, PANEL_BG)
            title_label.pack(anchor="w", pady=(2, 0))

            self.card_labels[key] = value_label

        progress_box = tk.Frame(self.root, bg=APP_BG)
        progress_box.pack(fill="x", padx=28, pady=(0, 10))

        self.progress_text = make_label(progress_box, "Completion Progress: 0%", self.FONT_LABEL, TEXT_LIGHT, APP_BG)
        self.progress_text.pack(anchor="w")

        self.progress_bar = RoundedProgressBar(progress_box, height=18)
        self.progress_bar.pack(fill="x", pady=(7, 0))

    def create_control_area(self):
        control_area = tk.Frame(self.root, bg=APP_BG)
        control_area.pack(fill="x", padx=28, pady=(0, 12))

        self.task_panel = RoundedFrame(control_area, bg=APP_BG, fill=PANEL_BG, radius=26, padding=18, height=285)
        self.task_panel.pack(side="left", fill="both", expand=True, padx=(0, 16))

        self.category_panel = RoundedFrame(
            control_area,
            bg=APP_BG,
            fill=CATEGORY_PANEL_BG,
            radius=26,
            padding=18,
            width=405,
            height=285
        )
        self.category_panel.pack(side="right", fill="y")

        self.create_task_form(self.task_panel.inner)
        self.create_category_form(self.category_panel.inner)

    def create_task_form(self, parent):
        add_accent_line(parent, SKY, 12)

        title = make_label(parent, "Task Workspace", self.FONT_SECTION, WHITE, PANEL_BG)
        title.pack(anchor="w", pady=(0, 10))

        fields_row = tk.Frame(parent, bg=PANEL_BG)
        fields_row.pack(fill="x")

        for column, weight in enumerate([5, 1, 1, 2, 2]):
            fields_row.grid_columnconfigure(column, weight=weight)

        title_box = self.create_field_box(fields_row, "Task Title", PANEL_BG)
        title_box.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.task_entry = RoundedEntry(title_box, "Enter task title", self.FONT_NORMAL, height=42)
        self.task_entry.pack(fill="x", pady=(6, 0))

        category_box = self.create_field_box(fields_row, "Category", PANEL_BG)
        category_box.grid(row=0, column=1, sticky="w", padx=(0, 12))
        self.category_dropdown = ModernDropdown(category_box, self.categories, self.FONT_NORMAL, width=155)
        self.category_dropdown.pack(pady=(6, 0))

        priority_box = self.create_field_box(fields_row, "Priority", PANEL_BG)
        priority_box.grid(row=0, column=2, sticky="w", padx=(0, 12))
        self.priority_dropdown = ModernDropdown(priority_box, ["Low", "Medium", "High"], self.FONT_NORMAL, width=135)
        self.priority_dropdown.pack(pady=(6, 0))

        date_box = self.create_field_box(fields_row, "Due Date", PANEL_BG)
        date_box.grid(row=0, column=3, sticky="w", padx=(0, 12))
        self.create_due_date_inputs(date_box)

        time_box = tk.Frame(fields_row, bg=PANEL_BG)
        time_box.grid(row=0, column=4, sticky="w")
        self.create_due_time_header(time_box)
        self.create_due_time_inputs(time_box)

        button_row = tk.Frame(parent, bg=PANEL_BG)
        button_row.pack(anchor="w", pady=(12, 0))

        for text, bg, hover_bg, method_name, needs_selection in ACTION_BUTTONS:
            button_width = 95 if text != "Complete" else 105
            button = self.create_action_button(button_row, text, bg, hover_bg, getattr(self, method_name), width=button_width)

            if needs_selection:
                self.selection_buttons.append(button)

    def create_due_time_header(self, parent):
        time_header = tk.Frame(parent, bg=PANEL_BG)
        time_header.pack(anchor="w")

        time_label = make_label(time_header, "Due Time", self.FONT_LABEL, TEXT_LIGHT, PANEL_BG)
        time_label.pack(side="left")

        self.time_checkbox = ModernCheckbox(
            time_header,
            text="Add time",
            font=self.FONT_LABEL,
            command=self.set_time_enabled,
            checked=False,
            height=20,
            box_size=18
        )
        self.time_checkbox.pack(side="left", padx=(12, 0))

    def create_category_form(self, parent):
        add_accent_line(parent, TEAL, 12)

        title = make_label(parent, "Category Manager", self.FONT_SECTION, WHITE, CATEGORY_PANEL_BG)
        title.pack(anchor="w")

        subtitle = make_label(parent, "Create, rename, or remove task groups.", self.FONT_LABEL, TEXT_MUTED, CATEGORY_PANEL_BG)
        subtitle.pack(anchor="w", pady=(3, 8))

        label = make_label(parent, "Category Name", self.FONT_LABEL, TEXT_LIGHT, CATEGORY_PANEL_BG)
        label.pack(anchor="w")

        self.new_category_entry = RoundedEntry(parent, "Example: Business", self.FONT_NORMAL, height=42)
        self.new_category_entry.pack(fill="x", pady=(5, 8))

        category_button_row = tk.Frame(parent, bg=CATEGORY_PANEL_BG)
        category_button_row.pack(anchor="w", pady=(8, 0))

        category_buttons = [
            ("Add Category", self.add_category, TEAL, TEAL_HOVER, 112),
            ("Rename", self.rename_category, GRAY_BUTTON, GRAY_BUTTON_HOVER, 92),
            ("Delete", self.delete_category, RED, RED_HOVER, 92),
        ]

        for text, command, bg, hover_bg, width in category_buttons:
            button = RoundedButton(
                category_button_row,
                text=text,
                command=command,
                bg=bg,
                hover_bg=hover_bg,
                fg=WHITE,
                font=self.FONT_BUTTON,
                width=width,
                height=42,
                radius=16
            )
            button.pack(side="left", padx=(0, 9))

    def create_field_box(self, parent, label_text, bg):
        frame = tk.Frame(parent, bg=bg)
        label = make_label(frame, label_text, self.FONT_LABEL, TEXT_LIGHT, bg)
        label.pack(anchor="w")
        return frame

    def create_due_date_inputs(self, parent):
        row = tk.Frame(parent, bg=PANEL_BG)
        row.pack(pady=(6, 0))

        today = date.today()

        self.year_entry = RoundedEntry(row, "Year", self.FONT_NORMAL, width=82, height=42)
        self.year_entry.pack(side="left", padx=(0, 7))
        self.year_entry.set_value(str(today.year))

        self.month_dropdown = ModernDropdown(row, self.months, self.FONT_NORMAL, width=150)
        self.month_dropdown.pack(side="left", padx=(0, 7))
        self.month_dropdown.set(self.months[today.month - 1])

        self.day_entry = RoundedEntry(row, "Day", self.FONT_NORMAL, width=62, height=42)
        self.day_entry.pack(side="left")
        self.day_entry.set_value(str(today.day))

    def create_due_time_inputs(self, parent):
        time_row = tk.Frame(parent, bg=PANEL_BG)
        time_row.pack(anchor="w")

        self.hour_entry = RoundedEntry(time_row, "HH", self.FONT_NORMAL, width=58, height=42)
        self.hour_entry.pack(side="left", padx=(0, 7))

        self.minute_entry = RoundedEntry(time_row, "MM", self.FONT_NORMAL, width=58, height=42)
        self.minute_entry.pack(side="left", padx=(0, 8))

        self.am_button = RoundedButton(
            time_row,
            text="AM",
            command=lambda: self.select_period("AM"),
            bg=BLUE,
            hover_bg=BLUE_HOVER,
            font=self.FONT_BUTTON,
            width=54,
            height=42,
            radius=16
        )
        self.am_button.pack(side="left", padx=(0, 6))

        self.pm_button = RoundedButton(
            time_row,
            text="PM",
            command=lambda: self.select_period("PM"),
            bg=INPUT_BG,
            hover_bg=GRAY_BUTTON,
            font=self.FONT_BUTTON,
            width=54,
            height=42,
            radius=16
        )
        self.pm_button.pack(side="left")

    def create_action_button(self, parent, text, bg, hover_bg, command, width=100):
        button = RoundedButton(
            parent,
            text=text,
            command=command,
            bg=bg,
            hover_bg=hover_bg,
            fg=WHITE,
            font=self.FONT_BUTTON,
            width=width,
            height=42,
            radius=16
        )
        button.pack(side="left", padx=(0, 9))
        return button

    def create_task_board(self):
        board = RoundedFrame(self.root, bg=APP_BG, fill=PANEL_BG, radius=24, padding=20, height=380)
        board.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        add_accent_line(board.inner, VIOLET, 14)
        self.create_task_board_top_bar(board.inner)
        self.create_filter_bar(board.inner)
        self.create_task_table(board.inner)

    def create_task_board_top_bar(self, parent):
        top_bar = tk.Frame(parent, bg=PANEL_BG)
        top_bar.pack(fill="x", pady=(0, 10))

        title = make_label(top_bar, "Task Board", self.FONT_SECTION, WHITE, PANEL_BG)
        title.pack(side="left")

        instruction = make_label(
            top_bar,
            "Double-click a task to edit • Click headers to sort",
            self.FONT_LABEL,
            TEXT_FADED,
            PANEL_BG
        )
        instruction.pack(side="left", padx=(16, 0))

        self.showing_label = make_label(top_bar, "Showing 0 of 0", self.FONT_LABEL, TEXT_MUTED, PANEL_BG)
        self.showing_label.pack(side="right", padx=(12, 0))

        self.search_entry = RoundedEntry(top_bar, "Search tasks...", self.FONT_NORMAL, width=245, height=42)
        self.search_entry.pack(side="right")
        self.search_entry.bind_key("<KeyRelease>", self.search_tasks)

    def create_filter_bar(self, parent):
        filter_bar = tk.Frame(parent, bg=PANEL_BG, height=44)
        filter_bar.pack(fill="x", pady=(0, 12))
        filter_bar.pack_propagate(False)

        for label, key in FILTER_DEFINITIONS:
            button = RoundedButton(
                filter_bar,
                text=label,
                command=lambda selected=key: self.set_filter(selected),
                bg=INPUT_BG,
                hover_bg=GRAY_BUTTON,
                fg=TEXT_LIGHT,
                font=self.FONT_BUTTON,
                width=112 if label in ["In Progress", "High Priority"] else 90,
                height=36,
                radius=14
            )
            button.pack(side="left", padx=(0, 8), pady=(4, 0))
            self.filter_buttons[key] = button

        clear_button = RoundedButton(
            filter_bar,
            text="Clear Completed",
            command=self.clear_completed_tasks,
            bg=RED,
            hover_bg=RED_HOVER,
            fg=WHITE,
            font=self.FONT_BUTTON,
            width=165,
            height=36,
            radius=14
        )
        clear_button.pack(side="right", pady=(4, 0))

        self.update_filter_buttons()

    def create_task_table(self, parent):
        table_shell = RoundedFrame(parent, bg=PANEL_BG, fill=TABLE_BG, radius=20, padding=8, height=260)
        table_shell.pack(fill="both", expand=True)

        table_frame = tk.Frame(table_shell.inner, bg=TABLE_BG)
        table_frame.pack(fill="both", expand=True)

        self.task_table = ModernTaskTable(table_frame, TABLE_COLUMNS, self.FONT_NORMAL, self.FONT_LABEL)
        self.task_scrollbar = ModernScrollbar(table_frame, command=self.task_table.yview_moveto)
        self.task_table.configure(yscrollcommand=self.task_scrollbar.set)

        self.task_table.set_sort_callback(self.sort_tasks_by_column)
        self.task_table.set_select_callback(self.update_action_buttons)
        self.task_table.set_double_click_callback(self.load_selected_task_into_form)

        self.task_table.pack(side="left", fill="both", expand=True)
        self.task_scrollbar.pack(side="right", fill="y", padx=(10, 0))
        self.create_empty_state(table_frame)

    def create_empty_state(self, parent):
        self.empty_state = tk.Frame(parent, bg=TABLE_BG)

        title = make_label(self.empty_state, "No matching tasks found", self.FONT_SECTION, SILVER, TABLE_BG)
        title.pack(anchor="center")

        subtitle = make_label(self.empty_state, "Try another search term or change the filter.", self.FONT_LABEL, TEXT_MUTED, TABLE_BG)
        subtitle.pack(anchor="center", pady=(6, 0))

    def show_empty_state(self, show):
        if show:
            self.empty_state.place(relx=0.5, rely=0.58, anchor="center")
        else:
            self.empty_state.place_forget()

    # -------------------------------------------------------------------------
    # Time controls
    # -------------------------------------------------------------------------

    def set_time_enabled(self, enabled):
        self.hour_entry.set_enabled(enabled)
        self.minute_entry.set_enabled(enabled)
        self.am_button.set_disabled(not enabled)
        self.pm_button.set_disabled(not enabled)

        if enabled:
            if self.hour_entry.get_value() == "":
                self.hour_entry.set_value("12")

            if self.minute_entry.get_value() == "":
                self.minute_entry.set_value("00")

            self.select_period(self.selected_period)
        else:
            self.hour_entry.clear()
            self.minute_entry.clear()
            self.am_button.set_colors(DISABLED_BUTTON_BG, DISABLED_BUTTON_BG)
            self.pm_button.set_colors(DISABLED_BUTTON_BG, DISABLED_BUTTON_BG)

    def select_period(self, period):
        self.selected_period = period

        if not self.time_checkbox.get():
            return

        if period == "AM":
            self.am_button.set_colors(BLUE, BLUE_HOVER)
            self.pm_button.set_colors(INPUT_BG, GRAY_BUTTON)
        else:
            self.am_button.set_colors(INPUT_BG, GRAY_BUTTON)
            self.pm_button.set_colors(BLUE, BLUE_HOVER)

    # -------------------------------------------------------------------------
    # Popups
    # -------------------------------------------------------------------------

    def center_popup(self, popup, width, height):
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def show_alert(self, title, message, alert_type="info"):
        colors = {"info": BLUE, "warning": ORANGE, "success": GREEN_BUTTON, "error": RED}
        icons = {"info": "i", "warning": "!", "success": "✓", "error": "!"}

        accent = colors.get(alert_type, BLUE)
        icon = icons.get(alert_type, "i")

        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("460x225")
        popup.configure(bg=POPUP_BG)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        self.center_popup(popup, 460, 225)

        top_line = tk.Frame(popup, bg=accent, height=6)
        top_line.pack(fill="x")

        body = tk.Frame(popup, bg=POPUP_BG)
        body.pack(fill="both", expand=True, padx=28, pady=24)

        icon_label = make_label(body, icon, (self.FONT_TITLE[0], 26, "bold"), accent, POPUP_BG, width=2)
        icon_label.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 16))

        title_label = make_label(body, title, (self.FONT_SECTION[0], 18, "bold"), TEXT_DARK, POPUP_BG)
        title_label.grid(row=0, column=1, sticky="w")

        message_label = make_label(body, message, self.FONT_NORMAL, POPUP_TEXT, POPUP_BG, wraplength=340, justify="left")
        message_label.grid(row=1, column=1, sticky="w", pady=(8, 0))

        ok_button = RoundedButton(
            body,
            text="OK",
            command=popup.destroy,
            bg=accent,
            hover_bg=accent,
            fg=WHITE,
            font=self.FONT_BUTTON,
            width=90,
            height=38,
            radius=16
        )
        ok_button.grid(row=2, column=1, sticky="e", pady=(24, 0))

    def show_confirm(self, title, message):
        result = {"answer": False}

        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("480x235")
        popup.configure(bg=POPUP_BG)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        self.center_popup(popup, 480, 235)

        top_line = tk.Frame(popup, bg=RED, height=6)
        top_line.pack(fill="x")

        title_label = make_label(popup, title, (self.FONT_SECTION[0], 18, "bold"), TEXT_DARK, POPUP_BG)
        title_label.pack(anchor="w", padx=28, pady=(26, 8))

        message_label = make_label(popup, message, self.FONT_NORMAL, POPUP_TEXT, POPUP_BG, wraplength=410, justify="left")
        message_label.pack(anchor="w", padx=28)

        button_row = tk.Frame(popup, bg=POPUP_BG)
        button_row.pack(anchor="e", padx=28, pady=(26, 0))

        def confirm_yes():
            result["answer"] = True
            popup.destroy()

        cancel_button = RoundedButton(
            button_row,
            text="Cancel",
            command=popup.destroy,
            bg=CONFIRM_CANCEL_BG,
            hover_bg=CONFIRM_CANCEL_HOVER,
            fg=TEXT_DARK,
            font=self.FONT_BUTTON,
            width=96,
            height=38,
            radius=16
        )
        cancel_button.pack(side="left", padx=(0, 12))

        delete_button = RoundedButton(
            button_row,
            text="Delete",
            command=confirm_yes,
            bg=RED,
            hover_bg=RED_HOVER,
            fg=WHITE,
            font=self.FONT_BUTTON,
            width=96,
            height=38,
            radius=16
        )
        delete_button.pack(side="left")

        self.root.wait_window(popup)
        return result["answer"]

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def validate_due_date(self):
        year_text = self.year_entry.get_value()
        day_text = self.day_entry.get_value()
        month_name = self.month_dropdown.get()

        if year_text == "":
            return False, "Please enter a year."

        if day_text == "":
            return False, "Please enter a day."

        if not year_text.isdigit():
            return False, "Year must contain numbers only."

        if not day_text.isdigit():
            return False, "Day must contain numbers only."

        year = int(year_text)
        day = int(day_text)
        month = self.months.index(month_name) + 1

        if year < 2000 or year > 2100:
            return False, "Year must be between 2000 and 2100."

        try:
            selected_date = date(year, month, day)
        except ValueError:
            return False, "Please enter a valid calendar date."

        return True, selected_date.isoformat()

    def validate_due_time(self):
        if not self.time_checkbox.get():
            return True, "No time"

        hour_text = self.hour_entry.get_value()
        minute_text = self.minute_entry.get_value()

        if hour_text == "":
            return False, "Please enter an hour."

        if minute_text == "":
            return False, "Please enter minutes."

        if not hour_text.isdigit():
            return False, "Hour must contain numbers only."

        if not minute_text.isdigit():
            return False, "Minutes must contain numbers only."

        hour = int(hour_text)
        minute = int(minute_text)

        if hour < 1 or hour > 12:
            return False, "Hour must be between 1 and 12."

        if minute < 0 or minute > 59:
            return False, "Minutes must be between 0 and 59."

        due_time = f"{hour:02d}:{minute:02d} {self.selected_period}"
        return True, due_time

    # -------------------------------------------------------------------------
    # Form helpers
    # -------------------------------------------------------------------------

    def reset_form(self):
        self.task_entry.clear()
        self.new_category_entry.clear()
        self.category_dropdown.set(self.categories[0])
        self.priority_dropdown.set("Low")

        today = date.today()
        self.year_entry.set_value(str(today.year))
        self.month_dropdown.set(self.months[today.month - 1])
        self.day_entry.set_value(str(today.day))

        self.selected_period = "AM"
        self.time_checkbox.set_checked(False)
        self.set_time_enabled(False)

        self.task_table.clear_selection()
        self.update_action_buttons()
        self.root.focus_set()

    def set_date_controls(self, due_date):
        try:
            selected_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            self.year_entry.set_value(str(selected_date.year))
            self.month_dropdown.set(self.months[selected_date.month - 1])
            self.day_entry.set_value(str(selected_date.day))
        except ValueError:
            today = date.today()
            self.year_entry.set_value(str(today.year))
            self.month_dropdown.set(self.months[today.month - 1])
            self.day_entry.set_value(str(today.day))

    def set_time_controls(self, due_time):
        if due_time == "No time":
            self.time_checkbox.set_checked(False)
            self.set_time_enabled(False)
            return

        try:
            time_part, period = due_time.split()
            hour, minute = time_part.split(":")

            self.time_checkbox.set_checked(True)
            self.set_time_enabled(True)
            self.hour_entry.set_value(str(int(hour)))
            self.minute_entry.set_value(minute)
            self.select_period(period)
        except ValueError:
            self.time_checkbox.set_checked(False)
            self.set_time_enabled(False)

    def update_action_buttons(self, event=None):
        has_selection = len(self.task_table.selection()) > 0 if hasattr(self, "task_table") else False

        for button in self.selection_buttons:
            button.set_disabled(not has_selection)

    def get_valid_task_inputs(self, update_mode=False):
        title = self.task_entry.get_value()

        if title == "":
            message = "Please enter a task title before updating." if update_mode else "Please enter a task title."
            self.show_alert("Missing Task", message, "warning")
            return None

        if len(title) > 80:
            self.show_alert("Title Too Long", "Task title must be 80 characters or fewer.", "warning")
            return None

        date_valid, due_date = self.validate_due_date()
        if not date_valid:
            self.show_alert("Invalid Date", due_date, "warning")
            return None

        time_valid, due_time = self.validate_due_time()
        if not time_valid:
            self.show_alert("Invalid Time", due_time, "warning")
            return None

        return {
            "title": title,
            "category": self.category_dropdown.get(),
            "priority": self.priority_dropdown.get(),
            "due_date": due_date,
            "due_time": due_time,
        }

    # -------------------------------------------------------------------------
    # Task actions
    # -------------------------------------------------------------------------

    def add_task(self):
        task_inputs = self.get_valid_task_inputs()

        if task_inputs is None:
            return

        new_task = self.create_task_record(
            task_inputs["title"],
            task_inputs["category"],
            task_inputs["priority"],
            task_inputs["due_date"],
            task_inputs["due_time"],
            "Pending"
        )

        self.tasks.append(new_task)
        self.after_data_changed()
        self.reset_form()

    def update_selected_task(self):
        task = self.get_selected_task()

        if task is None:
            self.show_alert("No Selection", "Please select a task first.", "warning")
            return

        task_inputs = self.get_valid_task_inputs(update_mode=True)

        if task_inputs is None:
            return

        task.update(task_inputs)
        self.after_data_changed()
        self.reset_form()
        self.show_alert("Task Updated", "The selected task was updated successfully.", "success")

    def add_category(self):
        new_category = self.new_category_entry.get_value()

        if new_category == "":
            self.show_alert("Missing Category", "Please enter a category name.", "warning")
            return

        if len(new_category) > 25:
            self.show_alert("Category Too Long", "Category name must be 25 characters or fewer.", "warning")
            return

        for category in self.categories:
            if category.lower() == new_category.lower():
                self.show_alert("Category Exists", "This category already exists.", "info")
                return

        self.categories.append(new_category)
        self.category_dropdown.update_values(self.categories)
        self.category_dropdown.set(new_category)
        self.new_category_entry.clear()
        self.save_data()
        self.root.focus_set()
        self.show_alert("Category Added", f"'{new_category}' was added successfully.", "success")

    def rename_category(self):
        old_category = self.category_dropdown.get()
        new_category = self.new_category_entry.get_value()

        if old_category == "":
            self.show_alert("No Category", "Please select a category first.", "warning")
            return

        if new_category == "":
            self.show_alert("Missing Name", "Enter the new category name first.", "warning")
            return

        if len(new_category) > 25:
            self.show_alert("Category Too Long", "Category name must be 25 characters or fewer.", "warning")
            return

        for category in self.categories:
            if category.lower() == new_category.lower() and category != old_category:
                self.show_alert("Category Exists", "This category already exists.", "info")
                return

        for index, category in enumerate(self.categories):
            if category == old_category:
                self.categories[index] = new_category
                break

        for task in self.tasks:
            if task["category"] == old_category:
                task["category"] = new_category

        self.category_dropdown.update_values(self.categories)
        self.category_dropdown.set(new_category)
        self.new_category_entry.clear()
        self.after_data_changed()
        self.show_alert("Category Renamed", f"'{old_category}' was renamed to '{new_category}'.", "success")

    def delete_category(self):
        category = self.category_dropdown.get()

        if len(self.categories) <= 1:
            self.show_alert("Cannot Delete", "At least one category must remain.", "warning")
            return

        tasks_using_category = sum(1 for task in self.tasks if task["category"] == category)

        if tasks_using_category > 0:
            self.show_alert(
                "Category In Use",
                f"{tasks_using_category} task(s) still use this category. Rename it or move those tasks first.",
                "warning"
            )
            return

        confirmed = self.show_confirm("Delete Category", f"Delete the '{category}' category?")

        if not confirmed:
            return

        self.categories.remove(category)
        self.category_dropdown.update_values(self.categories)
        self.category_dropdown.set(self.categories[0])
        self.save_data()
        self.show_alert("Category Deleted", f"'{category}' was removed.", "success")

    def start_task(self):
        task = self.get_selected_task()

        if task is None:
            self.show_alert("No Selection", "Please select a task first.", "warning")
            return

        if task["status"] != "Pending":
            self.show_alert("Cannot Start Task", "Only pending tasks can be started.", "warning")
            return

        task["status"] = "In Progress"
        self.after_data_changed()
        self.reset_form()

    def mark_complete(self):
        task = self.get_selected_task()

        if task is None:
            self.show_alert("No Selection", "Please select a task first.", "warning")
            return

        if task["status"] != "In Progress":
            self.show_alert("Cannot Complete Task", "Only tasks that are in progress can be completed.", "warning")
            return

        task["status"] = "Completed"
        self.after_data_changed()
        self.reset_form()

    def delete_task(self):
        task = self.get_selected_task()

        if task is None:
            self.show_alert("No Selection", "Please select a task first.", "warning")
            return

        confirmed = self.show_confirm("Delete Task", f"Are you sure you want to delete '{task['title']}'?")

        if not confirmed:
            return

        self.tasks.remove(task)
        self.after_data_changed()
        self.reset_form()

    def clear_completed_tasks(self):
        completed_count = sum(1 for task in self.tasks if task["status"] == "Completed")

        if completed_count == 0:
            self.show_alert("No Completed Tasks", "There are no completed tasks to clear.", "info")
            return

        confirmed = self.show_confirm("Clear Completed", f"Remove {completed_count} completed task(s)?")

        if not confirmed:
            return

        self.tasks = [task for task in self.tasks if task["status"] != "Completed"]
        self.after_data_changed()
        self.reset_form()

    def load_selected_task_into_form(self, event=None):
        task = self.get_selected_task()

        if task is None:
            return

        self.task_entry.set_value(task["title"])
        self.category_dropdown.set(task["category"])
        self.priority_dropdown.set(task["priority"])
        self.set_date_controls(task["due_date"])
        self.set_time_controls(task["due_time"])

    def open_notes_popup(self):
        task = self.get_selected_task()

        if task is None:
            self.show_alert("No Selection", "Please select a task first.", "warning")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Task Notes")
        popup.geometry("560x420")
        popup.configure(bg=POPUP_BG)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        self.center_popup(popup, 560, 420)

        top_line = tk.Frame(popup, bg=VIOLET, height=6)
        top_line.pack(fill="x")

        title_label = make_label(popup, "Task Notes", (self.FONT_SECTION[0], 18, "bold"), TEXT_DARK, POPUP_BG)
        title_label.pack(anchor="w", padx=28, pady=(22, 4))

        task_label = make_label(popup, task["title"], self.FONT_LABEL, POPUP_TEXT, POPUP_BG, wraplength=500, justify="left")
        task_label.pack(anchor="w", padx=28, pady=(0, 12))

        notes_box = tk.Text(
            popup,
            font=self.FONT_NORMAL,
            bg=WHITE,
            fg=TEXT_DARK,
            insertbackground=TEXT_DARK,
            relief="flat",
            bd=0,
            height=10,
            wrap="word"
        )
        notes_box.pack(fill="both", expand=True, padx=28)
        notes_box.insert("1.0", task.get("notes", ""))

        button_row = tk.Frame(popup, bg=POPUP_BG)
        button_row.pack(anchor="e", padx=28, pady=(18, 22))

        def save_notes():
            task["notes"] = notes_box.get("1.0", "end-1c").strip()
            self.save_data()
            popup.destroy()

        cancel_button = RoundedButton(
            button_row,
            text="Cancel",
            command=popup.destroy,
            bg=CONFIRM_CANCEL_BG,
            hover_bg=CONFIRM_CANCEL_HOVER,
            fg=TEXT_DARK,
            font=self.FONT_BUTTON,
            width=96,
            height=38,
            radius=16
        )
        cancel_button.pack(side="left", padx=(0, 12))

        save_button = RoundedButton(
            button_row,
            text="Save Notes",
            command=save_notes,
            bg=VIOLET,
            hover_bg=VIOLET_HOVER,
            fg=WHITE,
            font=self.FONT_BUTTON,
            width=120,
            height=38,
            radius=16
        )
        save_button.pack(side="left")

    def after_data_changed(self):
        self.save_data()
        self.refresh_table()
        self.update_dashboard()

    # -------------------------------------------------------------------------
    # Table logic
    # -------------------------------------------------------------------------

    def is_overdue(self, task):
        if task["status"] == "Completed":
            return False

        try:
            if task["due_time"] == "No time":
                task_due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                return task_due_date < date.today()

            task_due_datetime = datetime.strptime(task["due_date"] + " " + task["due_time"], "%Y-%m-%d %I:%M %p")
            return task_due_datetime < datetime.now()
        except ValueError:
            return False

    def get_due_state(self, task):
        if self.is_overdue(task):
            return "Overdue"

        try:
            task_due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return "Upcoming"

        today = date.today()

        if task_due_date == today:
            return "Today"

        if task_due_date == today + timedelta(days=1):
            return "Tomorrow"

        return "Upcoming"

    def get_table_task(self, task):
        display_task = task.copy()
        display_task["due_state"] = self.get_due_state(task)
        return display_task

    def get_selected_task(self):
        selected_item = self.task_table.selection()

        if not selected_item:
            return None

        task_id = int(selected_item[0])

        for task in self.tasks:
            if task["id"] == task_id:
                return task

        return None

    def set_filter(self, filter_name):
        self.active_filter = filter_name
        self.update_filter_buttons()
        self.refresh_table()

    def update_filter_buttons(self):
        for filter_name, button in self.filter_buttons.items():
            if filter_name == self.active_filter:
                button.set_colors(CYAN_DARK, CYAN_HOVER)
            else:
                button.set_colors(INPUT_BG, GRAY_BUTTON)

    def task_matches_filter(self, task):
        if self.active_filter == "All":
            return True

        if self.active_filter in ["Pending", "In Progress", "Completed"]:
            return task["status"] == self.active_filter

        if self.active_filter == "High Priority":
            return task["priority"] == "High"

        if self.active_filter == "Overdue":
            return self.is_overdue(task)

        return True

    def get_filtered_tasks(self):
        search_text = self.search_entry.get_value().lower()
        tasks_to_show = []

        for task in self.tasks:
            if not self.task_matches_filter(task):
                continue

            task_text = (
                task["title"] + " " +
                task["category"] + " " +
                task["priority"] + " " +
                task["due_date"] + " " +
                self.get_due_state(task) + " " +
                task["due_time"] + " " +
                task["status"] + " " +
                task.get("notes", "")
            ).lower()

            if search_text == "" or search_text in task_text:
                tasks_to_show.append(task)

        return tasks_to_show

    def load_tasks(self, tasks_to_show):
        table_tasks = [self.get_table_task(task) for task in tasks_to_show]
        self.task_table.load_tasks(table_tasks)
        self.show_empty_state(len(tasks_to_show) == 0)
        self.showing_label.config(text=f"Showing {len(tasks_to_show)} of {len(self.tasks)}")
        self.update_action_buttons()

    def refresh_table(self):
        if not hasattr(self, "search_entry"):
            return

        self.load_tasks(self.get_filtered_tasks())

    def search_tasks(self, event=None):
        self.refresh_table()

    def get_due_sort_value(self, task):
        try:
            if task["due_time"] == "No time":
                return datetime.strptime(task["due_date"], "%Y-%m-%d") + timedelta(hours=23, minutes=59)

            return datetime.strptime(task["due_date"] + " " + task["due_time"], "%Y-%m-%d %I:%M %p")
        except ValueError:
            return datetime.max

    def sort_tasks_by_column(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        if column == "priority":
            sort_key = lambda task: PRIORITY_RANK.get(task["priority"], 99)
        elif column == "status":
            sort_key = lambda task: STATUS_RANK.get(task["status"], 99)
        elif column == "due_state":
            sort_key = lambda task: DUE_STATE_RANK.get(self.get_due_state(task), 99)
        elif column in ["due_date", "due_time"]:
            sort_key = self.get_due_sort_value
        else:
            sort_key = lambda task: str(task[column]).lower()

        self.tasks.sort(key=sort_key, reverse=self.sort_reverse)
        self.refresh_table()
        self.save_data()

    # -------------------------------------------------------------------------
    # Dashboard logic
    # -------------------------------------------------------------------------

    def update_dashboard(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["status"] == "Completed")
        progress = sum(1 for task in self.tasks if task["status"] == "In Progress")
        pending = sum(1 for task in self.tasks if task["status"] == "Pending")
        high_priority = sum(1 for task in self.tasks if task["priority"] == "High")

        completion_rate = 0

        if total > 0:
            completion_rate = int((completed / total) * 100)

        self.card_labels["total"].config(text=str(total))
        self.card_labels["completed"].config(text=str(completed))
        self.card_labels["progress"].config(text=str(progress))
        self.card_labels["pending"].config(text=str(pending))
        self.card_labels["high_priority"].config(text=str(high_priority))

        self.progress_text.config(text=f"Completion Progress: {completion_rate}%")
        self.progress_bar.set_progress(completion_rate)


# =============================================================================
# PROGRAM START
# =============================================================================

def run_app():
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()
