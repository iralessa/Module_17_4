# from pydantic import BaseModel
#
# class CreateProduct(BaseModel):
#     name : str
#     description : str
#     price : int
#     image_url : str
#     stock : int
#     category : int
# class CreateCategory(BaseModel):
#     name : str
#     parent_id : int
from pydantic import BaseModel

class CreateUser (BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser (BaseModel):
    firstname: str
    lastname: str
    age: int
class CreateTask (BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask (BaseModel):
    title: str
    content: str
    priority: int

class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    slug: str
    user_id: int

