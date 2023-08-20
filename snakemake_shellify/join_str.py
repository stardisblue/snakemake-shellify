def join_str(*args, sep=" \\\n"):
    r"""Joins argument strings using joiner attribute.

    Will ignore Falsy strings

    Parameters
    ----------
    *args: str[]
        strings to join together
    sep: str, default=`' \\n'`
        string used to join `*args`, default allows newline for cmds

    Returns
    -------
    the joined string

    Example
    -------

    >>> join_str('a', 'b', 'c', sep=" ")
    'a b c'

    >>> join_str('a', 'b', 'c', sep=', ')
    'a, b, c'
    """
    return sep.join(filter(None, args))
