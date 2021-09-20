import pytest

from textwrap import dedent
from pathlib import Path

INI = dedent(
    """        
    [HEADER_1]
    int = 1
    float = 3.3
    int_as_str = "1"
    float_as_str = "3.2"
    
    [HEADER_2]
    # some comment
    bool_1 = true
    bool_2 = TruE
    bool_3 = FALSE
    empty = 
    none = None
    dt_fmt= %%d.%%m.%%Y %%H:%%M:%%S
    
    [HEADER_3]
    nested=
        first= 1
        second = two
        third = [2,3,4]
        fourth = 4.3
        fifth = 
    """
)

@pytest.fixture()
def ini(tmp_path):
    ini_path = tmp_path / "test_cfg.ini"
    ini_path.write_text(
        INI
    )
    return ini_path
