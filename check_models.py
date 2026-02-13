import os
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    print("Error: API Key nahi mili .env file mein!")
else:
    print(f"Checking models for API Key: {api_key[:10]}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Available Models for you:")
            found_any = False
            for model in data.get('models', []):
                if 'generateContent' in model['supportedGenerationMethods']:
                    print(f" - {model['name']}")
                    found_any = True
            
            if not found_any:
                print("❌ Koi chat model nahi mila. Shayad API Key restricted hai.")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")