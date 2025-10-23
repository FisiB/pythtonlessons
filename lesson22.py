from pydantic import BaseModel , conint, constr
from typing import Optional

# class Users(BaseModel):
#     id: int
#     emri: str
#     email: str
#     age: int
# user = Users(id=1 , name="Lis" , age=20, email="dioni@gmail.com")
# print(Users)

class User(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    email: Optional[str] = None

user1 = User(id=1, name="Dion", age=17, email="dion@gmail.com")
print(user1)

user2= User(id=2 , name="Darsej" , email="darsej@gmail.com")
print(user2)
user3 = User(id=3, name="Oltion")
print (user3)


class another_user(BaseModel):
    id:conint(gt=0) # <0
    name: constr(min_length=2, max_length=50)

valid_user = another_user(id=1 , name="Subaru")
print(valid_user)


# valid_user1 = another_user(id=0 , name="S")
# print(valid_user1)
#qikjo eshte error int value duhet me u kan ma nalt se 0 edhe str value duhet me i pas ma shum se 2 shkronja
