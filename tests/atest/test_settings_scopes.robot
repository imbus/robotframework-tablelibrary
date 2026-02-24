*** Settings ***
Library   Tables    ignore_header=True
Suite Setup    Suite Setup & Teardown - Verify Scope Settings
Suite Teardown    Suite Setup & Teardown - Verify Scope Settings


*** Test Cases ***
TC-000 - Verify Test Setup & Teardown
    [Setup]    Suite Setup & Teardown - Verify Scope Settings
    [Teardown]    Suite Setup & Teardown - Verify Scope Settings
    Log    Verify Test Setup and Teardown

TC-001 - Suite Scope - Change Parameter with Scope - Ignore Header - False
    [Documentation]    Set config parameter with suite scope
    [Setup]    Configure Ignore Header    ${True}
    &{cfg} =    Tables.Get Library Configuration
    Should Be Equal    ${cfg.ignore_header}    ${True}

    Tables.Configure Ignore Header    False    Suite
    &{cfg} =    Tables.Get Library Configuration
    Should Be Equal    ${cfg.ignore_header}    ${False}

TC-001 - Suite Scope - Parameter Should Be - Ignore Header - False
    [Documentation]    Config parameter should still have new value due to suite scope.
    &{cfg} =    Tables.Get Library Configuration
    Should Be Equal    ${cfg.ignore_header}    ${False}

TC-002 - Test Scope - Change Parameter - Ignore Header - False
    [Documentation]    Set config parameter with test scope
    [Setup]    Configure Ignore Header    ${True}

    &{cfg} =    Tables.Get Library Configuration
    Should Be Equal    ${cfg.ignore_header}    ${True}

    Tables.Configure Ignore Header    False    Test
    &{cfg} =    Tables.Get Library Configuration
    Should Be Equal    ${cfg.ignore_header}    ${False}

TC-002 - Test Scope - Parameter Should Be - Ignore Header - True
    [Documentation]    Config parameter from previous test case should be reverted due to test scope
    &{cfg} =    Tables.Get Library Configuration
    Should Be Equal    ${cfg.ignore_header}    ${True}


*** Keywords ***
Suite Setup & Teardown - Verify Scope Settings
    VAR    @{header} =    name    age
    Configure Ignore Header    False
    Tables.Create Table    ${header}
    Tables.Append Row    ${{["peter", "55"]}}
    Tables.Set Table Row    ${{["peter", "55"]}}    0
    Tables.Insert Row    ${{["peter", "55"]}}    -1
    Tables.Insert Row    ${{["marvin", "26"]}}    -1
    ${table} =    Tables.Get Table
    Tables.Write Table    ${table}    ${CURDIR}${/}results${/}setupteardown.csv
