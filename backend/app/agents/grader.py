# backend/app/agents/grader.py
from groq import Groq, AsyncGroq

client = AsyncGroq()

async def grade_user(parsed, matches):

    # Rule-based baseline
    if not parsed["skills"]:
        return 1

    if parsed["experience_years"] < 1:
        base = 2
    elif parsed["experience_years"] < 3:
        base = 3
    else:
        base = 4

    # LLM refinement
    prompt = f"""
User data:
{parsed}

Matches:
{matches}

Adjust level (1-6) based on portfolio quality, skill depth.
Return ONLY number.
"""

    response = await client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        refined = int(response.choices[0].message.content.strip())
        return max(base, refined)
    except:
        return base