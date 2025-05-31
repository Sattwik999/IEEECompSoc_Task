import tkinter as tk
from tkinter import filedialog, Text, messagebox
from PIL import Image, ImageTk
import cv2
import os

from utils import detect_document, extract_text

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 Card/Paper Scanner with OCR")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="Upload an image to scan", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.upload_button.pack(pady=10)

        self.text_box = Text(root, wrap=tk.WORD, height=10, width=100, font=("Courier", 10))
        self.text_box.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not file_path:
            return

        image = cv2.imread(file_path)
        scanned = detect_document(image)

        if scanned is None:
            messagebox.showerror("Error", "Document not detected.")
            return

        output_path = "output/scanned.jpg"
        os.makedirs("output", exist_ok=True)
        cv2.imwrite(output_path, scanned)

        scanned_pil = Image.fromarray(cv2.cvtColor(scanned, cv2.COLOR_BGR2RGB))
        scanned_pil = scanned_pil.resize((500, 300))
        scanned_img_tk = ImageTk.PhotoImage(scanned_pil)
        self.canvas.configure(image=scanned_img_tk)
        self.canvas.image = scanned_img_tk

        text = extract_text(scanned)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()
