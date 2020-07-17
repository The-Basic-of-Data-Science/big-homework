# -*- coding: utf-8 -*-
from pylint import epylint as lint
import re

def load_code_style_score(path):
    if (path == ""):
        return
    (pylint_stdout, pylint_stderr) = lint.py_run(path, return_std=True)

    pylint_stdout.seek(0)
    stdout = []
    while True:
        strBuf = pylint_stdout.readline()
        if strBuf == "":
            break
        stdout.append(strBuf.strip())
    stdout = '\n'.join(stdout)
    print(stdout)
    matchObj = re.search('Your code has been rated at (.*)/10', stdout)

    if (matchObj == None):
        score = -1
    else:
        score = eval(matchObj.group(0).split("/")[0].split(" ")[-1])
    print(score)

if __name__ == '__main__':
    # load_code_style_score('OurModelOutPut\python_source\\test_data_1\Python\\3544\\2908\\252578_result1582558143535.py')
    from operator import itemgetter
    student_tuples = [[1,2,3],[1,1,3],[0,1,3]]
    student_tuples.sort(key=itemgetter(0, 1))
    print(student_tuples)