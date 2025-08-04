#!/usr/bin/env python3
"""
Server runner script for the Smart Contact Router API.
This script runs the FastAPI application using uvicorn.
"""
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )