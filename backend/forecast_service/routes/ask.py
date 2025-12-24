from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ask", tags=["LLM"])

class Question(BaseModel):
    question: str

@router.post("")
def ask_question(q: Question):
    # Stub response (replace with real LLM later)
    return {
        "answer": (
            "This answer is generated based on historical demand data "
            "stored in the system. Forecast values are computed from "
            "time-series trends and recent sales patterns."
        )
    }
