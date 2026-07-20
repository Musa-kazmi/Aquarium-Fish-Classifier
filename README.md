# 🐠 AquaVision — Aquarium Fish Classifier

AquaVision is a professional, production-grade Streamlit web application that classifies **6 species of aquarium and freshwater fish** using a custom-trained **MobileNetV2** deep learning model.

Designed with a premium dark ocean theme, the app offers single-image upload, real-time prediction confidence metrics with Plotly charts, batch image processing, and a detailed species encyclopedia.

---

## ✨ Features

- **🔍 Classify Page**: Upload any fish image (JPG, PNG, WEBP) to get predictions, confidence charts (bar + radar), and detailed species profiles.
- **📊 Batch Processing**: Process multiple images at once in a grid layout with bulk summary metrics.
- **📋 History**: Session-based classification log with a species distribution donut chart.
- **🧠 Model Info**: Technical specs of the neural network pipeline (optimizer, validation accuracy, model parameters).
- **🐟 Fish Encyclopedia**: Comprehensive facts about the 6 supported species.
- **📓 Training Notebook**: Includes `image_classifier.ipynb` showing model training, data augmentation, MobileNetV2 transfer learning, and evaluation.

---

## 🐟 Supported Species

The model classifies the following 6 species (alphabetically ordered matching the Keras output):
1. **Bete** (Siamese Fighting Fish)
2. **Cray** (Freshwater Crayfish)
3. **Discuss** (Discus Fish)
4. **Gold** (Goldfish)
5. **Guppy** (Rainbow Fish)
6. **Oscar** (Velvet Cichlid)

---

## 📂 Repository Structure

- `app.py`: Main Streamlit application
- `styles.py`: Custom CSS styling for the dark ocean theme
- `utils.py`: Image preprocessing and Keras model inference logic
- `fish_data.py`: Fish species database and facts
- `image_classifier.ipynb`: Original Jupyter Notebook used to train the MobileNetV2 model
- `best_fish_model.keras`: Trained model weights file
- `requirements.txt`: Python package requirements

---

## 🛠️ Tech Stack

- **Streamlit**: App frontend framework
- **TensorFlow / Keras**: Deep learning model & training
- **Plotly**: Dynamic visualization charts
- **Pillow**: Image processing utilities
- **NumPy**: Numeric computations

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Musa-Kazmi/aquavision-fish-classifier.git
cd aquavision-fish-classifier
```

### 2. Create a virtual environment & install requirements
It is recommended to run this project in **Python 3.10 to 3.12** since TensorFlow does not support Python 3.13+ on Windows yet.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# OR
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser.
