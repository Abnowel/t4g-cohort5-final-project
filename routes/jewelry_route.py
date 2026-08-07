from fastapi import APIRouter, Body, status, HTTPException
from services.jewelry_service import JewelryService

# Creating jewelry router with a common prefix
router = APIRouter(prefix="/jewelry")

jewelry_service = JewelryService()

# Creating a new jewelry item
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_jewelry(body: dict = Body(...)):
    new_jewelry = jewelry_service.create_jewelry(body)

    return new_jewelry.to_dict()

# Get all jewelry items
@router.get("/",status_code=status.HTTP_200_OK)
def get_jewelry():
    jewelry = jewelry_service.get_all_jewelry()

    result = []

    for item in jewelry:
        result.append(item.to_dict())

    return result

# Get one jewelry item by ID
@router.get("/{jewelry_id}", status_code=status.HTTP_200_OK)
def get_jewelry_by_id(jewelry_id: str):

    jewelry = jewelry_service.get_jewelry_by_id(jewelry_id)

    if jewelry is None:
        raise HTTPException(
            status_code=404,
            detail="Jewelry item not found"
        )

    return jewelry.to_dict()
