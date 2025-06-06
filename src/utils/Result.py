# Generated by ChatGPT

from typing import Generic, TypeVar, Optional

T = TypeVar('T') # It is convention to use 'T' for generic types

class Result(Generic[T]):
    def __init__(self, success: bool, message: str, data: Optional[T] = None):
        self.success = success
        self.message = message
        self.data = data

    def __str__(self):
        return f"self.success: {self.success}, self.message: {self.message}"
