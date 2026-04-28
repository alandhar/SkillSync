from groq import Groq, AsyncGroq
import json

client = AsyncGroq()

PROMPT = """
Extract structured data from CV:

Return JSON:
{
  "skills": [],
  "experience_years": number,
  "projects": [],
  "publications": []
}

CV:
"""

async def parse_cv(text: str):
    response = await client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": PROMPT + text}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)