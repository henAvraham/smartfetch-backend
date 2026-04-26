# SmartFetch Backend

SmartFetch is an AI-powered RAG (Retrieval-Augmented Generation) system that allows users to submit a web page URL, crawl and index its content, and ask natural language questions about that source.

This repository contains the backend API, built with FastAPI. It handles authentication, source management, web crawling, semantic search, and communication with the AI model.

## Features

- User authentication with JWT
- Add and manage web sources
- Crawl web pages and extract relevant text content
- Generate embeddings for indexed content
- Store and search documents using Elasticsearch
- Ask questions over retrieved context using an AI model
- Source-based retrieval to keep answers relevant to the selected content
- REST API endpoints for frontend integration

## Tech Stack

- Python
- FastAPI
- MongoDB
- Elasticsearch
- OpenAI API / LLM API
- JWT Authentication
- Docker
- BeautifulSoup
- REST APIs

## Main Flow

1. User registers or logs in.
2. User adds a web page URL as a source.
3. The backend crawls the page and extracts its textual content.
4. The extracted content is embedded and indexed in Elasticsearch.
5. User asks a question about the source.
6. The backend retrieves the most relevant chunks.
7. The retrieved context is sent to the AI model.
8. The model returns a context-aware answer.

```http
POST /auth/register
POST /auth/login
