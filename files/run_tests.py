#!/usr/bin/python3
import pytest
import sys
import json

def main():
    """
    :return: 1 if test failed ; 0 if none of the tests failed
    """
    tests_file=sys.argv[1]
    test_info_json=sys.argv[2]
    print(json.loads(test_info_json))
    status=pytest.main([tests_file])
    return_code=int(not((str(status)=="ExitCode.OK")))
    return return_code

if __name__ == '__main__':
    rc=main()
    sys.exit(rc)
