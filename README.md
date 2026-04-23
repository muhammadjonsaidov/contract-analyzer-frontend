# ⚖️ Enterprise Contract Analyzer & Risk Agent (Frontend)

A premium, enterprise-grade Streamlit application designed for deep contract analysis, risk assessment, and interactive legal consultation. This frontend integrates with a Spring Boot AI backend to provide real-time insights into legal documents.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B.svg)

## 🌟 Key Features

- **🔐 Secure Authentication**: 
  - JWT-based Login and Registration.
  - Social Login integration (Google OAuth2).
- **📄 Deep Contract Analysis**: 
  - Upload PDF contracts for instant AI processing.
  - Executive summary with automated risk scoring.
- **🚩 Risk Management**:
  - Automated detection of Red Flags and high-priority risks.
  - Legal obligations and key terms extraction.
  - Critical dates and deadline identification.
- **💬 Smart Persistent Chat**:
  - RAG-powered (Retrieval-Augmented Generation) chat interface.
  - Message editing with automated response regeneration.
  - History persistence across sessions.
- **📁 Session Management**:
  - Save, delete, and switch between multiple contract analysis sessions.
  - Sidebar navigation for quick access to history.
- **🎨 Premium UI/UX**:
  - Dark Luxury design system with glassmorphism effects.
  - Responsive layout with sticky document preview.
  - Interactive data visualization and progress tracking.

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Language**: Python 3.9+
- **Styling**: Vanilla CSS (Custom Dark Luxury Theme)
- **API Communication**: `requests`
- **Design Principles**: Glassmorphism, Modern Typography (Outfit Font), Linear Gradients.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Access to the [Contract Analyzer Backend](https://github.com/muhammadjonsaidov/contract-analyzer-backend) (Spring Boot)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/muhammadjonsaidov/contract-analyzer-frontend.git
   cd contract-analyzer-frontend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install streamlit requests
   ```

### Configuration

The application uses a central `config.py` file to manage backend connections. Update the `BACKEND_URL` in `config.py` if your backend address changes:

```python
# config.py
BACKEND_URL = "https://your-ngrok-url.ngrok-free.dev/backend"
```

### Running the App

```bash
streamlit run streamlit.py
```

## 📂 Project Structure

```text
.
├── streamlit.py       # Main entry point and application logic
├── config.py          # Centralized configuration (URLs, API endpoints)
├── api_client.py      # Backend API communication layer
├── components.py      # Custom UI components (PDF preview, metrics, cards)
├── styles.py          # Dark Luxury CSS theme and global styles
└── README.md          # Project documentation
```

## 💎 Design Aesthetics

The application features a **Dark Luxury** theme designed to feel premium and enterprise-ready:
- **Color Palette**: Deep Obsidian (#0a0b10) to Midnight Blue (#13161f) gradients.
- **Typography**: "Outfit" font family for a modern, tech-forward look.
- **Visual Effects**: Glassmorphism containers with subtle backdrops and glow effects.
- **Micro-animations**: Smooth hover transitions on cards and buttons.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
