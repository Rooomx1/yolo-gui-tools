# YOLO GUI Tools

A collection of user-friendly GUI tools to streamline your YOLO-based workflows.  
This toolkit includes:

## 🧰 Tools Included

### 1. YOLO Auto Labeling Tool
Automatically generate YOLO-format `.txt` files using your trained YOLOv5 or YOLOv8 model.
- Supports `.pt` model loading
- Easy GUI: select image folder, model, and `data.yaml`
- Compatible with both YOLOv5 and YOLOv8

### 2. YOLO Format Converter
Convert between major annotation formats:
- YOLO ↔ COCO
- YOLO ↔ Pascal VOC
- COCO ↔ YOLO
- Includes class name input
- Simple format selection GUI

### 3. YOLO Data Generator
Generate a complete `data.yaml` file visually:
- Select train/val/test folders
- Add classes manually
- Choose list or dict format for classes
- Save as `data.yaml` with one click

### 4. YOLO Label Inspector ✅ NEW
A GUI-based tool to visually inspect and edit YOLO labels:
- Draw and delete bounding boxes with your mouse
- Custom class shortcuts and colors
- Auto-loads classes from existing `.txt` files
- Progress tracker (e.g., `127/1000 12.7%`)
- Save corrected labels to a separate folder

> ⚙ Shortcut Keys:
> - `z`: Delete box mode  
> - `x`: Save & next  
> - `ESC`: Exit  
> - Number/letter keys: Add box for selected class

---

## 🔽 Download Tools (.exe)

### 🔹 YOLO Auto Labeling Tool (2.6GB)

[📦 Click to download](https://drive.google.com/file/d/1_GdyNwUooAU0tYSeOKy8jhlEPEgCxA1x/view?usp=sharing)

---

### 🔹 YOLO Label Inspector (58.9MB)

[📦 Click to download](https://drive.google.com/file/d/152hvz7TOl_g0P9hUIWoUdrQr3LMN4z2C/view?usp=drive_link)

⚠ No installation required. Just run the `.exe` file.  
ℹ️ Python and dependencies are **not required**.

---

## 📦 How to Use

1. Download the `.exe` file(s) from the links above
2. Run the tool (no installation required)
3. Follow the GUI instructions to label, convert, inspect, or generate data

---

## 🛠 Requirements (for .py files)

```bash
pip install tk torch ultralytics pyyaml
