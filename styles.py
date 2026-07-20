"""
Custom CSS styles for the Fish Classifier Streamlit Application.
Dark ocean theme with glassmorphism, gradients, and micro-animations.
"""


def get_main_styles():
    """Return the main CSS stylesheet for the application."""
    return """
    <style>
    /* ═══════════════════════════════════════════════════════
       IMPORTS & ROOT VARIABLES
       ═══════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #111827;
        --bg-card: rgba(17, 24, 39, 0.7);
        --bg-glass: rgba(255, 255, 255, 0.04);
        --border-glass: rgba(255, 255, 255, 0.08);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-primary: #06b6d4;
        --accent-secondary: #3b82f6;
        --accent-tertiary: #8b5cf6;
        --accent-success: #10b981;
        --accent-warning: #f59e0b;
        --accent-danger: #ef4444;
        --gradient-ocean: linear-gradient(135deg, #06b6d4, #3b82f6, #8b5cf6);
        --gradient-card: linear-gradient(145deg, rgba(6,182,212,0.08), rgba(59,130,246,0.04));
        --shadow-glow: 0 0 30px rgba(6, 182, 212, 0.15);
        --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.3);
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
        --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ═══════════════════════════════════════════════════════
       GLOBAL OVERRIDES
       ═══════════════════════════════════════════════════════ */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp > header {
        background: transparent !important;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 3px;
    }

    /* ═══════════════════════════════════════════════════════
       SIDEBAR
       ═══════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
        border-right: 1px solid var(--border-glass) !important;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
        font-family: 'Outfit', sans-serif !important;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-secondary) !important;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-secondary) !important;
    }

    /* ═══════════════════════════════════════════════════════
       TYPOGRAPHY
       ═══════════════════════════════════════════════════════ */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-primary) !important;
    }

    p, span, li, label, div {
        color: var(--text-secondary) !important;
    }

    /* ═══════════════════════════════════════════════════════
       HERO HEADER
       ═══════════════════════════════════════════════════════ */
    .hero-header {
        background: linear-gradient(135deg, rgba(6,182,212,0.12) 0%, rgba(59,130,246,0.08) 50%, rgba(139,92,246,0.12) 100%);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-lg);
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-ocean);
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }

    .hero-header h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        background: var(--gradient-ocean);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }

    .hero-header p {
        font-size: 1.05rem !important;
        color: var(--text-muted) !important;
        margin: 0 !important;
        font-weight: 300;
    }

    /* ═══════════════════════════════════════════════════════
       GLASS CARD
       ═══════════════════════════════════════════════════════ */
    .glass-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: var(--transition-smooth);
        box-shadow: var(--shadow-card);
    }

    .glass-card:hover {
        border-color: rgba(6, 182, 212, 0.2);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }

    .glass-card h3 {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.8rem !important;
    }

    /* ═══════════════════════════════════════════════════════
       PREDICTION RESULT CARD
       ═══════════════════════════════════════════════════════ */
    .prediction-card {
        background: linear-gradient(145deg, rgba(16,185,129,0.1), rgba(6,182,212,0.06));
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .prediction-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #06b6d4);
    }

    .prediction-label {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #10b981 !important;
        margin: 0.5rem 0 !important;
        letter-spacing: -0.3px;
    }

    .prediction-confidence {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #06b6d4, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 !important;
    }

    .prediction-subtitle {
        font-size: 0.85rem !important;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem !important;
    }

    /* ═══════════════════════════════════════════════════════
       METRIC BADGES
       ═══════════════════════════════════════════════════════ */
    .metric-badge {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        text-align: center;
        transition: var(--transition-smooth);
    }

    .metric-badge:hover {
        border-color: rgba(6,182,212,0.3);
        background: rgba(6,182,212,0.06);
    }

    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: var(--accent-primary) !important;
        margin: 0 !important;
    }

    .metric-label {
        font-size: 0.75rem !important;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.3rem !important;
    }

    /* ═══════════════════════════════════════════════════════
       FISH INFO CARD
       ═══════════════════════════════════════════════════════ */
    .fish-info-card {
        background: linear-gradient(145deg, rgba(59,130,246,0.08), rgba(139,92,246,0.04));
        border: 1px solid rgba(59,130,246,0.15);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .fish-info-card h4 {
        font-family: 'Outfit', sans-serif;
        color: var(--accent-secondary) !important;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }

    .info-key {
        color: var(--text-muted) !important;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .info-value {
        color: var(--text-primary) !important;
        font-size: 0.85rem;
        font-weight: 400;
    }

    /* ═══════════════════════════════════════════════════════
       HISTORY ITEMS
       ═══════════════════════════════════════════════════════ */
    .history-item {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: var(--transition-smooth);
    }

    .history-item:hover {
        border-color: rgba(6,182,212,0.2);
    }

    /* ═══════════════════════════════════════════════════════
       FILE UPLOADER OVERRIDE
       ═══════════════════════════════════════════════════════ */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(6,182,212,0.3) !important;
        border-radius: var(--radius-lg) !important;
        background: rgba(6,182,212,0.03) !important;
        padding: 1rem !important;
        transition: var(--transition-smooth);
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(6,182,212,0.5) !important;
        background: rgba(6,182,212,0.06) !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 1rem !important;
    }

    /* ═══════════════════════════════════════════════════════
       BUTTON OVERRIDES
       ═══════════════════════════════════════════════════════ */
    .stButton > button {
        background: var(--gradient-ocean) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.3px;
        transition: var(--transition-smooth) !important;
        box-shadow: 0 4px 15px rgba(6,182,212,0.25) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(6,182,212,0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ═══════════════════════════════════════════════════════
       TAB OVERRIDES
       ═══════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255,255,255,0.03);
        border-radius: var(--radius-md);
        padding: 4px;
        border: 1px solid var(--border-glass);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        color: var(--text-muted) !important;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: var(--transition-smooth);
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background: rgba(6,182,212,0.08);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(6,182,212,0.15) !important;
        color: var(--accent-primary) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--accent-primary) !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }

    /* ═══════════════════════════════════════════════════════
       EXPANDER OVERRIDES
       ═══════════════════════════════════════════════════════ */
    .streamlit-expanderHeader {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    /* ═══════════════════════════════════════════════════════
       SPINNER / LOADING
       ═══════════════════════════════════════════════════════ */
    .loading-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeInUp 0.5s ease-out forwards;
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .shimmer {
        background: linear-gradient(90deg, transparent, rgba(6,182,212,0.08), transparent);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }

    /* ═══════════════════════════════════════════════════════
       DIVIDER
       ═══════════════════════════════════════════════════════ */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-glass), transparent);
        margin: 1.5rem 0;
    }

    /* ═══════════════════════════════════════════════════════
       IMAGE CONTAINER
       ═══════════════════════════════════════════════════════ */
    .image-container {
        border-radius: var(--radius-lg);
        overflow: hidden;
        border: 1px solid var(--border-glass);
        box-shadow: var(--shadow-card);
    }

    .image-container img {
        border-radius: var(--radius-lg);
    }

    /* ═══════════════════════════════════════════════════════
       STATUS BADGE
       ═══════════════════════════════════════════════════════ */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .status-ready {
        background: rgba(16,185,129,0.15);
        color: #10b981;
        border: 1px solid rgba(16,185,129,0.3);
    }

    .status-processing {
        background: rgba(245,158,11,0.15);
        color: #f59e0b;
        border: 1px solid rgba(245,158,11,0.3);
    }

    /* Hide default streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* ═══════════════════════════════════════════════════════
       PLOTLY CHART CONTAINER
       ═══════════════════════════════════════════════════════ */
    .stPlotlyChart {
        border-radius: var(--radius-md);
        overflow: hidden;
    }
    </style>
    """
