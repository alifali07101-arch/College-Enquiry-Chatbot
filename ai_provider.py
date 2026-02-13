import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

PREDEFINED_PATH = "chatbot_data/predefined_answers.json"

def load_knowledge_base():
    """JSON file ko text mein convert karta hai taaki AI usse padh sake"""
    try:
        with open(PREDEFINED_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        knowledge_text = "OFFICIAL INFORMATION ABOUT RUNGTA INTERNATIONAL SKILLS UNIVERSITY:\n"
        for key, value in data.items():
            knowledge_text += f"- {key}: {value}\n"
        return knowledge_text
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return ""

def ask_ai(prompt):
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        return "System Error: API Key missing."

    context_data = load_knowledge_base()

    final_prompt = f"""
    You are a friendly and intelligent Admission Counsellor for 'Rungta International Skills University'.
    
    INSTRUCTIONS:
    1. Use the provided 'Context' below to answer the user's question accurately.
    2. If the answer is in the Context, explain it nicely in a conversational tone.
    3. If the answer is NOT in the Context, apologize politely and suggest contacting the college administration.
    4. Keep answers concise (under 3-4 sentences) but helpful.
    5. Do not say "According to the document". Just answer naturally.
    6. Always end with a friendly note, e.g., "Feel free to ask more!" or "Hope this helps!".
    7. If the user asks something completely unrelated, gently steer them back to college-related queries.
    8. Don't start all answers with Hello. Vary your greetings and responses to sound more human.

    CONTEXT DATA:
    {context_data}

    USER QUESTION:
    {prompt}
    """

    models_to_try = [
        "gemini-2.5-flash",           # Newest & Best
        "gemini-1.5-flash-latest",    # Reliable
        "gemini-1.5-flash-001",       # Backup
        "gemini-2.0-flash-lite-001",  # Fast
        "gemini-1.5-pro-latest"       # High Intelligence
    ]

    print("[INFO] Asking AI with Knowledge Base...")

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": final_prompt}]}]
        }

        try:
            print(f"Trying model: {model_name}...")
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"✅ Success with {model_name}!")
                return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            
            elif response.status_code == 429:
                print(f"⚠️ {model_name} busy (Rate Limit). Switching...")
                time.sleep(1)
                continue 
            
            elif response.status_code == 404:
                 print(f"❌ {model_name} not found. Skipping...")
                 continue
            
            else:
                print(f"❌ Error {response.status_code}. Next...")
                continue

        except Exception as e:
            print(f"Connection error: {e}")
            continue

    return "Sorry, all servers are busy right now. Please wait a moment and try again later."