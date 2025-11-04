import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ===============================================================
# 🌿 Plant Disease Classifier - Multi-Page App
# ===============================================================

st.set_page_config(
    page_title="🌿 Plant Disease Classifier",
    page_icon="🪴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# 🎨 Premium CSS Styling
# =======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
        padding: 2rem;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        opacity: 0.95;
        color: white;
        margin-bottom: 2rem;
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.8;
        color: white;
        opacity: 0.9;
    }
    
    /* Stat Cards */
    .stat-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: #2e7d32;
        margin: 1rem 0;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #333;
        font-weight: 500;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Info Cards */
    .info-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    .info-card h3 {
        color: #2e7d32;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .info-card p, .info-card li {
        color: #333;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Prediction Card */
    .prediction-card {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .prediction-title {
        font-size: 1.3rem;
        font-weight: 600;
        opacity: 0.95;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .prediction-result {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white;
    }
    
    .confidence-badge {
        background: rgba(255,255,255,0.3);
        padding: 0.7rem 2rem;
        border-radius: 25px;
        display: inline-block;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1rem;
        color: white;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e8f5e9 0%, #f1f8e9 100%);
    }
    
    .sidebar-info {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .sidebar-info p {
        color: #333;
        margin: 0.5rem 0;
    }
    
    /* Navigation */
    .nav-link {
        display: block;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: 600;
        color: #2e7d32;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .nav-link:hover {
        background: #2e7d32;
        color: white;
        transform: translateX(5px);
    }
    
    /* Section Headers */
    .section-header {
        color: #1b5e20;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2e7d32;
    }
    
    /* Table Styling */
    .metric-table {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 1rem;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .metric-row:last-child {
        border-bottom: none;
    }
    
    .metric-label {
        font-weight: 600;
        color: #2e7d32;
    }
    
    .metric-value {
        color: #333;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: #666;
        margin-top: 4rem;
        background: white;
        border-radius: 15px;
    }
    
    .footer h3 {
        color: #2e7d32;
    }
    
    /* Upload Box */
    .upload-section {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        border: 3px dashed #2e7d32;
        text-align: center;
        margin: 2rem 0;
    }
    
    .upload-section:hover {
        border-color: #1b5e20;
        background: #f1f8e9;
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# 🧠 Load Model and Data
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
        with open("model_config.json", "r") as f:
            info["config"] = json.load(f)
    except:
        info["config"] = None
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
# 📱 Navigation Sidebar
# =======================
with st.sidebar:
    st.markdown("## 🌿 Navigation")
    
    page = st.radio(
        "Go to:",
        ["🏠 Home", "📊 Model Info", "🔬 Disease Detection"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div class='sidebar-info'>
        <h3 style='color: #2e7d32; margin-bottom: 1rem;'>Quick Stats</h3>
        <p><strong>🎯 Accuracy:</strong> {:.1f}%</p>
        <p><strong>🌱 Classes:</strong> {}</p>
        <p><strong>⚡ Speed:</strong> ~0.5s</p>
        <p><strong>🧠 Model:</strong> MobileNetV2</p>
    </div>
    """.format(
        model_info["metrics"]["accuracy"] * 100 if model_info["metrics"] else 0,
        len(class_names)
    ), unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📞 Support")
    st.markdown("Need help? Check the Model Info page for detailed documentation.")

# =======================
# 🏠 HOME PAGE
# =======================
if page == "🏠 Home":
    st.markdown("""
        <div class='hero-section'>
            <div class='hero-title'>🌿 Plant Disease Classifier</div>
            <div class='hero-subtitle'>AI-Powered Plant Health Detection System</div>
            <div class='hero-description'>
                Harness the power of deep learning to identify plant diseases instantly. 
                Our advanced MobileNetV2 model analyzes leaf images with 94% accuracy, 
                helping farmers, gardeners, and researchers protect their crops and plants.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Dashboard
    st.markdown("<h2 class='section-header'>📊 System Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <div class='feature-icon'>🎯</div>
                <div class='stat-number'>{:.1f}%</div>
                <div class='stat-label'>Accuracy</div>
            </div>
        """.format(model_info["metrics"]["accuracy"] * 100 if model_info["metrics"] else 0), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='stat-card'>
                <div class='feature-icon'>🌱</div>
                <div class='stat-number'>{len(class_names)}</div>
                <div class='stat-label'>Disease Classes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        plants_count = len(set(name.split('___')[0] for name in class_names))
        st.markdown(f"""
            <div class='stat-card'>
                <div class='feature-icon'>🪴</div>
                <div class='stat-number'>{plants_count}</div>
                <div class='stat-label'>Plant Types</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='stat-card'>
                <div class='feature-icon'>⚡</div>
                <div class='stat-number'>0.5s</div>
                <div class='stat-label'>Analysis Time</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown("<h2 class='section-header'>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>🚀</div>
            <h3>Fast & Accurate</h3>
            <p>Get results in under a second with 94% accuracy using state-of-the-art MobileNetV2 deep learning architecture trained on thousands of plant images.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>🌍</div>
            <h3>Multi-Plant Support</h3>
            <p>Detects diseases across 14+ plant species including tomato, apple, grape, corn, potato, pepper, cherry, peach, strawberry, and more.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>📱</div>
            <h3>Easy to Use</h3>
            <p>Simply upload a clear photo of a plant leaf and get instant diagnosis with detailed confidence scores and actionable insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown("<h2 class='section-header'>🔍 How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>📸</div>
            <h3>1. Upload</h3>
            <p>Take or upload a clear photo of a plant leaf showing any symptoms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>🧬</div>
            <h3>2. Analyze</h3>
            <p>Our AI model processes the image through neural networks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>🎯</div>
            <h3>3. Detect</h3>
            <p>Get instant disease identification with confidence scores</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='info-card'>
            <div class='feature-icon'>💡</div>
            <h3>4. Act</h3>
            <p>Receive insights and recommendations for treatment</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Supported Plants
    st.markdown("<h2 class='section-header'>🌱 Supported Plants</h2>", unsafe_allow_html=True)
    
    plants = set()
    for name in class_names:
        plant = name.split('___')[0]
        plants.add(plant)
    
    cols = st.columns(4)
    for idx, plant in enumerate(sorted(plants)):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class='info-card' style='padding: 1rem;'>
                <p style='font-size: 1.2rem; font-weight: 600; color: #2e7d32; margin: 0;'>
                    🌿 {plant}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='info-card' style='text-align: center; padding: 3rem;'>
            <h2 style='color: #2e7d32;'>Ready to Get Started?</h2>
            <p style='font-size: 1.2rem; color: #666; margin: 1.5rem 0;'>
                Navigate to the Disease Detection page to analyze your plant leaves!
            </p>
        </div>
        """, unsafe_allow_html=True)

# =======================
# 📊 MODEL INFO PAGE
# =======================
elif page == "📊 Model Info":
    st.markdown("""
        <div class='hero-section'>
            <div class='hero-title'>📊 Model Information</div>
            <div class='hero-subtitle'>Technical Details & Performance Metrics</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Model Architecture
    st.markdown("<h2 class='section-header'>🏗️ Model Architecture</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h3>🧠 Base Architecture</h3>
            <p><strong>Model Type:</strong> MobileNetV2</p>
            <p><strong>Framework:</strong> TensorFlow {}</p>
            <p><strong>Keras Version:</strong> {}</p>
            <p><strong>Input Shape:</strong> 224 × 224 × 3 (RGB)</p>
            <p><strong>Total Parameters:</strong> ~3.5M</p>
            <p><strong>Model Size:</strong> ~9 MB</p>
        </div>
        """.format(
            model_info['metrics']['tensorflow_version'] if model_info['metrics'] else 'N/A',
            model_info['metrics']['keras_version'] if model_info['metrics'] else 'N/A'
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='info-card'>
            <h3>🎯 Output Specifications</h3>
            <p><strong>Number of Classes:</strong> {len(class_names)}</p>
            <p><strong>Output Format:</strong> Softmax Probabilities</p>
            <p><strong>Classification Type:</strong> Multi-class</p>
            <p><strong>Inference Time:</strong> ~0.5 seconds</p>
            <p><strong>Batch Processing:</strong> Supported</p>
            <p><strong>GPU Acceleration:</strong> Enabled</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Metrics
    st.markdown("<h2 class='section-header'>📈 Performance Metrics</h2>", unsafe_allow_html=True)
    
    if model_info["metrics"]:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            accuracy = model_info["metrics"]["accuracy"] * 100
            st.markdown(f"""
            <div class='stat-card'>
                <div class='feature-icon'>🎯</div>
                <div class='stat-number'>{accuracy:.2f}%</div>
                <div class='stat-label'>Test Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            loss = model_info["metrics"]["test_loss"]
            st.markdown(f"""
            <div class='stat-card'>
                <div class='feature-icon'>📉</div>
                <div class='stat-number'>{loss:.4f}</div>
                <div class='stat-label'>Test Loss</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='feature-icon'>🌱</div>
                <div class='stat-number'>{model_info["metrics"]["num_classes"]}</div>
                <div class='stat-label'>Total Classes</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Training Details
    st.markdown("<h2 class='section-header'>🎓 Training Configuration</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h3>📚 Dataset Information</h3>
            <p><strong>Dataset:</strong> PlantVillage</p>
            <p><strong>Source:</strong> Hugging Face</p>
            <p><strong>Total Images:</strong> ~54,000+</p>
            <p><strong>Train/Val/Test Split:</strong> 70/15/15</p>
            <p><strong>Image Resolution:</strong> 224 × 224 pixels</p>
            <p><strong>Data Format:</strong> RGB Images</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h3>⚙️ Training Parameters</h3>
            <p><strong>Optimizer:</strong> Adam</p>
            <p><strong>Learning Rate:</strong> 0.001</p>
            <p><strong>Loss Function:</strong> Categorical Crossentropy</p>
            <p><strong>Batch Size:</strong> 32</p>
            <p><strong>Epochs:</strong> 5 (with early stopping)</p>
            <p><strong>Callbacks:</strong> Early Stopping, Model Checkpoint</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Augmentation
    st.markdown("<h2 class='section-header'>🔄 Data Augmentation</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-card'>
        <h3>🎨 Augmentation Techniques Applied</h3>
        <ul>
            <li><strong>Rotation:</strong> Random rotation up to ±20 degrees</li>
            <li><strong>Width Shift:</strong> Horizontal shift up to 20% of image width</li>
            <li><strong>Height Shift:</strong> Vertical shift up to 20% of image height</li>
            <li><strong>Zoom:</strong> Random zoom up to 20%</li>
            <li><strong>Horizontal Flip:</strong> Random horizontal flipping</li>
            <li><strong>Rescaling:</strong> Pixel normalization (0-1 range)</li>
        </ul>
        <p style='margin-top: 1rem;'><em>These augmentation techniques help the model generalize better and become robust to various image conditions.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Layers
    st.markdown("<h2 class='section-header'>🧬 Network Layers</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-card'>
        <h3>📐 Layer Architecture</h3>
        <ol>
            <li><strong>Input Layer:</strong> 224 × 224 × 3 RGB image</li>
            <li><strong>MobileNetV2 Base:</strong> Pre-trained on ImageNet (frozen)</li>
            <li><strong>Global Average Pooling:</strong> Dimensionality reduction</li>
            <li><strong>Dense Layer 1:</strong> 256 units, ReLU activation</li>
            <li><strong>Dropout 1:</strong> 50% dropout rate</li>
            <li><strong>Dense Layer 2:</strong> 128 units, ReLU activation</li>
            <li><strong>Dropout 2:</strong> 30% dropout rate</li>
            <li><strong>Output Layer:</strong> 38 units, Softmax activation</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Cases
    st.markdown("<h2 class='section-header'>🎯 Applications & Use Cases</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h3>🌾 Agriculture</h3>
            <ul>
                <li>Early disease detection in crops</li>
                <li>Crop health monitoring</li>
                <li>Pest and disease management</li>
                <li>Yield optimization</li>
            </ul>
        </div>
        
        <div class='info-card'>
            <h3>🔬 Research</h3>
            <ul>
                <li>Plant pathology studies</li>
                <li>Disease spread analysis</li>
                <li>Agricultural research</li>
                <li>Climate impact studies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h3>📚 Education</h3>
            <ul>
                <li>Teaching plant pathology</li>
                <li>Student learning tools</li>
                <li>Agricultural training</li>
                <li>Disease identification practice</li>
            </ul>
        </div>
        
        <div class='info-card'>
            <h3>🏡 Home Gardening</h3>
            <ul>
                <li>Garden health monitoring</li>
                <li>Plant care assistance</li>
                <li>Disease prevention</li>
                <li>Treatment recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =======================
# 🔬 DISEASE DETECTION PAGE
# =======================
elif page == "🔬 Disease Detection":
    st.markdown("""
        <div class='hero-section'>
            <div class='hero-title'>🔬 Disease Detection</div>
            <div class='hero-subtitle'>Upload a Leaf Image for Instant Analysis</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>📸 Upload Image</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='info-card' style='text-align: center;'>
            <p style='font-size: 1.1rem; color: #333;'>
                <strong>Tips for Best Results:</strong><br>
                📱 Use good lighting conditions<br>
                🎯 Focus on a single leaf<br>
                📷 Ensure the disease symptoms are visible<br>
                ✨ Avoid blurry or dark images
            </p>
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
            st.markdown("<h3 style='color: #2e7d32;'>🖼️ Uploaded Image</h3>", unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            
            st.markdown(f"""
            <div class='info-card'>
                <h3>📏 Image Details</h3>
                <p><strong>Dimensions:</strong> {image.size[0]} × {image.size[1]} pixels</p>
                <p><strong>Format:</strong> {image.format}</p>
                <p><strong>Mode:</strong> {image.mode}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h3 style='color: #2e7d32;'>🔬 Analysis</h3>", unsafe_allow_html=True)
            
            if st.button("🔍 Analyze Plant Disease", use_container_width=True):
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

                    # Display main result
                    st.markdown("""
                    <div class='prediction-card'>
                        <div class='prediction-title'>🌱 Predicted Disease</div>
                        <div class='prediction-result'>{}</div>
                        <div class='confidence-badge'>Confidence: {:.2f}%</div>
                    </div>
                    """.format(top_classes[0], top_scores[0]), unsafe_allow_html=True)

                    # 📊 Plot Top-5 Bar Chart
                    fig = px.bar(
                        x=top_scores[::-1],
                        y=top_classes[::-1],
                        orientation='h',
                        text=[f"{s:.2f}%" for s in top_scores[::-1]],
                        color=top_scores[::-1],
                        color_continuous_scale="Greens"
                    )
                    fig.update_layout(
                        title="Top 5 Predictions",
                        xaxis_title="Confidence (%)",
                        yaxis_title="Disease Class",
                        template="simple_white",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Confidence Breakdown Table
                    st.markdown("<h3 class='section-header'>📋 Confidence Breakdown</h3>", unsafe_allow_html=True)
                    for i, (cls, score) in enumerate(zip(top_classes, top_scores)):
                        st.markdown(f"<p><strong>{i+1}. {cls}</strong> — {score:.2f}%</p>", unsafe_allow_html=True)

                st.success("✅ Analysis complete! Scroll down for details.")

                # Optional Recommendation Section
                st.markdown("<h2 class='section-header'>💡 Recommendations</h2>", unsafe_allow_html=True)
                st.markdown("""
                <div class='info-card'>
                    <h3>🌾 General Guidance</h3>
                    <ul>
                        <li>Ensure proper watering and soil drainage.</li>
                        <li>Inspect nearby plants for similar symptoms.</li>
                        <li>Use organic or recommended fungicides if applicable.</li>
                        <li>Remove heavily infected leaves to prevent spread.</li>
                    </ul>
                    <p style='margin-top: 1rem; font-style: italic;'>*Always verify results with an agricultural expert for best practices.*</p>
                </div>
                """, unsafe_allow_html=True)
