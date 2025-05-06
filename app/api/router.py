from fastapi import APIRouter

# Main API router
api_router = APIRouter()

# Import and include other routers
from app.api.v1.endpoints import terraform, jobs, templates, validation
from app.llm_enhancement.routes import router as llm_router

# Include routers with proper prefixes
api_router.include_router(terraform.router, prefix="/terraform", tags=["Terraform"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])
api_router.include_router(validation.router, prefix="/validation", tags=["Validation"])
api_router.include_router(llm_router, tags=["LLM Enhancement"]) 