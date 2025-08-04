from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api  # Make sure routes/api.py has `router` defined
import logging

app = FastAPI(title="Smart Contact Router API", version="1.0.0")

# Optional: Enable CORS for frontend support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routes
app.include_router(api.router, prefix="/api")

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Contact routing API is healthy."}

# ✅ Startup event
@app.on_event("startup")
async def on_startup():
    logging.info("🚀 FastAPI is starting up...")
    # You could add DB connections, load cache, validate secrets here
    # e.g., await db.connect()

# ✅ Shutdown event (optional)
@app.on_event("shutdown")
async def on_shutdown():
    logging.info("🛑 FastAPI is shutting down...")
    # e.g., await db.disconnect()
