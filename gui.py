import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk
from ocr import process_selection

def select_area(root, canvas, screenshot):
    coords = {'start': (0, 0), 'end': (0, 0)}
    rect = None

    def on_click(event):
        coords['start'] = (event.x, event.y)

    def on_drag(event):
        nonlocal rect
        coords['end'] = (event.x, event.y)
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(*coords['start'], *coords['end'], outline='red')

    def on_release(event):
        coords['end'] = (event.x, event.y)
        root.quit()

    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()

    return process_selection(screenshot, coords)
