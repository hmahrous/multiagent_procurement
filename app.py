# -*- coding: utf-8 -*-
from fastapi import FastAPI
from endpoints import document_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import document_router  # Assuming your APIRouter is in 'your_module.py'

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)