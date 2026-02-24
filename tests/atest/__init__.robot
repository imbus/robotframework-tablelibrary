*** Settings ***
Library    Tables
Suite Setup    Suite Setup & Teardown - Verify Scope Settings
Suite Teardown    Suite Setup & Teardown - Verify Scope Settings


*** Keywords ***
Suite Setup & Teardown - Verify Scope Settings
    VAR    @{header} =    name    age
    Tables.Create Table    ${header}
    Tables.Insert Row    ${{["peter", "55"]}}    -1
    Tables.Insert Row    ${{["marvin", "26"]}}    -1
    ${table} =    Tables.Get Table
    Should Be Equal    ${table}[0][0]   name
    Should Be Equal    ${table}[1][0]   peter
    Should Be Equal    ${table}[2][0]   marvin
    Log  1234