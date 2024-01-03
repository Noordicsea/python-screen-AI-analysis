import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, ImageGrab
import pytesseract
import openai
import keyboard
import sys
import time
import os

# Global variable to store the user's menu choice
user_choice = None

# Function to process the selected area in the screenshot
def process_selection(image, coords):
    # Try block to handle potential exceptions
    try:
        # Unpack the coordinates from the dictionary and assign them to variables
        x0, y0, x1, y1 = coords['start'] + coords['end']
        # Sort the x coordinates
        x0, x1 = sorted([x0, x1])
        # Sort the y coordinates
        y0, y1 = sorted([y0, y1])
        # Crop the image using the sorted coordinates
        cropped_image = image.crop((x0, y0, x1, y1))
        # Use pytesseract to extract text from the cropped image
        text = pytesseract.image_to_string(cropped_image)
        # Return the extracted text
        return text
    # Exception handling block
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"Error during text extraction: {e}")
        # Return an empty string in case of an error
        return ""



# Function to query the OpenAI API
def query_openai_api(question):
    # Create an OpenAI client
    client = openai.ChatCompletion.create(
        # Use the Babbage model
        model="gpt-4",
        # Send the user's question to the model
        messages=[
            {"role": "user", "content": question},
        ],
    )
    # Return the model's response
    return client.choices[0].message.content

# Function to select an area on the screenshot
def select_area(root, canvas, screenshot):
    # Initialize coordinates dictionary with start and end points
    coords = {'start': (0, 0), 'end': (0, 0)}
    # Initialize rectangle variable
    rect = None
    # Define function to handle mouse click event
    def on_click(event):
        # Update start coordinates on mouse click
        coords['start'] = (event.x, event.y)

    # Define function to handle mouse drag event
    def on_drag(event):
        # Use nonlocal keyword to access rect variable in outer scope
        nonlocal rect
        # Update end coordinates on mouse drag
        coords['end'] = (event.x, event.y)
        # Delete previous rectangle if it exists
        if rect:
            canvas.delete(rect)
        # Create a new rectangle with updated coordinates
        rect = canvas.create_rectangle(*coords['start'], *coords['end'], outline='red')

    # Define function to handle mouse release event
    def on_release(event):
        # Update end coordinates on mouse release
        coords['end'] = (event.x, event.y)
        # Quit the Tkinter main loop
        root.quit()

    # Bind mouse click, drag and release events to their respective handlers
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    # Start the Tkinter main loop
    root.mainloop()

    # Return the final coordinates
    return coords

# Function to display the menu
def display_menu():
    # Print the first option to the user
    print("1. Get information")
    # Print the second option to the user
    print("2. Answer the question")
    # Print the third option to the user
    print("3. Identify the object")
    # Print the fourth option to the user
    print("4. Settings")
    # Print the fifth option to the user
    print("5. Exit")
    # Get the user's choice
    choice = input("Enter your choice: ")
    # Return the user's choice
    return choice

# Function to process the screenshot based on the user's choice
def process_screenshot_based_on_choice(screenshot):
    # Declare global variable user_choice
    global user_choice
    # Create a new Tkinter root window
    root = tk.Tk()
    # Set the title of the window
    root.title("Select Area")
    # Set the window to fullscreen
    root.attributes('-fullscreen', True)
    # Convert the screenshot to a Tkinter-compatible image
    tk_screenshot = ImageTk.PhotoImage(screenshot)
    # Create a new canvas widget with the dimensions of the screenshot
    canvas = Canvas(root, width=screenshot.width, height=screenshot.height)
    # Pack the canvas widget and expand it to fill the window
    canvas.pack(fill="both", expand=True)
    # Draw the screenshot on the canvas
    canvas.create_image(0, 0, image=tk_screenshot, anchor="nw")
    # Call the select_area function to let the user select an area on the screenshot
    coords = select_area(root, canvas, screenshot)
    # Destroy the root window
    root.destroy()
    
    # If the user chose the first or second option
    if user_choice == '1' or user_choice == '2':
        # Process the selected area and extract text
        text = process_selection(screenshot, coords)
        # If text was extracted
        if text:
            # Query the OpenAI API with the extracted text
            response = query_openai_api("""Answer the question correctly: (Remove any odd symbols from the answer.)""" + text)
            # Print the response from the OpenAI API
            print("\nOpenAI Response:\n\033[41m\033[37m", response, "\033[0m")
        else:
            # Print an error message if no text was extracted or the text is not a string
            print("No text extracted or text is not a string.")
    # If the user chose the third option
    elif user_choice == '3':
        # Print a placeholder message for object identification
        print("Object identification is not implemented yet.")
    # If the user chose the fourth option
    elif user_choice == '4':
        # Print a placeholder message for settings
        print("Settings functionality is not implemented yet.")

# Function to start the screenshot process
def start_screenshot_process():
    # Capture the entire screen and store it in the variable screenshot
    screenshot = ImageGrab.grab()
    # Call the function process_screenshot_based_on_choice with the screenshot as argument
    process_screenshot_based_on_choice(screenshot)

# Function to stop the program
# Define the function to stop the program
def stop_program():
    # Declare the global variable 'running'
    global running
    # Set the global variable 'running' to False
    running = False
    # Unhook all hotkeys
    keyboard.unhook_all_hotkeys()

# Main function
def main():
    # Declare global variables 'running' and 'user_choice'
    global running, user_choice
    # Add hotkey 'ctrl+alt+shift+s' to start the screenshot process
    keyboard.add_hotkey('ctrl+alt+shift+s', start_screenshot_process)
    # Add hotkey 'ctrl+alt+shift+x' to stop the program
    keyboard.add_hotkey('ctrl+alt+shift+x', stop_program)
    # Set 'running' to True
    running = True
    user_choice = display_menu()
    # While the program is running
    while running:
        # Display the menu and get the user's choice
        
        # If the user chooses '5', stop the program
        if user_choice == '5':
            stop_program()
        # If the user chooses '1', '2', '3', or '4', wait for the screenshot hotkey
        elif user_choice in ['1', '2', '3', '4']:
            print("Press 'ctrl+alt+shift+s' to start the screenshot process.")
            keyboard.wait('ctrl+alt+shift+s')
            # After screenshot process, loop back to the menu
            continue

if __name__ == "__main__":
    # If the script is run directly (not imported), call the main function
    main()