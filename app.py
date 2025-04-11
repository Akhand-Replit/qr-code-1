import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageOps
import io
import base64
from pathlib import Path
import os
import numpy as np

# Set page config
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="📱",
    layout="wide"
)

# Add custom CSS for retro-futuristic theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Share+Tech+Mono&display=swap');
    
    /* Base styling */
    .main {
        background-color: #0a0a1a;
        color: #00fffc;
        padding: 2rem;
        background-image: 
            linear-gradient(0deg, rgba(10, 10, 26, 0.9) 0%, 
            rgba(10, 10, 26, 0.9) 100%),
            repeating-linear-gradient(0deg, transparent, transparent 2px, 
            rgba(0, 255, 252, 0.1) 2px, rgba(0, 255, 252, 0.1) 4px);
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Scanline effect for the whole page */
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: repeating-linear-gradient(
            to bottom,
            rgba(0, 0, 0, 0),
            rgba(0, 0, 0, 0) 1px,
            rgba(0, 0, 0, 0.15) 1px,
            rgba(0, 0, 0, 0.15) 2px
        );
        pointer-events: none;
        z-index: 1000;
    }
    
    /* Special text glowing effect */
    h1, h2, h3, .retro-text {
        font-family: 'Orbitron', sans-serif;
        color: #ff00ff;
        text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff;
        letter-spacing: 1px;
    }
    
    /* Step header */
    .step-header {
        background-color: rgba(0, 0, 0, 0.5);
        border: 2px solid #ff00ff;
        color: #00fffc;
        padding: 8px 15px;
        border-radius: 0;
        margin-bottom: 20px;
        display: inline-block;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 0 10px #ff00ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        clip-path: polygon(0 0, 95% 0, 100% 30%, 100% 100%, 5% 100%, 0 70%);
    }
    
    /* Info box */
    .info-box {
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid #00fffc;
        border-radius: 0;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px #00fffc;
        position: relative;
        overflow: hidden;
    }
    
    .info-box::before {
        content: "";
        position: absolute;
        background: linear-gradient(45deg, transparent 49%, #00fffc 49%, #00fffc 51%, transparent 51%);
        width: 30px;
        height: 30px;
        top: -15px;
        left: -15px;
        z-index: 1;
    }
    
    /* Download button */
    .download-btn {
        background-color: rgba(0, 0, 0, 0.7);
        color: #ff00ff;
        border: 2px solid #ff00ff;
        padding: 12px 25px;
        border-radius: 0;
        text-align: center;
        cursor: pointer;
        margin-top: 20px;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px #ff00ff;
        clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
    }
    
    .download-btn:hover {
        background-color: rgba(255, 0, 255, 0.2);
        box-shadow: 0 0 20px #ff00ff;
        transform: translateY(-2px);
    }
    
    /* Option container */
    .option-container {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
        background-color: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-left: 3px solid #00fffc;
        position: relative;
    }
    
    .option-container::after {
        content: "";
        position: absolute;
        right: 0;
        top: 0;
        height: 100%;
        width: 30px;
        background: linear-gradient(90deg, transparent, #00fffc);
        opacity: 0.2;
    }
    
    /* Pattern container */
    .pattern-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 10px;
        margin-top: 15px;
    }
    
    .pattern-item {
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid #00fffc;
        border-radius: 0;
        padding: 10px;
        cursor: pointer;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .pattern-item::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 252, 0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.5s ease;
    }
    
    .pattern-item:hover {
        border-color: #ff00ff;
        box-shadow: 0 0 15px #ff00ff;
        transform: translateY(-2px) scale(1.02);
    }
    
    .pattern-item:hover::before {
        left: 100%;
    }
    
    /* Preview container */
    .preview-container {
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid #00fffc;
        padding: 20px;
        border-radius: 0;
        text-align: center;
        box-shadow: 0 0 15px #00fffc;
        position: relative;
    }
    
    .preview-container::before, .preview-container::after {
        content: "";
        position: absolute;
        width: 20px;
        height: 20px;
        border: 2px solid #00fffc;
    }
    
    .preview-container::before {
        top: -2px;
        left: -2px;
        border-right: none;
        border-bottom: none;
    }
    
    .preview-container::after {
        bottom: -2px;
        right: -2px;
        border-left: none;
        border-top: none;
    }
    
    /* Logo grid */
    .logo-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 10px;
        margin-top: 15px;
    }
    
    .logo-item {
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid #00fffc;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .logo-item:hover {
        border-color: #ff00ff;
        box-shadow: 0 0 15px #ff00ff;
        transform: scale(1.1);
    }
    
    /* Custom inputs */
    input[type="text"], input[type="color"], .stTextInput input {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: #00fffc !important;
        border: 1px solid #00fffc !important;
        border-radius: 0 !important;
        padding: 10px !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    input[type="text"]:focus, .stTextInput input:focus {
        border-color: #ff00ff !important;
        box-shadow: 0 0 10px #ff00ff !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: #00fffc !important;
        border: 2px solid #00fffc !important;
        border-radius: 0 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        z-index: 1 !important;
    }
    
    .stButton > button:hover {
        color: #ff00ff !important;
        border-color: #ff00ff !important;
        box-shadow: 0 0 15px #ff00ff !important;
    }
    
    .stButton > button:hover::after {
        transform: translateX(100%) !important;
    }
    
    .stButton > button::after {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 0, 255, 0.2), transparent) !important;
        transition: transform 0.5s ease !important;
        z-index: -1 !important;
    }
    
    /* Primary buttons */
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: #ff00ff !important;
        border: 2px solid #ff00ff !important;
        box-shadow: 0 0 10px #ff00ff !important;
        clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox label span {
        color: #00fffc !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    /* Radio button styling */
    .stRadio label span {
        color: #00fffc !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 2px solid #00fffc !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00fffc !important;
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ff00ff !important;
        text-shadow: 0 0 5px #ff00ff !important;
        border-bottom: 2px solid #ff00ff !important;
    }
    
    /* File uploader styling */
    .stFileUploader [data-baseweb="button"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: #00fffc !important;
        border: 2px solid #00fffc !important;
        border-radius: 0 !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    .stFileUploader [data-baseweb="button"]:hover {
        color: #ff00ff !important;
        border-color: #ff00ff !important;
        box-shadow: 0 0 15px #ff00ff !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00fffc;
        border-radius: 0;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ff00ff;
    }
    
    /* Links */
    a {
        color: #00fffc !important;
        text-decoration: none !important;
        position: relative !important;
        transition: all 0.3s ease !important;
    }
    
    a:hover {
        color: #ff00ff !important;
        text-shadow: 0 0 5px #ff00ff !important;
    }
    
    a::after {
        content: "" !important;
        position: absolute !important;
        width: 100% !important;
        height: 1px !important;
        bottom: -2px !important;
        left: 0 !important;
        background-color: #00fffc !important;
        transform: scaleX(0) !important;
        transform-origin: right !important;
        transition: transform 0.3s ease !important;
    }
    
    a:hover::after {
        transform: scaleX(1) !important;
        transform-origin: left !important;
        background-color: #ff00ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to create QR code
def create_qr_code(url, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4, 
                  fill_color="#000000", back_color="#FFFFFF", logo_path=None, eye_style="square"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.convert("RGBA")
    
    # Apply custom eye style if needed
    if eye_style != "square":
        img = customize_eyes(img, eye_style, fill_color)
    
    # Add logo if provided
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            # Calculate logo size (25% of QR code)
            logo_size = int(img.size[0] * 0.25)
            logo = logo.resize((logo_size, logo_size))
            
            # Calculate position to center the logo
            pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            
            # Create a mask for rounded corners on the logo
            mask = Image.new("L", logo.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo_size, logo_size), fill=255)
            
            # Create white background circle for logo
            bg_circle = Image.new("RGBA", logo.size, (255, 255, 255, 255))
            bg_circle.putalpha(mask)
            
            # Paste background circle then logo
            img_with_bg = img.copy()
            img_with_bg.paste(bg_circle, pos, bg_circle)
            img_with_bg.paste(logo, pos, mask)
            
            return img_with_bg
        except Exception as e:
            st.error(f"Error adding logo: {e}")
            return img
    
    return img

# Function to customize QR code eyes
def customize_eyes(img, eye_style, color):
    # Convert to numpy array for manipulation
    img_array = np.array(img)
    width, height = img.size
    
    # Find the positions of the three finder patterns (eyes)
    # Top-left eye
    tl_eye_pos = (0, 0)
    # Top-right eye
    tr_eye_pos = (width - 70, 0)
    # Bottom-left eye
    bl_eye_pos = (0, height - 70)
    
    # Create a mask for the eyes
    mask = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    
    # Draw custom eyes based on style
    eye_size = 70
    
    if eye_style == "circle":
        # Draw circular eyes
        for pos in [tl_eye_pos, tr_eye_pos, bl_eye_pos]:
            draw.ellipse([pos[0], pos[1], pos[0] + eye_size, pos[1] + eye_size], 
                         fill=color)
            # Draw inner white circle
            draw.ellipse([pos[0] + 15, pos[1] + 15, pos[0] + eye_size - 15, pos[1] + eye_size - 15], 
                         fill="#FFFFFF")
            # Draw innermost colored circle
            draw.ellipse([pos[0] + 25, pos[1] + 25, pos[0] + eye_size - 25, pos[1] + eye_size - 25], 
                         fill=color)
    
    elif eye_style == "rounded":
        # Draw rounded square eyes
        for pos in [tl_eye_pos, tr_eye_pos, bl_eye_pos]:
            draw.rounded_rectangle([pos[0], pos[1], pos[0] + eye_size, pos[1] + eye_size], 
                                  radius=15, fill=color)
            # Draw inner white rounded square
            draw.rounded_rectangle([pos[0] + 15, pos[1] + 15, pos[0] + eye_size - 15, pos[1] + eye_size - 15], 
                                  radius=10, fill="#FFFFFF")
            # Draw innermost colored rounded square
            draw.rounded_rectangle([pos[0] + 25, pos[1] + 25, pos[0] + eye_size - 25, pos[1] + eye_size - 25], 
                                  radius=5, fill=color)
    
    # Create the composite image
    result = Image.alpha_composite(img.convert("RGBA"), mask)
    return result

# Function to get image as base64
def get_image_as_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Function to create download link
def get_download_link(img, filename, format="PNG"):
    buffered = io.BytesIO()
    if format.upper() == "SVG":
        # Convert to SVG (simplified)
        # For real SVG conversion, you would need more complex logic
        img.save(buffered, format="PNG")
        mime = "image/png"  # Using PNG as a fallback
    else:
        img.save(buffered, format="PNG")
        mime = "image/png"
    
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:{mime};base64,{img_str}" download="{filename}.{format.lower()}" class="download-btn">Download {format}</a>'
    return href

# Load social media logos
def load_social_logos():
    logos = {
        "Facebook": ("facebook.png", "#1877F2"),
        "Instagram": ("instagram.png", "#E4405F"),
        "Pinterest": ("pinterest.png", "#BD081C"),
        "Twitter": ("twitter.png", "#1DA1F2"),
        "YouTube": ("youtube.png", "#FF0000"),
        "Snapchat": ("snapchat.png", "#FFFC00"),
        "TikTok": ("tiktok.png", "#000000"),
        "LinkedIn": ("linkedin.png", "#0A66C2"),
        "WhatsApp": ("whatsapp.png", "#25D366"),
        "Telegram": ("telegram.png", "#26A5E4"),
        "Google": ("google.png", "#4285F4"),
        "Gmail": ("gmail.png", "#EA4335"),
        "PayPal": ("paypal.png", "#00457C"),
    }
    return logos

# App title with retro-futuristic styling
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="font-size: 3rem; letter-spacing: 3px; margin-bottom: 0;">QUANTUM QR</h1>
    <div style="font-size: 1.2rem; color: #00fffc; font-family: 'Share Tech Mono', monospace; 
                letter-spacing: 2px; margin-top: -5px; margin-bottom: 20px;">
        C Y B E R N E T I C · C O D E · G E N E R A T O R · 2 0 2 5
    </div>
    <div style="width: 80%; margin: 0 auto; height: 2px; background: linear-gradient(90deg, transparent, #ff00ff, transparent);"></div>
    <p style="margin-top: 20px; font-size: 1.1rem; color: #c8c8c8;">
        Generate hyper-dimensional QR codes for neural-link integration across digital realms
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'url' not in st.session_state:
    st.session_state.url = ""
if 'qr_type' not in st.session_state:
    st.session_state.qr_type = "static"
if 'pattern' not in st.session_state:
    st.session_state.pattern = "default"
if 'eye_style' not in st.session_state:
    st.session_state.eye_style = "square"
if 'logo_path' not in st.session_state:
    st.session_state.logo_path = None
if 'fill_color' not in st.session_state:
    st.session_state.fill_color = "#054080"
if 'back_color' not in st.session_state:
    st.session_state.back_color = "#FFFFFF"
if 'transparent_bg' not in st.session_state:
    st.session_state.transparent_bg = False

# Navigation functions
def go_to_step(step):
    st.session_state.current_step = step

# STEP 1: URL Input
if st.session_state.current_step == 1:
    st.markdown('<div class="step-header">STEP 1</div> <span style="color:#00fffc; font-family: \'Share Tech Mono\', monospace; letter-spacing: 1px;">ENTER TARGET DIGITAL COORDINATE</span>', unsafe_allow_html=True)
    
    # URL input with retro-futuristic styling
    st.markdown("""
    <div style="position: relative; margin-bottom: 20px;">
        <div style="position: absolute; top: -10px; left: -10px; width: 20px; height: 20px; border-top: 2px solid #00fffc; border-left: 2px solid #00fffc;"></div>
        <div style="position: absolute; top: -10px; right: -10px; width: 20px; height: 20px; border-top: 2px solid #00fffc; border-right: 2px solid #00fffc;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.url = st.text_input("", value=st.session_state.url, placeholder="https://www.netrunner-access.cy")
    
    st.markdown("""
    <div style="position: relative; margin-top: -10px;">
        <div style="position: absolute; bottom: -10px; left: -10px; width: 20px; height: 20px; border-bottom: 2px solid #00fffc; border-left: 2px solid #00fffc;"></div>
        <div style="position: absolute; bottom: -10px; right: -10px; width: 20px; height: 20px; border-bottom: 2px solid #00fffc; border-right: 2px solid #00fffc;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload image option
    st.markdown("""
    <div style="color:#00fffc; font-family: 'Share Tech Mono', monospace; margin: 20px 0 10px 0; display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; border: 1px solid #00fffc; margin-right: 10px; position: relative;">
            <div style="position: absolute; top: 2px; left: 2px; right: 2px; bottom: 2px; background-color: #00fffc; opacity: 0.5;"></div>
        </div>
        ALTERNATIVE: UPLOAD IMAGE FOR COORDINATE EXTRACTION
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    
    # QR Type selection with retro-futuristic styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="option-container">', unsafe_allow_html=True)
        static_qr = st.radio("Static QR", ["STATIC QUANTUM CODE"], label_visibility="collapsed")
        if static_qr:
            st.session_state.qr_type = "static"
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="option-container">', unsafe_allow_html=True)
        dynamic_qr = st.radio("Dynamic QR", ["DYNAMIC NEURAL LINK"], label_visibility="collapsed", disabled=True)
        if dynamic_qr:
            st.session_state.qr_type = "dynamic"
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; margin-top: 5px;">
            <div style="width: 8px; height: 8px; background-color: #ff00ff; margin-right: 8px;"></div>
            <span>EDIT DATA</span>
            <div style="width: 1px; height: 15px; background-color: #00fffc; margin: 0 10px;"></div>
            <span>TRACK SCANS</span>
            <div style="margin-left: 10px;">
                <a href="https://www.example.com" style="color: #00fffc; text-decoration: none; border-bottom: 1px dashed #00fffc;">ACCESS MANUAL</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Info box with retro-futuristic styling
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: flex-start;">
        <div style="min-width: 30px; margin-right: 15px;">
            <div style="width: 20px; height: 20px; border: 2px solid #00fffc; border-radius: 50%; display: flex; justify-content: center; align-items: center; position: relative;">
                <span style="color: #00fffc; font-weight: bold;">i</span>
                <div style="position: absolute; top: -5px; right: -5px; width: 10px; height: 10px; background-color: #00fffc; border-radius: 50%; animation: pulse 2s infinite;"></div>
            </div>
        </div>
        <div>
            <span style="color: #00fffc; font-weight: bold; letter-spacing: 1px;">SYSTEM RECOMMENDATION:</span> Deploy dynamic quantum codes for real-time tracking metrics and post-materialization data modifications.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate button with retro-futuristic styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("INITIALIZE QUANTUM CODE"):
            if st.session_state.url:
                go_to_step(2)
            else:
                st.markdown("""
                <div style="color: #ff5555; background-color: rgba(255, 0, 0, 0.1); border: 1px solid #ff5555; padding: 10px; margin: 10px 0; font-family: 'Share Tech Mono', monospace; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255, 0, 0, 0.1) 10px, rgba(255, 0, 0, 0.1) 20px);"></div>
                    <div style="position: relative; z-index: 1;">
                        <span style="font-weight: bold; letter-spacing: 1px;">ERROR:</span> TARGET COORDINATE REQUIRED FOR INITIALIZATION
                    </div>
                </div>
                """, unsafe_allow_html=True)

# STEP 2: Customize QR
elif st.session_state.current_step == 2:
    st.markdown('<div class="step-header">STEP 2</div> Customize your QR', unsafe_allow_html=True)
    
    # Create tabs for customization options
    tab_pattern, tab_eyes, tab_logo, tab_colors, tab_frame, tab_templates = st.tabs([
        "Pattern", "Eyes", "Logo", "Colors", "Frame", "Templates"
    ])
    
    # Pattern tab
    with tab_pattern:
        st.markdown("You can customize these templates later to match your brand")
        
        # Display pattern options in a grid
        st.markdown('<div class="pattern-container">', unsafe_allow_html=True)
        patterns = ["default", "dots", "rounded", "square", "circular", "random", 
                    "vertical", "horizontal", "diagonal", "circular2", "flower", "diamond"]
        
        # Create a 2x6 grid for pattern selection
        cols = st.columns(6)
        for i, pattern in enumerate(patterns):
            with cols[i % 6]:
                if st.button(f"Pattern {i+1}", key=f"pattern_{pattern}"):
                    st.session_state.pattern = pattern
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Eyes tab
    with tab_eyes:
        st.markdown("Select eyes to make your QR code stand out. Eyes are what your camera recognizes when scanning")
        
        # Display eye options in a grid
        st.markdown('<div class="pattern-container">', unsafe_allow_html=True)
        eye_styles = ["square", "circle", "rounded", "dot", "diamond", "flower"]
        
        # Create a 3x6 grid for eye selection
        cols = st.columns(6)
        for i, style in enumerate(eye_styles):
            with cols[i % 6]:
                if st.button(f"Eye {i+1}", key=f"eye_{style}"):
                    st.session_state.eye_style = style
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Logo tab
    with tab_logo:
        st.markdown("With this QR code generator with logo, you can easily add your logo for stronger brand recall (300 x 300px, 72dpi)")
        
        # Upload logo
        uploaded_logo = st.file_uploader("Upload", type=["png", "jpg", "jpeg"])
        if uploaded_logo:
            # Save the uploaded file temporarily
            logo_path = f"temp_logo_{uploaded_logo.name}"
            with open(logo_path, "wb") as f:
                f.write(uploaded_logo.getbuffer())
            st.session_state.logo_path = logo_path
        
        # Remove logo button
        if st.session_state.logo_path:
            if st.button("Remove logo"):
                if os.path.exists(st.session_state.logo_path):
                    os.remove(st.session_state.logo_path)
                st.session_state.logo_path = None
        
        # Supported formats
        st.markdown("Supported formats:")
        col1, col2 = st.columns(2)
        with col1:
            st.button("PNG")
        with col2:
            st.button("JPG")
        
        # Pre-defined logos
        st.markdown("Or use our available logos:")
        logos = load_social_logos()
        
        # Create grid for social media logos
        st.markdown('<div class="logo-grid">', unsafe_allow_html=True)
        for logo_name, (logo_file, logo_color) in logos.items():
            # In a real app, you would have these logo files available
            # Here we'll just create buttons with the names
            if st.button(logo_name, key=f"logo_{logo_name}"):
                st.session_state.logo_path = f"logos/{logo_file}"  # This is a placeholder path
                st.session_state.fill_color = logo_color
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Colors tab
    with tab_colors:
        st.markdown("Embellish your customized QR with your brand colors")
        
        # Color options
        color_type = st.radio("", ["Solid Color", "Gradient", "Custom Eye Color"], horizontal=True)
        
        if color_type == "Solid Color":
            st.session_state.fill_color = st.color_picker("", value=st.session_state.fill_color)
        elif color_type == "Gradient":
            st.session_state.fill_color = st.color_picker("Gradient Start", value=st.session_state.fill_color)
            gradient_end = st.color_picker("Gradient End", value="#000000")
            # Gradient functionality would need more complex implementation
        elif color_type == "Custom Eye Color":
            st.session_state.fill_color = st.color_picker("QR Color", value=st.session_state.fill_color)
            eye_color = st.color_picker("Eye Color", value="#000000")
            # Custom eye color would need more implementation
        
        # Background color
        st.markdown("Background")
        st.session_state.back_color = st.color_picker("", value=st.session_state.back_color)
        
        # Transparent background option
        st.session_state.transparent_bg = st.checkbox("Transparent background")
        if st.session_state.transparent_bg:
            st.session_state.back_color = "transparent"
    
    # Frame tab (placeholder)
    with tab_frame:
        st.markdown("Add a frame to your QR code (Coming soon)")
    
    # Templates tab (placeholder)
    with tab_templates:
        st.markdown("Choose from pre-designed templates (Coming soon)")
    
    # Preview and download section
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("You can customize these templates later to match your brand.")
        st.markdown("Always scan to test that your QR code works")
        
        # Download options
        format_col1, format_col2 = st.columns(2)
        with format_col1:
            png_selected = st.radio("PNG", ["PNG"], label_visibility="collapsed")
        with format_col2:
            svg_selected = st.radio("SVG", ["SVG"], label_visibility="collapsed", disabled=True)
        
        # Save as template
        st.checkbox("Save as a template")
        
        # Download button (functionality will be added after preview)
        st.button("Download", type="primary")
    
    with col2:
        # Create preview of QR code
        if st.session_state.url:
            try:
                # Set background color based on transparency selection
                back_color = "transparent" if st.session_state.transparent_bg else st.session_state.back_color
                
                # Create QR code
                qr_img = create_qr_code(
                    st.session_state.url,
                    fill_color=st.session_state.fill_color,
                    back_color=back_color,
                    logo_path=st.session_state.logo_path,
                    eye_style=st.session_state.eye_style
                )
                
                # Display preview
                st.markdown('<div class="preview-container">', unsafe_allow_html=True)
                st.image(qr_img, caption="QR Code Preview", use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Create download link
                st.markdown(get_download_link(qr_img, "qr_code", "PNG"), unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating QR code: {e}")
        else:
            st.warning("Please enter a URL to generate a QR code")
    
    # Back button
    if st.button("Back to Step 1"):
        go_to_step(1)

# Footer
st.markdown("---")
st.markdown("© 2025 QR Code Generator. All rights reserved. Akhand Foundation _ Shuvo_WebDev")
