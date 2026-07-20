"""
🐠 Aquarium Fish Classifier — Professional Streamlit Application
Powered by MobileNetV2 Transfer Learning
Classifies 8 species of aquarium/freshwater fish.
"""

import streamlit as st

# Save original markdown function and override to strip indentation from HTML
_original_markdown = st.markdown
def custom_markdown(body, *args, **kwargs):
    if isinstance(body, str) and kwargs.get('unsafe_allow_html', False):
        body = '\n'.join(line.strip() for line in body.split('\n'))
    return _original_markdown(body, *args, **kwargs)
st.markdown = custom_markdown

import numpy as np
from PIL import Image
import plotly.graph_objects as go
import time
import io
import os
from datetime import datetime

# Local modules
from styles import get_main_styles
from utils import (
    load_model, get_model_path, preprocess_image, predict,
    CLASS_NAMES, MODEL_INFO, IMG_SIZE,
    get_confidence_color, get_confidence_label,
)
from fish_data import get_fish_info, get_all_species, FISH_DATABASE


# ═══════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="AquaVision — Fish Classifier",
    page_icon="🐠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject CSS
st.markdown(get_main_styles(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════

if "model" not in st.session_state:
    st.session_state.model = None
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
if "history" not in st.session_state:
    st.session_state.history = []
if "total_predictions" not in st.session_state:
    st.session_state.total_predictions = 0


# ═══════════════════════════════════════════════════════
# MODEL LOADING
# ═══════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def cached_load_model():
    """Load and cache the model."""
    model_path = get_model_path()
    if os.path.exists(model_path):
        model = load_model(model_path)
        return model
    return None


def ensure_model_loaded():
    """Ensure model is loaded into session state."""
    if not st.session_state.model_loaded:
        with st.spinner("🔄 Loading AI model..."):
            model = cached_load_model()
            if model is not None:
                st.session_state.model = model
                st.session_state.model_loaded = True
                return True
            else:
                return False
    return True


# ═══════════════════════════════════════════════════════
# HELPER: PLOTLY CHARTS
# ═══════════════════════════════════════════════════════

def create_confidence_chart(predictions: dict) -> go.Figure:
    """Create a beautiful horizontal bar chart for prediction confidences."""
    species = list(predictions.keys())
    confidences = [v * 100 for v in predictions.values()]

    # Color gradient based on confidence
    colors = []
    for conf in confidences:
        if conf >= 80:
            colors.append("#10b981")
        elif conf >= 50:
            colors.append("#06b6d4")
        elif conf >= 20:
            colors.append("#3b82f6")
        else:
            colors.append("#64748b")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=species[::-1],
        x=confidences[::-1],
        orientation="h",
        marker=dict(
            color=colors[::-1],
            line=dict(width=0),
            cornerradius=6,
        ),
        text=[f"{c:.1f}%" for c in confidences[::-1]],
        textposition="auto",
        textfont=dict(color="white", size=13, family="Inter"),
        hovertemplate="<b>%{y}</b><br>Confidence: %{x:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter"),
        xaxis=dict(
            title=dict(text="Confidence (%)", font=dict(size=12, color="#64748b")),
            range=[0, 105],
            gridcolor="rgba(255,255,255,0.04)",
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(size=13, color="#f1f5f9"),
        ),
        margin=dict(l=10, r=20, t=10, b=40),
        height=340,
        bargap=0.25,
    )

    return fig


def create_radar_chart(predictions: dict) -> go.Figure:
    """Create a radar/spider chart for prediction distribution."""
    species = list(predictions.keys())
    values = [v * 100 for v in predictions.values()]
    # Close the polygon
    values_closed = values + [values[0]]
    species_closed = species + [species[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=species_closed,
        fill="toself",
        fillcolor="rgba(6,182,212,0.15)",
        line=dict(color="#06b6d4", width=2),
        marker=dict(size=6, color="#06b6d4"),
        hovertemplate="<b>%{theta}</b><br>%{r:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.06)",
                tickfont=dict(size=9, color="#64748b"),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.06)",
                tickfont=dict(size=11, color="#94a3b8"),
            ),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=60, t=30, b=30),
        height=350,
        showlegend=False,
    )

    return fig


