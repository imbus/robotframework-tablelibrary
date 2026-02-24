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
    Log  1234