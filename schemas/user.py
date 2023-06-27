from pydantic import BaseModel

class user(BaseModel):
    email:str 
    password: str