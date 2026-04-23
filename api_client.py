import requests
import streamlit as st

API_BASE_URL = "http://localhost:8080/api"

def get_headers():
    headers = {}
    if "jwt_token" in st.session_state and st.session_state.jwt_token:
        headers["Authorization"] = f"Bearer {st.session_state.jwt_token}"
    return headers

# Authentication
def login(email, password):
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def register(username, email, password):
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def upload_contract(file_bytes):
    """Sends the PDF file to the backend for analysis."""
    files = {"file": file_bytes}
    try:
        response = requests.post(f"{API_BASE_URL}/contracts/upload", files=files, headers=get_headers())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            st.error("Session expired. Please login again.")
            st.session_state.jwt_token = None
            st.rerun()
        else:
            st.error(f"Server Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# Session Management
def get_sessions(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/user/{user_id}", headers=get_headers())
        return response.json() if response.status_code == 200 else []
    except:
        return []

def create_session(user_id, contract_id, title):
    try:
        params = {"userId": user_id, "contractId": contract_id, "title": title}
        response = requests.post(f"{API_BASE_URL}/sessions", params=params, headers=get_headers())
        return response.json() if response.status_code == 200 else None
    except:
        return None

def delete_session(session_id):
    try:
        return requests.delete(f"{API_BASE_URL}/sessions/{session_id}", headers=get_headers()).status_code == 200
    except:
        return False

def get_session_history(session_id):
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/{session_id}/history", headers=get_headers())
        return response.json() if response.status_code == 200 else []
    except:
        return []

# Chat Logic
def ask_question(session_id, query):
    """Sends a query to the RAG chat API via Session."""
    payload = {"question": query}
    try:
        response = requests.post(f"{API_BASE_URL}/contracts/{session_id}/chat", json=payload, headers=get_headers())
        if response.status_code == 200:
            return response.json().get("answer", "No answer provided.")
        return None
    except Exception as e:
        st.error(f"Chat Error: {str(e)}")
        return None

def edit_chat_message(session_id, message_id, new_query):
    """Edits a message and gets a regenerated AI response."""
    payload = {"question": new_query}
    try:
        response = requests.put(f"{API_BASE_URL}/sessions/{session_id}/messages/{message_id}", json=payload, headers=get_headers())
        if response.status_code == 200:
            return response.json().get("answer")
        return None
    except Exception as e:
        st.error(f"Edit Error: {str(e)}")
        return None
