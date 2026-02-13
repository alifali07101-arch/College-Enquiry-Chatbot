# 🎓 College Enquiry - AI Chatbot

A smart, hybrid AI chatbot designed for college enquiry. It assists students and parents with admissions, fees, placements, and campus life queries using **Google Gemini AI** and a custom **Knowledge Base**.

## 🚀 Features

- **Hybrid AI Engine:** Uses a structured JSON Knowledge Base for accurate college info + Google Gemini (Flash Model) for natural conversation.
- **Smart Context Awareness:** Answers queries about Fees, Courses, Hostels, and Placements with official data.
- **User System:** Signup/Login functionality for students.
- **Chat History:** Saves previous conversations in a database.
- **Interactive UI:** Typing animations, quick reply buttons, and auto-scrolling chat window.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI Model:** Google Gemini 1.5 Flash / 2.0 Flash Lite (via Google GenAI SDK)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/College Enquiry-chatbot.git](https://github.com/YOUR_USERNAME/rungta-chatbot.git)
   cd College Enquiry-chatbot

2.**Create a Virtual Environment**
Bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

3.**Install Dependencies**
Bash
pip install -r requirements.txt

4.**Set up Environment Variables**
Create a .env file in the root directory and add your Google API Key:
Code snippet
GENAI_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key

5.**Run the Application**
Bash
python app.py
Open http://127.0.0.1:5000 in your browser.

**📂 Project Structure**
app.py: Main Flask application.

ai_provider.py: Handles logic to switch between Knowledge Base and Gemini AI.

chatbot_data/predefined_answers.json: The "Brain" of the chatbot containing college data.

templates/: HTML files.

static/: CSS and JavaScript files.   
