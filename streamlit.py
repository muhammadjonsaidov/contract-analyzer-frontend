import streamlit as st
import json
import base64
from styles import apply_dark_luxury_theme
from config import GOOGLE_LOGIN_URL
from api_client import (
    upload_contract, ask_question, get_sessions, create_session, 
    delete_session, get_session_history, edit_chat_message, login, register
)
from components import (
    render_pdf_preview, render_dynamic_progress_bar, 
    render_info_card, render_metric_group
)

# Set page config
st.set_page_config(layout="wide", page_title="Enterprise Contract Analyzer", page_icon="⚖️")
apply_dark_luxury_theme()

# --- Helper for JWT Decoding ---
def decode_jwt(token):
    try:
        _, payload_b64, _ = token.split('.')
        # Add padding if needed
        payload_b64 += '=' * (-len(payload_b64) % 4)
        payload_json = base64.b64decode(payload_b64).decode('utf-8')
        return json.loads(payload_json)
    except Exception as e:
        st.error(f"Error decoding token: {e}")
        return None

# --- Handle OAuth2 Callback ---
if "token" in st.query_params:
    token = st.query_params["token"]
    payload = decode_jwt(token)
    if payload:
        st.session_state.jwt_token = token
        st.session_state.user_id = payload.get("userId")
        st.session_state.username = payload.get("username")
        # Clear query params to prevent re-login on refresh
        st.query_params.clear()
        st.success(f"Welcome, {st.session_state.username}!")
        st.rerun()

# --- Initialize Session State ---
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "editing_message_id" not in st.session_state:
    st.session_state.editing_message_id = None
if "overview_risks_page" not in st.session_state:
    st.session_state.overview_risks_page = 0
if "all_risks_page" not in st.session_state:
    st.session_state.all_risks_page = 0
if "terms_page" not in st.session_state:
    st.session_state.terms_page = 0

# --- Helper for Pagination ---
def paginate_items(items, page_size, key_prefix):
    if not items:
        return []
    total_pages = (len(items) - 1) // page_size + 1
    page_key = f"{key_prefix}_page"
    
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
        
    current_page = st.session_state[page_key]
    
    # Ensure current page is within bounds
    if current_page >= total_pages:
        current_page = total_pages - 1
        st.session_state[page_key] = current_page
    if current_page < 0:
        current_page = 0
        st.session_state[page_key] = current_page
        
    start_idx = current_page * page_size
    end_idx = start_idx + page_size
    
    # Render pagination buttons
    if total_pages > 1:
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("⬅️ Previous", key=f"prev_{key_prefix}", disabled=current_page == 0):
                st.session_state[page_key] -= 1
                st.rerun()
        with col_page:
            st.markdown(f"<p style='text-align: center; color: #94a3b8; margin-top: 10px;'>Page {current_page + 1} of {total_pages}</p>", unsafe_allow_html=True)
        with col_next:
            if st.button("Next ➡️", key=f"next_{key_prefix}", disabled=current_page >= total_pages - 1):
                st.session_state[page_key] += 1
                st.rerun()
                
    return items[start_idx:end_idx]

# --- Authentication UI ---
if not st.session_state.jwt_token:
    st.title("🔐 Welcome to Contract Analyzer")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted:
                data = login(email, password)
                if data:
                    st.session_state.jwt_token = data['token']
                    st.session_state.user_id = data['userId']
                    st.session_state.username = data['username']
                    st.success(f"Welcome back, {data['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown("<div style='text-align: center;'>OR</div>", unsafe_allow_html=True)
        # Google Login Link
        st.link_button("🚀 Login with Google", GOOGLE_LOGIN_URL, use_container_width=True)

    with tab_register:
        with st.form("register_form"):
            reg_username = st.text_input("Full Name")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_submitted = st.form_submit_button("Register", use_container_width=True)
            if reg_submitted:
                data = register(reg_username, reg_email, reg_password)
                if data:
                    st.session_state.jwt_token = data['token']
                    st.session_state.user_id = data['userId']
                    st.session_state.username = data['username']
                    st.success("Account created successfully!")
                    st.rerun()
                else:
                    st.error("Registration failed")
    st.stop()

# --- Sidebar: Session Management ---
with st.sidebar:
    st.title(f"👤 {st.session_state.username}")
    if st.button("🚪 Logout"):
        st.session_state.jwt_token = None
        st.session_state.user_id = None
        st.rerun()
        
    st.divider()
    st.title("💬 Chat Sessions")
    
    sessions = get_sessions(st.session_state.user_id)
    
    if st.button("➕ New Analysis", use_container_width=True):
        st.session_state.current_session_id = None
        st.session_state.analysis = None
        st.rerun()
        
    for s in sessions:
        col_s, col_del = st.columns([0.8, 0.2])
        with col_s:
            title = s['title'] if s['title'] else "Untitled Analysis"
            if st.button(f"📄 {title[:20]}...", key=f"session_{s['id']}", use_container_width=True):
                st.session_state.current_session_id = s['id']
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"del_{s['id']}"):
                if delete_session(s['id']):
                    if st.session_state.current_session_id == s['id']:
                        st.session_state.current_session_id = None
                    st.rerun()

