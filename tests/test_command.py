import re
from subprocess import check_output


def test_command():
    output = check_output(['clk', 'command'], encoding='utf8')
    assert re.search(r'flowdep\s+Manipulate command flow dependencies\.', output)
