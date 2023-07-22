from pydantic import BaseModel

class FeaturesMap(BaseModel):
    name: str
    source: str
    features: dict

class ModelMap(BaseModel):
    save: bool
    dataset_name: str
    parameters_map: dict