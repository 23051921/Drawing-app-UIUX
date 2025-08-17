from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw
from tkinter import filedialog

# Functionality for the Drawing App
class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Application")
        self.master.geometry("800x600")

        # Initialize Canvas and Drawing State
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = Canvas(self.master, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=10)

        # Store drawing history for undo/redo
        self.history = []  # Each element is a list of stroke dictionaries
        self.redo_stack = []
        self.current_stroke = []

        # PIL Image for saving
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Add buttons and options
        self.button_frame = Frame(self.master)
        self.button_frame.pack()

        self.color_button = Button(self.button_frame, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=0, column=0, padx=10)

        self.size_label = Label(self.button_frame, text="Pen Size:")
        self.size_label.grid(row=0, column=1, padx=5)

        self.size_var = IntVar(value=2)  # Default pen size
        self.size_slider = Scale(self.button_frame, from_=1, to=10, orient=HORIZONTAL, variable=self.size_var)
        self.size_slider.grid(row=0, column=2, padx=10)

        self.eraser_button = Button(self.button_frame, text="Eraser", command=self.enable_eraser)
        self.eraser_button.grid(row=0, column=9, padx=10)

        self.undo_button = Button(self.button_frame, text="Undo", command=self.undo_last_stroke)
        self.undo_button.grid(row=0, column=3, padx=10)

        self.redo_button = Button(self.button_frame, text="Redo", command=self.redo_last_stroke)
        self.redo_button.grid(row=0, column=4, padx=10)

        self.clear_button = Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=5, padx=10)

        self.bg_button = Button(self.button_frame, text="Background Color", command=self.change_background)
        self.bg_button.grid(row=0, column=6, padx=10)

        self.save_button = Button(self.button_frame, text="Save", command=self.save_canvas)
        self.save_button.grid(row=0, column=7, padx=10)

        self.exit_button = Button(self.button_frame, text="Exit", command=self.master.destroy)
        self.exit_button.grid(row=0, column=8, padx=10)

        # Set initial drawing state
        self.old_x = None
        self.old_y = None
        self.pen_color = "black"

        # Bind mouse events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.start_stroke)  # Left mouse button pressed
        self.canvas.bind("<B1-Motion>", self.draw_line)  # Left mouse button dragging
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

    def start_stroke(self, event):
        """Start a new stroke."""
        self.current_stroke = []
        self.old_x, self.old_y = event.x, event.y

    def draw_line(self, event):
        """Draw lines on the canvas and save the state."""
        if self.old_x and self.old_y:
            # Draw on Canvas
            line_id = self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.size_var.get(), fill=self.pen_color, capstyle=ROUND, smooth=TRUE
            )
            # Draw on PIL image
            self.draw.line(
                [self.old_x, self.old_y, event.x, event.y],
                fill=self.pen_color, width=self.size_var.get()
            )
            # Save to the current stroke
            self.current_stroke.append({
                'id': line_id,
                'coords': [self.old_x, self.old_y, event.x, event.y],
                'color': self.pen_color,
                'size': self.size_var.get()
            })

        self.old_x, self.old_y = event.x, event.y

    def end_stroke(self, event):
        """End the current stroke and save it to the history."""
        if self.current_stroke:
            self.history.append(self.current_stroke)
            if len(self.history) > 50:  # Keep max 50 undo states
                self.history.pop(0)
            self.redo_stack.clear()
        self.old_x, self.old_y = None, None

    def enable_eraser(self):
        """Enable eraser mode by setting pen color to match background and using pen size."""
        self.pen_color = self.canvas["bg"]

    def undo_last_stroke(self):
        """Undo the last stroke."""
        if self.history:
            last_stroke = self.history.pop()
            self.redo_stack.append(last_stroke)
            for line in last_stroke:
                self.canvas.delete(line['id'])

    def redo_last_stroke(self):
        """Redo the last undone stroke."""
        if self.redo_stack:
            last_stroke = self.redo_stack.pop()
            self.history.append(last_stroke)
            for line in last_stroke:
                # Use stored coordinates to recreate the line
                line_id = self.canvas.create_line(
                    line['coords'],  # Use stored coordinates
                    width=line['size'], fill=line['color'], capstyle=ROUND, smooth=TRUE
                )
                # Update the line ID with the new one
                line['id'] = line_id

    def clear_canvas(self):
        """Clear the entire canvas."""
        self.canvas.delete("all")
        self.history.clear()
        self.redo_stack.clear()
        # Clear PIL image
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def change_background(self):
        """Change the background color of the canvas."""
        color = askcolor(color=self.canvas["bg"])[1]  # Returns a tuple, we need the hex color
        if color:
            self.canvas.config(bg=color)
            self.image.paste(Image.new("RGB", (self.canvas_width, self.canvas_height), color))

    def choose_color(self):
        """Open a color chooser and set the pen color."""
        color = askcolor(color=self.pen_color)[1]  # Returns a tuple, we need the hex color
        if color:
            self.pen_color = color

    def save_canvas(self):
        """Save the canvas as an image file with user-specified name."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            self.image.save(file_path)
            print(f"Canvas saved as {file_path}")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = DrawingApp(root)
    root.mainloop()
