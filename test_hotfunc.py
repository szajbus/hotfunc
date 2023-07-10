import sys

DUMMY_MODULE = """
from hotfunc import hotreload

@hotreload
def say():
    return {result}
"""


def write_file(path, result):
    with open(path, "w") as file:
        file.write(DUMMY_MODULE.format(result=result))


def test_hotreload(tmp_path):
    sys.path.append(str(tmp_path))
    write_file(tmp_path / "dummy.py", "\"Hello\"")

    print(sys.path)
    import dummy

    assert dummy.say() == "Hello"

    write_file(tmp_path / "dummy.py", "\"Ciao\"")
    assert dummy.say() == "Ciao"
