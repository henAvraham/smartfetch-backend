# app/routes/search.py
from fastapi import APIRouter, Depends, Query

from app.auth.auth_utils import get_current_user  
from app.elastic_client import (
    search_documents,
    semantic_search_documents,
)
from app.models.user import User
from app.utils.llm_client import answer_question_with_context
from app.schemas import AskRequest, AskResponse

router = APIRouter(prefix="/search", tags=["search"])



@router.get("/")
def search(
    q: str = Query(..., min_length=1, description="Text to search within the documents"),
    current_user: User = Depends(get_current_user),
):
    """
    חיפוש טקסטואלי (keyword search) במסמכים של המשתמש הנוכחי.
    """
    results = search_documents(query=q, user_id=current_user.id, size=5)
    return {
        "query": q,
        "results": results,
    }


@router.post("/ask", response_model=AskResponse)
def ask_question(
    body: AskRequest,
    current_user: User = Depends(get_current_user),
):
    """
    RAG: שואלים שאלה על בסיס מסמכים ממקור אחד (source_id יחיד).
    """

    if body.source_id is None:
   
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="source_id is required",
        )

    results = semantic_search_documents(
        question=body.question,
        user_id=current_user.id,
        source_id=body.source_id,
        size=5,
    )

    answer = answer_question_with_context(
        question=body.question,
        chunks=results,
    )

    return AskResponse(
        answer=answer,
        chunks=results,
    )
