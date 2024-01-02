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

choice = None
continue_waiting = True

def start_screenshot_process():
    global choice, continue_waiting
    if choice == '2':
        continue_waiting = False  # Stop waiting for user input
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
            print("Press 'ctrl+alt+shift+s' to screenshot another question or press 'ctrl+alt+shift+x' to exit.")
            continue_waiting = True  # Start waiting for user input again
        else:
            print("No text extracted or text is not a string.")
    else:
        print("Please select 'Answer the question' from the main menu to use this feature.")

def main():
    global choice, continue_waiting
    choice = display_menu()
    keyboard.add_hotkey('ctrl+alt+shift+s', start_screenshot_process)
    keyboard.add_hotkey('ctrl+alt+shift+x', lambda: exit())  # To stop the process

    # User reminder to use hotkeys based on the choice
    if choice == '2':
        print("Press 'ctrl+alt+shift+s' to start the screenshot process for OCR.")
    # Add similar reminders for other choices if needed

    while True:
        if choice == '5':
            break
        elif choice == '1':
            # Code for "Give info"
            pass
        elif choice == '3':
            # Code for "Identify the object"
            pass
        elif choice == '4':
            # Code for "Settings"
            pass

        # Wait for user input via hotkeys
        while continue_waiting:
            time.sleep(0.1)  # Prevent CPU overuse

        # Reset flag and choice for next interaction
        continue_waiting = True
        if choice != '2':
            choice = display_menu()

if __name__ == "__main__":
    main()
