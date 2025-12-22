from fastapi import APIRouter
import os
import openai

router = APIRouter(prefix="/llm", tags=["LLM Q&A"])

openai.api_key = os.getenv("OPENAI_API_KEY")


@router.post("/ask")
def ask_llm(payload: dict):
    question = payload.get("question", "")

    if not question:
        return {"answer": "Please ask a valid question."}

    prompt = f"""
You are a pharmaceutical demand analyst.
Answer the following question clearly and concisely:

Question: {question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a pharmaceutical analytics expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return {
        "question": question,
        "answer": response.choices[0].message["content"]
    }
