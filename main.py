import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

# Application details
app = {
    "label": "Detection Program",
    "file": "gesture2.py",  # Path to your game script
    "image": "./images/bg.png",  # Path to the app image
    "bg_image": "bg.png",  # Path to the static background image in the same folder
    "description": "Interpreting sign language into digital communication.",
}

# Function to run the application
def run_app(app_file, bg_image):
    try:
        # Update the background image
        update_game_background(bg_image)

        # Launch the game script
        if os.path.isfile(app_file):
            subprocess.Popen(["python3", app_file])
        else:
            print(f"Error: {app_file} not found.")
    except Exception as e:
        print(f"Error running {app_file}: {str(e)}")

# Function to update the background image
def update_game_background(bg_image_path):
    try:
        # Debugging: Check if the file exists
        if not os.path.isfile(bg_image_path):
            print(f"Background image not found: {bg_image_path}")
            return

        # Debugging: Print the loading process
        print(f"Loading background image: {bg_image_path}")

        # Open the background image
        bg_image = Image.open(bg_image_path)

        # Debugging: Print image size before resizing
        print(f"Original image size: {bg_image.size}")

        # Resize the image to fit the window dimensions
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)

        # Convert the image for Tkinter compatibility
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Update the background label with the new image
        bg_label.config(image=bg_image_tk)
        bg_label.image = bg_image_tk  # Prevent garbage collection

        # Debugging: Success message
        print("Background image successfully updated.")
    except Exception as e:
        print(f"Error setting background image: {str(e)}")

# Function to exit the application when Escape is pressed
def on_escape(event):
    root.quit()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Game Launcher")
root.attributes('-fullscreen', True)  # Make window full screen

# Get the window dimensions
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

# Create a label to hold the static background image
bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)  # Stretch to cover the entire window

# Add a title label
title_label = tk.Label(
    root,
    text="Gesture Detection Program",
    font=("Helvetica", 60, "bold"),
    bg="black",  # Set background color to black
    fg="#ffb20a"  # Neon green for title
)
title_label.pack(pady=20)

# Create a frame for the app details (adjusted size)
app_frame = tk.Frame(root, bg="grey", bd=5, relief="raised", padx=40, pady=40, width=600, height=400)
app_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Load the app image
try:
    app_image = Image.open(app["image"])
    app_image = app_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize image
    app_image_tk = ImageTk.PhotoImage(app_image)
except Exception as e:
    app_image_tk = None
    print(f"Error loading image for {app['label']}: {str(e)}")

# App image
if app_image_tk:
    app_img_label = tk.Label(app_frame, image=app_image_tk, bg="black")
    app_img_label.image = app_image_tk  # Keep a reference to the image
    app_img_label.grid(row=0, column=0, pady=10)

# App title and description
title_label = tk.Label(
    app_frame,
    text=app["label"],
    font=("Helvetica", 18, "bold"),
    fg="white",
    bg="grey"
)
description_label = tk.Label(
    app_frame,
    text=app["description"],
    font=("Helvetica", 12),
    fg="white",
    bg="grey",
    wraplength=300
)
title_label.grid(row=1, column=0, pady=5)
description_label.grid(row=2, column=0, pady=5)

# App button
play_button = tk.Button(
    app_frame,
    text="Start",
    command=lambda: run_app(app["file"], app["bg_image"]),
    font=("Arial", 14, "bold"),
    bg="#eae2b7",
    fg="black",
    activebackground="black",
    activeforeground="white",
    relief="raised",
    width=15,
    height=2
)
play_button.grid(row=3, column=0, pady=10)

# Add a footer
footer_label = tk.Label(
    root,
    text="Click 'Start' to initiate the detection!",
    font=("Helvetica", 14, "italic"),
    bg="black",
    fg="#ffb20a"
)
footer_label.pack(side="bottom", pady=20)

# Update the background image to the static one
update_game_background(app["bg_image"])

# Bind the Escape key to exit the application
root.bind("<Escape>", on_escape)

# Bind the Enter key to start the application
root.bind("<Return>", lambda event: run_app(app["file"], app["bg_image"]))

# Start the application
root.mainloop()
