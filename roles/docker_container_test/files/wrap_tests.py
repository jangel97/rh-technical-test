#!/usr/bin/python3
import pytest
import sys
import json

from collections import defaultdict

"""

posible mejora hacer checks 


"""

def main():
    """
    :return: 1 if test failed ; 0 if none of the tests failed ; 2 if test crashed
    """
    tests_file=sys.argv[1]
    test_info_json=sys.argv[2]
    status=pytest.main([tests_file])
    return_code=defaultdict(lambda: "2")
    return_code["ExitCode.OK"]=0
    return_code["ExitCode.TESTS_FAILED"]=1
    return_code["ExitCode.INTERRUPTED"]=2
    return return_code[str(status)]

if __name__ == '__main__':
    rc=main()
    sys.exit(rc)
