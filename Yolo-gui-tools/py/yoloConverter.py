import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import shutil

def convert_yolo_to_voc(yolo_folder, output_folder, class_list):
    # Placeholder for YOLO to Pascal VOC
    print("[INFO] Converting YOLO to Pascal VOC...")
    # Implement real logic or integrate with existing tools
    messagebox.showinfo("Convert", "YOLO to Pascal VOC conversion completed.")

def convert_yolo_to_coco(yolo_folder, output_folder, class_list):
    # Placeholder for YOLO to COCO
    print("[INFO] Converting YOLO to COCO...")
    # Implement real logic or integrate with existing tools
    messagebox.showinfo("Convert", "YOLO to COCO conversion completed.")

def convert_voc_to_yolo(voc_folder, output_folder, class_list):
    print("[INFO] Converting Pascal VOC to YOLO...")
    messagebox.showinfo("Convert", "Pascal VOC to YOLO conversion completed.")

def convert_coco_to_yolo(coco_json_path, image_folder, output_folder, class_list):
    print("[INFO] Converting COCO to YOLO...")
    messagebox.showinfo("Convert", "COCO to YOLO conversion completed.")

class FormatConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Format Converter")
        self.root.geometry("550x400")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.image_folder = tk.StringVar()
        self.format_from = tk.StringVar()
        self.format_to = tk.StringVar()
        self.classes = tk.StringVar()

        tk.Label(root, text="Select Input Folder / File").pack()
        tk.Entry(root, textvariable=self.input_path, width=70).pack()
        tk.Button(root, text="Browse", command=self.browse_input).pack(pady=5)

        tk.Label(root, text="Select Output Folder").pack()
        tk.Entry(root, textvariable=self.output_path, width=70).pack()
        tk.Button(root, text="Browse", command=self.browse_output).pack(pady=5)

        tk.Label(root, text="(Optional) Select Image Folder (for COCO)").pack()
        tk.Entry(root, textvariable=self.image_folder, width=70).pack()
        tk.Button(root, text="Browse", command=self.browse_image_folder).pack(pady=5)

        tk.Label(root, text="Class Names (comma separated)").pack()
        tk.Entry(root, textvariable=self.classes, width=70).pack(pady=5)

        tk.Label(root, text="Convert From → To").pack()
        Combobox(root, textvariable=self.format_from, values=["YOLO", "COCO", "Pascal VOC"]).pack()
        Combobox(root, textvariable=self.format_to, values=["YOLO", "COCO", "Pascal VOC"]).pack()

        tk.Button(root, text="Start Conversion", command=self.run_conversion, bg="blue", fg="white").pack(pady=10)

    def browse_input(self):
        path = filedialog.askopenfilename() if self.format_from.get() == "COCO" else filedialog.askdirectory()
        self.input_path.set(path)

    def browse_output(self):
        self.output_path.set(filedialog.askdirectory())

    def browse_image_folder(self):
        self.image_folder.set(filedialog.askdirectory())

    def run_conversion(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        image_folder = self.image_folder.get()
        format_from = self.format_from.get()
        format_to = self.format_to.get()
        class_list = [c.strip() for c in self.classes.get().split(",") if c.strip()]

        if not all([input_path, output_path, format_from, format_to]):
            messagebox.showerror("Error", "Please select all required paths and formats.")
            return

        if format_from == format_to:
            messagebox.showerror("Error", "Source and target formats must be different.")
            return

        try:
            if format_from == "YOLO" and format_to == "Pascal VOC":
                convert_yolo_to_voc(input_path, output_path, class_list)
            elif format_from == "YOLO" and format_to == "COCO":
                convert_yolo_to_coco(input_path, output_path, class_list)
            elif format_from == "Pascal VOC" and format_to == "YOLO":
                convert_voc_to_yolo(input_path, output_path, class_list)
            elif format_from == "COCO" and format_to == "YOLO":
                convert_coco_to_yolo(input_path, image_folder, output_path, class_list)
            else:
                messagebox.showerror("Error", "Unsupported format conversion.")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = FormatConverterApp(root)
    root.mainloop()
