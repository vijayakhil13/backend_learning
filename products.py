from pydantic import BaseModel

class Products(BaseModel):
        id: int
        name: str
        des: str
        quantity: int