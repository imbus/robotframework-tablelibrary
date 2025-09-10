*** Settings ***
Library    Tables    delimiter=,


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

Read Table Cell - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Read Table Cell    ${content}    1    0    ==    1

Read Table Cell - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    ${cell_value} =    Read Table Cell    ${content}    1    1    ==    alex

Read Table Cell - CSV - With Header - Column Name
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Read Table Cell    ${content}    1    name    ==    sascha

Read Table Cell - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${cell_value} =    Read Table Cell    ${content}    1    1    ==    ${4.76}

Read Table Cell - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${cell_value} =    Read Table Cell    ${content}    1    1    ==    ${0.81}

Read Table Cell - Parquet - With Header - Column Name
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    ${cell_value} =    Read Table Cell    ${content}    1    _strom    ==    ${4.76}

Read Table Column - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Read Table Column    ${content}    1    contains    alex
    Read Table Column    ${content}    1    not contains    franz

Read Table Column - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Read Table Column    ${content}    name    contains    alex
    Read Table Column    ${content}    name    not contains    franz

Read Table Column - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Read Table Column    ${content}    1    contains    ${4.0}

Read Table Column - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Read Table Column    ${content}    _strom    contains    ${4.0}

Read Table Row - CSV - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Read Table Row    ${content}    0    contains    alex

Read Table Row - CSV - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    Tables.Read Table Row    ${content}    0    contains    age

Read Table Row - Parquet - Without Header
    Tables.Configure Ignore Header    True
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Read Table Row    ${content}    0    contains    ${0.81}

Read Table Row - Parquet - With Header
    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_03.parquet
    Tables.Read Table Row    ${content}    0    contains    _strom

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

