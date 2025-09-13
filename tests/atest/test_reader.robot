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

Read CSV File - Return Dict Object
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv    Dicts
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

Get Table Cell - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Cell    ${content}    1    0    ==    1

Get Table Cell - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${cell_value} =    Get Table Cell    ${content}    1    1    ==    alex

Get Table Cell - CSV - With Header - Column Name
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Cell    ${content}    1    name    ==    sascha

Get Table Column - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Column    ${content}    1    contains    alex
    Get Table Column    ${content}    1    not contains    franz

Get Table Column - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Get Table Column    ${content}    name    contains    alex
    Get Table Column    ${content}    name    not contains    franz

Get Table Row - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Get Table Row    ${content}    0    contains    alex

Get Table Row - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Get Table Row    ${content}    0    contains    age

Get Row and Column Count - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Count Table    ${content}    Rows     ==    ${6}
    Tables.Count Table    ${content}    Columns    ==    ${3}

Get Row and Column Count - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Count Table    ${content}    Rows     ==    ${5}
    Tables.Count Table    ${content}    Columns    ==    ${3}

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

Read Parquet File - With Header - Normal DateTime Strings
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_05.parquet
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    BuiltIn.Should Be True    ${result}

Read Parquet File - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${result} =    BuiltIn.Evaluate    "_time" not in "${content}"
    BuiltIn.Should Be True    ${result}

Get Table Cell - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${cell_value} =    Get Table Cell    ${content}    1    1    ==    ${4.76}

Get Table Cell - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${cell_value} =    Get Table Cell    ${content}    1    1    ==    ${0.81}

Get Table Cell - Parquet - With Header - Column Name
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${cell_value} =    Get Table Cell    ${content}    1    _strom    ==    ${4.76}

Get Table Column - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Get Table Column    ${content}    1    contains    ${4.0}

Get Table Column - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Get Table Column    ${content}    _strom    contains    ${4.0}

Get Table Row - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Get Table Row    ${content}    0    contains    ${0.81}

Get Table Row - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Get Table Row    ${content}    0    contains    _strom

Get Row and Column Count - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Count Table    ${content}    Rows     ==    ${1001}
    Tables.Count Table    ${content}    Columns    ==    ${2}

Get Row and Column Count - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Count Table    ${content}    Rows     ==    ${1000}
    Tables.Count Table    ${content}    Columns    ==    ${2}

