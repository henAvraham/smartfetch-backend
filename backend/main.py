from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.elastic_client import get_es_client
from app.db.database import Base, engine
from app.auth.routes import router as auth_router
from app.routes.sources import router as sources_router
from app.routes.crawl import router as crawl_router
from app.routes.search import router as search_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "API is running"}


# רישום ה־routers
app.include_router(auth_router, tags=["auth"])
app.include_router(sources_router, prefix="/sources", tags=["sources"])
app.include_router(crawl_router, prefix="/crawl", tags=["crawl"])
app.include_router(search_router, prefix="/search", tags=["search"])


@app.get("/es-test")
def es_test():
    client = get_es_client()
    health = client.info()
    return {"connected": True, "cluster": health["cluster_name"]}
