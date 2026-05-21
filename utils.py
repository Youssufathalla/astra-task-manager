"""Small drawing and UI helper functions used by different modules."""

import tkinter as tk

def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    """Draw a rounded rectangle on a Canvas using a smoothed polygon."""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def make_label(parent, text, font, fg, bg, **kwargs):
    """Create a Label with common options in one place."""
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kwargs)


def add_accent_line(parent, color, bottom_padding):
    """Add the small colored line at the top of a panel."""
    line = tk.Frame(parent, bg=color, height=5)
    line.pack(fill="x", pady=(0, bottom_padding))
    return line
