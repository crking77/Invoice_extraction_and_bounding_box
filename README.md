
# 📄 Invoice AI Extraction & Bounding Box Visualization

## 🚀 Overview
This project uses **Google Gemini AI** to extract structured information from invoice PDFs and visualize detected fields by drawing bounding boxes directly onto the document.
### ✨ Features
* Extract key invoice fields:
  * Total amount
  * Tax
  * Sender name
  * Account number
* Get bounding box coordinates for each field
* Draw boxes + labels directly onto PDF
* Fully automated pipeline: **PDF → AI → JSON → Visualization**
---
## 🧠 Tech Stack
* Python
* Google Gemini API
* PyMuPDF (fitz)
* Pydantic
* dotenv
---
## 📂 Project Structure
```
invoice-ai/
│── main.py
│── invoice.pdf
│── output_invoice.pdf
│── .env
│── .gitignore
│── README.md
```
---
## ⚙️ Setup
### 1. Clone repo
```
git clone https://github.com/crking77/Invoice_extraction_and_bounding_box.git
cd Invoice_extraction_and_bounding_box
```
---

### 2. Install dependencies
```
pip install google-generativeai pymupdf pydantic python-dotenv
```
---
### 3. Setup environment variables
Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```
---
## ▶️ Usage
### Run the script:
```
python main.py
```
---
## 📌 Output
### Console:
```json
{
  "total": {...},
  "tax": {...},
  "sender": {...},
  "account": {...}
}
```
### File:
```
output_invoice.pdf
```
👉 PDF will contain:
* 🔴 Red bounding boxes
* 🏷️ Labels (TOTAL, TAX, etc.)
---
## 📐 Bounding Box Format
Gemini returns:
```
[y_min, x_min, y_max, x_max]  (range: 0 → 1000)
```
Converted to PDF coordinates:
```
x = (x / 1000) * page_width
y = (y / 1000) * page_height
```
---

## ⚠️ Important Notes

### 1. Coordinate System

* Origin (0,0) = top-left
* y increases downward
---
### 2. AI Inconsistency
Sometimes Gemini may:
* Return incorrect bounding boxes
* Swap coordinates
* Detect wrong regions
👉 Recommended fix:
* Validate and normalize box values
* Add stricter prompt constraints
---
### 3. Security
* Never commit `.env`
* API key must remain private
---
## 🔥 Future Improvements
* 🎯 Improve bounding box accuracy
* 🎨 Multi-color visualization per field
* 🌐 Build web UI viewer
* 📊 Confidence-based highlighting
* 🧠 Fine-tune prompt for better extraction
---
## 💡 Example Workflow
```
PDF → Gemini AI → JSON → Pydantic → Draw Box → Output PDF
```
---
## 👨‍💻 Author
Ngô Minh Quân
---
## ⭐ If you find this useful
Give it a star ⭐ and build something cool with it 🚀
