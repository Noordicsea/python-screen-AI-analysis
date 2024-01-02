import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, ImageGrab
import pytesseract
import openai
import keyboard
import sys
import time

# Global variables
running = True
user_choice = None
take_screenshot = False

def process_selection(image, coords):
    try:
        x0, y0, x1, y1 = coords['start'] + coords['end']
        x0, x1 = sorted([x0, x1])
        y0, y1 = sorted([y0, y1])
        cropped_image = image.crop((x0, y0, x1, y1))
        text = pytesseract.image_to_string(cropped_image)
        return text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return ""

def query_openai_api(question):
    client = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": question},
        ],
    )
    return client.choices[0].message.content

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

    return coords

def display_menu():
    print("1. Get information")
    print("2. Answer the question")
    print("3. Identify the object")
    print("4. Settings")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice

def process_screenshot_based_on_choice(screenshot):
    global user_choice
    root = tk.Tk()
    root.title("Select Area")
    root.attributes('-fullscreen', True)
    tk_screenshot = ImageTk.PhotoImage(screenshot)
    canvas = Canvas(root, width=screenshot.width, height=screenshot.height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=tk_screenshot, anchor="nw")
    coords = select_area(root, canvas, screenshot)
    root.destroy()
    
    if user_choice in ['1', '2']:
        text = process_selection(screenshot, coords)
        if text:
            response = query_openai_api(text)
            print("OpenAI Response:\n", response)
        else:
            print("No text extracted or text is not a string.")
    elif user_choice == '3':
        # Placeholder for object identification with OpenAI's visual API
        print("Object identification is not implemented yet.")
    elif user_choice == '4':
        # Placeholder for settings
        print("Settings functionality is not implemented yet.")

def start_screenshot_process():
    global take_screenshot
    take_screenshot = True


def stop_program():
    global running
    running = False
    keyboard.unhook_all_hotkeys()

def mode_handler():
    global user_choice
    if user_choice in ['1', '2', '3', '4']:
        while True:
            print("Press 'ctrl+alt+shift+s' for screenshot or 'ctrl+alt+shift+x' to return to menu.")
            keyboard.wait('ctrl+alt+shift+s')
            if not running:
                break
            start_screenshot_process()

def main():
    global running, user_choice
    keyboard.add_hotkey('ctrl+alt+shift+s', start_screenshot_process)
    keyboard.add_hotkey('ctrl+alt+shift+x', stop_program)

    while running:
        user_choice = display_menu()
        if user_choice == '5':
            stop_program()
            break
        elif user_choice in ['1', '2', '3', '4']:
            mode_handler()
        time.sleep(0.1)

    sys.exit(0)

if __name__ == "__main__":
    main()