# --- Main Layout ---
st.title("⚖️ Enterprise Contract Analyzer & Risk Agent")

# Layout: Two columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📄 Contract Preview")
    
    if not st.session_state.current_session_id:
        uploaded_file = st.file_uploader("Upload PDF to Analyze", type=["pdf"])
        if uploaded_file:
            file_bytes = uploaded_file.getvalue()
            with st.spinner("Deep Analysis in progress..."):
                data = upload_contract(file_bytes)
                if data:
                    new_session = create_session(
                        st.session_state.user_id, 
                        data['contractId'], 
                        f"Analysis: {uploaded_file.name}"
                    )
                    if new_session:
                        st.session_state.current_session_id = new_session['id']
                        st.session_state.analysis = data
                        st.session_state.file_bytes = file_bytes
                        st.rerun()
    else:
        if "file_bytes" in st.session_state:
            render_pdf_preview(st.session_state["file_bytes"])
        else:
            st.info("Contract preview not cached. Re-upload for preview.")

with col2:
    if st.session_state.current_session_id and "analysis" in st.session_state:
        data = st.session_state["analysis"]
        
        tab_overview, tab_risk, tab_terms, tab_qa = st.tabs([
            "📊 Overview", "🚩 Risk Analysis", "⚖️ Key Terms", "💬 Persistent Chat"
        ])
        
        with tab_overview:
            st.markdown("### Executive Summary")
            render_dynamic_progress_bar(data.get('riskScore', 0))
            
            st.markdown("<br>", unsafe_allow_html=True)
            render_metric_group({
                "Red Flags": len(data.get('redFlags', [])),
                "Obligations": len(data.get('obligations', [])),
                "Critical Dates": len(data.get('criticalDates', []))
            })
            
            st.markdown("### Top Risks Found")
            red_flags = data.get('redFlags', [])
            paged_risks = paginate_items(red_flags, 4, "overview_risks")
            for flag in paged_risks:
                st.error(f"**High Priority:** {flag}")

        with tab_risk:
            st.subheader("🚩 Detected Red Flags & Risks")
            red_flags = data.get("redFlags", [])
            if red_flags:
                paged_all_risks = paginate_items(red_flags, 4, "all_risks")
                for i, flag in enumerate(paged_all_risks):
                    render_info_card(f"Risk Item #{st.session_state.all_risks_page * 4 + i + 1}", flag, icon="🚨", color="#ef4444")
            else:
                st.success("No critical red flags detected.")

        with tab_terms:
            st.subheader("⚖️ Legal Obligations & Terms")
            obligations = data.get("obligations", [])
            critical_dates = data.get("criticalDates", [])
            
            if obligations:
                paged_terms = paginate_items(obligations, 4, "terms")
                for i, ob in enumerate(paged_terms):
                    render_info_card(f"Term #{st.session_state.terms_page * 4 + i + 1}", ob, icon="📜")
            
            if critical_dates:
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("📅 Critical Dates")
                for date in critical_dates:
                    st.warning(f"**Deadline / Date:** {date}")

        with tab_qa:
            st.subheader("💬 Smart Persistent Chat")
            history = get_session_history(st.session_state.current_session_id)
            
            chat_container = st.container(height=550)
            with chat_container:
                for msg in history:
                    with st.chat_message(msg['role'].lower()):
                        c_text, c_btn = st.columns([0.9, 0.1])
                        c_text.markdown(msg['content'])
                        if msg['role'] == "USER":
                            if c_btn.button("✏️", key=f"edit_btn_{msg['id']}"):
                                st.session_state.editing_message_id = msg['id']
                                st.session_state.edit_content = msg['content']
                                st.rerun()

            if st.session_state.get("editing_message_id"):
                with st.form("edit_form"):
                    edited_text = st.text_area("Edit your message", value=st.session_state.edit_content)
                    submit_edit = st.form_submit_button("Update & Regenerate")
                    if submit_edit:
                        new_answer = edit_chat_message(st.session_state.current_session_id, st.session_state.editing_message_id, edited_text)
                        if new_answer:
                            st.session_state.editing_message_id = None
                            st.rerun()
            else:
                if prompt := st.chat_input("Ask anything..."):
                    answer = ask_question(st.session_state.current_session_id, prompt)
                    if answer:
                        st.rerun()

    else:
        st.info("Please upload a contract or select a session.")