import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ===============================================================
# Plant Disease Classifier - Professional Enhanced Version
# ===============================================================

st.set_page_config(
    page_title="Plant Disease Classifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# Enhanced CSS Styling - Netflix Professional Theme
# =======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        padding: 2rem;
        min-height: 100vh;
    }
    
    /* Animated Background */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hero Section with Animation */
    .hero-section {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        background-size: 200% 200%;
        animation: gradient 8s ease infinite;
        padding: 4rem 2rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.4);
        position: relative;
        overflow: hidden;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .hero-section:hover {
        transform: scale(1.01);
        box-shadow: 0 25px 70px rgba(139, 92, 246, 0.5);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
        position: relative;
        z-index: 1;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.95;
        color: white;
        position: relative;
        z-index: 1;
    }
    
    /* Glassmorphism Cards - Netflix Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        opacity: 0;
        transform: translateY(30px);
        animation: netflixFadeIn 0.8s ease forwards;
    }
    
    @keyframes netflixFadeIn {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.7s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.4);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .glass-card h3 {
        color: #e0e7ff;
        margin-bottom: 1rem;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .glass-card p, .glass-card li {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Stats Card with Gradient */
    .stat-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .stat-card::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        transform: translate(-50%, -50%);
        transition: width 0.8s, height 0.8s;
    }
    
    .stat-card:hover::after {
        width: 400px;
        height: 400px;
    }
    
    .stat-card:hover {
        transform: translateY(-12px) scale(1.05);
        box-shadow: 0 25px 70px rgba(139, 92, 246, 0.5);
        border-color: rgba(139, 92, 246, 0.7);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0;
        position: relative;
        z-index: 1;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #cbd5e1;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Primary Prediction Card */
    .primary-prediction {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        background-size: 200% 200%;
        animation: gradient 6s ease infinite;
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(16, 185, 129, 0.4);
        position: relative;
        overflow: hidden;
        opacity: 0;
        transform: scale(0.9);
        animation: netflixScaleIn 0.6s ease forwards;
    }
    
    @keyframes netflixScaleIn {
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .primary-prediction::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .prediction-title {
        font-size: 0.95rem;
        font-weight: 600;
        opacity: 0.9;
        margin-bottom: 0.5rem;
        color: white;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    .prediction-result {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 1rem 0;
        color: white;
        position: relative;
        z-index: 1;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .confidence-badge {
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(10px);
        padding: 0.7rem 2rem;
        border-radius: 30px;
        display: inline-block;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1rem;
        color: white;
        position: relative;
        z-index: 1;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Analysis Metric Card */
    .metric-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateX(8px);
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e0e7ff;
    }
    
    /* Premium Buttons - Netflix Style */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.8s, height 0.8s;
    }
    
    .stButton>button:hover::before {
        width: 500px;
        height: 500px;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 20px 50px rgba(99, 102, 241, 0.6);
    }
    
    /* Sidebar with Dark Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0;
    }
    
    /* Sidebar Accuracy Badge */
    .sidebar-accuracy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sidebar-accuracy:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.6);
    }
    
    .sidebar-accuracy-label {
        font-size: 0.85rem;
        font-weight: 600;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-accuracy-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }
    
    /* Radio buttons styling */
    .stRadio > label {
        color: #e2e8f0 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .stRadio > div {
        background: rgba(139, 92, 246, 0.1);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .stRadio > div > label:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateX(8px);
    }
    
    /* Section Headers with Glow */
    .section-header {
        color: #e0e7ff;
        font-size: 2rem;
        font-weight: 700;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(139, 92, 246, 0.4);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, #8b5cf6, transparent);
        animation: slideRight 2s ease infinite;
    }
    
    @keyframes slideRight {
        0%, 100% { transform: translateX(0); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateX(200px); opacity: 0; }
    }
    
    /* Upload Section */
    .upload-info {
        background: rgba(99, 102, 241, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed rgba(139, 92, 246, 0.4);
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .upload-info:hover {
        border-color: rgba(139, 92, 246, 0.8);
        background: rgba(99, 102, 241, 0.15);
        transform: scale(1.02);
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: rgba(139, 92, 246, 0.1);
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(139, 92, 246, 0.8);
        background: rgba(139, 92, 246, 0.15);
    }
    
    /* Image Container */
    [data-testid="stImage"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stImage"]:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.3);
    }
    
    /* Result Item */
    .result-item {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
        transform: translateX(-20px);
        animation: slideInLeft 0.5s ease forwards;
    }
    
    @keyframes slideInLeft {
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .result-item:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 5px;
    }
    
    /* Animation Delays */
    .glass-card:nth-child(1) { animation-delay: 0.1s; }
    .glass-card:nth-child(2) { animation-delay: 0.2s; }
    .glass-card:nth-child(3) { animation-delay: 0.3s; }
    .glass-card:nth-child(4) { animation-delay: 0.4s; }
    .result-item:nth-child(1) { animation-delay: 0.1s; }
    .result-item:nth-child(2) { animation-delay: 0.2s; }
    .result-item:nth-child(3) { animation-delay: 0.3s; }
    .result-item:nth-child(4) { animation-delay: 0.4s; }
    .result-item:nth-child(5) { animation-delay: 0.5s; }
    </style>
""", unsafe_allow_html=True)

# =======================
# Helper Functions
# =======================
def format_disease_name(class_name):
    """Convert class names like 'Apple___Apple_scab' to 'Apple - Apple Scab'"""
    parts = class_name.split('___')
    plant = parts[0].replace('_', ' ').strip()
    disease = parts[1].replace('_', ' ').strip() if len(parts) > 1 else 'Unknown'
    
    plant = ' '.join(word.capitalize() for word in plant.split())
    disease = ' '.join(word.capitalize() for word in disease.split())
    
    return f"{plant} - {disease}"

def get_plant_name(class_name):
    """Extract plant name from class"""
    return class_name.split('___')[0].replace('_', ' ').title()

def get_disease_name(class_name):
    """Extract disease name from class"""
    parts = class_name.split('___')
    return parts[1].replace('_', ' ').title() if len(parts) > 1 else 'Unknown'

def is_healthy(class_name):
    """Check if prediction indicates healthy plant"""
    return 'healthy' in class_name.lower()

# =======================
# Load Model and Data
# =======================
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("plant_model.keras")
    return model

@st.cache_resource
def load_class_names():
    with open("class_names.json", "r") as f:
        return json.load(f)

@st.cache_resource
def load_model_info():
    info = {}
    try:
        with open("model_metrics.json", "r") as f:
            info["metrics"] = json.load(f)
    except:
        info["metrics"] = None
    return info

model = load_model()
class_names = load_class_names()
model_info = load_model_info()

# =======================
# Navigation Sidebar
# =======================
with st.sidebar:
    if model_info["metrics"]:
        accuracy = model_info["metrics"]["accuracy"] * 100
        st.markdown(f"""
        <div class='sidebar-accuracy'>
            <div class='sidebar-accuracy-label'>Model Accuracy</div>
            <div class='sidebar-accuracy-value'>{accuracy:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## Navigation")
    
    page = st.radio(
        "",
        ["Home", "Disease Detection", "About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0.5rem;'>Need Help?</p>
        <p style='color: #94a3b8; font-size: 0.85rem;'>Check the About page for detailed information</p>
    </div>
    """, unsafe_allow_html=True)

# =======================
# HOME PAGE
# =======================
if page == "Home":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>Plant Disease AI</div>
        <div class='hero-subtitle'>Next-generation plant health detection powered by deep learning</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>System Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        accuracy = model_info["metrics"]["accuracy"] * 100 if model_info["metrics"] else 0
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{accuracy:.1f}%</div>
            <div class='stat-label'>Detection Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{len(class_names)}</div>
            <div class='stat-label'>Disease Classes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        plants_count = len(set(name.split('___')[0] for name in class_names))
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{plants_count}</div>
            <div class='stat-label'>Plant Species</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Core Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>Lightning Fast</h3>
            <p>Get instant disease detection results in under a second with state-of-the-art deep learning technology.</p>
        </div>
        <div class='glass-card'>
            <h3>High Accuracy</h3>
            <p>Trained on thousands of images to deliver 94%+ accuracy across multiple plant diseases and conditions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h3>Multi-Species</h3>
            <p>Supports 14+ plant species including tomato, apple, grape, corn, potato, pepper, and more.</p>
        </div>
        <div class='glass-card'>
            <h3>Detailed Analysis</h3>
            <p>View comprehensive results with confidence scores, top predictions, and actionable insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3 style='font-size: 2rem; margin-bottom: 0.5rem;'>1</h3>
            <h3>Upload</h3>
            <p>Upload a clear leaf image</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3 style='font-size: 2rem; margin-bottom: 0.5rem;'>2</h3>
            <h3>Analyze</h3>
            <p>AI processes the image</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3 style='font-size: 2rem; margin-bottom: 0.5rem;'>3</h3>
            <h3>Detect</h3>
            <p>Get instant diagnosis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3 style='font-size: 2rem; margin-bottom: 0.5rem;'>4</h3>
            <h3>Act</h3>
            <p>Receive recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Supported Plants</h2>", unsafe_allow_html=True)
    
    plants = sorted(set(name.split('___')[0].replace('_', ' ') for name in class_names))
    
    cols = st.columns(4)
    for idx, plant in enumerate(plants):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class='glass-card' style='padding: 1.5rem; text-align: center;'>
                <p style='font-size: 1rem; font-weight: 600; color: #c4b5fd; margin: 0;'>{plant}</p>
            </div>
            """, unsafe_allow_html=True)

# =======================
# DISEASE DETECTION PAGE
# =======================
elif page == "Disease Detection":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>Disease Detection</div>
        <div class='hero-subtitle'>Upload a leaf image for instant AI-powered analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Upload Image</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='upload-info'>
            <p style='text-align: center; font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;'>Tips for Best Results</p>
            <p>Use good lighting conditions</p>
            <p>Focus on a single leaf</p>
            <p>Ensure symptoms are clearly visible</p>
            <p>Avoid blurry or dark images</p>
        </div>
        """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        
        st.markdown("<h2 class='section-header'>Uploaded Image</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, use_container_width=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Dimensions</div>
                <div class='metric-value'>{image.size[0]} × {image.size[1]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Format</div>
                <div class='metric-value'>{image.format}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Color Mode</div>
                <div class='metric-value'>{image.mode}</div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Analyze Image", use_container_width=True):
                with st.spinner("Analyzing leaf patterns..."):
                    # Preprocess
                    img = image.resize((224, 224))
                    img_array = np.array(img) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)

                    # Predict
                    predictions = model.predict(img_array, verbose=0)
                    preds = predictions[0]

                    # Store in session state
                    st.session_state['predictions'] = preds
                    st.session_state['last_analyzed_file'] = uploaded_file.name
                    st.rerun()

        # Display results if analysis was run
        if st.session_state.get('last_analyzed_file') == uploaded_file.name and 'predictions' in st.session_state:
            preds = st.session_state['predictions']
            
            # Get all predictions sorted
            all_indices = np.argsort(preds)[::-1]
            top_indices = all_indices[:5]
            
            # Primary prediction
            primary_idx = top_indices[0]
            primary_class = class_names[primary_idx]
            primary_score = preds[primary_idx] * 100
            primary_formatted = format_disease_name(primary_class)
            
            # Analysis metrics
            max_confidence = np.max(preds) * 100
            avg_top5_confidence = np.mean(preds[top_indices]) * 100
            confidence_spread = (preds[top_indices[0]] - preds[top_indices[4]]) * 100
            
            st.markdown("<h2 class='section-header'>Primary Detection</h2>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='primary-prediction'>
                <div class='prediction-title'>Detected Condition</div>
                <div class='prediction-result'>{primary_formatted}</div>
                <div class='confidence-badge'>Confidence: {primary_score:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed Analysis Section
            st.markdown("<h2 class='section-header'>Comprehensive Analysis</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Plant Species</div>
                    <div class='metric-value' style='font-size: 1.4rem;'>{get_plant_name(primary_class)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                health_status = "Healthy" if is_healthy(primary_class) else "Disease Detected"
                status_color = "#10b981" if is_healthy(primary_class) else "#ef4444"
                st.markdown(f"""
                <div class='metric-card' style='border: 2px solid {status_color};'>
                    <div class='metric-label'>Health Status</div>
                    <div class='metric-value' style='font-size: 1.4rem; color: {status_color};'>{health_status}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Condition</div>
                    <div class='metric-value' style='font-size: 1.4rem;'>{get_disease_name(primary_class)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Model Insights
            st.markdown("<h2 class='section-header'>Model Insights</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Max Confidence</div>
                    <div class='metric-value'>{max_confidence:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Avg Top-5 Confidence</div>
                    <div class='metric-value'>{avg_top5_confidence:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Confidence Spread</div>
                    <div class='metric-value'>{confidence_spread:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Top 5 Predictions Visualization
            st.markdown("<h2 class='section-header'>Top 5 Predictions</h2>", unsafe_allow_html=True)
            
            top_classes = [class_names[i] for i in top_indices]
            top_scores = preds[top_indices] * 100
            formatted_classes = [format_disease_name(cls) for cls in top_classes]
            
            # Horizontal Bar Chart
            fig = go.Figure(go.Bar(
                x=top_scores[::-1],
                y=formatted_classes[::-1],
                orientation='h',
                text=[f"{s:.2f}%" for s in top_scores[::-1]],
                textposition='outside',
                marker=dict(
                    color=top_scores[::-1],
                    colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#a78bfa']],
                    line=dict(color='rgba(139, 92, 246, 0.5)', width=2)
                ),
                hovertemplate='<b>%{y}</b><br>Confidence: %{x:.2f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': "Confidence Distribution",
                    'font': {'size': 20, 'color': '#e0e7ff', 'family': 'Inter'}
                },
                xaxis_title="Confidence (%)",
                yaxis_title="",
                template="plotly_dark",
                plot_bgcolor='rgba(30, 41, 59, 0.5)',
                paper_bgcolor='rgba(30, 41, 59, 0.5)',
                height=400,
                font=dict(color='#cbd5e1', family='Inter'),
                xaxis=dict(gridcolor='rgba(139, 92, 246, 0.2)', range=[0, 100]),
                yaxis=dict(gridcolor='rgba(139, 92, 246, 0.2)'),
                showlegend=False,
                margin=dict(l=20, r=100, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Full Probability Distribution
            st.markdown("<h2 class='section-header'>Complete Probability Distribution</h2>", unsafe_allow_html=True)
            
            # Show top 10 in detail
            top10_indices = all_indices[:10]
            for i, idx in enumerate(top10_indices):
                cls = class_names[idx]
                score = preds[idx] * 100
                formatted = format_disease_name(cls)
                
                if i == 0:
                    border_color = "#10b981"
                elif i < 3:
                    border_color = "#6366f1"
                elif i < 5:
                    border_color = "#8b5cf6"
                else:
                    border_color = "#64748b"
                
                st.markdown(f"""
                <div class='result-item' style='border-left-color: {border_color};'>
                    <p style='margin: 0; color: #e2e8f0;'>
                        <strong style='font-size: 1.1rem;'>{i+1}. {formatted}</strong>
                        <span style='float: right; color: {border_color}; font-weight: 700; font-size: 1.1rem;'>{score:.2f}%</span>
                    </p>
                    <div style='margin-top: 0.5rem; background: rgba(139, 92, 246, 0.1); border-radius: 10px; height: 8px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, {border_color}, rgba(139, 92, 246, 0.5)); height: 100%; width: {score}%; transition: width 1s ease;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Statistical Summary
            st.markdown("<h2 class='section-header'>Statistical Summary</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class='glass-card'>
                    <h3>Prediction Statistics</h3>
                """, unsafe_allow_html=True)
                
                mean_conf = np.mean(preds) * 100
                median_conf = np.median(preds) * 100
                std_conf = np.std(preds) * 100
                
                st.markdown(f"""
                    <p><strong>Mean Confidence:</strong> {mean_conf:.2f}%</p>
                    <p><strong>Median Confidence:</strong> {median_conf:.2f}%</p>
                    <p><strong>Std Deviation:</strong> {std_conf:.2f}%</p>
                    <p><strong>Total Classes:</strong> {len(class_names)}</p>
                    <p><strong>Classes > 1%:</strong> {np.sum(preds > 0.01)}</p>
                    <p><strong>Classes > 5%:</strong> {np.sum(preds > 0.05)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='glass-card'>
                    <h3>Confidence Analysis</h3>
                """, unsafe_allow_html=True)
                
                if max_confidence > 90:
                    interpretation = "The model is very confident in this prediction. The detected condition is highly likely."
                elif max_confidence > 75:
                    interpretation = "The model shows high confidence. The prediction is reliable but consider the top alternatives."
                elif max_confidence > 60:
                    interpretation = "The model has moderate confidence. Review the top predictions carefully."
                else:
                    interpretation = "The model has low confidence. Multiple conditions are possible."
                
                st.markdown(f"""
                    <p>{interpretation}</p>
                    <p style='margin-top: 1rem; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border-left: 3px solid #8b5cf6;'>
                        <strong>Note:</strong> This tool provides preliminary analysis. Always verify results with agricultural professionals.
                    </p>
                </div>
                """, unsafe_allow_html=True)

# =======================
# ABOUT PAGE
# =======================
elif page == "About":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>About the System</div>
        <div class='hero-subtitle'>Technical specifications and capabilities</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>System Architecture</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>Neural Network</h3>
            <p><strong>Architecture:</strong> Deep Convolutional Neural Network</p>
            <p><strong>Input Dimensions:</strong> 224 × 224 × 3 (RGB)</p>
            <p><strong>Output Classes:</strong> 38 disease categories</p>
            <p><strong>Framework:</strong> TensorFlow/Keras</p>
            <p><strong>Optimization:</strong> Adam optimizer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if model_info["metrics"]:
            st.markdown(f"""
            <div class='glass-card'>
                <h3>Performance Metrics</h3>
                <p><strong>Test Accuracy:</strong> {model_info["metrics"]["accuracy"]*100:.2f}%</p>
                <p><strong>Total Classes:</strong> {model_info["metrics"]["num_classes"]}</p>
                <p><strong>Inference Time:</strong> ~0.5 seconds</p>
                <p><strong>Model Type:</strong> {model_info["metrics"]["model_type"]}</p>
                <p><strong>TensorFlow:</strong> v{model_info["metrics"]["tensorflow_version"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Training Dataset</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3>PlantVillage Dataset</h3>
        <p><strong>Source:</strong> PlantVillage dataset via Hugging Face</p>
        <p><strong>Total Images:</strong> 54,000+ high-resolution plant leaf images</p>
        <p><strong>Data Split:</strong> 70% Training, 15% Validation, 15% Testing</p>
        <p><strong>Image Resolution:</strong> 224 × 224 pixels (standardized)</p>
        <p><strong>Classes:</strong> 38 different plant disease categories</p>
        <p><strong>Augmentation:</strong> Rotation, flipping, zooming, and shifting applied</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Applications</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>Agriculture</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Early disease detection in commercial crops</li>
                <li>Real-time crop health monitoring</li>
                <li>Yield optimization and loss prevention</li>
                <li>Integrated pest management support</li>
            </ul>
        </div>
        
        <div class='glass-card'>
            <h3>Research</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Plant pathology research and studies</li>
                <li>Disease spread pattern analysis</li>
                <li>Climate impact on plant diseases</li>
                <li>Agricultural AI model development</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h3>Education</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Plant pathology teaching tool</li>
                <li>Student learning and practice</li>
                <li>Agricultural training programs</li>
                <li>Interactive disease identification</li>
            </ul>
        </div>
        
        <div class='glass-card'>
            <h3>Home Gardening</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Personal garden health monitoring</li>
                <li>Plant care decision support</li>
                <li>Early disease prevention</li>
                <li>Treatment recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Technology Stack</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>Backend</h3>
            <p>Python 3.x</p>
            <p>TensorFlow</p>
            <p>NumPy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>Frontend</h3>
            <p>Streamlit</p>
            <p>Plotly</p>
            <p>Custom CSS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>AI/ML</h3>
            <p>Deep Learning</p>
            <p>CNN Architecture</p>
            <p>Transfer Learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Important Notice</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card' style='border-left: 4px solid #f59e0b;'>
        <h3>Disclaimer</h3>
        <p>This AI-powered plant disease detection system is designed to assist in preliminary diagnosis and should be used as a supportive tool rather than a definitive diagnostic solution.</p>
        
        <p style='margin-top: 1rem;'><strong>Important Considerations:</strong></p>
        <ul style='margin-left: 1rem; line-height: 2;'>
            <li>Always consult with certified agricultural professionals or plant pathologists for accurate diagnosis</li>
            <li>Predictions are based on visual patterns and may not account for all environmental factors</li>
            <li>Treatment decisions should be made in consultation with experts</li>
            <li>The system's accuracy depends on image quality and clarity</li>
            <li>Results may vary based on lighting, angle, and disease progression stage</li>
        </ul>
        
        <p style='margin-top: 1rem; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 8px;'>
            <strong>Recommendation:</strong> Use this tool as part of an integrated approach to plant health management, combining AI insights with professional expertise and field observations.
        </p>
    </div>
    """, unsafe_allow_html=True)
