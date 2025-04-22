from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select

from db.database import get_session
from models.category import Category, CategoryCreate, CategoryRead
from crud.category import (
    create_category,
    get_categories,
    get_category_by_id,
    update_category,
    delete_category,
    get_category_by_name,
    update_category_by_name,
    delete_category_by_name,
)

router = APIRouter()

@router.post("/", response_model=CategoryRead)
def create(category: CategoryCreate, session: Session = Depends(get_session)):
    try:
        category_data = Category(**category.model_dump())
        created_category = create_category(session, category_data)
        session.refresh(created_category)  # Refresh to load relationships
        return created_category
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[CategoryRead])
def read_all(session: Session = Depends(get_session)):
    try:
        return get_categories(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{category_id}", response_model=CategoryRead)
def read(category_id: int, session: Session = Depends(get_session)):
    try:
        category = get_category_by_id(session, category_id)
        if not category:
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
        return category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/name/{name}", response_model=CategoryRead)
def read_by_name(name: str, session: Session = Depends(get_session)):
    try:
        category = get_category_by_name(session, name)
        if not category:
            raise HTTPException(status_code=404, detail=f"Category with name '{name}' not found")
        return category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{category_id}", response_model=Category)
def update(
    category_id: int,
    category_data: dict = Body(
        ...,
        example={
            "name": "Updated category name",
            "description": "Updated description for the category"
        }
    ),
    session: Session = Depends(get_session),
):
    for key, value in category_data.items():
        print(key)
        if key == "id":
            raise HTTPException(status_code=400, detail="You're trying to update the ID.")
    try:
        updated_category = update_category(session, category_id, category_data)
        if not updated_category:
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/name/{name}", response_model=Category)
def update_by_name(
    name: str,
    category_data: dict = Body(
        ...,
        example={
            "name": "Updated category name",
            "description": "Updated description for the category"
        }
    ),
    session: Session = Depends(get_session),
):
    for key, value in category_data.items():
        print(key)
        if key == "id":
            raise HTTPException(status_code=400, detail="You're trying to update the ID.")
    try:
        updated_category = update_category_by_name(session, name, category_data)
        if not updated_category:
            raise HTTPException(status_code=404, detail=f"Category with name '{name}' not found")
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{category_id}", response_model=Category)
def delete(category_id: int, session: Session = Depends(get_session)):
    try:
        deleted_category = delete_category(session, category_id)
        if not deleted_category:
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
        return deleted_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/name/{name}", response_model=Category)
def delete_by_name(name: str, session: Session = Depends(get_session)):
    try:
        deleted_category = delete_category_by_name(session, name)
        if not deleted_category:
            raise HTTPException(status_code=404, detail=f"Category with name '{name}' not found")
        return deleted_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")