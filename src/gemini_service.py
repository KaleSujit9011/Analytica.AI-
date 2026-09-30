import os

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


def call_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-3.8-flash")

        response = model.generate_content(prompt)

        return {
            "response": response.text
        }

    except Exception as error:
        return {
            "error": f"Gemini service error: {str(error)}"
        }