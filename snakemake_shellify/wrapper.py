from collections import UserString
from functools import wraps
import inspect
from typing import Any, Callable, LiteralString


class ShellString(UserString):
    def __init__(self, seq: object, fn: Callable) -> None:
        super().__init__(seq)
        self.fn = fn

    def __str__(self):
        return f"<wrappy: {self.fn.__name__}{inspect.signature(self.fn)}>"


def formatter_decorator(*args, **kwargs) -> LiteralString:
    self, wrappy = args

    if not isinstance(wrappy, ShellString) or wrappy.fn is None:
        # passthrough
        return formatter_decorator.__format(*args, **kwargs)

    fn = wrappy.fn
    argspec = inspect.getfullargspec(fn)
    filtered_args: Any = kwargs
    if not argspec.varkw:
        filtered_args = {
            key: value for key, value in kwargs.items() if key in argspec.args
        }

    return formatter_decorator.__format(self, fn(**filtered_args), **kwargs)


def shellify(decorated: Callable):
    from snakemake.utils import SequenceFormatter

    # overwrite default snakemake string formatter to one that supports function evaluation
    if SequenceFormatter.format is not formatter_decorator:
        formatter_decorator.__format = SequenceFormatter.format

        SequenceFormatter.format = formatter_decorator

    @wraps(decorated)
    def decorator():
        return ShellString({}, decorated)

    return decorator
