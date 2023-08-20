from typing import Callable, Optional


def mappy(
    value: str,
    matcher: str
    | dict
    | tuple
    | list
    | Callable[[str, Optional[str]], Optional[str | bool]],
    default: Optional[str] = None,
):
    """Will try to match value with the matcher.

    If `default` is not provided and mappy cannot match the variable. it will raise an error.

    Note
    ----
    During DAG building phase, using mappy results

    Parameters
    ----------
    value: str
        the value to resolve using the matcher

    matcher: str, dict, tuple, list, callable
        holds the values to compare to.
        Depending on the type of the matcher, it will behave differently:

        str: will check if `value == matcher`, if so returns `value`
            returns `default` or raises ValueError otherwise

        dict: if `value` is present as a key, will return the corresponding `value`
            returns `default` or raises ValueError otherwise

        tuple, list: checks if `value` is present in the tuple/list
            returns `default` or raises ValueError otherwise

        callable:  (`value`: str, `default`: str) -> bool, str, None
            if the result is not None, mappy returns the result
            returns `default` or raises ValueError otherwise

    default: str, None
        defined, it will be returned if value cannot resolve using matcher.
        if None, mappy will raise ValueError if value is None

    Examples
    --------

    >>> from snakemake.rules import Params
    >>> params = Params(fromdict={"param1": "value 1", "param2": "value2"})

    Exact match

    >>> mappy(params.param1, "value 1")
    'value 1'

    >>> mappy(params.param1, "does not exist")
    Traceback (most recent call last):
    ...
    ValueError: ("'value 1' does not match given value and no default value have been defined", 'value 1', 'does not exist')

    Using a tuple of allowed values

    >>> mappy(params.param1, ("value 1", "other allowed value"))
    'value 1'

    >>> mappy(params.param1, ("value11", "other allowed value"))
    Traceback (most recent call last):
    ...
    ValueError: ("'value 1' does not match given values and no default value have been defined", 'value 1', ('value11', 'other allowed value'))

    Using a list of allowed values

    >>> mappy(params.param1, ["value 1", "other value"])
    'value 1'

    >>> mappy(params.param1, ["value11", "other value"])
    Traceback (most recent call last):
    ...
    ValueError: ("'value 1' does not match given values and no default value have been defined", 'value 1', ['value11', 'other value'])

    Using a dictionary for existing values and mapping

    >>> mappy(params.param1, {'value 1': 'another object', 'other accepted': 'Hello World'})
    'another object'

    >>> mappy(params.param1, {'value11': 'will raise an error'})
    Traceback (most recent call last):
    ...
    ValueError: ("'value 1' does not match given values and no default value have been defined", 'value 1', {'value11': 'will raise an error'})

    Using a function

    >>> mappy(params.param1, lambda needle, default : needle+" augmented")
    'value 1 augmented'

    >>> def validation(needle, default):
    ...     return needle if needle.startswith('value') else None
    >>> mappy(params.param1, validation)
    'value 1'
    """
    if isinstance(matcher, str):
        if matcher == value:
            return value
        else:
            if default == None:
                error_msg = f"{value!r} does not match given value and no default value have been defined"
                raise ValueError(error_msg, value, matcher)
            return default

    elif isinstance(matcher, dict):
        try:
            return matcher[value]
        except KeyError:
            pass

        if default == None:
            error_msg = f"{value!r} does not match given values and no default value have been defined"
            raise ValueError(error_msg, value, matcher)
        return default

    elif isinstance(matcher, (tuple, list)):
        if value in matcher:
            return value
        else:
            if default == None:
                error_msg = f"{value!r} does not match given values and no default value have been defined"
                raise ValueError(error_msg, value, matcher)

            return default

    elif callable(matcher):
        result = matcher(value, default)
        if result != None:
            return result

        if default != None:
            return default

        error_msg = f"passing {value!r} through {matcher!r} returned None and no default value have been defined"
        raise ValueError(error_msg, value, matcher)

    return value
