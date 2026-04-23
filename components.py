import streamlit as st
import base64

def render_pdf_preview(file_bytes):
    """Renders the PDF inside an iframe for preview with fixed dimensions."""
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    # Adding #view=FitH to fit the page horizontally and #toolbar=0 to hide the toolbar for a 'fixed' look
    pdf_display = f"""
        <div style="background: rgba(255,255,255,0.02); border-radius: 16px; padding: 10px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <iframe src="data:application/pdf;base64,{base64_pdf}#view=FitH&toolbar=0" 
                    width="100%" 
                    style="aspect-ratio: 1 / 1.414; border: none; border-radius: 12px; display: block;"
                    type="application/pdf">
            </iframe>
        </div>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

def render_dynamic_progress_bar(risk_score):
    """Renders a premium progress bar with dynamic colors."""
    color = "#10b981" # Green
    if risk_score > 70: color = "#ef4444" # Red
    elif risk_score > 40: color = "#f59e0b" # Amber
        
    st.markdown(f"""
        <div style="width: 100%; background-color: rgba(255,255,255,0.05); border-radius: 20px; height: 12px; margin: 10px 0;">
            <div style="width: {risk_score}%; background: linear-gradient(90deg, {color} 0%, #ffffff 200%); border-radius: 20px; height: 100%; transition: width 1s ease-in-out; box-shadow: 0 0 15px {color}66;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #94a3b8; font-size: 0.85rem;">Overall Contract Risk</span>
            <span style="color: {color}; font-weight: 700; font-size: 1.2rem;">{risk_score}%</span>
        </div>
    """, unsafe_allow_html=True)

def render_info_card(title, content, icon="ℹ️", color="#38bdf8"):
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; margin-bottom: 15px; transition: transform 0.3s ease;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
            <h4 style="margin: 0; color: white;">{title}</h4>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_group(metrics):
    cols = st.columns(len(metrics))
    for i, (label, value) in enumerate(metrics.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
                <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px;">{label}</div>
                <div style="color: #38bdf8; font-size: 1.8rem; font-weight: 700;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

def display_chat_message(role, content, message_id=None, on_edit=None):
    with st.chat_message(role):
        col_text, col_btn = st.columns([0.9, 0.1])
        with col_text:
            st.markdown(content)
        if role == "user" and message_id and on_edit:
            with col_btn:
                if st.button("✏️", key=f"edit_{message_id}", help="Edit message"):
                    on_edit(message_id, content)
