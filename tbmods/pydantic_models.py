from pydantic import BaseModel

class FeaturesMap(BaseModel):
    name: str
    features: dict