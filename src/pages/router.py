from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from src.hotels.router import all_hotels, get_hotels_in_location

router = APIRouter(
    prefix="/pages",
    tags=["Визуализация API"],
)


templates = Jinja2Templates(directory="src/templates")


@router.get("/index")
async def get_index_page(request: Request, hotels=Depends(all_hotels)):
    return templates.TemplateResponse(
        name="index.html", context={"request": request, "hotels": hotels}
    )


@router.get("/hotels")
async def get_hotels_page(request: Request, hotels=Depends(get_hotels_in_location)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )
