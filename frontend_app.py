import streamlit as st
import backend_ai as backend
import auth
import os

# --- 1. PAGE CONFIG & APPLE-STYLE CSS ---
st.set_page_config(
    page_title="ResumeAI",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed sidebar for cleaner look
)

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

# Initialize DB
auth.init_db()

if "agent" not in st.session_state:
    if not os.environ.get("OPENROUTER_API_KEY"):
        # We don't stop here to allow landing page to load even if key is missing (user might fix it later)
        pass
    else:
        st.session_state.agent = backend.ResumeAgent()

if "resume_data" not in st.session_state:
    st.session_state.resume_data = {
        "full_name": "", "contact": "", "skills": {}, "education": "", "jobs": []
    }

# Inject Apple-inspired CSS
st.markdown("""
<style>
    /* 1. Global Reset */
    .stApp {
        background-color: #f5f5f7;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Selection Color */
    ::selection {
        background: #0071e3; /* Apple Blue */
        color: white;
    }
    
    /* 2. Aligned Icon Headers */
    .icon-header {
        display: flex;
        align-items: center;
        gap: 8px; /* Space between icon and text */
        font-weight: 600;
        font-size: 1.1rem;
        color: #1d1d1f;
        margin-bottom: 8px; /* Tight spacing to input */
    }
    
    .icon-header span {
        font-size: 1.3rem; /* Slightly larger icon */
        line-height: 1;
    }

    /* 3. Hero Typography */
    .hero-kicker {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #86868b;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: left; /* Changed to left */
        line-height: 1.1;
        margin-bottom: 1rem;
        background: -webkit-linear-gradient(90deg, #1d1d1f 0%, #434344 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        text-align: left; /* Changed to left */
        color: #86868b;
        font-weight: 400;
        margin-bottom: 2rem;
        max-width: 90%;
    }

    /* Upload Box Styling */
    .upload-container {
        border: 2px dashed #a1a1a6;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.5);
        transition: all 0.3s ease;
        margin-bottom: 2rem;
    }
    .upload-container:hover {
        border-color: #0071e3;
        background: rgba(255,255,255,0.8);
    }

    /* Mock Laptop UI */
    .laptop-container {
        position: relative;
        width: 100%;
        padding-top: 60%; /* Aspect ratio */
        background: #1d1d1f;
        border-radius: 12px 12px 0 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin-top: 20px;
        border: 1px solid #424245;
    }
    .laptop-screen {
        position: absolute;
        top: 4%;
        left: 4%;
        right: 4%;
        bottom: 4%;
        background: #f5f5f7;
        overflow: hidden;
        border-radius: 4px;
    }
    .laptop-base {
        height: 12px;
        background: #424245;
        border-radius: 0 0 12px 12px;
        margin-bottom: 20px;
    }
    
    /* Mock UI Elements */
    .mock-header { height: 40px; background: #fff; border-bottom: 1px solid #e5e5e5; display: flex; align-items: center; padding: 0 15px; }
    .mock-dot { width: 8px; height: 8px; border-radius: 50%; background: #ff5f57; margin-right: 6px; }
    .mock-dot.yellow { background: #febc2e; }
    .mock-dot.green { background: #28c840; }
    .mock-content { padding: 20px; display: grid; grid-template-columns: 1fr 2fr; gap: 15px; }
    .mock-sidebar { background: #fff; height: 150px; border-radius: 8px; }
    .mock-main { background: #fff; height: 150px; border-radius: 8px; }

    /* Trust Badge */
    .trust-badge {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.9rem;
        color: #1d1d1f;
        margin-top: 20px;
        font-weight: 500;
    }
    .stars { color: #00b67a; }

    /* 4. Glassmorphism Cards (Inputs) */
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    
    /* 5. Input Fields Styling - Apple Aesthetic */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        padding: 12px 15px !important;
        font-size: 1rem !important;
        color: #1d1d1f !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0071e3 !important;
        box-shadow: 0 0 0 4px rgba(0,113,227,0.15) !important;
        background-color: #ffffff !important;
    }
    
    /* 6. Buttons (Pill Shaped & Greyish Transparent) */
    .stButton > button {
        background-color: rgba(0, 0, 0, 0.05);
        color: #1d1d1f;
        border-radius: 980px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background-color: rgba(0, 0, 0, 0.1);
        border-color: rgba(0, 0, 0, 0.2);
        color: #000000;
    }

    /* Primary Button (Simulated via specific text match or just overriding all for login) */
    /* We will use a specific container class for login buttons if needed, 
       but for now, let's make the "Sign In" button distinctive if we can. 
       Actually, Streamlit allows type="primary". */
    button[kind="primary"] {
        background-color: #0071e3 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3) !important;
    }
    button[kind="primary"]:hover {
        background-color: #0077ed !important;
        box-shadow: 0 6px 16px rgba(0, 113, 227, 0.4) !important;
        transform: scale(1.02) !important;
    }

    /* 11. Auth Card Container */
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.4);
        text-align: center;
    }
    .auth-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #1d1d1f;
    }
    .auth-sub {
        font-size: 1rem;
        color: #86868b;
        margin-bottom: 2rem;
    }
    /* 12. Float Animation for Logo */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    /* 13. Apple-Style Mesh Background */
    .mesh-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        background-color: #f5f5f7;
        background-image: 
            radial-gradient(at 0% 0%, rgba(173, 216, 230, 0.4) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(220, 220, 255, 0.4) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(200, 240, 220, 0.3) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(240, 230, 250, 0.4) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(255, 255, 255, 0.8) 0px, transparent 50%);
        filter: blur(80px);
        animation: meshMove 20s ease-in-out infinite alternate;
    }

    @keyframes meshMove {
        0% { transform: scale(1); }
        100% { transform: scale(1.1); }
    }

    /* 7. Hide Streamlit Bloat */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom File Uploader Styling (Apple Blue) */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #f0f8ff; /* Light blue background */
        border: 2px dashed #0071e3; /* Apple Blue border */
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        background-color: #e8f2ff; /* Slightly darker on hover */
        border-color: #005bb5;
    }
    [data-testid="stFileUploaderDropzone"] svg {
        fill: #0071e3; /* Apple Blue Icon */
    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #1d1d1f;
    }
    [data-testid="stFileUploaderDropzone"] small {
        color: #86868b;
    }
    [data-testid="stBaseButton-secondary"] {
        background-color: white;
        color: #0071e3;
        border: 1px solid #0071e3;
        border-radius: 8px;
    }
    [data-testid="stBaseButton-secondary"]:hover {
        background-color: #0071e3;
        color: white;
        border-color: #0071e3;
    }
    [data-testid="stBaseButton-secondary"]:active,
    [data-testid="stBaseButton-secondary"]:focus,
    [data-testid="stBaseButton-secondary"]:focus:not(:active) {
        background-color: #005bb5 !important;
        color: white !important;
        border-color: #005bb5 !important;
        box-shadow: none !important;
    }

    /* 8. Fix Top Bar Alignment */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    /* 9. Landing Page Tiles - Responsive Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        padding: 20px;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        box-sizing: border-box;
    }
    
    .feature-card {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        height: 100%;
        min-height: 200px;
    }
    .feature-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 10px;
    }
    .feature-desc {
        font-size: 1rem;
        color: #86868b;
        line-height: 1.5;
    }

    /* Responsive Breakpoints */
    @media (max-width: 1024px) {
        .feature-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 600px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 2.5rem !important;
        }
        .hero-subtitle {
            font-size: 1rem !important;
        }
        .feature-card {
            padding: 20px;
        }
    }
    
    /* Center the Get Started button */
    .get-started-container {
        display: flex;
        justify-content: center;
        margin-top: 40px;
        margin-bottom: 60px;
    }
    
    /* Auth Form Styling */
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    /* 10. Loading Morph Transition - Optimized for Smoothness */
    @keyframes fadeOut {
        0% { opacity: 1; }
        70% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }

    @keyframes morphLogo {
        0% { 
            transform: scale(1); 
            opacity: 1; 
        }
        25% { 
            transform: scale(0.85); 
            opacity: 1; 
        }
        100% { 
            transform: scale(50); 
            opacity: 0; 
        }
    }

    .loader-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #f5f5f7;
        z-index: 999999;
        display: flex;
        justify-content: center;
        align-items: center;
        /* Performance: animate opacity only, avoid heavy layout thrashing */
        animation: fadeOut 1.5s cubic-bezier(0.65, 0, 0.35, 1) forwards;
        will-change: opacity;
        pointer-events: none;
    }

    .loader-content {
        font-size: 5rem;
        /* Performance: promote to own layer */
        will-change: transform, opacity;
        animation: morphLogo 1.5s cubic-bezier(0.65, 0, 0.35, 1) forwards;
    }
    /* 14. Feature Sections */
    .section-container {
        padding: 80px 0;
        border-top: 1px solid #d1d1d6;
    }
    .section-white {
        background-color: #ffffff;
    }
    .section-grey {
        background-color: #f5f5f7;
    }
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1d1d1f;
        margin-bottom: 20px;
        line-height: 1.1;
    }
    .section-text {
        font-size: 1.1rem;
        color: #86868b;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    /* Mock Visuals for New Sections */
    .mock-card-stack {
        position: relative;
        height: 300px;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .profile-card {
        width: 180px;
        height: 220px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: absolute;
        border: 1px solid rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        transition: transform 0.3s ease;
    }
    .profile-card:nth-child(1) { transform: translateX(-60px) rotate(-10deg) scale(0.9); z-index: 1; }
    .profile-card:nth-child(2) { transform: translateX(60px) rotate(10deg) scale(0.9); z-index: 1; }
    .profile-card:nth-child(3) { transform: translateY(-20px) scale(1); z-index: 2; }
    
    .suggestion-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-left: 4px solid #0071e3;
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .suggestion-box:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .suggestion-box.bad { border-left-color: #ff3b30; opacity: 0.7; }
    
    .chart-container {
        display: flex;
        align-items: flex-end;
        height: 200px;
        gap: 20px;
        justify-content: center;
        padding: 20px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .chart-bar {
        width: 40px;
        background: #e5e5ea;
        border-radius: 8px 8px 0 0;
        transition: height 1s ease;
    }
    .chart-bar.active { background: #0071e3; }
    
    .checklist-item {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    .checklist-item:hover {
        transform: scale(1.02);
        background: #0071e3;
        border-color: #0071e3;
        box-shadow: 0 10px 30px rgba(0,113,227,0.3);
    }
    .checklist-item:hover .checklist-title {
        color: white !important;
    }
    .checklist-item:hover .checklist-desc {
        color: rgba(255,255,255,0.9) !important;
    }
    .checklist-item:hover .check-circle {
        background: white;
        color: #0071e3;
    }
    .check-circle {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #34c759;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    /* Login/Register Buttons Styling */
    div.stButton > button {
        background-color: #0071e3;
        color: white;
        border: none;
        border-radius: 980px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        background-color: #0077ed;
        box-shadow: 0 8px 20px rgba(0, 113, 227, 0.4);
        color: white;
        border: none;
    }

</style>

<!-- Animated Background -->
<div class="mesh-background"></div>
""", unsafe_allow_html=True)

