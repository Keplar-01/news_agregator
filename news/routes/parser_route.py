from typing import List, Annotated, Union
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, BackgroundTasks

from config.database import Session
from schemas.parse_data_schema import ParseDataOutput
from services.parser_service import ParserService

from schemas.parse_data_schema import ParseDataInput

router = APIRouter(
    prefix="/parser",
    tags=["parser"]
)
_service = ParserService(Session())


@router.get("/parse_data",
            response_model=List[ParseDataOutput])
async def get_parse_data() -> List[ParseDataOutput]:
    data = await _service.get_all()
    return data


@router.post("/add_parse_data",
             response_model=ParseDataOutput)
async def add_parse_data(parse_data: ParseDataInput) -> ParseDataOutput:
    parse_data = await _service.create(parse_data)
    if parse_data is None:
        raise HTTPException(status_code=401, detail="Этот источник данных уже добавлен")
    return parse_data


@router.put("/update_parse_data/{parse_data_id}",
            response_model=Annotated[dict[str, Union[ParseDataOutput, bool]], {"success": bool, "result": Union[ParseDataOutput, str]}])
async def update_parse_data(parse_data_id: int, data: ParseDataInput) -> dict:
    data = await _service.update(parse_data_id, data)

    if data['success'] is False:
        raise HTTPException(status_code=401, detail=data['result'])

    return data

@router.delete("/delete_parse_data/{parse_data_id}",
               response_model=bool)
async def delete_parse_data(parse_data_id: int) -> bool:
    data = await _service.delete(parse_data_id)
    return data

@router.post("/fetch_news_from_url_rss")
async def fetch_news():
    a = await _service.fetch_news_from_url_rss()

    return a

