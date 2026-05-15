import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from image_processor import DifferenceGenerator
from game_logic import GameLogic


class SpotTheDifferenceApp:
    """Main GUI application for the Spot the Difference game"""
    
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Spot the Difference Game")
        
        self._generator = DifferenceGenerator()
        self._logic = GameLogic()
        
        self._original_photo = None
        self._modified_photo = None
        self._game_active = False
        
        self._setup_gui()
    
    def _setup_gui(self):
        # Top frame for buttons and labels
        top_frame = tk.Frame(self._root)
        top_frame.pack(pady=10)
        
        self._load_button = tk.Button(top_frame, text="Load Image", command=self._load_image)
        self._load_button.pack(side=tk.LEFT, padx=10)
        
        self._reveal_button = tk.Button(top_frame, text="Reveal", command=self._reveal)
        self._reveal_button.pack(side=tk.LEFT, padx=10)
        
        self._remaining_label = tk.Label(top_frame, text="Remaining: 0", font=("Arial", 14))
        self._remaining_label.pack(side=tk.LEFT, padx=10)
        
        self._mistakes_label = tk.Label(top_frame, text="Mistakes: 0", font=("Arial", 14))
        self._mistakes_label.pack(side=tk.LEFT, padx=10)
        
        # Frame for the two images
        image_frame = tk.Frame(self._root)
        image_frame.pack(pady=10)
        
        # Left canvas - original image (no clicks)
        self._left_canvas = tk.Canvas(image_frame, width=500, height=400, bg="gray")
        self._left_canvas.pack(side=tk.LEFT, padx=5)
        
        # Right canvas - modified image (clickable)
        self._right_canvas = tk.Canvas(image_frame, width=500, height=400, bg="gray")
        self._right_canvas.pack(side=tk.LEFT, padx=5)
        self._right_canvas.bind("<Button-1>", self._on_click)

    def _load_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not file_path:
            return
        
        self._generator.load_image(file_path)
        self._logic.load_new_image(self._generator.get_regions())
        self._game_active = True
        
        self._display_images()
        self._update_labels()

    def _display_images(self):
        original = self._generator.get_original()
        modified = self._generator.get_modified()
        
        # Calculate aspect ratio
        img_h, img_w = original.shape[:2]
        ratio = min(500 / img_w, 400 / img_h)
        new_w = int(img_w * ratio)
        new_h = int(img_h * ratio)
        
        # Store display size for click scaling
        self._display_w = new_w
        self._display_h = new_h
        self._img_w = img_w
        self._img_h = img_h
        
        # Resize keeping aspect ratio
        original_resized = cv2.resize(original, (new_w, new_h))
        modified_resized = cv2.resize(modified, (new_w, new_h))
        
        # Convert BGR to RGB
        original_rgb = cv2.cvtColor(original_resized, cv2.COLOR_BGR2RGB)
        modified_rgb = cv2.cvtColor(modified_resized, cv2.COLOR_BGR2RGB)
        
        # Convert to Tkinter format
        original_pil = Image.fromarray(original_rgb)
        modified_pil = Image.fromarray(modified_rgb)
        
        self._original_photo = ImageTk.PhotoImage(original_pil)
        self._modified_photo = ImageTk.PhotoImage(modified_pil)
        
        # Update canvas sizes
        self._left_canvas.config(width=new_w, height=new_h)
        self._right_canvas.config(width=new_w, height=new_h)
        
        # Clear canvases and display
        self._left_canvas.delete("all")
        self._right_canvas.delete("all")
        
        self._left_canvas.create_image(0, 0, anchor=tk.NW, image=self._original_photo)
        self._right_canvas.create_image(0, 0, anchor=tk.NW, image=self._modified_photo)

    def _update_labels(self):
        remaining = self._logic.get_total_remaining()
        mistakes = self._logic.get_mistakes()
        self._remaining_label.config(text=f"Remaining: {remaining}")
        self._mistakes_label.config(text=f"Mistakes: {mistakes}")

    def _on_click(self, event):
        if not self._game_active:
            return
        
        click_x = event.x
        click_y = event.y
        
        # Scale clicks to match original image size
        scale_x = self._img_w / self._display_w
        scale_y = self._img_h / self._display_h
        actual_x = int(click_x * scale_x)
        actual_y = int(click_y * scale_y)
        
        result = self._logic.check_click(actual_x, actual_y)
        
        if result >= 0:
            region = self._generator.get_regions()[result]
            self._draw_circle(region, "red")
            self._update_labels()
            
            if self._logic.all_found():
                self._game_active = False
                messagebox.showinfo("Well Done!", "You found all the differences!")
        else:
            mistakes = self._logic.record_mistake()
            self._update_labels()
            
            if self._logic.is_game_over():
                self._game_active = False
                found = 5 - len(self._logic.get_unfound_regions())
                messagebox.showwarning(
                    "Game Over",
                    f"Too many mistakes! You found {found} out of 5 differences."
                )

    def _draw_circle(self, region, color):
        x, y, w, h = region
        
        # Scale to canvas size
        scale_x = self._display_w / self._img_w
        scale_y = self._display_h / self._img_h
        
        canvas_x = int(x * scale_x)
        canvas_y = int(y * scale_y)
        canvas_w = int(w * scale_x)
        canvas_h = int(h * scale_y)
        
        self._left_canvas.create_oval(
            canvas_x, canvas_y,
            canvas_x + canvas_w, canvas_y + canvas_h,
            outline=color, width=3
        )
        self._right_canvas.create_oval(
            canvas_x, canvas_y,
            canvas_x + canvas_w, canvas_y + canvas_h,
            outline=color, width=3
        )

    def _reveal(self):
        if not self._game_active:
            return
        
        unfound = self._logic.get_unfound_regions()
        
        for region in unfound:
            self._draw_circle(region, "blue")
        
        self._game_active = False
        messagebox.showinfo(
            "Revealed",
            "All unfound differences have been revealed in blue."
        )

    def run(self):
        self._root.mainloop()