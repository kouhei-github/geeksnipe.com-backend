from fastapi import APIRouter
health_check = APIRouter(
    prefix="/api/health",
    tags=["Health Check"]
)

@health_check.get("/")
async def health():
    return {"msg": "I am good health."}
