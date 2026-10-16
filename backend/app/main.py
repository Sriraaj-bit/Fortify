from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.router import auth_router, transactions_router, budgets_router, goals_router, dashboard_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(transactions_router.router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])
app.include_router(budgets_router.router, prefix=f"{settings.API_V1_STR}/budgets", tags=["budgets"])
app.include_router(goals_router.router, prefix=f"{settings.API_V1_STR}/goals", tags=["goals"])
app.include_router(dashboard_router.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

@app.get(f"{settings.API_V1_STR}/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}