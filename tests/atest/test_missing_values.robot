*** Settings ***
Library    Tables    missing_as_none=True
Library    Collections


*** Test Cases ***
Missing Values - Library Argument Returns None
    ${data} =    Tables.Read Table    ${CURDIR}${/}testdata${/}missing_values.csv
    @{header} =    Create List    name    email    empty
    Lists Should Be Equal    ${data}[0]    ${header}
    Should Be Equal    ${data}[1][2]    ${None}
    Should Be Equal    ${data}[2][1]    ${None}

    Tables.Open Table    ${CURDIR}${/}testdata${/}missing_values.csv    missing
    ${cell} =    Tables.Get Table Cell    1    email
    Should Be Equal    ${cell}    ${None}
    ${column} =    Tables.Get Table Column    empty
    @{empty_column} =    Create List    ${None}    ${None}
    Lists Should Be Equal    ${column}    ${empty_column}
    ${row} =    Tables.Get Table Row    2
    @{expected_row} =    Create List    Bob    ${None}    ${None}
    Lists Should Be Equal    ${row}    ${expected_row}

Missing Values - Configuration Keyword Toggles Conversion
    Tables.Configure Missing As None    False
    ${data} =    Tables.Read Table    ${CURDIR}${/}testdata${/}missing_values.csv
    Should Not Be Equal    ${data}[1][2]    ${None}

    Tables.Configure Missing As None    True
    ${data} =    Tables.Read Table    ${CURDIR}${/}testdata${/}missing_values.csv
    Should Be Equal    ${data}[1][2]    ${None}
