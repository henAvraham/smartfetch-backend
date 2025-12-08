from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.elastic_client import index_document
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.document import Document
from app.models.source import Source
from app.models.user import User
from app.schemas import DocumentRead
from app.utils.crawler import fetch_page_text

router = APIRouter(prefix="/crawl", tags=["crawl"])


@router.post("/{source_id}", response_model=DocumentRead)
def crawl_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Document:
    source = (
        db.query(Source)
            .filter(Source.id == source_id, Source.user_id == current_user.id)
            .first()
    )
    if source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found for this user",
        )

    title, content = fetch_page_text(source.url)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not fetch content from the URL",
        )

    document = Document(
        user_id=current_user.id,
        source_id=source.id,
        url=source.url,
        title=title,
        content=content,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    index_document(
        doc_id=document.id,
        user_id=current_user.id,
        source_id=source.id,
        title=title,
        content=content,
        url=source.url,
    )

    return document







