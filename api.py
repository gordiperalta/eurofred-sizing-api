from fastapi import FastAPI
from pydantic import BaseModel
from main import compute_project  # This must be defined

app = FastAPI()

class Bedroom(BaseModel):
    code: str
    area: float
    indoor_type: str
    dist_out_to_in: float
    dist_drain: float

class UserInput(BaseModel):
    address: str
    construction_year: int
    building_type: str
    square_meters: float
    floor_count: int
    orientation: str
    people_count: int
    isolation_change: str
    bedroom_info: list[Bedroom]

@app.post("/calculate")
def calculate(input: UserInput):
    result = compute_project(input.model_dump())
    return result
