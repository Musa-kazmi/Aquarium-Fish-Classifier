"""
Utility functions for the Fish Classifier application.
Handles model loading, image preprocessing, and predictions.
"""

import numpy as np
from PIL import Image
import os
import time

# ═══════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════

IMG_SIZE = (224, 224)

CLASS_NAMES = [
    "Bete",
    "Cray",
    "Discuss",
    "Gold",
    "Guppy",
    "Oscar",
]

MODEL_INFO = {
    "architecture": "MobileNetV2 (Transfer Learning)",
    "input_size": "224 × 224 × 3",
    "num_classes": 6,
    "framework": "TensorFlow / Keras",
    "optimizer": "Adam",
    "loss_function": "Sparse Categorical Crossentropy",
    "preprocessing": "Rescaling (1./255)",
    "augmentation": "RandomFlip, RandomRotation, RandomZoom",
    "callbacks": "EarlyStopping, ModelCheckpoint",
    "dataset": "Aquarium Fish Classification (Kaggle)",
    "model_file": "best_fish_model.keras",
}


# ═══════════════════════════════════════════════════════
# MODEL LOADING
# ═══════════════════════════════════════════════════════

def load_model(model_path: str):
    """
    Load the Keras model from disk.

    Args:
        model_path: Path to the .keras model file

    Returns:
        Loaded Keras model or None if loading fails
    """
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def get_model_path() -> str:
    """
    Determine the model file path.
    Checks current directory first, then Downloads folder.

    Returns:
        Path to the model file
    """
    # Check current directory
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_fish_model.keras")
    if os.path.exists(local_path):
        return local_path

    # Check Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", "best_fish_model.keras")
    if os.path.exists(downloads_path):
        return downloads_path

    return local_path  # Default — will show error if not found


# ═══════════════════════════════════════════════════════
# IMAGE PREPROCESSING
# ═══════════════════════════════════════════════════════

def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess a PIL image for model prediction.

    Args:
        image: PIL Image object

    Returns:
        Preprocessed numpy array ready for model input
    """
    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize to expected input size
    image = image.resize(IMG_SIZE, Image.Resampling.LANCZOS)

    # Convert to numpy array (keep in [0, 255] range since tf.keras.applications.mobilenet_v2.preprocess_input
    # is built inside the model config as TrueDivide and Subtract layers)
    img_array = np.array(image, dtype=np.float32)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# ═══════════════════════════════════════════════════════
# PREDICTION
# ═══════════════════════════════════════════════════════

def predict(model, image: Image.Image) -> dict:
    """
    Run prediction on a single image.

    Args:
        model: Loaded Keras model
        image: PIL Image object

    Returns:
        Dictionary with prediction results:
        {
            "top_class": str,
            "top_confidence": float,
            "all_predictions": dict[str, float],
            "inference_time_ms": float
        }
    """
    # Preprocess the image
    processed_img = preprocess_image(image)

    # Run inference with timing
    start_time = time.time()
    predictions = model.predict(processed_img, verbose=0)
    inference_time = (time.time() - start_time) * 1000  # Convert to ms

    # Get prediction probabilities
    probs = predictions[0]

    # If the output uses softmax, probs will already be normalized
    # Otherwise, apply softmax
    if np.sum(probs) < 0.99 or np.sum(probs) > 1.01:
        exp_probs = np.exp(probs - np.max(probs))
        probs = exp_probs / np.sum(exp_probs)

    # Create predictions dictionary
    all_predictions = {}
    for i, class_name in enumerate(CLASS_NAMES):
        all_predictions[class_name] = float(probs[i])

    # Sort by confidence (descending)
    all_predictions = dict(
        sorted(all_predictions.items(), key=lambda x: x[1], reverse=True)
    )

    # Get top prediction
    top_class = max(all_predictions, key=all_predictions.get)
    top_confidence = all_predictions[top_class]

    return {
        "top_class": top_class,
        "top_confidence": top_confidence,
        "all_predictions": all_predictions,
        "inference_time_ms": round(inference_time, 1),
    }


def get_confidence_color(confidence: float) -> str:
    """
    Return a color based on confidence level.

    Args:
        confidence: Float between 0 and 1

    Returns:
        Hex color string
    """
    if confidence >= 0.8:
        return "#10b981"  # Green — high confidence
    elif confidence >= 0.5:
        return "#f59e0b"  # Amber — medium confidence
    else:
        return "#ef4444"  # Red — low confidence


def get_confidence_label(confidence: float) -> str:
    """
    Return a human-readable confidence label.

    Args:
        confidence: Float between 0 and 1

    Returns:
        Confidence level string
    """
    if confidence >= 0.9:
        return "Very High"
    elif confidence >= 0.7:
        return "High"
    elif confidence >= 0.5:
        return "Moderate"
    elif confidence >= 0.3:
        return "Low"
    else:
        return "Very Low"