# ═══════════════════════════════════════════════════════
# HELPER: HTML COMPONENTS
# ═══════════════════════════════════════════════════════

def render_hero():
    """Render the hero header."""
    st.markdown("""
    <div class="hero-header">
        <h1>🐠 AquaVision</h1>
        <p>AI-Powered Aquarium Fish Classification — Identify 6 freshwater species with deep learning</p>
    </div>
    """, unsafe_allow_html=True)


def render_prediction_card(top_class: str, confidence: float, inference_time: float):
    """Render the main prediction result card."""
    conf_pct = confidence * 100
    conf_color = get_confidence_color(confidence)
    conf_label = get_confidence_label(confidence)
    fish_info = get_fish_info(top_class)
    emoji = fish_info["emoji"] if fish_info else "🐟"

    st.markdown(f"""
    <div class="prediction-card fade-in">
        <p class="prediction-subtitle">Identified Species</p>
        <p class="prediction-label">{emoji} {top_class}</p>
        <p class="prediction-confidence">{conf_pct:.1f}%</p>
        <p style="margin-top:0.5rem;">
            <span class="status-badge status-ready">{conf_label} Confidence</span>
        </p>
        <p style="font-size:0.8rem; color:#64748b !important; margin-top:0.8rem;">
            ⚡ Inference: {inference_time:.0f} ms
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_fish_info_card(species_name: str):
    """Render detailed fish species information."""
    info = get_fish_info(species_name)
    if not info:
        return

    rows_html = ""
    display_fields = [
        ("Scientific Name", "scientific_name"),
        ("Common Names", "common_names"),
        ("Family", "family"),
        ("Origin", "origin"),
        ("Habitat", "habitat"),
        ("Max Size", "max_size"),
        ("Lifespan", "lifespan"),
        ("Diet", "diet"),
        ("Temperature", "temperature"),
        ("pH Range", "ph_range"),
        ("Difficulty", "difficulty"),
    ]

    for label, key in display_fields:
        rows_html += f"""
        <div class="info-row">
            <span class="info-key">{label}</span>
            <span class="info-value">{info[key]}</span>
        </div>
        """

    st.markdown(f"""
    <div class="fish-info-card fade-in">
        <h4>📖 About {info['emoji']} {species_name}</h4>
        <p style="font-size:0.9rem; color:#94a3b8 !important; margin-bottom:1rem; line-height:1.6;">
            {info['description']}
        </p>
        {rows_html}
    </div>
    """, unsafe_allow_html=True)


def render_metric_badges(total_preds, avg_conf, avg_time):
    """Render metric badges row."""
    cols = st.columns(3)
    metrics = [
        ("🔢", f"{total_preds}", "Total Predictions"),
        ("🎯", f"{avg_conf:.1f}%", "Avg Confidence"),
        ("⚡", f"{avg_time:.0f}ms", "Avg Inference"),
    ]
    for col, (icon, value, label) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-badge">
                <p style="font-size:1.3rem; margin:0;">{icon}</p>
                <p class="metric-value">{value}</p>
                <p class="metric-label">{label}</p>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════

def render_sidebar():
    """Render the sidebar with navigation and info."""
    with st.sidebar:
        st.markdown("## 🐠 AquaVision")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Model status
        if st.session_state.model_loaded:
            st.markdown("""
            <span class="status-badge status-ready">● Model Loaded</span>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <span class="status-badge status-processing">● Model Not Loaded</span>
            """, unsafe_allow_html=True)

        st.markdown("")

        # Navigation
        page = st.radio(
            "Navigate",
            ["🔍 Classify", "📊 Batch Process", "📋 History", "ℹ️ Model Info", "🐟 Fish Encyclopedia"],
            label_visibility="collapsed",
        )

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Quick stats
        if st.session_state.history:
            st.markdown("### 📈 Session Stats")
            st.markdown(f"**Predictions:** {len(st.session_state.history)}")
            avg = np.mean([h['confidence'] for h in st.session_state.history]) * 100
            st.markdown(f"**Avg Confidence:** {avg:.1f}%")

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # About
        st.markdown("### About")
        st.markdown(
            "AquaVision uses **MobileNetV2** deep learning to classify "
            "**6 species** of aquarium fish with high accuracy."
        )
        st.markdown("")
        st.markdown(
            "<p style='font-size:0.7rem; color:#475569 !important;'>"
            "Built with Streamlit • TensorFlow • Plotly</p>",
            unsafe_allow_html=True,
        )

    return page


# ═══════════════════════════════════════════════════════
# PAGE: CLASSIFY
# ═══════════════════════════════════════════════════════

def page_classify():
    """Single image classification page."""
    render_hero()

    # Upload section
    st.markdown("""
    <div class="glass-card">
        <h3>📤 Upload a Fish Image</h3>
        <p style="font-size:0.9rem;">Drag and drop or browse to upload an image of a fish. Supported: JPG, JPEG, PNG, WEBP</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload a fish image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        key="single_upload",
    )

    # Determine image source
    image_source = uploaded_file

    if image_source is not None:
        image = Image.open(image_source)

        # Load model
        model_ok = ensure_model_loaded()

        if not model_ok:
            st.error(
                "⚠️ **Model not found!** Please ensure `best_fish_model.keras` is in the "
                "app directory or your Downloads folder."
            )
            model_path = get_model_path()
            st.code(f"Expected path: {model_path}", language="text")
            return

        # Run prediction
        with st.spinner("🧠 Analyzing image..."):
            result = predict(st.session_state.model, image)

        # Add to history
        st.session_state.total_predictions += 1
        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "species": result["top_class"],
            "confidence": result["top_confidence"],
            "inference_ms": result["inference_time_ms"],
        })

        # ─── RESULTS LAYOUT ───
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        col_img, col_result = st.columns([1, 1], gap="large")

        with col_img:
            st.markdown("""
            <div class="glass-card">
                <h3>🖼️ Uploaded Image</h3>
            </div>
            """, unsafe_allow_html=True)
            st.image(image, width="stretch")

        with col_result:
            render_prediction_card(
                result["top_class"],
                result["top_confidence"],
                result["inference_time_ms"],
            )

            # Top 3 runner-ups
            st.markdown("")
            preds_sorted = list(result["all_predictions"].items())
            if len(preds_sorted) > 1:
                st.markdown("""
                <div class="glass-card" style="padding:1rem;">
                    <h3 style="font-size:0.95rem !important;">🏆 Runner-ups</h3>
                </div>
                """, unsafe_allow_html=True)
                for species, conf in preds_sorted[1:4]:
                    pct = conf * 100
                    color = get_confidence_color(conf)
                    st.markdown(
                        f"<p style='margin:0.2rem 0; font-size:0.9rem;'>"
                        f"<span style='color:{color} !important; font-weight:600;'>{pct:.1f}%</span>"
                        f" — {species}</p>",
                        unsafe_allow_html=True,
                    )

        # Charts section
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        tab_bar, tab_radar = st.tabs(["📊 Confidence Breakdown", "🕸️ Radar View"])

        with tab_bar:
            st.plotly_chart(
                create_confidence_chart(result["all_predictions"]),
                width="stretch",
                config={"displayModeBar": False},
            )

        with tab_radar:
            st.plotly_chart(
                create_radar_chart(result["all_predictions"]),
                width="stretch",
                config={"displayModeBar": False},
            )

        # Fish info section
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        render_fish_info_card(result["top_class"])


