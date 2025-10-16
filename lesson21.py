# def format_name(first_name, last_name):
#     full_name = first_name.title() + " " + last_name.title()
#     return full_name
# print(format_name("Kung", "Lao"))
# def get_full_name(first_name: str, last_name: str):
#     full_name = first_name.title() + " " + last_name.title()
#     return full_name

# print(get_full_name("Leo", "Nardo"))

# def get_item(item_a: str, item_b: int, item_c: float, item_d: bytes, item_e: bool):
#     return item_a,item_b,item_c,item_d,item_e
# print(get_item("str", "2", "3", "4,5", True ))
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def get_items():
    return{"item_1","item_2","item_3"}

@app.post("/items/{items}")
def items(items: str, price: float):
    return{"name":items,"price": price}