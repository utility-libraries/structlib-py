# structurelib-py
similar function to the builtin struct-library but more efficient

## Installation

`pip install structurelib`

## Example

```python
from dataclasses import dataclass
import structurelib as sl
from structurelib.types import *

@dataclass
class MyStruct(sl.Structure):  # sl.Structure inheritance is optional
    name: string
    value: int8

sl.dumps(MyStruct("Hello World", 8))  # b'\x0bHello World\x08'
MyStruct.dump_struct(MyStruct("Hello World", 8))  # b'\x0bHello World\x08'
sl.loads(b'\x0bHello World\x08', cls=MyStruct)  # MyStruct(name="Hello World", value=8)
MyStruct.load_struct(b'\x0bHello World\x08')  # MyStruct(name="Hello World", value=8)
```
