import tkinter as tk  # Import the tkinter library for creating the GUI components
from tkinter import colorchooser, filedialog, messagebox  # Import specific modules from tkinter for additional functionalities
from PIL import Image, ImageDraw, ImageTk  # Import necessary modules from the PIL (Pillow) library for image processing

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")  # Set the title of the main window
        self.root.geometry("1000x600")  # Set the size of the main window (width x height)
        
        # Create a canvas widget where images can be displayed and edited
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        # Place the canvas in the grid layout of the window, spanning 4 columns
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.brush_color = "black"  # Set the default brush color to black
        # Bind the left mouse button click and drag event to the 'paint' method
        self.canvas.bind("<B1-Motion>", self.paint)
        
        # Create buttons and their functionalities
        open_button = tk.Button(root, text="Open Image", command=self.open_image)
        open_button.grid(row=1, column=0, padx=10, pady=10)  # Place the button in the grid layout

        save_button = tk.Button(root, text="Save Image", command=self.save_image)
        save_button.grid(row=1, column=1, padx=10, pady=10)  # Place the button in the grid layout

        color_button = tk.Button(root, text="Pick Color", command=self.pick_color)
        color_button.grid(row=1, column=2, padx=10, pady=10)  # Place the button in the grid layout

        brush_button = tk.Button(root, text="Brush", command=self.select_brush)
        brush_button.grid(row=1, column=3, padx=10, pady=10)  # Place the button in the grid layout

    def open_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename()
        if file_path:  # If a file is selected
            self.image = Image.open(file_path)  # Open the image using PIL
            self.img_draw = ImageDraw.Draw(self.image)  # Prepare the image for drawing
            self.update_canvas()  # Update the canvas to display the image

    def save_image(self):
        # Open a file dialog to specify where to save the image, defaulting to PNG format
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:  # If a file path is provided
            self.image.save(file_path)  # Save the image to the specified path
            # Show a message box confirming that the image was saved successfully
            messagebox.showinfo("Image Editor", "Image saved successfully")

    def pick_color(self):
        # Open a color chooser dialog to select a brush color
        self.brush_color = colorchooser.askcolor(color=self.brush_color)[1]

    def select_brush(self):
        # Set the current tool to 'brush' (this could be expanded for other tools)
        self.tool = "brush"

    def paint(self, event):
        # Calculate the coordinates for the oval (brush stroke)
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        # Draw the oval on the canvas with the selected brush color
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)

        # If the image is being edited (i.e., img_draw exists), draw on the image too
        if hasattr(self, 'img_draw'):
            self.img_draw.ellipse([x1, y1, x2, y2], fill=self.brush_color, outline=self.brush_color)

    def update_canvas(self):
        # Convert the image to a format suitable for display on the tkinter canvas
        self.canvas_image = ImageTk.PhotoImage(self.image)
        # Place the image on the canvas at the top-left corner (0,0)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor="nw")

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window (root)
    app = ImageEditor(root)  # Create an instance of the ImageEditor class with the root window
    root.mainloop()  # Start the tkinter main event loop to keep the window open
