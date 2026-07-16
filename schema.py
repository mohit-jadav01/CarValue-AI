from pydantic import BaseModel, Field
from enum import Enum

class Seller_type(str, Enum):
    Dealer = 'Dealer'
    Individual = 'Individual'

class Fuel_type(str, Enum):
    Petrol = 'Petrol'
    Diesel = 'Diesel'
    CNG = 'CNG'

class Transmission(str, Enum):
    Manual = 'Manual'
    Automatic = 'Automatic'

class CarFeature(BaseModel):
    Car_name: str = Field(..., examples=['ritz'])
    Year: int = Field(..., examples=[2015], ge=2000, le=2026)
    Present_Price: float = Field(..., examples=[7.45], gt=0)
    Kms_Driven: int = Field(..., examples=[27000], ge=0)
    Fuel_Type: Fuel_type
    Seller_Type: Seller_type
    Transmission: Transmission
    Owner: int = Field(..., ge=0, le=3, examples=[0])

    class Config:
        use_enum_values = True  # This will use the actual string values of enums

class PredictionResponce(BaseModel):
    prediction_price: float