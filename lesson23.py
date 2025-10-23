from typing import Optional
from typing import Union
from typing import Any
from typing import List

def process_union(value: Any) -> str:
    return f"Procces{value}"

print(process_union(1))

def process_value(value: Union[int,str]) -> str:
  if isinstance(value, int):
    return f"Number {value}"
  return f"String {value}"

print(process_value("Digital School"))

def process_list(numbers: List[int]) ->int:
   return sum(numbers)

numbers: List[int]= [1,2,3,4]

result: List = process_list(numbers)

print(result)