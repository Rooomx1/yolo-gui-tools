# 📘 YOLO GUI Tools - Usage Guide

This guide explains how to use each of the included tools in the [YOLO GUI Tools repository](https://github.com/Rooomx1/yolo-gui-tools).

---

## 1. 🔹 YOLO Auto Labeling Tool

**Purpose:** Automatically generate YOLO-format labels from a trained `.pt` model.

**Steps:**
1. Select your trained `.pt` model file
2. Choose the image folder containing `.jpg` or `.png` files
3. Select your `data.yaml` file
4. Select where to save the labels
5. Click “Start Auto Labeling”

**Supports:**
- YOLOv5 (torch hub)
- YOLOv8 (`ultralytics`)

---

## 2. 🔹 YOLO Format Converter

**Purpose:** Convert between YOLO, COCO, and Pascal VOC formats.

**Steps:**
1. Choose input format and output format
2. Select the input `.txt`, `.json`, or `.xml` files
3. Select output folder
4. Input or load class names
5. Click “Convert”

---

## 3. 🔹 YOLO Data Generator

**Purpose:** Easily generate a `data.yaml` file.

**Steps:**
1. Select folders for train / val / test
2. Add class names manually
3. Choose class format (`list` or `dict`)
4. Click “Save data.yaml”

---

## 4. 🔹 YOLO Label Inspector

**Purpose:** Visually inspect and correct bounding boxes in YOLO-labeled images.

**Steps:**
1. Select image folder
2. Select label folder (existing YOLO `.txt`)
3. Select save folder for fixed labels
4. Add class shortcuts or auto-load from `.txt`

**Controls:**
- `z`: delete box mode (click to delete)
- `x`: save & next
- `ESC`: exit
- number/letter keys: add box for selected class
- drag mouse: create new box

---

## 🛠 Requirements (for `.py` version)

```bash
pip install tk torch ultralytics pyyaml
```

---

## ☕ Support

If this tool helped you, please consider supporting me at:  
👉 [Buy Me a Coffee](https://www.buymeacoffee.com/ctpjszzangf)