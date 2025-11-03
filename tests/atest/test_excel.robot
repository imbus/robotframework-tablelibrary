#*** Settings ***
Library    Tables    file_type=Excel


#*** Test Cases ***
Read Excel File - One File - One Sheet
    Tables.Excel Open    excel_01    ${CURDIR}/testdata/example_02.xlsx
    ${list} =    Tables.Excel Get Open Files
    ${sheet_content} =    Tables.Excel Sheet Read    Sheet1
    Tables.Excel Close    excel_01
    ${list} =    Tables.Excel Get Open Files

Read Excel File - Two Files - One Sheet
    Tables.Excel Open    excel_01    ${CURDIR}/testdata/example_02.xlsx
    Tables.Excel Open    excel_02    ${CURDIR}/testdata/example_02.xlsx
    ${list} =    Tables.Excel Get Open Files
    Tables.Excel File Switch    excel_01
    ${sheet_content} =    Tables.Excel Sheet Read    Sheet1
    Tables.Excel File Switch    excel_02
    ${sheet_content} =    Tables.Excel Sheet Read    Sheet1
    Tables.Excel Close    excel_01
    ${list} =    Tables.Excel Get Open Files
    Tables.Excel Close    excel_02
    ${list} =    Tables.Excel Get Open Files

Read Excel File - One File - Two Sheets - Read All
    Tables.Excel Open    excel_01    ${CURDIR}/testdata/example_06.xlsx
    ${sheet_content} =    Tables.Excel Sheet Read    Personen
    ${sheet_content} =    Tables.Excel Sheet Read    Produkte
    Tables.Excel Close    excel_01

Read Excel File - One File - Two Sheets - Read One Sheet
    # Read sheet via list
    VAR  @{sheets}     Personen
    Tables.Excel Open    excel_01    ${CURDIR}/testdata/example_06.xlsx    ${sheets}
    ${sheets} =    Tables.Excel Get Available Sheets
    Should Contain    ${sheets}    Personen
    ${sheet_content} =    Tables.Excel Sheet Read    Personen
    Should Contain    ${sheet_content}[2]    Bob
    Tables.Excel Close    excel_01

    # Read sheet via string value
    Tables.Excel Open    excel_01    ${CURDIR}/testdata/example_06.xlsx    Produkte
    ${sheets} =    Tables.Excel Get Available Sheets
    Should Contain    ${sheets}    Produkte
    ${sheet_content} =    Tables.Excel Sheet Read    Produkte
    Should Contain    ${sheet_content}[1]    Apfel
    Tables.Excel Close    excel_01

Read Excel Read
    Tables.Excel Open    excel_01    ${CURDIR}/testdata/example_06.xlsx
    ${data} =    Tables.Excel Sheet Read    Personen
    ${sheet_content} =    Tables.Get Table Cell    ${data}   0    1
    ${names} =    Tables.Get Table Column    ${data}    Name
    Should Contain    ${names}    Charlie
    ${ages} =    Tables.Get Table Column    ${data}    Alter
    Should Contain    ${ages}    ${35}
    ${names} =    Tables.Get Table Column    ${data}    ${0}
    Should Contain    ${names}    Charlie
    ${ages} =    Tables.Get Table Column    ${data}    ${1}
    Should Contain    ${ages}    ${35}
    