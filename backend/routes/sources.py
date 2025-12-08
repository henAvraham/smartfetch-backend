from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.source import Source
from app.models.user import User
from app.schemas import SourceCreate, SourceRead


from app.utils.crawler import fetch_page_text
from app.elastic_client import index_document

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/", response_model=SourceRead)
def create_source(
    source_in: SourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Source:

 
    source = Source(
        user_id=current_user.id,
        url=str(source_in.url),
    )
    db.add(source)
    db.commit()
    db.refresh(source)

 
    title, content = fetch_page_text(source.url)
    if not content:
        content = ""
    if not title:
        title = source.url

    index_document(
        doc_id=source.id,
        user_id=current_user.id,
        source_id=source.id,
        title=title,
        content=content,
        url=source.url,
    )

    return source


@router.get("/", response_model=list[SourceRead])
def list_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Source]:
    sources = db.query(Source).filter(Source.user_id == current_user.id).all()
    return sources
