"""Main API routes for the LLM Enhancement Layer"""
from fastapi import APIRouter, HTTPException
from .parsers.routes import router as parser_router
from .generators.routes import router as generator_router
from .validators.routes import router as validator_router
from .optimizers.routes import router as optimizer_router

# Create the main router for the LLM Enhancement Layer
router = APIRouter(prefix="/llm", tags=["LLM Enhancement"])

# Include all component routers with their own prefixes
router.include_router(
    parser_router,
    prefix="/parser",
    tags=["Natural Language Parser"]
)

router.include_router(
    generator_router,
    prefix="/generator",
    tags=["Template Generator"]
)

router.include_router(
    validator_router,
    prefix="/validator",
    tags=["Intelligent Validator"]
)

router.include_router(
    optimizer_router,
    prefix="/optimizer",
    tags=["Resource Optimizer"]
) 