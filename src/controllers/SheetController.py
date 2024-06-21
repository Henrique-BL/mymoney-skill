from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from typing import List
from src.schemas.Cell import CellIn, CellUpdateIn, CellOut, CellUpdateOut
from src.services.SheetService import SheetService

sheet_service = SheetService()

router = APIRouter()


@router.post(
    path="/",
    summary="Add cell to worksheet",
    status_code=status.HTTP_201_CREATED,
    response_model=CellOut,
)
async def post(body: CellIn = Body(...)) -> CellOut:
    await sheet_service._initialize()

    result = await sheet_service.create_cell(body)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create cell"
        )

    sheet_service._repository.close()

    return result


@router.get(
    path="/{worksheet_name}",
    summary="Get cell from worksheet",
    status_code=status.HTTP_200_OK,
    response_model=CellOut,
)
async def get(
    worksheet_name: str = Path(..., alias="worksheet_name"),
    column_name: str = Query(..., alias="column_name"),
    row: int = Query(..., alias="row"),
    col: int = Query(..., alias="column"),
) -> CellOut:
    await sheet_service._initialize()
    data = {
        "value": 0,
        "type": "",
        "worksheet_name": worksheet_name,
        "column_name": column_name,
        "row": row,
        "col": col,
    }
    cell_in = CellIn(**data)

    result = await sheet_service.get_cell(cell_in)
    if result is None:
        raise HTTPException(status_code=404, detail="Failed to get cell data.")

    sheet_service._repository.close()
    return result


@router.get(
    path="/all/{column_name}",
    summary="Get columns cells data.",
    status_code=status.HTTP_200_OK,
    response_model=List[CellOut],
)
async def query(
    worksheet_name: str = Query(..., alias="worksheet_name"),
    column_name: str = Path(..., alias="column_name"),
) -> List[CellOut]:
    await sheet_service._initialize()

    result = await sheet_service.get_all_cells(worksheet_name, column_name)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="Failed to get column data."
        )

    sheet_service._repository.close()

    return result


@router.put(
    path="/",
    summary="Update a cell.",
    status_code=status.HTTP_200_OK,
    response_model=CellUpdateOut,
)
async def update_cell(
    row: int = Query(..., alias="row"),
    col: int = Query(..., alias="col"),
    cell_in: CellUpdateIn = Body(...),
) -> CellUpdateOut:
    await sheet_service._initialize()

    coords: dict = {"row": row, "col": col}

    result = await sheet_service.update_cell(coords, cell_in)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Failed to update cell"
        )

    sheet_service._repository.close()

    return result


@router.delete(
    path="/", summary="Delete a cell.", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_cell(cell_in: CellIn = Body(...)) -> None:
    await sheet_service._initialize()

    result = await sheet_service.delete_cell(cell_in)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete cell"
        )

    sheet_service._repository.close()

    return result
