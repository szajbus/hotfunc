# hotfunc

This package provides a decorator for hot-reloading python functions.

It allows to redefine the function in the source code and see the changes immediately without restarting the program.

## Installation

Install with `pip`

```bash
$ python -m pip install hotfunc
```

## Usage

The following example uses the REPL, but `hotfunc` can be used in any python program.

Begin with importing the module and decorating the function that you want to hot-reload.

```python
# myfile.py
from hotfunc import hotreload

name = "Mike"

@hotreload
def say():
    print(f"Hello world! My name is {name}.")
```

Start python REPL, import the source file and call your function.

```
>>> from myfile import say
>>> say()
Hello world! My name is Mike.
```

Now, without stopping the interpreter, edit the source file changing the decorated function's body.

```python
# myfile.py
from hotfunc import hotreload

name = "Mike"

@hotreload
def say():
    print(f"Ciao mondo! Mi chiamo {name}.")
```

Switch back to REPL and call the function again.

```
>>> say()
Ciao mondo! Mi chiamo Mike.
```

As you can see, the function has been redefined, but its local environment (`name` variable defined outside the function) was preserved.

## Caveats

When hot-reloading a function, its source file is read, definition found and the function itself redefined. Currenty **it is done on every call**, so is rather slow.

As of now, only top-level functions (defined at indentation level zero) are supported.

By default, exceptions raised when redefining or calling hot-reloaded functions are not re-raised. Instead, they are printed to `stdout` and the result of last successful function call is returned. This behaviour can be changed by enabling `reraise` flag:

```python
@hotreload(reraise=True)
def myfunc():
    # ...
```

## License

Copyright (c) 2023 Michał Szajbe

Licensed under [The MIT License](LICENSE).
