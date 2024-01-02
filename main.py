import keyboard
from PIL import ImageGrab
import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk
from ocr import process_selection
from gui import select_area
from openai_api import query_openai_api
from menu import display_menu
import time
import sys
import threading

running = True

def start_screenshot_process():
    screenshot = ImageGrab.grab()
    root = tk.Tk()
    root.title("Select Area for OCR")
    root.attributes('-fullscreen', True)
    tk_screenshot = ImageTk.PhotoImage(screenshot)
    canvas = Canvas(root, width=screenshot.width, height=screenshot.height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=tk_screenshot, anchor="nw")
    extracted_text = select_area(root, canvas, screenshot)
    root.destroy()
    if extracted_text and isinstance(extracted_text, str):
        response = query_openai_api(extracted_text)
        print("OpenAI Response:\n", response)
    else:
        print("No text extracted or text is not a string.")
    print("Press 'ctrl+alt+shift+s' to screenshot another question or press 'ctrl+alt+shift+x' to exit.")

def main():
    global running

    # Setting up hotkeys
    keyboard.add_hotkey('ctrl+alt+shift+s', start_screenshot_process)
    keyboard.add_hotkey('ctrl+alt+shift+x', lambda: stop_program())

    # Main loop
    while running:
        choice = display_menu()

        if choice == '1':
            # Code for "Give info"
            pass
        elif choice == '2':
            # Just a message, actual action is triggered by hotkey
            print("Press 'ctrl+alt+shift+s' to start the screenshot process for OCR.")
        elif choice == '3':
            # Code for "Identify the object"
            pass
        elif choice == '4':
            # Code for "Settings"
            pass
        elif choice == '5':
            stop_program()

        # If choice is not '2', display menu again
        if choice != '2':
            time.sleep(0.1)  # Prevent CPU overuse

    sys.exit(0)

def stop_program():
    global running
    running = False
    keyboard.unhook_all_hotkeys()

if __name__ == "__main__":
    main()
