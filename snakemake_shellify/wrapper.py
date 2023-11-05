from collections import UserString
from functools import wraps
import inspect
from types import MethodType
from typing import Any, Callable


class ShellString(UserString):
    def __init__(self, fn: Callable) -> None:
        super().__init__({})
        self.callable = fn

    def __str__(self):
        return (
            f"ShellString({self.callable.__name__}{inspect.signature(self.callable)})"
        )


class ShellStringFormatter:
    def __init__(self, format: Callable) -> None:
        self._format = format

    def __call__(self, instance, shell_str, /, *args, **kwargs: Any) -> Any:
        if not isinstance(shell_str, ShellString):
            # passthrough
            return self._format(instance, shell_str, *args, **kwargs)

        argspec = inspect.getfullargspec(shell_str.callable)
        filtered_args: Any = kwargs
        if not argspec.varkw:
            filtered_args = {
                key: value for key, value in kwargs.items() if key in argspec.args
            }

        return self._format(
            instance, shell_str.callable(**filtered_args), *args, **kwargs
        )

    def __get__(self, instance, owner):
        return MethodType(self, instance) if instance else self


def shellify(decorated: Callable):
    from snakemake.utils import SequenceFormatter

    # overwrite default snakemake string formatter to one that supports function evaluation
    if not isinstance(SequenceFormatter.format, ShellStringFormatter):
        SequenceFormatter.format = ShellStringFormatter(SequenceFormatter.format)

    @wraps(decorated)
    def decorator():
        return ShellString(decorated)

    return decorator
