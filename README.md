## Real-Time Object & Face Detection with Beautification

**即時物件偵測與人臉美化系統**

---

### 📖 Overview | 專案簡介

This project is a **real-time computer vision application** that integrates **YOLOv5 object detection**, **Mediapipe face beautification**, and **OpenCV image processing** into a PyQt5-based GUI.

本專案是一個**即時電腦視覺應用程式**，整合了 **YOLOv5 物件偵測**、**Mediapipe 人臉美化**與 **OpenCV 影像處理**，並使用 **PyQt5** 建立圖形化使用介面。

---

### ✨ Features | 功能特點

* 🎥 **Real-time Camera Processing** — Supports switching between **webcam** and **loaded images**
  🎥 **即時攝影機處理** — 支援**攝影機**與**載入圖片**的切換
* 📦 **YOLOv5 Object Detection** — Detects common objects with bounding boxes
  📦 **YOLOv5 物件偵測** — 偵測常見物件並繪製框框
* 💄 **Face Beautification** — Smooth skin, brighten face using Mediapipe Face Mesh
  💄 **人臉美化** — 使用 Mediapipe Face Mesh 進行皮膚平滑與臉部亮化
* 🎨 **Image Effects** — Apply grayscale, blur, and edge detection
  🎨 **影像特效** — 套用灰階、模糊與邊緣偵測
* 💾 **Save Processed Images** — Export processed results as image files
  💾 **儲存處理後圖片** — 將處理後的結果匯出成圖片
* 🔄 **Reset Function** — Clear all effects and restore the original image
  🔄 **重置功能** — 清除所有效果並恢復原始圖片

---

### 🛠 Tech Stack | 技術堆疊

* **Python 3.8+**
* **PyQt5** — GUI Framework
* **OpenCV** — Image & Video Processing
* **YOLOv5** — Object Detection
* **Mediapipe** — Face Mesh Beautification
* **Torch** — Deep Learning Framework

---

### 📦 Installation & Usage | 安裝與使用

#### 1️⃣ Clone Repository | 複製專案

```bash
git clone https://github.com/your-username/object-face-detector.git
cd object-face-detector
```

#### 2️⃣ Install Dependencies | 安裝相依套件

```bash
pip install -r requirements.txt
```

#### 3️⃣ Download YOLOv5 Model | 下載 YOLOv5 模型

Download `yolov5s.pt` and place it in the project directory
下載 `yolov5s.pt` 並放在專案資料夾中

```bash
wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt
```

#### 4️⃣ Run Application | 執行程式

```bash
python main_app.py
```

---

### 📂 Project Structure | 專案結構

```
object-face-detector/
│── main_app.py           # Main GUI application
│── object_detector.py    # YOLOv5 object detection module
│── face_beautifier.py    # Mediapipe face beautification module
│── requirements.txt      # Required dependencies
│── yolov5s.pt            # YOLOv5 model file (downloaded separately)
│── assets/               # (Optional) screenshots or sample images
```

---

### 🚀 Future Improvements | 未來改進方向

* ✅ Support custom-trained YOLOv5 models | 支援自訂訓練的 YOLOv5 模型
* ✅ GPU acceleration toggle | GPU 加速切換
* ✅ Video file input & batch processing | 支援影片檔與批次處理
* ✅ Enhanced UI design | 改進 UI 設計

---

### 📜 License | 授權

MIT License — You are free to use and modify.
MIT 授權 — 可自由使用與修改。

---

### 👤 Author | 作者

Developed by Ching-Han Chang

Email: chinhanchang@gmail.com

GitHub: https://github.com/Hank0421