# ═══════════════════════════════════════════════════════
# PAGE: BATCH PROCESS
# ═══════════════════════════════════════════════════════

def page_batch():
    """Batch image classification page."""
    render_hero()

    st.markdown("""
    <div class="glass-card">
        <h3>📦 Batch Image Processing</h3>
        <p style="font-size:0.9rem;">Upload multiple fish images at once for bulk classification.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload multiple images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="batch_upload",
    )

    if uploaded_files:
        model_ok = ensure_model_loaded()
        if not model_ok:
            st.error("⚠️ Model not found! Check the Classify page for details.")
            return

        st.markdown(f"**{len(uploaded_files)} images uploaded** — Processing...")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        progress_bar = st.progress(0)
        batch_results = []

        for idx, file in enumerate(uploaded_files):
            image = Image.open(file)
            result = predict(st.session_state.model, image)
            batch_results.append({
                "filename": file.name,
                "image": image,
                "result": result,
            })
            progress_bar.progress((idx + 1) / len(uploaded_files))

            # Add to history
            st.session_state.total_predictions += 1
            st.session_state.history.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "species": result["top_class"],
                "confidence": result["top_confidence"],
                "inference_ms": result["inference_time_ms"],
            })

        progress_bar.empty()

        # Display results in grid
        cols_per_row = 3
        for i in range(0, len(batch_results), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(batch_results):
                    item = batch_results[i + j]
                    res = item["result"]
                    conf_pct = res["top_confidence"] * 100
                    color = get_confidence_color(res["top_confidence"])
                    fish = get_fish_info(res["top_class"])
                    emoji = fish["emoji"] if fish else "🐟"

                    with col:
                        st.image(item["image"], width="stretch")
                        st.markdown(
                            f"<div class='glass-card' style='padding:0.8rem; text-align:center;'>"
                            f"<p style='font-weight:700; color:#f1f5f9 !important; font-size:1rem; margin:0;'>"
                            f"{emoji} {res['top_class']}</p>"
                            f"<p style='color:{color} !important; font-weight:600; font-size:1.2rem; margin:0.3rem 0;'>"
                            f"{conf_pct:.1f}%</p>"
                            f"<p style='font-size:0.75rem; color:#64748b !important; margin:0;'>"
                            f"{item['filename']}</p>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

        # Summary
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        avg_conf = np.mean([r["result"]["top_confidence"] for r in batch_results]) * 100
        avg_time = np.mean([r["result"]["inference_time_ms"] for r in batch_results])
        render_metric_badges(len(batch_results), avg_conf, avg_time)


# ═══════════════════════════════════════════════════════
# PAGE: HISTORY
# ═══════════════════════════════════════════════════════

def page_history():
    """Classification history page."""
    render_hero()

    st.markdown("""
    <div class="glass-card">
        <h3>📋 Classification History</h3>
        <p style="font-size:0.9rem;">All predictions made during this session.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:3rem;">
            <p style="font-size:2rem; margin-bottom:0.5rem;">🔍</p>
            <p style="color:#64748b !important; font-size:1rem;">No predictions yet. Go to <strong>Classify</strong> to get started!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Summary metrics
    avg_conf = np.mean([h["confidence"] for h in st.session_state.history]) * 100
    avg_time = np.mean([h["inference_ms"] for h in st.session_state.history])
    render_metric_badges(len(st.session_state.history), avg_conf, avg_time)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Species distribution chart
    species_counts = {}
    for h in st.session_state.history:
        sp = h["species"]
        species_counts[sp] = species_counts.get(sp, 0) + 1

    if species_counts:
        fig = go.Figure()
        sp_names = list(species_counts.keys())
        sp_vals = list(species_counts.values())
        sp_colors = [FISH_DATABASE.get(s, {}).get("color", "#64748b") for s in sp_names]

        fig.add_trace(go.Pie(
            labels=sp_names,
            values=sp_vals,
            hole=0.55,
            marker=dict(colors=sp_colors, line=dict(color="#0a0e1a", width=2)),
            textinfo="label+percent",
            textfont=dict(color="white", size=12, family="Inter"),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
        ))

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", family="Inter"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            showlegend=False,
            annotations=[dict(
                text="Species<br>Distribution",
                x=0.5, y=0.5,
                font=dict(size=14, color="#94a3b8", family="Outfit"),
                showarrow=False,
            )],
        )

        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # History table
    for i, h in enumerate(reversed(st.session_state.history)):
        conf_pct = h["confidence"] * 100
        color = get_confidence_color(h["confidence"])
        fish = get_fish_info(h["species"])
        emoji = fish["emoji"] if fish else "🐟"

        st.markdown(
            f"<div class='history-item'>"
            f"<span style='color:#475569 !important; font-size:0.8rem; min-width:50px;'>#{len(st.session_state.history) - i}</span>"
            f"<span style='font-size:1.2rem;'>{emoji}</span>"
            f"<span style='color:#f1f5f9 !important; font-weight:600; flex:1;'>{h['species']}</span>"
            f"<span style='color:{color} !important; font-weight:700; font-size:1.05rem;'>{conf_pct:.1f}%</span>"
            f"<span style='color:#475569 !important; font-size:0.75rem; min-width:60px; text-align:right;'>"
            f"⚡{h['inference_ms']:.0f}ms</span>"
            f"<span style='color:#475569 !important; font-size:0.75rem; min-width:70px; text-align:right;'>"
            f"🕐 {h['timestamp']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Clear button
    st.markdown("")
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.total_predictions = 0
        st.rerun()


# ═══════════════════════════════════════════════════════
# PAGE: MODEL INFO
# ═══════════════════════════════════════════════════════

def page_model_info():
    """Model information dashboard."""
    render_hero()

    st.markdown("""
    <div class="glass-card">
        <h3>🧠 Model Architecture & Training Details</h3>
        <p style="font-size:0.9rem;">Technical specifications of the fish classification model.</p>
    </div>
    """, unsafe_allow_html=True)

    # Model specs in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>🏗️ Architecture</h3>
        </div>
        """, unsafe_allow_html=True)

        arch_items = [
            ("Base Model", MODEL_INFO["architecture"]),
            ("Input Size", MODEL_INFO["input_size"]),
            ("Classes", str(MODEL_INFO["num_classes"])),
            ("Framework", MODEL_INFO["framework"]),
            ("Model File", MODEL_INFO["model_file"]),
        ]
        for label, value in arch_items:
            st.markdown(
                f"<div class='info-row'>"
                f"<span class='info-key'>{label}</span>"
                f"<span class='info-value'>{value}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>⚙️ Training Configuration</h3>
        </div>
        """, unsafe_allow_html=True)

        train_items = [
            ("Optimizer", MODEL_INFO["optimizer"]),
            ("Loss Function", MODEL_INFO["loss_function"]),
            ("Preprocessing", MODEL_INFO["preprocessing"]),
            ("Augmentation", MODEL_INFO["augmentation"]),
            ("Callbacks", MODEL_INFO["callbacks"]),
        ]
        for label, value in train_items:
            st.markdown(
                f"<div class='info-row'>"
                f"<span class='info-key'>{label}</span>"
                f"<span class='info-value'>{value}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Dataset info
    st.markdown("""
    <div class="glass-card">
        <h3>📂 Dataset Information</h3>
        <p style="font-size:0.9rem; line-height:1.7;">
            The model was trained on the <strong>Aquarium Fish Classification</strong> dataset from Kaggle,
            containing images of 8 species of freshwater/aquarium fish. Transfer learning was applied using
            a MobileNetV2 backbone pretrained on ImageNet, with custom classification layers fine-tuned
            on the fish dataset.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Classes grid
    st.markdown("""
    <div class="glass-card">
        <h3>🏷️ Classification Labels</h3>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, species in enumerate(CLASS_NAMES):
        info = get_fish_info(species)
        emoji = info["emoji"] if info else "🐟"
        color = info["color"] if info else "#64748b"
        with cols[i % 4]:
            st.markdown(
                f"<div class='metric-badge' style='margin-bottom:0.8rem; border-left: 3px solid {color};'>"
                f"<p style='font-size:1.5rem; margin:0;'>{emoji}</p>"
                f"<p style='color:#f1f5f9 !important; font-weight:600; font-size:0.95rem; margin:0.3rem 0 0 0;'>{species}</p>"
                f"<p style='font-size:0.7rem; color:#64748b !important; margin:0;'>{info['scientific_name'] if info else ''}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # MobileNetV2 architecture visualization
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h3>🔬 Pipeline Overview</h3>
    </div>
    """, unsafe_allow_html=True)

    pipeline_fig = go.Figure()

    steps = ["Input Image\n(224×224×3)", "Rescale\n(1/255)", "MobileNetV2\nBackbone", "Global Avg\nPooling", "Dense\nLayers", "Softmax\n(8 classes)"]
    x_pos = list(range(len(steps)))

    # Nodes
    pipeline_fig.add_trace(go.Scatter(
        x=x_pos, y=[0]*len(steps),
        mode="markers+text",
        marker=dict(size=50, color=["#3b82f6", "#06b6d4", "#8b5cf6", "#f59e0b", "#ef4444", "#10b981"],
                    line=dict(width=2, color="rgba(255,255,255,0.1)")),
        text=steps,
        textposition="bottom center",
        textfont=dict(size=10, color="#94a3b8", family="Inter"),
        hoverinfo="skip",
    ))

    # Arrows
    for i in range(len(steps) - 1):
        pipeline_fig.add_annotation(
            x=x_pos[i+1] - 0.15, y=0,
            ax=x_pos[i] + 0.15, ay=0,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=3, arrowsize=1.5, arrowwidth=2,
            arrowcolor="rgba(6,182,212,0.5)",
        )

    pipeline_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, range=[-0.5, len(steps) - 0.5]),
        yaxis=dict(visible=False, range=[-1.2, 0.8]),
        margin=dict(l=20, r=20, t=10, b=60),
        height=180,
        showlegend=False,
    )

    st.plotly_chart(pipeline_fig, width="stretch", config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════
# PAGE: FISH ENCYCLOPEDIA
# ═══════════════════════════════════════════════════════

def page_encyclopedia():
    """Fish species encyclopedia page."""
    render_hero()

    st.markdown("""
    <div class="glass-card">
        <h3>🐟 Fish Encyclopedia</h3>
        <p style="font-size:0.9rem;">Learn about all 6 fish species the model can identify.</p>
    </div>
    """, unsafe_allow_html=True)

    # Species selector
    selected = st.selectbox(
        "Select a species to learn more",
        CLASS_NAMES,
        format_func=lambda x: f"{FISH_DATABASE[x]['emoji']} {x} — {FISH_DATABASE[x]['scientific_name']}",
    )

    if selected:
        render_fish_info_card(selected)

    # All species overview
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h3>📋 All Species at a Glance</h3>
    </div>
    """, unsafe_allow_html=True)

    for species in CLASS_NAMES:
        info = get_fish_info(species)
        if info:
            with st.expander(f"{info['emoji']}  {species}  —  {info['scientific_name']}"):
                st.markdown(f"**{info['description']}**")
                st.markdown("")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"🌍 **Origin:** {info['origin']}")
                    st.markdown(f"📏 **Max Size:** {info['max_size']}")
                    st.markdown(f"⏳ **Lifespan:** {info['lifespan']}")
                    st.markdown(f"🌡️ **Temperature:** {info['temperature']}")
                with col_b:
                    st.markdown(f"🏠 **Habitat:** {info['habitat']}")
                    st.markdown(f"🍽️ **Diet:** {info['diet']}")
                    st.markdown(f"💧 **pH Range:** {info['ph_range']}")
                    st.markdown(f"⭐ **Difficulty:** {info['difficulty']}")


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

def main():
    page = render_sidebar()

    if page == "🔍 Classify":
        page_classify()
    elif page == "📊 Batch Process":
        page_batch()
    elif page == "📋 History":
        page_history()
    elif page == "ℹ️ Model Info":
        page_model_info()
    elif page == "🐟 Fish Encyclopedia":
        page_encyclopedia()


if __name__ == "__main__":
    main()
