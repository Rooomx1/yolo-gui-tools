import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser, Frame, Canvas
import glob
import random

class_settings = {}
colors = []

class LabelInspectorApp:
    def __init__(self, master):
        self.master = master
        master.title("YOLO Label Inspector")

        self.image_dir = tk.StringVar()
        self.label_dir = tk.StringVar()
        self.save_dir = tk.StringVar()

        tk.Label(master, text="Image Folder").pack()
        tk.Entry(master, textvariable=self.image_dir, width=60).pack()
        tk.Button(master, text="Browse", command=self.browse_image_dir).pack()

        tk.Label(master, text="Label Folder").pack()
        tk.Entry(master, textvariable=self.label_dir, width=60).pack()
        tk.Button(master, text="Browse", command=self.browse_label_dir).pack()

        tk.Label(master, text="Save Folder (for corrected labels)").pack()
        tk.Entry(master, textvariable=self.save_dir, width=60).pack()
        tk.Button(master, text="Browse", command=self.browse_save_dir).pack()

        tk.Label(master, text="Class List").pack()
        self.class_frame = Frame(master)
        self.class_frame.pack()
        tk.Button(master, text="Add Class", command=self.add_class).pack(pady=5)

        tk.Button(master, text="Start Inspection", command=self.start_inspection, bg="green", fg="white").pack(pady=10)

    def browse_image_dir(self):
        self.image_dir.set(filedialog.askdirectory())

    def browse_label_dir(self):
        self.label_dir.set(filedialog.askdirectory())
        self.load_classes_from_labels()

    def browse_save_dir(self):
        self.save_dir.set(filedialog.askdirectory())

    def load_classes_from_labels(self):
        global class_settings, colors
        class_settings.clear()
        colors.clear()
        used_keys = set()
        label_path = self.label_dir.get()
        txt_files = glob.glob(os.path.join(label_path, "*.txt"))
        found_classes = set()
        for txt in txt_files:
            with open(txt, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 1:
                        cls_id = int(float(parts[0]))
                        found_classes.add(cls_id)

        for cls_id in sorted(found_classes):
            name = f"class_{cls_id}"
            key = chr(49 + cls_id) if 49 + cls_id <= 57 else chr(97 + cls_id - 10)  # '1' ~ '9' or 'a' ~
            while key in used_keys:
                cls_id += 1
                key = chr(97 + cls_id)
            used_keys.add(key)
            class_settings[name] = key
            colors.append(tuple(random.randint(50, 255) for _ in range(3)))
        self.rebuild_class_list_frame()

    def rebuild_class_list_frame(self):
        for widget in self.class_frame.winfo_children():
            widget.destroy()

        for i, (name, key) in enumerate(class_settings.items()):
            color_box = Canvas(self.class_frame, width=20, height=20)
            color_box.grid(row=i, column=0, padx=3)
            color_box.create_rectangle(0, 0, 20, 20, fill=self.rgb_to_hex(colors[i]), outline="")
            tk.Label(self.class_frame, text=f"{name} (Key: {key})").grid(row=i, column=1, sticky="w")
            tk.Button(self.class_frame, text="Delete", command=lambda n=name, idx=i: self.delete_class(n, idx)).grid(row=i, column=2)

    def delete_class(self, name, index):
        if name in class_settings:
            del class_settings[name]
            if index < len(colors):
                colors.pop(index)
            self.rebuild_class_list_frame()

    def add_class(self):
        class_name = simpledialog.askstring("Class Name", "Enter class name:")
        if class_name:
            key = simpledialog.askstring("Shortcut Key", f"Set shortcut key for '{class_name}':")
            if key:
                color = colorchooser.askcolor(title=f"Choose color for '{class_name}'")[0]
                if color:
                    class_settings[class_name] = key
                    colors.append(tuple(map(int, color)))
                    self.rebuild_class_list_frame()

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def start_inspection(self):
        img_dir = self.image_dir.get()
        label_dir = self.label_dir.get()
        save_dir = self.save_dir.get()

        if not all([img_dir, label_dir, save_dir]):
            messagebox.showerror("Error", "모든 경로를 설정해야 합니다.")
            return

        if not class_settings:
            messagebox.showerror("Error", "최소 하나 이상의 클래스를 추가해야 합니다.")
            return

        self.master.destroy()
        run_inspection(img_dir, label_dir, save_dir)


def run_inspection(img_dir, label_dir, save_dir):
    img_files = sorted(glob.glob(os.path.join(img_dir, '*.jpg')) + glob.glob(os.path.join(img_dir, '*.png')))
    total = len(img_files)
    index = 0
    label_names = list(class_settings.keys())

    while index < total:
        img_path = img_files[index]
        base = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(label_dir, base + ".txt")
        save_path = os.path.join(save_dir, base + ".txt")

        img = cv2.imread(img_path)
        if img is None:
            index += 1
            continue

        h, w = img.shape[:2]
        boxes = []

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    parts = list(map(float, line.strip().split()))
                    if len(parts) != 5:
                        continue
                    cls, x, y, bw, bh = parts
                    x1 = int((x - bw/2) * w)
                    y1 = int((y - bh/2) * h)
                    x2 = int((x + bw/2) * w)
                    y2 = int((y + bh/2) * h)
                    boxes.append([int(cls), x1, y1, x2, y2])

        drawing = False
        current_mode = None
        selected_class = None
        start_point = (-1, -1)

        def draw():
            disp = img.copy()
            for cls, x1, y1, x2, y2 in boxes:
                color = colors[cls % len(colors)]
                name = label_names[cls] if cls < len(label_names) else f"class_{cls}"
                cv2.rectangle(disp, (x1, y1), (x2, y2), color, 2)
                cv2.putText(disp, f"{name} ({cls})", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            progress = f"{index+1}/{total} {round((index+1)/total*100, 1)}%"
            cv2.putText(disp, progress, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (200,255,200), 2)
            return disp

        def mouse(event, x, y, flags, param):
            nonlocal drawing, start_point, current_mode, selected_class
            if current_mode == 'delete' and event == cv2.EVENT_LBUTTONDOWN:
                for i, (cls, x1, y1, x2, y2) in enumerate(boxes):
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        boxes.pop(i)
                        break
                current_mode = None
            elif current_mode == 'add':
                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    start_point = (x, y)
                elif event == cv2.EVENT_MOUSEMOVE and drawing:
                    temp = draw()
                    cv2.rectangle(temp, start_point, (x, y), colors[selected_class % len(colors)], 1)
                    cv2.imshow("Inspector", temp)
                elif event == cv2.EVENT_LBUTTONUP and drawing:
                    drawing = False
                    x1, y1 = start_point
                    x2, y2 = x, y
                    x1, x2 = sorted([x1, x2])
                    y1, y2 = sorted([y1, y2])
                    boxes.append([selected_class, x1, y1, x2, y2])
                    current_mode = None

        cv2.namedWindow("Inspector")
        cv2.setMouseCallback("Inspector", mouse)

        while True:
            disp = draw()
            cv2.imshow("Inspector", disp)
            key = cv2.waitKey(1)

            if key == ord('z'):
                current_mode = 'delete'
            elif key == ord('x'):
                with open(save_path, 'w') as f:
                    for cls, x1, y1, x2, y2 in boxes:
                        x_c = (x1 + x2)/2 / w
                        y_c = (y1 + y2)/2 / h
                        bw = (x2 - x1) / w
                        bh = (y2 - y1) / h
                        f.write(f"{cls} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")
                break
            elif key == 27:
                cv2.destroyAllWindows()
                exit()
            elif key != -1:
                try:
                    key_char = chr(key)
                    if key_char in class_settings.values():
                        selected_class = list(class_settings.values()).index(key_char)
                        current_mode = 'add'
                except ValueError:
                    pass

        cv2.destroyWindow("Inspector")
        index += 1

if __name__ == '__main__':
    root = tk.Tk()
    app = LabelInspectorApp(root)
    root.mainloop()
