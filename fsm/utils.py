import inspect
from typing import Callable


def get_function_kwargs(func: Callable, **kwargs: dict) -> dict:
    """入力関数に必要なキーワード引数のみに選定"""
    arg_names = inspect.signature(func).parameters
    func_kwargs = {arg_name: kwargs[arg_name] for arg_name in arg_names.keys() if arg_name in kwargs}
    return func_kwargs
