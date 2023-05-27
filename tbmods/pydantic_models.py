from pydantic import BaseModel

class FeaturesMap(BaseModel):
    name: str
    source: str
    features: dict