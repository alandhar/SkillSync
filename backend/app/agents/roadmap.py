from groq import Groq, AsyncGroq

client = AsyncGroq()

async def generate_roadmap(parsed, gaps, level):

    prompt = f"""
User level: {level}

Skill gaps:
{gaps}

Generate 4-week roadmap.
If level 3-4: skip basic theory.

Format:
Week 1:
- ...
"""

    response = await client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content