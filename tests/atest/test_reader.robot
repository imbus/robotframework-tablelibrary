*** Settings ***
Library    Tables    file_type=CSV


*** Test Cases ***
Read CSV File
    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv