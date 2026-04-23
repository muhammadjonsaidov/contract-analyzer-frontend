import streamlit as st

def apply_dark_luxury_theme():
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }

        /* App Background */
        .stApp {
            background: linear-gradient(135deg, #0a0b10 0%, #13161f 100%);
            color: #e2e8f0;
        }

        /* Titles and Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #f8fafc !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em;
        }

        /* Glassmorphism Metric Cards */
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.4);
        }

        /* Metric Values (e.g. 85 / 100) */
        div[data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* File Uploader Customization */
        section[data-testid="stFileUploader"] {
            background: rgba(255, 255, 255, 0.02);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        section[data-testid="stFileUploader"]:hover {
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.05);
        }

        /* Custom Tabs */
        button[data-baseweb="tab"] {
            background: transparent;
            border: none;
            color: #94a3b8 !important;
            font-weight: 500;
            padding: 1rem 2rem;
            border-bottom: 2px solid transparent !important;
            transition: all 0.3s ease;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #f8fafc !important;
            border-bottom: 2px solid #38bdf8 !important;
            background: rgba(56, 189, 248, 0.05);
            border-radius: 8px 8px 0 0;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4);
            color: white;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1px;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 8px;
            font-weight: 500;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* Chat Messages */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        /* Sticky Left Column for Preview */
        [data-testid="column"]:nth-child(1) {
            position: sticky;
            top: 2rem;
            align-self: start;
        }
    </style>
    """, unsafe_allow_html=True)
