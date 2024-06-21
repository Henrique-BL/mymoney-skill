from fastapi import APIRouter
from src.controllers.SheetController import router as cells

router = APIRouter()

router.include_router(router=cells, prefix="/cells", tags=["cells"])
