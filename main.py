from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

# 1. Read single sheep by ID
@app.get("/sheep/{id}", response_model=Sheep, status_code=status.HTTP_200_OK)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if not sheep:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sheep not found"
        )
    return sheep


# 2. Add new sheep
@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sheep with this ID already exists"
        )
    return db.add_sheep(sheep)


# 3. Read all sheep (Extra Credit)
@app.get("/sheep/", response_model=list[Sheep], status_code=status.HTTP_200_OK)
def read_all_sheep():
    return db.get_all_sheep()


# 4. Update sheep (Extra Credit)
@app.put("/sheep/{id}", response_model=Sheep, status_code=status.HTTP_200_OK)
def update_sheep(id: int, sheep: Sheep):
    if id not in db.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sheep with this ID does not exist"
        )
    return db.update_sheep(id, sheep)


# 5. Delete sheep (Extra Credit)
@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if id not in db.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sheep with this ID does not exist"
        )
    db.delete_sheep(id)
    return None