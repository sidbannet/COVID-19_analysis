"""
Helper tools for plotting.

Author: siddhartha.banerjee
"""

def markers(n: int = None) -> str:
    """Gives out marker definition based on integer number."""

    if n is None:
        raise Exception('Give integer number in argument')
    markers = [
        '.',
        ',',
        'o',
        'v',
        '^',
        '<',
        '>',
        '1',
        '2',
        '3',
        '4',
        '8',
        's',
        'p',
        'P',
        '*',
        'h',
        'H',
        '+',
        'x',
        'X',
        'D',
        'd',
        '|',
        '_',
    ]
    number = n % len(markers)
    return markers[number]