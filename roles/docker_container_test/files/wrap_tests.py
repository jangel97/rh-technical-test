#!/usr/bin/python3
"""
The purpose of this python script is to start the pytest script.
This script will receive a json parameter. The script will validate that the json is parseable
Once the pytest script ends, this script will set the return code depending on the execution of the pytest script.
Return code will be:
    - 0 if all tests ran successfully
    - 1 if any test failed
    - 2 if pytest script crashed
"""
import pytest
import sys
import json
import logging
from collections import defaultdict

logger=logging.getLogger('TEST_WRAPPER')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    """
    :return: 1 if test failed ; 0 if none of the tests failed ; 2 if test crashed
    """
    DEFAULT_RETURN_CODE=2
    return_code=defaultdict(lambda: DEFAULT_RETURN_CODE)
    return_code["ExitCode.OK"]=0
    return_code["ExitCode.TESTS_FAILED"]=1
    return_code["ExitCode.INTERRUPTED"]=2
    logger.info("Wrapper test is executing...")
    
    tests_file=sys.argv[1]
    test_params_json=sys.argv[2]
    logger.info("Test to execute is: "+tests_file)
    logger.info("Proceeding to parse json params: "+test_params_json)
    
    try:
      json.loads(test_params_json)
    except:
      logger.error("Unable to parse json: "+test_params_json)
      return DEFAULT_RETURN_CODE

    logger.info("Test parameters: "+test_params_json)
      
    status=str(pytest.main([tests_file]))
    
    logger.info("Pytest output was: "+status)
    
    return return_code[status]

if __name__ == '__main__':
    rc=main()
    sys.exit(rc)
