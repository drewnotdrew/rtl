import functools
from typing import List


def repeat(num_repeats: int):
    """
    Repeat a cocotb test a specified amount of times.

    Useful for repeated random testing.

    Args:
      num_repeats (int): The number of times to repeat a test.
    """

    def decorator_repeat(func):

        @functools.wraps(func)
        async def wrapper_repeat(*args, **kwargs):
            for _ in range(0, num_repeats):
                await func(*args, **kwargs)

        return wrapper_repeat

    return decorator_repeat


def parameterize(parameter_name: str, values: List[int]):
    """
    Parameterize an input to a dut in a cocotb test.

    Tests using this decorator must provide the parameter as an input.

    Args:
      parameter_name (str): The name of the parameter to parameterize in the
        verilog source.
      values (List[int]): The list of values to test.
    """

    def decorator_parameterize(func):

        @functools.wraps(func)
        async def wrapper_parameterize(*args, **kwargs):
            for value in values:
                kwargs[parameter_name] = value
                await func(*args, **kwargs)

        return wrapper_parameterize

    return decorator_parameterize
