*** Settings ***
Library    Tables    file_type=CSV    delimiter=,


*** Test Cases ***
Read CSV File - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
    BuiltIn.Should Be True    ${result}

Read CSV File - With Header - New Delimiter
    [Setup]    Tables.Configure Delimiter    ;
    [Teardown]    Tables.Configure Delimiter    ,
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_04.csv
    ${result} =    BuiltIn.Evaluate    "${content}[0][1]" == "temp"
    BuiltIn.Should Be True    ${result}

Read CSV File - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${result} =    BuiltIn.Evaluate    "index" not in "${content}"
    BuiltIn.Should Be True    ${result}

Read Excel File - With Header
    Tables.Configure File Type    Excel
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_02.xlsx
    ${result} =    BuiltIn.Evaluate    "${content}[Sheet1][0][0]" == "_time"
    BuiltIn.Should Be True    ${result}

Read Excel File - Without Header
    Tables.Configure File Type    Excel
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_02.xlsx
    ${result} =    BuiltIn.Evaluate    "_time" not in "${content}[Sheet1]"
    BuiltIn.Should Be True    ${result}

Read Parquet File - With Header - Raw Timestamp Object
    Tables.Configure File Type    Parquet
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    BuiltIn.Should Be True    ${result}

Read Parquet File - With Header - Normal DateTime Strings
    Tables.Configure File Type    Parquet
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_05.parquet
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    BuiltIn.Should Be True    ${result}

Read Parquet File - Without Header
    Tables.Configure File Type    Parquet
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${result} =    BuiltIn.Evaluate    "_time" not in "${content}"
    BuiltIn.Should Be True    ${result}

Read Table Row - CSV
    
    Tables.Configure Ignore Header    False
    Tables.Configure File Type    CSV
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${row_01} =    Tables.Read Table Row    ${content}    0
    ${row_02} =    Tables.Read Table Row    ${content}    1
    BuiltIn.Should Contain    ${row_01}    alex
    BuiltIn.Should Contain    ${row_02}    30

