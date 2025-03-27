import os
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import tempfile
import base64
import torch

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

# Base64-encoded icon (.ico format recommended)
ICON_BASE64 = b'iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAADO3WNhQlgAAM7danVtYgAAAB5qdW1kYzJwYQARABCAAACqADibcQNjMnBhAAAANxVqdW1iAAAASGp1bWRjMm1hABEAEIAAAKoAOJtxA3VybjpjMnBhOjo3ZjUzYmM2Ni0yZjIzLTRhNTktODUyZi1hNjk0ZmQ1NjFhN2YAAAAB4Wp1bWIAAAApanVtZGMyYXMAEQAQgAAAqgA4m3EDYzJwYS5hc3NlcnRpb25zAAAAAQVqdW1iAAAAKWp1bWRj'

def get_temp_icon_path():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ico")
    temp_file.write(base64.b64decode(ICON_BASE64))
    temp_file.close()
    return temp_file.name

# YOLOv5 Auto Labeling Function
def autolabel_yolov5(model_path, image_folder, save_folder):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    imgs = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]

    for img_path in imgs:
        results = model(img_path)
        labels = results.xywh[0].cpu().numpy()
        label_path = os.path.join(save_folder, os.path.basename(img_path).rsplit('.', 1)[0] + '.txt')

        with open(label_path, 'w') as f:
            for *xywh, conf, cls in labels:
                f.write(f"{int(cls)} {' '.join(map(str, xywh))}\n")

# YOLOv8 Auto Labeling Function
def autolabel_yolov8(model_path, image_folder, save_folder):
    if not ULTRALYTICS_AVAILABLE:
        raise ImportError("The 'ultralytics' library is not installed.")

    model = YOLO(model_path)
    imgs = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]

    for img_path in imgs:
        results = model.predict(source=img_path, save=False, save_txt=False)
        boxes = results[0].boxes
        label_path = os.path.join(save_folder, os.path.basename(img_path).rsplit('.', 1)[0] + '.txt')

        with open(label_path, 'w') as f:
            for box in boxes:
                cls = int(box.cls.item())
                x_center, y_center, w, h = box.xywh[0].tolist()
                f.write(f"{cls} {x_center} {y_center} {w} {h}\n")

# Load class names from YAML
def load_classes_from_yaml(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('names', [])

# GUI Class
class AutoLabelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Auto Labeling Tool")
        self.root.geometry("520x420")

        self.model_path = tk.StringVar()
        self.image_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.yaml_path = tk.StringVar()
        self.version = tk.StringVar(value='YOLOv5')

        tk.Label(root, text="Select YOLO Model File (.pt)").pack()
        tk.Entry(root, textvariable=self.model_path, width=60).pack()
        tk.Button(root, text="Browse", command=self.browse_model).pack()

        tk.Label(root, text="Select Image Folder").pack()
        tk.Entry(root, textvariable=self.image_folder, width=60).pack()
        tk.Button(root, text="Browse", command=self.browse_images).pack()

        tk.Label(root, text="Select Output Folder").pack()
        tk.Entry(root, textvariable=self.output_folder, width=60).pack()
        tk.Button(root, text="Browse", command=self.browse_output).pack()

        tk.Label(root, text="Select data.yaml File").pack()
        tk.Entry(root, textvariable=self.yaml_path, width=60).pack()
        tk.Button(root, text="Browse", command=self.browse_yaml).pack()

        tk.Label(root, text="Select YOLO Version").pack()
        Combobox(root, textvariable=self.version, values=["YOLOv5", "YOLOv8"]).pack()

        tk.Button(root, text="Start Auto Labeling", command=self.run_autolabeling, bg="green", fg="white").pack(pady=10)

    def browse_model(self):
        self.model_path.set(filedialog.askopenfilename(filetypes=[("PyTorch Model", "*.pt")]))

    def browse_images(self):
        self.image_folder.set(filedialog.askdirectory())

    def browse_output(self):
        self.output_folder.set(filedialog.askdirectory())

    def browse_yaml(self):
        self.yaml_path.set(filedialog.askopenfilename(filetypes=[("YAML File", "*.yaml")]))

    def run_autolabeling(self):
        model = self.model_path.get()
        image_folder = self.image_folder.get()
        output_folder = self.output_folder.get()
        yaml_path = self.yaml_path.get()
        version = self.version.get()

        # Check for missing paths
        missing = []
        if not model:
            missing.append("YOLO model file")
        if not image_folder:
            missing.append("Image folder")
        if not output_folder:
            missing.append("Output folder")
        if not yaml_path:
            missing.append("data.yaml file")

        if missing:
            messagebox.showerror("Missing Paths", "Please select the following paths:\n- " + "\n- ".join(missing))
            return

        try:
            class_names = load_classes_from_yaml(yaml_path)
            if version == "YOLOv5":
                autolabel_yolov5(model, image_folder, output_folder)
            else:
                autolabel_yolov8(model, image_folder, output_folder)
            messagebox.showinfo("Completed", "✅ Auto labeling has been completed successfully!")
        except Exception as e:
            messagebox.showerror("Execution Error", f"❌ An error occurred:\n\n{type(e).__name__}: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap(get_temp_icon_path())  # Set custom icon from base64
    app = AutoLabelApp(root)
    root.mainloop()
