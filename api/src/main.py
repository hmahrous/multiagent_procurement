from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.api_router import api_router

app = FastAPI(
    title="UBS Procurement Chatbot",
    docs_url="/docs",
)


# Include application routers
app.include_router(api_router)

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
