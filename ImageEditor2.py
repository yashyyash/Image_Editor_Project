import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

        # Remove default title bar
        self.root.overrideredirect(True)

        # Custom Title Bar
        self.title_bar = tk.Frame(self.root, bg="#551a8b", relief="raised", bd=0)
        self.title_bar.pack(side="top", fill="x")

        # Title
        self.title_label = tk.Label(self.title_bar, text=" Image Editor", bg="#551a8b", fg="white")
        self.title_label.pack(side="left", padx=10)

        # Button Frame for the top-right corner buttons
        button_frame = tk.Frame(self.title_bar, bg="#551a8b")
        button_frame.pack(side="right")

        # Minimize Button
        self.minimize_button = tk.Button(button_frame, text="_", command=self.minimize_window, bg="#551a8b", fg="white", bd=0, padx=5, pady=2)
        self.minimize_button.pack(side="left")

        # Maximize/Restore Button
        self.maximize_button = tk.Button(button_frame, text="[]", command=self.toggle_maximize, bg="#551a8b", fg="white", bd=0, padx=5, pady=2)
        self.maximize_button.pack(side="left")

        # Close Button
        self.close_button = tk.Button(button_frame, text="X", command=self.root.destroy, bg="#551a8b", fg="white", bd=0, padx=5, pady=2)
        self.close_button.pack(side="left")

        # Enable window dragging by clicking the title bar
        self.title_bar.bind("<B1-Motion>", self.move_window)

        # Canvas for Image
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.brush_color = "black"
        self.canvas.bind("<B1-Motion>", self.paint)

        # Drawer Frame for the right side buttons
        self.drawer_frame = tk.Frame(self.root, bg="#551a8b", width=150)
        self.drawer_frame.pack(side="right", fill="y")

        # Buttons in the drawer
        open_button = tk.Button(self.drawer_frame, text="Open Image", command=self.open_image, bg="white", fg="#551a8b")
        open_button.pack(fill="x", padx=5, pady=5)

        save_button = tk.Button(self.drawer_frame, text="Save Image", command=self.save_image, bg="white", fg="#551a8b")
        save_button.pack(fill="x", padx=5, pady=5)

        color_button = tk.Button(self.drawer_frame, text="Pick Color", command=self.pick_color, bg="white", fg="#551a8b")
        color_button.pack(fill="x", padx=5, pady=5)

        brush_button = tk.Button(self.drawer_frame, text="Brush", command=self.select_brush, bg="white", fg="#551a8b")
        brush_button.pack(fill="x", padx=5, pady=5)

        # Toggle Drawer Button
        self.toggle_drawer_button = tk.Button(self.root, text="open drawer", command=self.toggle_drawer, bg="#551a8b", fg="white", bd=0, padx=10)
        self.toggle_drawer_button.place(x=1650, y=50)

        self.is_maximized = False
        self.drawer_open = True

    def minimize_window(self):
        self.root.withdraw()  # Hide the window

    def toggle_maximize(self):
        if self.is_maximized:
            self.root.geometry("800x600")
            self.is_maximized = False
        else:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
            self.is_maximized = True

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root}+{event.y_root}')

    def toggle_drawer(self):
        if self.drawer_open:
            self.drawer_frame.pack_forget()
            self.toggle_drawer_button.config(text="<")
            self.drawer_open = False
        else:
            self.drawer_frame.pack(side="right", fill="y")
            self.toggle_drawer_button.config(text=">")
            self.drawer_open = True

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.img_draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Image Editor", "Image saved successfully")

    def pick_color(self):
        self.brush_color = colorchooser.askcolor(color=self.brush_color)[1]

    def select_brush(self):
        self.tool = "brush"

    def paint(self, event):
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)
        if hasattr(self, 'img_draw'):
            self.img_draw.ellipse([x1, y1, x2, y2], fill=self.brush_color, outline=self.brush_color)

    def update_canvas(self):
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor="nw")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
