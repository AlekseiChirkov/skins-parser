import os
from typing import Callable


def clean_directory(directories: list) -> Callable:
    """
    Decorator to clean directory from all files
    :param directories: list with string paths to directory
    :return: func
    """

    def decorator(function: Callable) -> Callable:
        """
        Decorator
        :param function: function to wrap
        :return: Callable function
        """

        def wrapper() -> Callable:
            """
            Wrapper to process cleaning directory
            :return: Callable function
            """

            for directory in directories:
                pages = os.listdir(directory)
                for page in pages:
                    os.remove(directory + page)

            return function()

        return wrapper

    return decorator
