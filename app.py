import streamlit as st
import qrcode
from PIL import Image
import io
import base64
from datetime import datetime
import numpy as np

# Configure the page
st.set_page_config(
    page_title="Akhand QR Generate",
    page_icon="https://i.ibb.co/8gByP557/7ca29bb23a48.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for retro futuristic UI
st.markdown("""
<style>
    /* Retro Futuristic Theme */
    :root {
        --primary-color: #5928E5;
        --secondary-color: #FF4081;
        --background-color: #0F172A;
        --text-color: #E2E8F0;
        --accent-color: #38BDF8;
    }
    
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    h1, h2, h3 {
        color: var(--accent-color) !important;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 5px;
        border: 2px solid var(--accent-color);
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-color);
        color: var(--background-color);
        transform: scale(1.05);
        box-shadow: 0 0 15px var(--accent-color);
    }
    
    .retro-card {
        background: linear-gradient(145deg, #131c33, #0d1425);
        border: 1px solid var(--accent-color);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
        margin-bottom: 20px;
    }
    
    .stTextInput>div>div {
        border-radius: 5px;
        border: 2px solid var(--primary-color);
    }
    
    .stTextInput>div>div:focus-within {
        border: 2px solid var(--accent-color);
        box-shadow: 0 0 10px var(--accent-color);
    }
    
    .stSelectbox>div>div, .stMultiselect>div>div {
        border-radius: 5px;
        border: 2px solid var(--primary-color);
    }
    
    /* QR Code Display */
    .qr-display {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    /* Logo */
    .site-logo {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .site-logo h1 {
        font-size: 3em;
        margin-bottom: 0;
        background: linear-gradient(to right, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    
    /* Glow effect for important elements */
    .glow-effect {
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from {
            box-shadow: 0 0 5px var(--accent-color);
        }
        to {
            box-shadow: 0 0 20px var(--accent-color);
        }
    }
    
    /* Download button styling */
    .download-button {
        display: inline-block;
        background-color: var(--primary-color);
        color: white !important;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 5px;
        margin: 10px 5px;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid var(--accent-color);
        font-weight: bold;
    }
    
    .download-button:hover {
        background-color: var(--accent-color);
        color: var(--background-color) !important;
        transform: scale(1.05);
        box-shadow: 0 0 15px var(--accent-color);
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">

<div class="site-logo">
    <h1>Akhand QR Generate</h1>
</div>
""", unsafe_allow_html=True)

# Function to generate QR code
def generate_qr_code(data, box_size, border, fill_color, back_color):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

# Function to add logo to QR code
def add_logo_to_qr(qr_img, logo):
    # Open the logo image
    logo = Image.open(logo).convert('RGBA')
    
    # Calculate the size of the QR code
    qr_width, qr_height = qr_img.size
    
    # Size the logo to be 1/4 of the QR code
    logo_size = int(min(qr_width, qr_height) / 4)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    
    # Calculate the position to place the logo (center)
    pos_x = (qr_width - logo_size) // 2
    pos_y = (qr_height - logo_size) // 2
    
    # Convert QR to RGBA if it's not already
    if qr_img.mode != 'RGBA':
        qr_img = qr_img.convert('RGBA')
    
    # Create a new image with the same size as the QR code
    qr_with_logo = Image.new('RGBA', qr_img.size, (0, 0, 0, 0))
    
    # Paste the QR code onto the new image
    qr_with_logo.paste(qr_img, (0, 0))
    
    # Paste the logo onto the new image
    qr_with_logo.paste(logo, (pos_x, pos_y), logo)
    
    return qr_with_logo

# Function to get download link
def get_download_link(img, file_format, filename):
    buffered = io.BytesIO()
    
    if file_format.lower() == 'png':
        img.save(buffered, format="PNG")
    else:  # JPG
        # Convert RGBA to RGB for JPG (JPG doesn't support transparency)
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = bg
        img.save(buffered, format="JPEG", quality=90)
    
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    href = f'<a href="data:image/{file_format.lower()};base64,{img_str}" download="{filename}.{file_format.lower()}" class="download-button">Download {file_format.upper()}</a>'
    return href

# Main app layout
st.markdown('<div class="retro-card">', unsafe_allow_html=True)
st.subheader("Generate Your Custom QR Code")

# Input for QR code content
qr_data = st.text_area("Enter text or URL for your QR code", "https://example.com")

# QR Code customization options
col1, col2 = st.columns(2)

with col1:
    st.markdown("### QR Code Settings")
    box_size = st.slider("QR Code Size", min_value=5, max_value=20, value=10)
    border = st.slider("Border Size", min_value=1, max_value=5, value=2)
    
    # Color pickers
    fill_color = st.color_picker("QR Code Color", "#000000")
    back_color = st.color_picker("Background Color", "#FFFFFF")
    
    # Option for transparent background
    transparent_bg = st.checkbox("Transparent Background (PNG only)")

with col2:
    st.markdown("### Logo Settings")
    add_logo = st.checkbox("Add Logo to QR Code")
    logo_file = None
    
    if add_logo:
        logo_file = st.file_uploader("Upload Logo (PNG or JPG recommended)", type=["png", "jpg", "jpeg"])
        st.info("For best results, use a logo with a transparent background.")
    
    st.markdown("### Download Options")
    file_format = st.radio("File Format", ["PNG", "JPG"])
    custom_filename = st.text_input("Filename (optional)", f"AkhandQR_{datetime.now().strftime('%Y%m%d')}")

st.markdown('</div>', unsafe_allow_html=True)

# Generate button
st.markdown('<div class="retro-card glow-effect">', unsafe_allow_html=True)
generate_btn = st.button("✨ Generate QR Code ✨", key="generate_btn")
st.markdown('</div>', unsafe_allow_html=True)

# Generate and display QR code
if generate_btn and qr_data:
    st.markdown('<div class="retro-card qr-display">', unsafe_allow_html=True)
    
    # Generate the QR code
    qr_img = generate_qr_code(
        qr_data, 
        box_size, 
        border, 
        fill_color,
        "rgba(0,0,0,0)" if transparent_bg and file_format.lower() == "png" else back_color
    )
    
    # Add logo if requested
    if add_logo and logo_file is not None:
        qr_img = add_logo_to_qr(qr_img, logo_file)
    
    # Convert the PIL image to a format streamlit can use
    img_array = np.array(qr_img)
    st.image(img_array, caption="Your Generated QR Code", use_container_width=True)
    
    # Provide download link
    filename = custom_filename if custom_filename else f"AkhandQR_{datetime.now().strftime('%Y%m%d')}"
    st.markdown(get_download_link(qr_img, file_format, filename), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display usage instructions
    st.markdown('<div class="retro-card">', unsafe_allow_html=True)
    st.markdown("### Usage Tips")
    st.info("""
    - **Test your QR code** with a QR code scanner to ensure it works properly, especially when adding a logo.
    - **Keep your data short** for better scanning reliability.
    - **Choose contrasting colors** for better scan reliability.
    - If using a **logo**, ensure it doesn't cover too much of the QR code pattern.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="retro-card">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-top: 20px; opacity: 0.7;">
    <p>Akhand QR Generate © 2025 | A modern QR code generator with retro-futuristic style | Shuvo_WebDev</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
