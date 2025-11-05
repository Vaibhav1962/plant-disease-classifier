import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ===============================================================
# Plant Disease Classifier - Premium Version
# ===============================================================

st.set_page_config(
    page_title="Plant Disease Classifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# Premium CSS Styling with Animations
# =======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #0f172a;
        padding: 2rem;
        min-height: 100vh;
    }
    
    /* Dark theme for all Streamlit elements */
    .stApp {
        background: #0f172a !important;
    }
    
    /* Override white backgrounds */
    [data-testid="stAppViewContainer"] {
        background: #0f172a !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Force dark theme regardless of browser settings */
    body {
        background: #0f172a !important;
        color: #e2e8f0 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
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
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 48px rgba(139, 92, 246, 0.3);
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
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
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
        transition: width 0.6s, height 0.6s;
    }
    
    .stat-card:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .stat-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.4);
        border-color: rgba(139, 92, 246, 0.6);
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
    
    /* Prediction Card with Animation */
    .prediction-card {
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
        transform: scale(0.95);
        animation: scaleIn 0.5s ease forwards;
    }
    
    @keyframes scaleIn {
        to {
            transform: scale(1);
        }
    }
    
    .prediction-card::before {
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
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 400px;
        height: 400px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.5);
    }
    
    /* Sidebar with Dark Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0;
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
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .stRadio > div > label:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateX(5px);
    }
    
    .stRadio > div > label > div {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    .sidebar-info {
        background: rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .sidebar-info h3 {
        color: #c4b5fd;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-info p {
        color: #cbd5e1;
        margin: 0.7rem 0;
        font-size: 0.95rem;
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
    
    /* Upload Section with Hover Effect */
    .upload-info {
        background: rgba(99, 102, 241, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed rgba(139, 92, 246, 0.4);
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-info:hover {
        border-color: rgba(139, 92, 246, 0.8);
        background: rgba(99, 102, 241, 0.15);
        transform: scale(1.02);
    }
    
    .upload-info p {
        color: #cbd5e1;
        margin: 0.5rem 0;
        font-size: 1rem;
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: rgba(139, 92, 246, 0.1);
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(139, 92, 246, 0.8);
        background: rgba(139, 92, 246, 0.15);
    }
    
    [data-testid="stFileUploader"] label {
        color: #e2e8f0 !important;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 10px !important;
        color: #6ee7b7 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
    
    /* Image Container */
    [data-testid="stImage"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stImage"]:hover {
        transform: scale(1.02);
    }
    
    /* Plotly Chart Styling */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Scrollbar Styling */
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
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    }
    
    /* Fade In Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .glass-card, .stat-card {
        animation: fadeIn 0.6s ease forwards;
    }
    
    .glass-card:nth-child(1) { animation-delay: 0.1s; }
    .glass-card:nth-child(2) { animation-delay: 0.2s; }
    .glass-card:nth-child(3) { animation-delay: 0.3s; }
    .glass-card:nth-child(4) { animation-delay: 0.4s; }
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
    
    # Capitalize each word properly
    plant = ' '.join(word.capitalize() for word in plant.split())
    disease = ' '.join(word.capitalize() for word in disease.split())
    
    return f"{plant} - {disease}"

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
    st.markdown("## 🌿 Navigation")
    
    page = st.radio(
        "",
        ["Home", "Disease Detection", "About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if model_info["metrics"]:
        st.markdown("""
        <div class='sidebar-info'>
            <h3>⚡ Quick Stats</h3>
            <p><strong>Accuracy:</strong> {:.1f}%</p>
            <p><strong>Classes:</strong> {}</p>
            <p><strong>Speed:</strong> ~0.5s</p>
        </div>
        """.format(
            model_info["metrics"]["accuracy"] * 100,
            len(class_names)
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class='sidebar-info'>
        <h3>💡 Need Help?</h3>
        <p>Check the About page for detailed information</p>
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
    
    # System Capabilities
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
    
    # Features
    st.markdown("<h2 class='section-header'>Core Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>⚡ Lightning Fast</h3>
            <p>Get instant disease detection results in under a second with state-of-the-art deep learning technology.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
            <h3>🎯 High Accuracy</h3>
            <p>Trained on thousands of images to deliver 94%+ accuracy across multiple plant diseases and conditions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h3>🌍 Multi-Species</h3>
            <p>Supports 14+ plant species including tomato, apple, grape, corn, potato, pepper, and more.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
            <h3>📊 Detailed Analysis</h3>
            <p>View comprehensive results with confidence scores, top predictions, and actionable insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown("<h2 class='section-header'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>1️⃣</h3>
            <h3>Upload</h3>
            <p>Upload a clear leaf image</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>2️⃣</h3>
            <h3>Analyze</h3>
            <p>AI processes the image</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>3️⃣</h3>
            <h3>Detect</h3>
            <p>Get instant diagnosis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>4️⃣</h3>
            <h3>Act</h3>
            <p>Receive recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Supported Plants
    st.markdown("<h2 class='section-header'>Supported Plants</h2>", unsafe_allow_html=True)
    
    plants = sorted(set(name.split('___')[0].replace('_', ' ') for name in class_names))
    
    cols = st.columns(4)
    for idx, plant in enumerate(plants):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class='glass-card' style='padding: 1.5rem; text-align: center;'>
                <p style='font-size: 1rem; font-weight: 600; color: #c4b5fd; margin: 0;'>
                    🌿 {plant}
                </p>
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
            <p style='text-align: center; font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;'>📸 Tips for Best Results</p>
            <p>✓ Use good lighting conditions</p>
            <p>✓ Focus on a single leaf</p>
            <p>✓ Ensure symptoms are clearly visible</p>
            <p>✓ Avoid blurry or dark images</p>
        </div>
        """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<h3 style='color: #e0e7ff; margin-bottom: 1rem;'>🖼️ Uploaded Image</h3>", unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            
            st.markdown(f"""
            <div class='glass-card'>
                <h3>Image Details</h3>
                <p><strong>Dimensions:</strong> {image.size[0]} × {image.size[1]} pixels</p>
                <p><strong>Format:</strong> {image.format}</p>
                <p><strong>Mode:</strong> {image.mode}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h3 style='color: #e0e7ff; margin-bottom: 1rem;'>🔬 Analysis</h3>", unsafe_allow_html=True)
            
            if st.button("🚀 Analyze Image", use_container_width=True):
                with st.spinner("🧬 Analyzing leaf patterns..."):
                    # Preprocess
                    img = image.resize((224, 224))
                    img_array = np.array(img) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)

                    # Predict
                    predictions = model.predict(img_array, verbose=0)
                    preds = predictions[0]

                    # Get Top 5 predictions
                    top_indices = np.argsort(preds)[::-1][:5]
                    top_classes = [class_names[i] for i in top_indices]
                    top_scores = preds[top_indices] * 100
                    
                    # Format disease names
                    formatted_classes = [format_disease_name(cls) for cls in top_classes]

                    # Display main result
                    st.markdown("""
                    <div class='prediction-card'>
                        <div class='prediction-title'>Detected Condition</div>
                        <div class='prediction-result'>{}</div>
                        <div class='confidence-badge'>Confidence: {:.1f}%</div>
                    </div>
                    """.format(formatted_classes[0], top_scores[0]), unsafe_allow_html=True)

                    # Plot Top-5 Bar Chart
                    fig = go.Figure(go.Bar(
                        x=top_scores[::-1],
                        y=formatted_classes[::-1],
                        orientation='h',
                        text=[f"{s:.1f}%" for s in top_scores[::-1]],
                        textposition='outside',
                        marker=dict(
                            color=top_scores[::-1],
                            colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#a78bfa']],
                            line=dict(color='rgba(139, 92, 246, 0.5)', width=2)
                        ),
                        hovertemplate='<b>%{y}</b><br>Confidence: %{x:.1f}%<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title={
                            'text': "Top 5 Predictions",
                            'font': {'size': 20, 'color': '#e0e7ff', 'family': 'Inter'}
                        },
                        xaxis_title="Confidence (%)",
                        yaxis_title="",
                        template="plotly_dark",
                        plot_bgcolor='rgba(30, 41, 59, 0.5)',
                        paper_bgcolor='rgba(30, 41, 59, 0.5)',
                        height=400,
                        font=dict(color='#cbd5e1', family='Inter'),
                        xaxis=dict(gridcolor='rgba(139, 92, 246, 0.2)'),
                        yaxis=dict(gridcolor='rgba(139, 92, 246, 0.2)'),
                        showlegend=False,
                        margin=dict(l=20, r=100, t=60, b=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Confidence Breakdown
                    st.markdown("<h3 class='section-header'>Detailed Results</h3>", unsafe_allow_html=True)
                    
                    for i, (formatted_cls, score) in enumerate(zip(formatted_classes, top_scores)):
                        confidence_color = "#10b981" if i == 0 else "#6366f1" if i < 3 else "#64748b"
                        st.markdown(f"""
                        <div class='glass-card' style='padding: 1.2rem; border-left: 4px solid {confidence_color};'>
                            <p style='margin: 0; color: #e2e8f0;'>
                                <strong style='font-size: 1.1rem;'>{i+1}. {formatted_cls}</strong>
                                <span style='float: right; color: {confidence_color}; font-weight: 700; font-size: 1.1rem;'>{score:.2f}%</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                st.success("✅ Analysis complete!")

                # Recommendations
                st.markdown("<h2 class='section-header'>💡 Recommendations</h2>", unsafe_allow_html=True)
                st.markdown("""
                <div class='glass-card'>
                    <h3>General Guidance</h3>
                    <ul style='margin-left: 1rem; line-height: 2;'>
                        <li>Monitor the affected plant closely for symptom progression</li>
                        <li>Isolate infected plants to prevent disease spread</li>
                        <li>Ensure proper watering and drainage</li>
                        <li>Consider consulting an agricultural expert for treatment options</li>
                        <li>Remove heavily infected leaves if necessary</li>
                    </ul>
                    <p style='margin-top: 1.5rem; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border-left: 3px solid #8b5cf6;'>
                        <strong>⚠️ Disclaimer:</strong> This tool provides preliminary analysis. Always verify results with agricultural professionals for treatment decisions.
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
    
    # System Information
    st.markdown("<h2 class='section-header'>System Architecture</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>🧠 Neural Network</h3>
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
                <h3>📊 Performance Metrics</h3>
                <p><strong>Test Accuracy:</strong> {model_info["metrics"]["accuracy"]*100:.2f}%</p>
                <p><strong>Total Classes:</strong> {model_info["metrics"]["num_classes"]}</p>
                <p><strong>Inference Time:</strong> ~0.5 seconds</p>
                <p><strong>Model Type:</strong> {model_info["metrics"]["model_type"]}</p>
                <p><strong>TensorFlow:</strong> v{model_info["metrics"]["tensorflow_version"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Dataset Information
    st.markdown("<h2 class='section-header'>Training Dataset</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3>📚 PlantVillage Dataset</h3>
        <p><strong>Source:</strong> PlantVillage dataset via Hugging Face</p>
        <p><strong>Total Images:</strong> 54,000+ high-resolution plant leaf images</p>
        <p><strong>Data Split:</strong> 70% Training, 15% Validation, 15% Testing</p>
        <p><strong>Image Resolution:</strong> 224 × 224 pixels (standardized)</p>
        <p><strong>Classes:</strong> 38 different plant disease categories</p>
        <p><strong>Augmentation:</strong> Rotation, flipping, zooming, and shifting applied</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Applications
    st.markdown("<h2 class='section-header'>Applications</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>🌾 Agriculture</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Early disease detection in commercial crops</li>
                <li>Real-time crop health monitoring</li>
                <li>Yield optimization and loss prevention</li>
                <li>Integrated pest management support</li>
            </ul>
        </div>
        
        <div class='glass-card'>
            <h3>🔬 Research</h3>
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
            <h3>🎓 Education</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Plant pathology teaching tool</li>
                <li>Student learning and practice</li>
                <li>Agricultural training programs</li>
                <li>Interactive disease identification</li>
            </ul>
        </div>
        
        <div class='glass-card'>
            <h3>🏡 Home Gardening</h3>
            <ul style='margin-left: 1rem; line-height: 2;'>
                <li>Personal garden health monitoring</li>
                <li>Plant care decision support</li>
                <li>Early disease prevention</li>
                <li>Treatment recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("<h2 class='section-header'>Technology Stack</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>🐍 Backend</h3>
            <p>Python 3.x</p>
            <p>TensorFlow</p>
            <p>NumPy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>🎨 Frontend</h3>
            <p>Streamlit</p>
            <p>Plotly</p>
            <p>Custom CSS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>🤖 AI/ML</h3>
            <p>Deep Learning</p>
            <p>CNN Architecture</p>
            <p>Transfer Learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("<h2 class='section-header'>Important Notice</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card' style='border-left: 4px solid #f59e0b;'>
        <h3>⚠️ Disclaimer</h3>
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
