import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageDraw
from tkinter import ttk

# Initialize the main application window
root = tk.Tk()
root.geometry("1000x600")
root.title("Moe's Image Tool")
root.config(bg='#ffb6c1')

history = []

# Function to change the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

# Function to add an image to the canvas
def add_image():
    global file_path, displayed_image, original_image
    file_path = filedialog.askopenfilename(
        initialdir="C:/Users/somem/Tkinter Image Editor/Pictures")
    original_image = Image.open(file_path)
    width, height = int(original_image.width / 2), int(original_image.height / 2)
    original_image = original_image.resize((width, height), Image.LANCZOS)
    displayed_image = ImageTk.PhotoImage(original_image)
    canvas.config(width=original_image.width, height=original_image.height)
    canvas.image = displayed_image
    canvas.create_image(0, 0, image=displayed_image, anchor="nw")

# Function to draw on the canvas
def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="")
    history.append(canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline=""))

# Function to clear the canvas
def clear_canvas():
    canvas.delete("all")
    canvas.create_image(0, 0, image=canvas.image, anchor="nw")

# Function to apply filters to the image
def apply_filter(filter_name):
    global displayed_image
    if file_path:
        image = Image.open(file_path)
        width, height = int(image.width / 2), int(image.height / 2)
        image = image.resize((width, height), Image.LANCZOS)
        if filter_name == "Black and White":
            image = ImageOps.grayscale(image)
        elif filter_name == "Blur":
            image = image.filter(ImageFilter.BLUR)
        elif filter_name == "Emboss":
            image = image.filter(ImageFilter.EMBOSS)
        elif filter_name == "Sharpen":
            image = image.filter(ImageFilter.SHARPEN)
        elif filter_name == "Smooth":
            image = image.filter(ImageFilter.SMOOTH)

        displayed_image = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.create_image(0, 0, image=displayed_image, anchor="nw")

# Function to change the size of the pen
def change_size(size):
    global pen_size
    pen_size = size

# Function to create rounded corner images for buttons
def round_corner(radius, fill):
    corner = Image.new('RGBA', (radius, radius), (255, 255, 255, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner

def add_round_corners(size, color):
    width, height = size
    radius = 20
    image = Image.new('RGBA', size, color)
    corner = round_corner(radius, color)

    # Apply the rounded corners
    image.paste(corner, (0, 0))
    image.paste(corner.rotate(90), (0, height - radius))
    image.paste(corner.rotate(180), (width - radius, height - radius))
    image.paste(corner.rotate(270), (width - radius, 0))

    return ImageTk.PhotoImage(image)

# Function to save the edited image
def save_image():
    if file_path:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            original_image.save(save_path)

# Function to zoom in on the image
def zoom_in():
    global displayed_image, original_image
    width, height = int(original_image.width * 1.2), int(original_image.height * 1.2)
    zoomed_image = original_image.resize((width, height), Image.LANCZOS)
    displayed_image = ImageTk.PhotoImage(zoomed_image)
    canvas.config(width=zoomed_image.width, height=zoomed_image.height)
    canvas.image = displayed_image
    canvas.create_image(0, 0, image=displayed_image, anchor="nw")

# Function to zoom out of the image
def zoom_out():
    global displayed_image, original_image
    width, height = int(original_image.width * 0.8), int(original_image.height * 0.8)
    zoomed_image = original_image.resize((width, height), Image.LANCZOS)
    displayed_image = ImageTk.PhotoImage(zoomed_image)
    canvas.config(width=zoomed_image.width, height=zoomed_image.height)
    canvas.image = displayed_image
    canvas.create_image(0, 0, image=displayed_image, anchor="nw")

# Function to rotate the image
def rotate_image():
    global displayed_image, original_image
    rotated_image = original_image.rotate(90, expand=True)
    displayed_image = ImageTk.PhotoImage(rotated_image)
    original_image = rotated_image
    canvas.config(width=rotated_image.width, height=rotated_image.height)
    canvas.image = displayed_image
    canvas.create_image(0, 0, image=displayed_image, anchor="nw")

pen_color = "black"
pen_size = 5
file_path = ""
displayed_image = None
original_image = None

# Left frame configuration
left_frame = tk.Frame(root, width=200, height=600, bg='#add8e6')
left_frame.pack(side="left", fill="y")

# Canvas configuration
canvas = tk.Canvas(root, width=750, height=600, bg='#ffe4e1')
canvas.pack()

# Create images with rounded corners for buttons
button_image = add_round_corners((120, 40), '#ffb6c1')

# Buttons and controls
image_button = tk.Button(left_frame, text="Add Image",
                         command=add_image, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
image_button.pack(pady=10)

color_button = tk.Button(left_frame, text="Change Pen Color",
                         command=change_color, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
color_button.pack(pady=5)

pen_size_frame = tk.Frame(left_frame, bg='#ffb6c1')
pen_size_frame.pack(pady=5)

pen_size_1 = tk.Radiobutton(
    pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg='#ffb6c1')
pen_size_1.pack(side="left", padx=5)

pen_size_2 = tk.Radiobutton(
    pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg='#ffb6c1')
pen_size_2.pack(side="left", padx=5)
pen_size_2.select()

pen_size_3 = tk.Radiobutton(
    pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg='#ffb6c1')
pen_size_3.pack(side="left", padx=5)

zoom_in_button = tk.Button(left_frame, text="Zoom In",
                           command=zoom_in, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
zoom_in_button.pack(pady=5)

zoom_out_button = tk.Button(left_frame, text="Zoom Out",
                            command=zoom_out, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
zoom_out_button.pack(pady=5)

rotate_button = tk.Button(left_frame, text="Rotate",
                          command=rotate_image, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
rotate_button.pack(pady=5)

clear_button = tk.Button(left_frame, text="Clear",
                         command=clear_canvas, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
clear_button.pack(pady=10)

# Filter selection
filter_label = tk.Label(left_frame, text="Select Filter", bg='#add8e6')
filter_label.pack()

filter_combobox = ttk.Combobox(left_frame, values=["Black and White", "Blur",
                                                   "Emboss", "Sharpen", "Smooth"])
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>",
                     lambda event: apply_filter(filter_combobox.get()))

# Save button
save_button = tk.Button(left_frame, text="Save",
                        command=save_image, image=button_image, borderwidth=0, compound="center", bg='#ffb6c1')
save_button.pack(pady=20)

# Canvas bindings
canvas.bind("<B1-Motion>", draw)
root.mainloop()
