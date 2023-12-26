# structurelib-py
similar function to the builtin struct-library but more friendly

<!-- TOC -->
* [structurelib-py](#structurelib-py)
  * [Installation](#installation)
  * [Examples](#examples)
    * [Example 1: Basic](#example-1-basic)
    * [Example 2: Nested Objects](#example-2-nested-objects)
  * [Documentation](#documentation)
    * [Supported types](#supported-types)
      * [Why are there so many types?](#why-are-there-so-many-types)
        * [Optimizations](#optimizations)
        * [Compatibility](#compatibility)
    * [`dumps()`](#dumps)
    * [`loads()`](#loads)
    * [`Structure`-class](#structure-class)
<!-- TOC -->

## Installation

[![PyPI - Version](https://img.shields.io/pypi/v/structurelib)
](https://pypi.org/project/structurelib/)

`pip install structurelib`

## Examples

### Example 1: Basic

```python
from dataclasses import dataclass
import structurelib as sl
from structurelib.types import *

@dataclass
class MyStruct(sl.Structure):  # sl.Structure inheritance is optional
    name: str  # `string` is also possible
    value: int8

sl.dumps(MyStruct("Hello World", 8))  # b'\x0bHello World\x08'
MyStruct.dump_struct(MyStruct("Hello World", 8))  # b'\x0bHello World\x08'
sl.loads(b'\x0bHello World\x08', cls=MyStruct)  # MyStruct(name="Hello World", value=8)
MyStruct.load_struct(b'\x0bHello World\x08')  # MyStruct(name="Hello World", value=8)
```

### Example 2: Nested Objects

```python
import dataclasses
import structurelib as sl
from structurelib.types import *


@dataclasses.dataclass
class Credentials:
    name: string
    password: string


@dataclasses.dataclass
class User:
    name: string
    credentials: Credentials


instance = User("hello", Credentials("hello", "world"))
print(instance)  # User(name="hello", Credentials(name="hello", password="world"))
sld = sl.dumps(instance)
print(f"dump | {len(sld):>3} | {sld}")
loaded = sl.loads(sld, cls=User)
print(loaded)  # User(name="hello", Credentials(name="hello", password="world"))
```

## Documentation

### Supported types

> You can add additional types by importing them at the top of your file.
> These types can reduce the output size.
> ```python
> from structurelib.types import *
> ```
> All additional types can be used without problem to replace the old ones and won't interfere with typechecking.
> ```python
> class MyClass:
>     attr: uint16
> ```

| type              | description               | size    | values                                                 |
|-------------------|---------------------------|---------|--------------------------------------------------------|
| int/integer       | any integer               | dynamic | -∞ - +∞                                                |
| integer[n, False] | integer                   | n byte  | 0 - 2<sup>8*n</sup>                                    |
| integer[n, True]  | integer                   | n byte  | -2<sup>8*(n-1)</sup> - 2<sup>8*(n-1)</sup>             |
| int8              | integer                   | 1 byte  | -128 - 127                                             |
| int16             | integer                   | 2 bytes | -32,768 - 32,767                                       |
| int32             | integer                   | 4 bytes | -2,147,483,648 - 2,147,483,647                         |
| int64             | integer                   | 8 bytes | -9,223,372,036,854,775,808 - 9,223,372,036,854,775,807 |
| uint              | any positive integer      | dynamic | 0 - +∞                                                 |
| uint8             | positive integer          | 1 byte  | 0 - 255                                                |
| uint16            | positive integer          | 2 bytes | 0 - 65,535                                             |
| uint32            | positive integer          | 4 bytes | 0 - 4,294,967,295                                      |
| uint64            | positive integer          | 8 bytes | 0 - 18,446,744,073,709,551,615                         |
| float/floating    | floating point number     | 8 bytes | -1.7e308 - 1.7e308                                     |
| float32           | floating point number     | 4 bytes | -3.4e38 - 3.4e38                                       |
| float64           | floating point number     | 8 bytes | -1.7e308 - 1.7e308                                     |
| str/string        | text of any kind          | dynamic |                                                        |
| string[n]         | text with length n        | n bytes |                                                        |
| bytes/binary      | any binary data           | dynamic |                                                        |
| binary[n]         | binary data with length n | n nyte  |                                                        |
| bool/boolean      | boolean value             | 1 byte  | True/False                                             |

#### Why are there so many types?

For optimizations and compatibility with other languages.

##### Optimizations

For example. If you know your number will always be positive.
Then you can reduce the output-size by using `uint` instead of the normal `int`.

In the same way. If you know the number will always be very short (e.g. max 20).
Then you can use `int8` or `uint8` to save the size-byte that is prepended to the normal `int`.

##### Compatibility

If you sent the dumped data over the network to another server that used for example c++ instead of python, then it's a little bit easier to load `uint16` than the dynamic `uint`.

### `dumps()`

> dump any object into bytes

> Note: only annotations of a class are dumped and later reconstructed

```python
def dumps(obj: object) -> bytes: ...
```

### `loads()`

> reconstructs object of `cls` from the dumped data

```python
def loads(dump: bytes | BinaryIO, cls: Type[T]) -> T: ...
```

### `Structure`-class

> This class is only for convenience and wraps the `dumps` and `loads` functions.

```python
class Structure:
    @classmethod
    def load_struct(cls: Type[T], dump: bytes | BinaryIO) -> T: ...
    def dump_struct(self) -> bytes: ...
```
