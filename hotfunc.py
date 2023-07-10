import functools
import inspect
import re
import traceback

VERSION = "0.0.1"


def hotreload(func=None, *, reraise=False):
    """
    Make function hot-reloadable.

    This allows to redefine the function in the source code and see
    the changes immediately without restarting the program.

    Keyword args:
        * reraise: bool, default=False

          If `True`, exceptions raised when redefining or calling
          the function will be re-raised. Otherwise, they will be
          printed to stdout and the result from the last good call
          will be returned.
    """

    FUNCTION_NOT_FOUND_ERROR = (
        "Function `{function}` not found in hot-reloaded file.\n\n"
        + "Hot-reloading does not work when function is renamed or removed."
    )

    FUNCTION_LOAD_ERROR = (
        "Exception raised when hot-reloading function `{function}`\n\n"
        + "{traceback}\n\n"
        + "Ignoring exception and returning previous result.\n"
    )

    FUNCTION_CALL_ERROR = (
        "Exception raised when calling hot-reloaded function `{function}` from {filename}:{lineno}\n\n"
        + "{traceback}\n\n"
        + "Ignoring exception and returning previous result.\n"
    )

    def decorator(func):
        file = inspect.getfile(func)

        signature_regex = re.compile(
            r"^(def {function}\(.*\):\w*)$".format(function=func.__name__),
            flags=re.MULTILINE,
        )
        body_end_regex = re.compile(r"^\S", flags=re.MULTILINE)

        result = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal result

            source = open(file).read()
            parts = re.split(signature_regex, source)

            if len(parts) < 3:
                raise Exception(FUNCTION_NOT_FOUND_ERROR.format(function=func.__name__))

            # keep empty lines before function signature to preserve
            # correct line numbers in traceback
            whitespace = parts[0].count("\n") * "\n"

            # we don't want to redefine the original function because it would
            # lose its globals, so we create a dummy function instead
            signature = parts[1].replace(
                "def " + func.__name__,
                "def __hot_" + func.__name__,
                1,
            )

            body = re.split(body_end_regex, parts[2])[0]

            try:
                # define the dummy function with access to the same globals
                # as the original function
                exec(whitespace + signature + body, func.__globals__)
            except Exception as exception:
                if reraise:
                    raise exception

                print(
                    FUNCTION_LOAD_ERROR.format(
                        function=func.__name__, traceback=traceback.format_exc()
                    )
                )

                return result

            try:
                # forward the call to the dummy function and memoize the result
                result = func.__globals__["__hot_" + func.__name__](*args, **kwargs)
            except Exception as exception:
                if reraise:
                    raise exception

                frame = inspect.stack()[1]

                print(
                    FUNCTION_CALL_ERROR.format(
                        function=func.__name__,
                        traceback=traceback.format_exc(),
                        filename=frame.filename,
                        lineno=frame.lineno,
                    )
                )

            return result

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
