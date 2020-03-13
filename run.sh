#!/bin/bash
# Script for running the tests

if [[ "$1" == "-h" ]];
then
    echo "Usage:"
    echo "-r    Runs the test for parser"
    echo "-c    Runs test coverage for parser"
    echo "-rh   Runs mutex coverage for parser and makes a html report"
    echo "-rm   Runs the mutex report for parser and makes a text report"
elif [[ "$1" == "-r" ]];
then
    pytest tests/test_parser.py
#-c runs the coverage for test_parser
elif [[ "$1" == "-c" ]]; 
then
    if [ -d "htmlcov" ];
    then
        rm -rf htmlcov
    fi
    python -m pytest --cov=test_parser
    coverage html tests/test_parser.py
#runs the mutex tests for test_parser and makes an html report
elif [[ "$1" == "-rh" ]];
then
    mut.py --target npc/parser.py --unit-test tests/test_parser.py --runner pytest --report-html mutpy_report/
#runs the mutex tests for test_parser and returns the results to a text
#file in mutpy_report as result.txt
elif [[ "$1" == "-rm" ]];
then
    echo "Writing report..."
    mut.py --target npc/parser.py --unit-test tests/test_parser.py --runner pytest -m > "mutpy_report/result.txt"
    echo "Report complete."
else
    echo "Command not found."
    echo "use -h for help."
fi