# Loading Overlay HTML (Only show once)
if "loader_shown" not in st.session_state:
    st.markdown("""
    <div class="loader-overlay">
        <div class="loader-content">🍏</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.loader_shown = True

def landing_page():
    # --- Custom Fixed Header (Matches Resume Worded Image) ---
    st.markdown("""
<style>
    /* Hide default Streamlit header decoration */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Main Header Bar */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background-color: rgba(44, 44, 46, 0.85); /* Semi-transparent Grey */
        backdrop-filter: blur(12px); /* Glassmorphism effect */
        -webkit-backdrop-filter: blur(12px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        z-index: 100000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Logo Area */
    .header-left {
        display: flex;
        align-items: center;
        gap: 40px;
    }
    .header-logo {
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        cursor: pointer;
    }
    
    /* Navigation */
    .header-nav {
        display: flex;
        align-items: center;
        gap: 20px;
        height: 100%;
    }
    
    /* Dropdown Container */
    .nav-item-dropdown {
        position: relative;
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
        font-weight: 500;
        cursor: pointer;
        height: 100%;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .nav-item-dropdown:hover {
        color: white;
    }
    
    /* Dropdown Menu Content */
    .dropdown-menu {
        position: absolute;
        top: 70px;
        left: -20px;
        width: 320px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        padding: 10px 0;
        display: none; /* Hidden by default */
        flex-direction: column;
        z-index: 100001;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Show on Hover */
    .nav-item-dropdown:hover .dropdown-menu {
        display: flex;
        animation: fadeIn 0.2s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Dropdown Items */
    .dropdown-item {
        display: flex;
        align-items: flex-start;
        padding: 12px 20px;
        text-decoration: none;
        transition: transform 0.2s ease, background 0.1s ease;
        gap: 15px;
        border-radius: 6px;
    }
    .dropdown-item:hover {
        background-color: #0071e3;
        transform: scale(1.02);
    }
    .dropdown-item:hover .dd-title {
        color: white;
    }
    .dropdown-item:hover .dd-desc {
        color: rgba(255,255,255,0.9);
    }
    .dropdown-item:hover .dd-icon {
        background: white;
    }

    .dd-icon {
        font-size: 1.4rem;
        background: #e8f2ff;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-shrink: 0;
    }
    
    .dd-text {
        display: flex;
        flex-direction: column;
    }
    .dd-title {
        font-weight: 700;
        font-size: 0.85rem;
        color: #0071e3;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dd-desc {
        font-size: 0.8rem;
        color: #6e6e73;
        line-height: 1.3;
    }
    
    /* Header Buttons */
    .header-btn-link {
        color: white;
        font-size: 0.95rem;
        font-weight: 500;
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 6px;
        transition: background 0.2s;
    }
    .header-btn-link:hover {
        background: rgba(255,255,255,0.1);
    }
    
    .header-cta {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0071e3 0%, #4facfe 100%);
        color: white !important;
        padding: 10px 24px;
        border-radius: 980px;
        font-weight: 600;
        font-size: 0.95rem;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(0,113,227,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        line-height: 1.2;
        margin: 0;
        white-space: nowrap;
    }
    .header-cta:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,113,227,0.4);
        color: white !important;
    }
    
    /* Adjust page content to prevent overlap */
    .block-container {
        padding-top: 80px !important;
    }
</style>

<div class="custom-header">
<div class="header-left">
<div class="header-logo">RESUME AI</div>
</div>

<div class="header-nav">
<div class="nav-item-dropdown">
Products ▾
<div class="dropdown-menu">
<div class="dropdown-item">
<div class="dd-icon">📄</div>
<div class="dd-text">
<div class="dd-title">Score My Resume</div>
<div class="dd-desc">Get a free expert resume review, instantly</div>
</div>
</div>
<div class="dropdown-item">
<div class="dd-icon">🎯</div>
<div class="dd-text">
<div class="dd-title">Targeted Resume</div>
<div class="dd-desc">Tailor your resume to a job description in seconds</div>
</div>
</div>
<div class="dropdown-item">
<div class="dd-icon">👔</div>
<div class="dd-text">
<div class="dd-title">LinkedIn Review</div>
<div class="dd-desc">Get personalized feedback on your LinkedIn profile</div>
</div>
</div>
<div class="dropdown-item">
<div class="dd-icon">✍️</div>
<div class="dd-text">
<div class="dd-title">Cover Letter Generator</div>
<div class="dd-desc">Generate personalized cover letters using AI</div>
</div>
</div>
</div>
</div>
<a class="header-cta">Get a free resume review</a>
</div>
</div>
""", unsafe_allow_html=True)

    # Spacer for fixed header
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # Auth logic wrapper (since we removed the old buttons, we need to add them back or hook them up)
    # To make the header buttons functional, we can't easily click the HTML button to run Python.
    # So we'll put the Python buttons below the header in a hidden way or just use the main page buttons.
    # For this task, the user emphasized the visual "header" and "dropdown".
    # We will keep the Login/Register flow available via the main hero button for now.
    
    # We also need to add back the "ResumeAI" hero title if it was removed, or adjust the layout.
    # The previous layout had "ResumeAI" centered.
    # We'll add a smaller spacer and then the Hero section.

    st.markdown("<br>", unsafe_allow_html=True)

    # Split Hero Section
    c_hero_left, c_hero_right = st.columns([1.2, 1], gap="large")
    
    with c_hero_left:
        st.markdown('<div class="hero-kicker">SCORE MY RESUME - FREE RESUME CHECKER</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Get expert feedback on your resume, instantly</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Our free AI-powered resume checker scores your resume on key criteria recruiters and hiring managers look for. Get actionable steps to revamp your resume and land more interviews.</div>', unsafe_allow_html=True)
        
        # Upload Box (Wrapper removed)
        uploaded = st.file_uploader("Drop your resume here or choose a file.", type=['pdf', 'docx'], label_visibility="collapsed")
        
        if uploaded:
            st.session_state.pending_upload = uploaded
            st.success("File ready! Sign in to analyze.")
            if st.button("Analyze My Resume ->", type="primary"):
                if st.session_state.logged_in:
                    st.session_state.page = "app"
                else:
                    st.session_state.page = "login"
                st.rerun()

        # Social Proof
        st.markdown("""
        <div class="trust-badge">
            <div>Excellent</div>
            <div class="stars">★★★★★</div>
            <div style="color: #86868b; font-weight: 400;">Rated 4.9 out of 5 based on 1000+ reviews by <span style="font-weight:600">users</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c_hero_right:
        # Mock Laptop Visual
        st.markdown("""
        <div class="laptop-container">
            <div class="laptop-screen">
                <div class="mock-header">
                    <div class="mock-dot"></div>
                    <div class="mock-dot yellow"></div>
                    <div class="mock-dot green"></div>
                </div>
                <div class="mock-content">
                    <div class="mock-sidebar" style="background: #f0f0f5; padding: 10px;">
                        <div style="height: 8px; width: 60%; background: #d1d1d6; border-radius: 4px; margin-bottom: 8px;"></div>
                        <div style="height: 8px; width: 80%; background: #d1d1d6; border-radius: 4px; margin-bottom: 8px;"></div>
                        <div style="height: 8px; width: 50%; background: #d1d1d6; border-radius: 4px;"></div>
                    </div>
                    <div class="mock-main" style="padding: 10px;">
                         <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
                            <div style="text-align:center;">
                                <div style="font-size: 24px; font-weight:bold; color:#0071e3;">65</div>
                                <div style="font-size: 8px; color:#86868b;">OVERALL</div>
                            </div>
                            <div style="text-align:center;">
                                <div style="font-size: 24px; font-weight:bold; color:#0071e3;">90</div>
                                <div style="font-size: 8px; color:#86868b;">IMPACT</div>
                            </div>
                            <div style="text-align:center;">
                                <div style="font-size: 24px; font-weight:bold; color:#0071e3;">85</div>
                                <div style="font-size: 8px; color:#86868b;">BREVITY</div>
                            </div>
                         </div>
                         <div style="height: 8px; width: 100%; background: #f0f0f5; border-radius: 4px; margin-bottom: 10px;"></div>
                         <div style="height: 8px; width: 90%; background: #f0f0f5; border-radius: 4px; margin-bottom: 10px;"></div>
                         <div style="height: 8px; width: 95%; background: #f0f0f5; border-radius: 4px; margin-bottom: 10px;"></div>
                         <div style="height: 40px; width: 100%; background: #e8f2ff; border-radius: 6px; margin-top: 20px; border: 1px dashed #0071e3;"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="laptop-base"></div>
        """, unsafe_allow_html=True)
    
    # Spacing
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Feature Tiles Grid
    features = [
        {
            "icon": "📄",
            "title": "Smart Parsing",
            "desc": "Upload your existing PDF resume and let our AI extract your details instantly."
        },
        {
            "icon": "🎯",
            "title": "Tailored Content",
            "desc": "Paste a Job Description and get a resume perfectly matched to the role."
        },
        {
            "icon": "⚡",
            "title": "ATS Optimized",
            "desc": "Ensure your resume passes Applicant Tracking Systems with high scores."
        },
        {
            "icon": "✍️",
            "title": "Cover Letters",
            "desc": "Generate compelling cover letters that tell your unique professional story."
        }
    ]

    # Render features using Responsive Grid
    features_html = '<div class="feature-grid">'
    for feature in features:
        features_html += f"""<div class="feature-card"><div class="feature-icon">{feature['icon']}</div><div class="feature-title">{feature['title']}</div><div class="feature-desc">{feature['desc']}</div></div>"""
    features_html += '</div>'
    
    st.markdown(features_html, unsafe_allow_html=True)
    
    # --- New Feature Sections (Alternating Layout) ---
    
    # Section 1: Designed by Experts (Text Left, Visual Right)
    st.markdown('<div style="margin: 80px 0; border-top: 1px solid #d1d1d6;"></div>', unsafe_allow_html=True)
    c1_l, c1_r = st.columns([1, 1], gap="large")
    with c1_l:
        st.markdown('<div class="section-title">Designed by hiring managers</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-text">Our feedback engine is curated by recruiters from top tech companies. We know what gets a resume tossed and what gets it read. Stop guessing and start applying with confidence.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-kicker">CURATED EXPERTISE</div>', unsafe_allow_html=True)
    with c1_r:
        st.markdown("""
        <div class="mock-card-stack">
            <div class="profile-card">
                <div style="width: 50px; height: 50px; border-radius: 50%; background: #e5e5ea; margin-bottom: 15px;"></div>
                <div style="width: 80%; height: 10px; background: #f0f0f5; margin-bottom: 8px; border-radius: 4px;"></div>
                <div style="width: 60%; height: 10px; background: #f0f0f5; border-radius: 4px;"></div>
            </div>
            <div class="profile-card">
                <div style="width: 50px; height: 50px; border-radius: 50%; background: #d1d1d6; margin-bottom: 15px;"></div>
                <div style="width: 80%; height: 10px; background: #f0f0f5; margin-bottom: 8px; border-radius: 4px;"></div>
                <div style="width: 60%; height: 10px; background: #f0f0f5; border-radius: 4px;"></div>
            </div>
            <div class="profile-card">
                <div style="width: 50px; height: 50px; border-radius: 50%; background: #0071e3; margin-bottom: 15px;"></div>
                <div style="width: 80%; height: 10px; background: #f0f0f5; margin-bottom: 8px; border-radius: 4px;"></div>
                <div style="width: 60%; height: 10px; background: #f0f0f5; border-radius: 4px;"></div>
                <div style="margin-top: 20px; color: #0071e3; font-weight: bold; font-size: 0.8rem;">Recruiter Approved</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Section 2: Smart Suggestions (Visual Left, Text Right)
    st.markdown('<div style="margin: 80px 0; border-top: 1px solid #d1d1d6;"></div>', unsafe_allow_html=True)
    c2_l, c2_r = st.columns([1, 1], gap="large")
    with c2_l:
         st.markdown("""
         <div style="padding: 20px;">
            <div class="suggestion-box bad">
                <div style="font-weight: 600; color: #ff3b30; margin-bottom: 5px;">BEFORE</div>
                <div style="color: #1d1d1f; font-size: 0.9rem;">Managed a team of sales people and increased revenue.</div>
            </div>
            <div style="text-align: center; font-size: 2rem; color: #86868b; margin: 10px 0;">↓</div>
            <div class="suggestion-box">
                <div style="font-weight: 600; color: #0071e3; margin-bottom: 5px;">AFTER (AI Suggested)</div>
                <div style="color: #1d1d1f; font-size: 0.9rem;">Led a team of <strong>15 sales representatives</strong>, driving a <strong>20% increase in annual revenue</strong> through strategic mentorship.</div>
            </div>
         </div>
         """, unsafe_allow_html=True)
    with c2_r:
        st.markdown('<div class="section-title">Smart resume suggestions</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-text">We don\'t just find errors; we suggest improvements. Turn weak bullet points into powerful impact statements that highlight your achievements with quantifiable metrics.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-kicker">INSTANT IMPROVEMENTS</div>', unsafe_allow_html=True)

    # Section 3: Detailed Scoring (Text Left, Visual Right)
    st.markdown('<div style="margin: 80px 0; border-top: 1px solid #d1d1d6;"></div>', unsafe_allow_html=True)
    c3_l, c3_r = st.columns([1, 1], gap="large")
    with c3_l:
        st.markdown('<div class="section-title">Improve your resume\'s score</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-text">Get a comprehensive score based on Impact, Brevity, and Style. Watch your score rise as you fix issues and optimize your content for maximum readability.</div>', unsafe_allow_html=True)
        st.button("Get My Score Now", type="primary")
    with c3_r:
        st.markdown("""
        <div class="chart-container">
            <div class="chart-bar" style="height: 40%;"></div>
            <div class="chart-bar" style="height: 60%;"></div>
            <div class="chart-bar" style="height: 30%;"></div>
            <div class="chart-bar active" style="height: 90%;">
                <div style="text-align: center; color: white; padding-top: 5px; font-weight: bold;">92</div>
            </div>
            <div class="chart-bar" style="height: 50%;"></div>
        </div>
        """, unsafe_allow_html=True)

    # Section 4: What We Look For (Visual Left, Text Right)
    st.markdown('<div style="margin: 80px 0; border-top: 1px solid #d1d1d6;"></div>', unsafe_allow_html=True)
    c4_l, c4_r = st.columns([1, 1], gap="large")
    with c4_l:
        st.markdown("""
        <div style="padding: 20px;">
            <div class="checklist-item">
                <div class="check-circle">✓</div>
                <div>
                    <div class="checklist-title" style="font-weight: 600; color: #1d1d1f;">ATS Compatibility Check</div>
                    <div class="checklist-desc" style="font-size: 0.9rem; color: #86868b; margin-top: 2px;">Ensure your resume is readable by automated screening tools.</div>
                </div>
            </div>
            <div class="checklist-item">
                <div class="check-circle">✓</div>
                <div>
                    <div class="checklist-title" style="font-weight: 600; color: #1d1d1f;">Action Verb Analysis</div>
                    <div class="checklist-desc" style="font-size: 0.9rem; color: #86868b; margin-top: 2px;">Use strong leadership verbs to describe your achievements.</div>
                </div>
            </div>
            <div class="checklist-item">
                <div class="check-circle">✓</div>
                <div>
                    <div class="checklist-title" style="font-weight: 600; color: #1d1d1f;">Quantifiable Metrics Scan</div>
                    <div class="checklist-desc" style="font-size: 0.9rem; color: #86868b; margin-top: 2px;">Highlight your impact with numbers, percentages, and results.</div>
                </div>
            </div>
            <div class="checklist-item">
                <div class="check-circle">✓</div>
                <div>
                    <div class="checklist-title" style="font-weight: 600; color: #1d1d1f;">Formatting Consistency</div>
                    <div class="checklist-desc" style="font-size: 0.9rem; color: #86868b; margin-top: 2px;">Verify fonts, margins, and bullet points are professional and uniform.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c4_r:
        st.markdown('<div class="section-title">What our checker looks for</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-text">Recruiters spend less than 6 seconds on a resume. We check for the exact criteria they use to filter candidates, ensuring you make a lasting first impression.</div>', unsafe_allow_html=True)

    # Section 5: Related Resources (Cards)
    st.markdown('<div style="margin: 80px 0; border-top: 1px solid #d1d1d6;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align: center;">Want more? Discover our related resources.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 20px; max-width: 800px; margin-left: auto; margin-right: auto;">
        <div class="suggestion-box" style="border-left-color: #5856d6;">
            <div style="font-weight: 600; color: #5856d6; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Resume Proofreading</div>
            <div style="color: #1d1d1f; font-size: 0.95rem; line-height: 1.5;">Find and fix your resume's mistakes. Before a hiring manager sees them. Upload your resume and get instant feedback on mistakes you might be overlooking, and where it falls short (compared to other resumes in your industry).</div>
        </div>
        <div class="suggestion-box" style="border-left-color: #5856d6;">
            <div style="font-weight: 600; color: #5856d6; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Resume Keyword Scanner</div>
            <div style="color: #1d1d1f; font-size: 0.95rem; line-height: 1.5;">Optimize your resume's keywords instantly. This tool will scan your resume and a job description. Then, it will tell you what which keywords your resume is missing.</div>
        </div>
        <div class="suggestion-box" style="border-left-color: #5856d6;">
            <div style="font-weight: 600; color: #5856d6; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Google Docs Resume Templates</div>
            <div style="color: #1d1d1f; font-size: 0.95rem; line-height: 1.5;">Need a resume template that's recruiter-approved and passes automated hiring systems? Choose one from 300+ free Google Docs templates we've curated that you can edit online.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer Section
    st.markdown('<div style="margin: 80px 0; border-top: 1px solid #d1d1d6;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
        .footer-container {
            background-color: #0071e3;
            color: white;
            padding: 60px 40px;
            border-radius: 24px;
            margin-bottom: 40px;
        }
        .footer-col-title {
            font-weight: 600;
            margin-bottom: 20px;
            color: white;
            font-size: 1.1rem;
        }
        .footer-link {
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 12px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: color 0.2s ease;
            display: block;
        }
        .footer-link:hover {
            color: white;
            text-decoration: underline;
        }
    </style>
    <div class="footer-container">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px;">
            <div>
                <div class="footer-col-title">Improve your resume</div>
                <div class="footer-link">Score my resume</div>
                <div class="footer-link">Targeted resume</div>
                <div class="footer-link">Write your resume</div>
            </div>
            <div>
                <div class="footer-col-title">Optimize your career</div>
                <div class="footer-link">LinkedIn review</div>
                <div class="footer-link">Optimize your LinkedIn profile</div>
                <div class="footer-link">LinkedIn headline samples</div>
                <div class="footer-link">Networking emails</div>
                <div class="footer-link">AI cover letter generator</div>
            </div>
            <div>
                <div class="footer-col-title">Get to know us</div>
                <div class="footer-link">Help center</div>
                <div class="footer-link">Get in touch</div>
                <div class="footer-link">For businesses</div>
                <div class="footer-link">For resume writers</div>
                <div class="footer-link">Affiliates</div>
            </div>
             <div>
                <div class="footer-col-title">Resources</div>
                <div class="footer-link">ATS resume templates</div>
                <div class="footer-link">ATS resume test</div>
                <div class="footer-link">Resume optimizer</div>
                <div class="footer-link">Resume examples</div>
            </div>
        </div>
        <div style="margin-top: 60px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.2); text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.8rem;">
            &copy; 2026 ResumeAI. All rights reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br><br>", unsafe_allow_html=True)

def login_page():
    # Back button
    c_back, _ = st.columns([1, 6])
    with c_back:
        if st.button("← Back"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centered Auth Card
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        # Apple-style Header
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 10px; animation: float 6s ease-in-out infinite;">🍏</div>
                <div class="auth-header">Sign In</div>
                <div class="auth-sub">Welcome back to ResumeAI</div>
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if auth.login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 30px; margin-bottom: 10px; color: #86868b; font-size: 0.9rem;">
                New to ResumeAI?
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Account", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

def register_page():
    # Back button
    c_back, _ = st.columns([1, 6])
    with c_back:
        if st.button("← Back"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 10px; animation: float 6s ease-in-out infinite;">🍏</div>
                <div class="auth-header">Create Account</div>
                <div class="auth-sub">Join the future of career building</div>
            </div>
        """, unsafe_allow_html=True)

        new_user = st.text_input("Choose Username", placeholder="Username", label_visibility="collapsed")
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        new_pass = st.text_input("Choose Password", type="password", placeholder="Password", label_visibility="collapsed")
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Create Account", type="primary", use_container_width=True):
            if new_pass != confirm_pass:
                st.error("Passwords do not match")
            elif not new_user or not new_pass:
                st.error("Please fill all fields")
            else:
                if auth.register_user(new_user, new_pass):
                    st.success("Account created! Please log in.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Username already exists")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 30px; margin-bottom: 10px; color: #86868b; font-size: 0.9rem;">
                Already have an account?
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

def main_app():
    # Check if logged in
    if not st.session_state.logged_in:
        st.warning("Please log in to access the application.")
        st.session_state.page = "login"
        st.rerun()

    # Check API Key
    if "agent" not in st.session_state or not st.session_state.agent:
        if not os.environ.get("OPENROUTER_API_KEY"):
            st.error("⚠️ OPENROUTER_API_KEY not found! Please check your .env file.")
            st.stop()
        else:
            st.session_state.agent = backend.ResumeAgent()

    # --- Header with Logout ---
    c_back, c_title, c_user = st.columns([1, 6, 2])
    with c_back:
        if st.button("← Home"):
            st.session_state.page = "landing"
            st.rerun()
    with c_user:
        st.write(f"👤 {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.page = "landing"
            st.rerun()

    # --- 4. CONTROL DASHBOARD ---
    # Apple uses centered layouts. We'll use columns to center the inputs.
    _, col_main, _ = st.columns([1, 8, 1])
    
    with col_main:
        # Top Control Bar in a "Glass" Container
        with st.container():
            c1, c2, c3 = st.columns([1.5, 2, 1])
            with c1:
                st.markdown("**Target Role**")
                target_role = st.text_input("role", value="Software Engineer", label_visibility="collapsed", placeholder="e.g. Product Manager")
            with c2:
                st.markdown("**Job Description Context**")
                jd_text = st.text_area("jd", height=100, label_visibility="collapsed", placeholder="Paste the JD here for keyword matching...")
            with c3:
                st.markdown("**Auto-Fill**")
                uploaded_file = st.file_uploader("upload", type=["pdf"], label_visibility="collapsed")
    
    # Check for pending upload from landing page
    if "pending_upload" in st.session_state:
        uploaded_file = st.session_state.pending_upload
        del st.session_state.pending_upload
        
    # Handle Upload
    if uploaded_file is not None and "file_processed" not in st.session_state:
        with st.status("Reading document...", expanded=True) as status:
            try:
                raw_text = backend.extract_text_from_pdf(uploaded_file)
                parsed_data = st.session_state.agent.parse_resume_text(raw_text)
                
                st.session_state.resume_data["full_name"] = parsed_data.full_name
                st.session_state.resume_data["contact"] = parsed_data.contact_info
                st.session_state.resume_data["skills"] = parsed_data.skills
                
                if parsed_data.education:
                    edu = parsed_data.education[0]
                    st.session_state.resume_data["education"] = f"{edu.get('school','')} | {edu.get('degree','')} | {edu.get('year','')}"
                st.session_state.resume_data["jobs"] = parsed_data.experience
                
                st.session_state.file_processed = True
                status.update(label="Complete", state="complete", expanded=False)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- 5. WORKSPACE (Tabs) ---
    tab_build, tab_ats, tab_write = st.tabs(["Builder", "ATS Checker", "Cover Letter"])
    
    # ==========================
    # TAB 1: BUILDER
    # ==========================
    with tab_build:
        c_side, c_body = st.columns([1, 3])
        
        # --- LEFT SIDEBAR (Profile) ---
        with c_side:
            st.markdown("### Profile")
            with st.expander("Basics", expanded=True):
                full_name = st.text_input("Name", value=st.session_state.resume_data["full_name"], placeholder="Your Name")
                contact = st.text_input("Contact", value=st.session_state.resume_data["contact"], placeholder="Email | Phone")
            
            with st.expander("Skills", expanded=True):
                skills_text = str(st.session_state.resume_data["skills"]) if st.session_state.resume_data["skills"] else "{}"
                skills_input = st.text_area("JSON List", value=skills_text, height=200)
                education_str = st.text_input("Education", value=st.session_state.resume_data["education"])
    
        # --- MAIN BODY (Experience) ---
        with c_body:
            c_head, c_btn = st.columns([3, 1])
            with c_head: 
                st.markdown("### Experience")
            with c_btn:
                if st.button("➕ New Position"):
                    st.session_state.resume_data["jobs"].insert(0, backend.ExperienceItem())
                    st.rerun()
    
            # Job Cards
            jobs_to_keep = []
            for i, job in enumerate(st.session_state.resume_data["jobs"]):
                title = f"{job.role} @ {job.company}" if job.role else f"Position {i+1}"
                with st.expander(title, expanded=True):
                    col1, col2 = st.columns(2)
                    job.role = col1.text_input("Role", value=job.role, key=f"r{i}", placeholder="Role Title")
                    job.company = col2.text_input("Company", value=job.company, key=f"c{i}", placeholder="Company Name")
                    
                    col3, col4 = st.columns(2)
                    job.duration = col3.text_input("Dates", value=job.duration, key=f"d{i}", placeholder="Dates")
                    job.location = col4.text_input("Location", value=job.location, key=f"l{i}", placeholder="City")
                    
                    job.tech_stack = st.text_input("Tech Stack", value=job.tech_stack, key=f"t{i}", placeholder="Tools used...")
                    job.summary_input = st.text_area("Tasks", value=job.summary_input, height=100, key=f"s{i}", placeholder="What did you do?")
                    
                    if not st.checkbox("Delete", key=f"del{i}"):
                        jobs_to_keep.append(job)
    
            if len(jobs_to_keep) != len(st.session_state.resume_data["jobs"]):
                st.session_state.resume_data["jobs"] = jobs_to_keep
                st.rerun()
    
            # --- GENERATION AREA ---
            st.markdown("---")
            c_tone, c_go = st.columns([2, 1])
            with c_tone:
                tone_sel = st.radio("Tone", ["Standard", "Humanized"], horizontal=True, label_visibility="collapsed")
            with c_go:
                gen_click = st.button("✨ Generate Resume", use_container_width=True)
    
            if gen_click:
                if not st.session_state.resume_data["jobs"]:
                    st.error("Add experience first.")
                else:
                    with st.status("Architecting Resume...", expanded=True) as s:
                        try:
                            # 1. AI Logic
                            enhanced_jobs = st.session_state.agent.rewrite_all_jobs(
                                st.session_state.resume_data["jobs"], 
                                target_role, 
                                jd_text, 
                                tone_sel
                            )
                            
                            # 2. Compile
                            try: final_skills = eval(skills_input)
                            except: final_skills = {"Skills": skills_input}
                            
                            resume_obj = backend.ResumeData(
                                full_name=full_name, contact_info=contact, 
                                education=[{"school": education_str, "degree": "", "year": ""}], 
                                skills=final_skills, experience=enhanced_jobs
                            )
                            
                            # 3. Render
                            fpath = backend.create_styled_resume(resume_obj)
                            s.update(label="Done", state="complete", expanded=False)
                            
                            # 4. Success UI
                            st.success("Ready for Download")
                            
                            c_dl, c_stat = st.columns(2)
                            with c_dl:
                                with open(fpath, "rb") as f:
                                    st.download_button("📥 Download .DOCX", f, file_name="Resume.docx", use_container_width=True)
                            
                            # 5. ATS Score
                            if jd_text:
                                with c_stat:
                                    with st.spinner("Analyzing..."):
                                        audit = st.session_state.agent.audit_resume(resume_obj, jd_text)
                                        st.metric("ATS Score", f"{audit.score}/100")
                                        with st.expander("Details"):
                                            for k in audit.missing_keywords: st.write(f"🔴 {k}")
                                            for t in audit.suggestions: st.caption(f"• {t}")
    
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    # ==========================
    # TAB 2: ATS CHECKER
    # ==========================
    with tab_ats:
        st.markdown("### ATS Score Checker")
        st.info("Upload your resume and compare it against the Job Description to get an ATS score.")
        
        col_ats_left, col_ats_right = st.columns([1, 1])
        
        with col_ats_left:
            ats_file = st.file_uploader("Upload Resume (PDF) to Check", type=["pdf"], key="ats_upload")
            
        with col_ats_right:
            st.markdown("**Job Description**")
            if jd_text:
                st.caption("Using JD from Control Dashboard")
                st.text_area("JD Preview", value=jd_text, height=150, disabled=True)
            else:
                st.warning("Please paste a Job Description in the Control Dashboard above.")

        if st.button("🔍 Analyze Score", use_container_width=True):
            if not jd_text:
                st.error("Job Description is required!")
            else:
                resume_obj_to_check = None
                
                # Determine source: Uploaded file OR Workspace
                if ats_file:
                    with st.spinner("Parsing uploaded resume..."):
                        try:
                            raw_text_ats = backend.extract_text_from_pdf(ats_file)
                            resume_obj_to_check = st.session_state.agent.parse_resume_text(raw_text_ats)
                        except Exception as e:
                            st.error(f"Error parsing PDF: {e}")
                else:
                    # Use workspace data
                    try:
                        try: final_skills = eval(skills_input)
                        except: final_skills = {"Skills": skills_input}
                        
                        resume_obj_to_check = backend.ResumeData(
                            full_name=full_name, contact_info=contact, 
                            education=[{"school": education_str, "degree": "", "year": ""}], 
                            skills=final_skills, experience=st.session_state.resume_data["jobs"]
                        )
                    except Exception as e:
                        st.error(f"Error reading workspace data: {e}")

                if resume_obj_to_check:
                    with st.spinner("Calculating ATS Score..."):
                        try:
                            audit = st.session_state.agent.audit_resume(resume_obj_to_check, jd_text)
                            
                            # Display Results
                            st.markdown("---")
                            c_score, c_details = st.columns([1, 2])
                            
                            with c_score:
                                st.metric("ATS Score", f"{audit.score}/100")
                                if audit.score >= 80:
                                    st.success("Excellent match!")
                                elif audit.score >= 50:
                                    st.warning("Good, but needs improvement.")
                                else:
                                    st.error("Low match. Optimize keywords.")
                                    
                            with c_details:
                                st.markdown("#### Missing Keywords")
                                if audit.missing_keywords:
                                    for k in audit.missing_keywords:
                                        st.write(f"🔴 {k}")
                                else:
                                    st.write("✅ No critical keywords missing!")
                                    
                                st.markdown("#### Suggestions")
                                for s in audit.suggestions:
                                    st.info(f"💡 {s}")
                                    
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")

    # ==========================
    # TAB 3: COVER LETTER
    # ==========================
    with tab_write:
        col_centered, _ = st.columns([1, 1]) # Left align
        with col_centered:
            st.markdown("### Cover Letter Writer")
            st.info("Generates a narrative connecting your history to the JD.")
            
            if st.button("📝 Draft Letter"):
                if not jd_text: st.warning("Paste a JD above first.")
                else:
                    with st.spinner("Writing..."):
                        try:
                            # Simple Compile
                            try: fs = eval(skills_input)
                            except: fs = {"Skills": skills_input}
                            res_sim = backend.ResumeData(
                                full_name=full_name, contact_info=contact,
                                education=[{"school": education_str}], skills=fs,
                                experience=st.session_state.resume_data["jobs"]
                            )
                            cl_text = st.session_state.agent.generate_cover_letter(res_sim, jd_text)
                            st.text_area("Draft", value=cl_text, height=400)
                            st.download_button("📥 Download", cl_text, "CoverLetter.txt")
                        except Exception as e: st.error(e)

# --- MAIN EXECUTION ---
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "app":
    main_app()
else:
    landing_page()
