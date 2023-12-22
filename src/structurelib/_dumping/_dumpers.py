# -*- coding=utf-8 -*-
r"""

"""
import struct
import typing as t
from ..types import *


__all__ = [
    'dump_int', 'load_int',
    'dump_float', 'load_float',
    'dump_str', 'load_str',
    'dump_bytes', 'load_bytes',
    'dump_bool', 'load_bool',
]


def dump_int(value: int, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    signed = next(args, True)
    if length is not None:
        return int.to_bytes(value, length, "big", signed=signed)
    else:
        # todo: fix this try-error style
        n_bytes = 1
        while True:
            try:
                dump = int.to_bytes(value, n_bytes, "big", signed=signed)
            except OverflowError:
                n_bytes += 1
                continue
            else:
                return int.to_bytes(n_bytes, 1, "big", signed=False) + dump


def load_int(stream: t.BinaryIO, hint: t.TypeAlias) -> int:
    args = iter(t.get_args(hint))
    length = next(args, None)
    signed = next(args, True)
    if length is not None:
        return int.from_bytes(stream.read(length), "big", signed=signed)
    else:
        length = int.from_bytes(stream.read(1), "big", signed=False)
        return int.from_bytes(stream.read(length), "big", signed=signed)


def dump_float(value: float, hint: t.TypeAlias) -> bytes:
    fmt = '!f' if hint == float32 else '!d'
    return struct.pack(fmt, value)


def load_float(stream: t.BinaryIO, hint: t.TypeAlias) -> float:
    fmt = '!f' if hint == float32 else '!d'
    return struct.unpack(fmt, stream.read(struct.calcsize(fmt)))[0]


def dump_str(value: str, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    encoded = value.encode()
    if length is not None:
        if len(encoded) > length:
            raise ValueError(f"{value!r} is longer than {length} bytes")
        return encoded.ljust(length, b'\0')
    else:
        return int.to_bytes(len(encoded), 1, byteorder="big") + encoded


def load_str(stream: t.BinaryIO, hint: t.TypeAlias) -> str:
    args = iter(t.get_args(hint))
    length = next(args, None)
    if length is not None:
        return stream.read(length).rstrip(b'\0').decode()
    else:
        length = int.from_bytes(stream.read(1), byteorder="big")
        return stream.read(length).decode()


def dump_bytes(value: bytes, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    if length is not None:
        if len(value) > length:
            raise ValueError(f"{value!r} is longer than {length} bytes")
        return value.ljust(length, b'\0')
    else:
        return int.to_bytes(len(value), 1, byteorder="big") + value


def load_bytes(stream: t.BinaryIO, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    if length is not None:
        return stream.read(length).rstrip(b'\0')
    else:
        length = int.from_bytes(stream.read(1), byteorder="big")
        return stream.read(length)


def dump_bool(value: bool, _hint: t.TypeAlias) -> bytes:
    return b'\x01' if value else b'\x00'


def load_bool(stream: t.BinaryIO, _hint: t.TypeAlias) -> bool:
    return stream.read(1) != b'\x00'
