*** Settings ***
Library    Tables    separator=,


*** Test Cases ***
########################################################################################
# CSV
########################################################################################
Read CSV File - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
    BuiltIn.Should Be True    ${result}

Read CSV File - Return Table Object
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv    List of dicts
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv    List of lists
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv    Dataframe
    Log    123

Read CSV File - With Header - New Delimiter
    [Setup]    Tables.Configure Separator    ;
    [Teardown]    Tables.Configure Separator    ,
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_04.csv
    ${result} =    BuiltIn.Evaluate    "${content}[0][1]" == "temp"
    BuiltIn.Should Be True    ${result}

Read CSV File - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${result} =    BuiltIn.Evaluate    "index" not in "${content}"
    BuiltIn.Should Be True    ${result}

Open CSV Files - With Header
    [Tags]    skip_file
    VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
    VAR    ${file_path_2}    ${CURDIR}${/}testdata${/}example_04.csv  
    ${uuid} =    Tables.Open Table   ${file_path}
    ${uuid2} =    Tables.Open Table   ${file_path_2}
    Should Not Be Equal As Strings    ${uuid}    ${uuid2}
    Tables.Get Table
    Tables.Switch Table    ${uuid}
    Tables.Get Table


Get Table Cell - CSV - Without Header
    Tables.Configure Ignore Header    True
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Cell    1    0    ==    1

Get Table Cell - CSV - With Header
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Cell    1    1    ==    alex

Get Table Cell - CSV - With Header - Column Name
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Cell    1    name    ==    sascha

Get Table Column - CSV - Without Header
    Tables.Configure Ignore Header    True
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Column    1    contains    alex
    Get Table Column    1    not contains    franz

Get Table Column - CSV - With Header
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Column    name    contains    alex
    Get Table Column    name    not contains    franz

Get Table Row - CSV - Without Header
    Tables.Configure Ignore Header    True
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Get Table Row    0    contains    alex

Get Table Row - CSV - With Header
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Get Table Row    0    contains    age

Get Row and Column Count - CSV - With Header
    Tables.Configure Ignore Header    False
    VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
    ${uuid} =    Tables.Open Table    ${file_path}
    Tables.Count Table    ${uuid}    Rows     ==    ${6}
    Tables.Count Table    ${uuid}    Columns    ==    ${3}

Count Table Rows with Validation Operator
    Tables.Configure Ignore Header    False
    VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
    ${uuid} =    Tables.Open Table    ${file_path}
    Tables.Count Table    ${uuid}    Rows    validate    5 < value < 7

Get Row and Column Count - CSV - Without Header
    Tables.Configure Ignore Header    True
    VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
    ${uuid} =    Tables.Open Table    ${file_path}
    Tables.Count Table    ${uuid}    Rows     ==    ${5}
    Tables.Count Table    ${uuid}    Columns    ==    ${3}
Read Row Count - CSV - With Header
    Tables.Configure Ignore Header    False
    VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
    ${row_count}  Tables.Count Table    ${file_path}    Rows
    BuiltIn.Should Be Equal    ${row_count}    ${6}

########################################################################################
# TXT
########################################################################################
Read TXT File as CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.txt
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
    BuiltIn.Should Be True    ${result}

Read TXT File as CSV - With Header - New Delimiter
    [Setup]    Tables.Configure Separator    ;
    [Teardown]    Tables.Configure Separator    ,
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_04.txt
    ${result} =    BuiltIn.Evaluate    "${content}[0][1]" == "temp"
    BuiltIn.Should Be True    ${result}

Read TXT File as CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.txt
    ${result} =    BuiltIn.Evaluate    "index" not in "${content}"
    BuiltIn.Should Be True    ${result}

########################################################################################
# PARQUET
########################################################################################
Read Parquet File - With Header - Raw Timestamp Object
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    BuiltIn.Should Be True    ${result}

Read Parquet File - Normal DateTime Strings
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_05.parquet
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    BuiltIn.Should Be True    ${result}

Read Parquet File - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${result} =    BuiltIn.Evaluate    "_time" not in "${content}"
    BuiltIn.Should Be True    ${result}

Get Table Cell - Parquet
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Get Table Cell    1    1    ==    ${4.76}

Get Table Cell - Parquet - Column Name
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Get Table Cell    1    _strom    ==    ${4.76}

Get Table Column - Parquet
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Get Table Column    _strom    contains    ${4.0}


#TODO: In order for parquet to get header names a new keyword might be needed (ie. Get Table Header)
Get Table Row - Parquet - With Header
    Tables.Configure Ignore Header    False
    Tables.Open Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Get Table Row    0    contains    ${0.81}

Get Row and Column Count - Parquet
    ${uuid} =    Tables.Open Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Count Table    ${uuid}    Rows     ==    ${1001}
    Tables.Count Table    ${uuid}    Columns    ==    ${2}

Read Row and Column Count - Parquet
    Tables.Configure Ignore Header    False
    VAR     ${parquet_path}    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Count Table    ${parquet_path}    Rows     ==    ${1001}
    Tables.Count Table    ${parquet_path}    Columns    ==    ${2}
    Tables.Configure Ignore Header    True
    Tables.Count Table    ${parquet_path}    Rows     ==    ${1000}
    Tables.Count Table    ${parquet_path}    Columns    ==    ${2}


