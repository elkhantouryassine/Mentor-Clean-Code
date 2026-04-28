import os
from google import genai
from app.prompts import SYSTEM_PROMPT

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_code(
    code: str,
    language: str = "python",
    mode: str = "Clean Code"
) -> str:
    user_prompt = f"""
{SYSTEM_PROMPT}

Langage : {language}
Type d'analyse : {mode}

Analyse et corrige ce code :

```{language}
{code}
"""
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
)

    return response.text