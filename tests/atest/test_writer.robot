*** Settings ***
Library     Tables    file_type=CSV
Library     Collections
Library     OperatingSystem
Library     String


*** Test Cases ***    
Write Excel File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.xlsx
    
########################################################################################
# TXT
########################################################################################
Write CSV to TXT File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.txt
    BuiltIn.Log    ${file_path}
    BuiltIn.Should Contain    ${file_path}    results/test_writer.txt

Write CSV to TXT File - Quoting
    [Teardown]    Configure Quoting    MINIMAL
    Configure Quoting Character    '
    Configure Quoting    ALL
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.txt
    BuiltIn.Log    ${file_path}
    BuiltIn.Should Contain    ${file_path}    results/test_writer.txt
    ${content} =    Tables.Read Table    ${file_path}
    Should Contain    ${content}[1]    '2025'
    Should Contain    ${content}[1]    '30'

    
########################################################################################
# CSV
########################################################################################
Write CSV File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv
    BuiltIn.Log    ${file_path}
    BuiltIn.Should Contain    ${file_path}    results/test_writer.csv

Write CSV File - Without Header
    VAR    @{data_00} =    2026    31
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${data_00}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer_2.csv

Set CSV - Cell - Without Read Table
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv

    Tables.Open Table    ${csv_path}
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp   header=True
    Tables.Set Table Cell    not temp    0    1    header=False

    @{content}    Tables.Get Table
    Tables.Set Table Cell    first column    0    1    header=False
    ${result} =    BuiltIn.Evaluate    "${content}[0][1]" == "not temp"
    BuiltIn.Should Be True    ${result}
    ${result} =    BuiltIn.Evaluate    ${content}[1][1] == 25
    BuiltIn.Should Be True    ${result}
    ${result} =    BuiltIn.Evaluate    ${content}[2][1] == 10
    BuiltIn.Should Be True    ${result}

Set CSV - Row
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    VAR   @{row_list_2}    column 1    column 2

    Tables.Open Table    ${csv_path}
    Tables.Set Table Row    ${row_list}    1    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=False
    Tables.Set Table Row    ${row_list_2}    0    header=False

    @{content}    Tables.Get Table
    Collections.Lists Should Be Equal    ${content}[0]     ${row_list_2}
    Collections.Lists Should Be Equal    ${content}[1]     ${row_list_1}
    Collections.Lists Should Be Equal    ${content}[2]     ${row_list}

Set CSV - Column
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march

    Tables.Open Table    ${csv_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    year    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False

    @{content}    Tables.Get Table    List of dicts
    @{first_column_list} =    Evaluate    [row["year"] for row in ${content}]
    @{second_column_list} =    Evaluate    [row["month"] for row in ${content}]
    Collections.Lists Should Be Equal    ${first_column_list}     ${column_list}
    Collections.Lists Should Be Equal    ${second_column_list}     ${column_list_1}[1:]

Modify CSV Table - Row
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    VAR    @{column_list} =   column 1    column 2

    VAR    @{original_column} =     year    temp
    VAR    @{original_row} =    2025    30
    VAR    @{original_row_2} =   2024    29

    ${uuid} =    Tables.Open Table    ${csv_path}
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Insert Row    ${column_list}    0    header=False
    Tables.Append Row    ${row_list_2}
    Tables.Remove Row    0    header=True

    @{content}    Tables.Get Table
    Collections.List Should Not Contain Value    ${content}[0]    ${original_column}[0]
    Collections.List Should Not Contain Value    ${content}[0]    ${original_column}[1]
    Collections.Lists Should Be Equal    ${content}[0]     ${column_list}
    Collections.Lists Should Be Equal    ${content}[1]     ${row_list}
    Collections.Lists Should Be Equal    ${content}[2]     ${original_row}
    Collections.Lists Should Be Equal    ${content}[3]     ${original_row_2}
    Collections.Lists Should Be Equal    ${content}[4]     ${row_list_2}

    Tables.Count Table    ${uuid}    Columns    ==    ${2}
    Tables.Count Table    ${uuid}    Rows    ==    ${5}


Modify CSV Table - Column
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2

    VAR    @{expected_column} =    month    day
    VAR    @{expected_row} =    june    1
    VAR    @{expected_row_2} =    july    2

    ${uuid} =    Tables.Open Table    ${csv_path}
    Tables.Insert Column    ${column_list}        1
    Tables.Append Column    ${column_list_2}
    Tables.Remove Column    0
    Tables.Remove Column    temp

    @{content}    Tables.Get Table
    Collections.Lists Should Be Equal    ${content}[0]     ${expected_column}
    Collections.Lists Should Be Equal    ${content}[1]     ${expected_row}
    Collections.Lists Should Be Equal    ${content}[2]     ${expected_row_2}
    Tables.Count Table    ${uuid}    Columns    ==    ${2}
    Tables.Count Table    ${uuid}    Rows    ==    ${3}
    
    

Modify first Table - Write in second table
    [Setup]    Reset Both Csv Tables
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    ${csv_path_2} =   ${CURDIR}/results/test_writer_2.csv

    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2
    VAR    @{column_list_3} =    2010     2008

    ${uuid} =    Tables.Open Table    ${csv_path}
    ${uuid2} =    Tables.Open Table    ${csv_path_2}

    Tables.Switch Table   ${uuid}
    Tables.Insert Column    ${column_list}        1
    Tables.Append Column    ${column_list_2}
    Tables.Remove Column    0

    ${new_content}    Tables.Get Table
    Tables.Write Table    ${new_content}    ${uuid2}

    Tables.Configure Ignore Header    False
    ${content} =    Tables.Read Table    ${csv_path_2}
    ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "month"
    BuiltIn.Should Be True    ${result}

Modify and Write Table - Without Write Path
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{column_list} =    month      june      july
    Tables.Open Table    ${csv_path}
    Tables.Append Column    ${column_list}
    ${content}    Get Table
    Tables.Write Table    ${content}

    ${content} =     Tables.Read Table    ${csv_path}
    ${result} =    BuiltIn.Evaluate    "${content}[0][2]" == "month"
    BuiltIn.Should Be True    ${result}

Create New Empy Table - Append & Insert Data
    
    VAR    @{headers} =    name    age
    VAR    @{person1} =    Michael    34
    VAR    @{person2} =    John    19
    
    ${uuid} =    Tables.Create Table    headers=${headers}
    
    Tables.Append Row    ${person1}
    Tables.Append Row    ${person2}
    Count Table    ${uuid}    Rows    equal    ${3}
    
    VAR    @{column1} =    city    MG    ERL
    Tables.Append Column    ${column1}
    Count Table    ${uuid}    Columns    equal    ${3}

    Get Table Cell    1    1    equals    34
    Tables.Set Table Cell    25    0    1
    Get Table Cell    1    1    equals    25

    VAR    @{insert_row} =    Lu    26    Hamburg
    Insert Row    ${insert_row}    0
    Get Table Cell    1    0    equals    Lu
    Count Table    ${uuid}    Rows    equal    ${4}

Create New Empty Table - Random Data - Write to CSV
    
    VAR    @{headers} =    name    age
    ${uuid} =    Create Table    ${headers}

    FOR    ${_}    IN RANGE    ${100}
        ${a} =    Generate Random String
        ${b} =    Generate Random String
        VAR    @{data}    ${a}    ${b}
        Tables.Append Row    ${data}
    END

    Count Table    ${uuid}    Rows    equals    ${101}
    Write Table    ${uuid}    ${CURDIR}/results/test_writer_new_table.csv

    Count Table    ${CURDIR}/results/test_writer_new_table.csv    Rows    equals    ${101}

    
########################################################################################
# Parquet
########################################################################################
Write Parquet File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.parquet

Set Parquet - Cell
    Reset Parquet Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    Tables.Open Table    ${parquet_path}
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp   header=True
    Tables.Set Table Cell    not temp    0    1    header=False

    @{content}    Tables.Get Table
    Tables.Set Table Cell    first column    0    1    header=False
    ${result} =    BuiltIn.Evaluate    "${content}[0][1]" == "not temp"
    BuiltIn.Should Be True    ${result}
    ${result} =    BuiltIn.Evaluate    ${content}[1][1] == 25
    BuiltIn.Should Be True    ${result}
    ${result} =    BuiltIn.Evaluate    ${content}[2][1] == 10
    BuiltIn.Should Be True    ${result}

Write Parquet - Cell - Without Read Table
    Reset Parquet Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    Tables.Set Table Cell    100    0    1    ${parquet_path}

Set Parquet - Row
    [Setup]   Reset Parquet Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    VAR   @{row_list_2}    column 1    column 2

    Tables.Open Table    ${parquet_path}
    Tables.Set Table Row    ${row_list}    1    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=False
    Tables.Set Table Row    ${row_list_2}    0    header=False

    @{content}    Tables.Get Table
    Collections.Lists Should Be Equal    ${content}[0]     ${row_list_2}
    Collections.Lists Should Be Equal    ${content}[1]     ${row_list_1}
    Collections.Lists Should Be Equal    ${content}[2]     ${row_list}

Set Parquet - Column
    [Setup]   Reset Parquet Table
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march

    Tables.Open Table    ${parquet_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    year    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False

    @{content}    Tables.Get Table    List of dicts
    @{first_column_list} =    Evaluate    [row["year"] for row in ${content}]
    @{second_column_list} =    Evaluate    [row["month"] for row in ${content}]
    Collections.Lists Should Be Equal    ${first_column_list}     ${column_list}
    Collections.Lists Should Be Equal    ${second_column_list}     ${column_list_1}[1:]


Modify Parquet Row
    [Setup]   Reset Parquet Table
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    VAR    @{column_list} =   column 1    column 2

    VAR    @{original_column} =     year    temp
    VAR    @{original_row} =    2025    30
    VAR    @{original_row_2} =   2024    29

    ${uuid} =    Tables.Open Table    ${parquet_path}
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Insert Row    ${column_list}    0    header=False
    Tables.Append Row    ${row_list_2}
    Tables.Remove Row    0    header=True

    @{content}    Tables.Get Table
    Collections.List Should Not Contain Value    ${content}[0]    ${original_column}[0]
    Collections.List Should Not Contain Value    ${content}[0]    ${original_column}[1]
    Collections.Lists Should Be Equal    ${content}[0]     ${column_list}
    Collections.Lists Should Be Equal    ${content}[1]     ${row_list}
    Collections.Lists Should Be Equal    ${content}[2]     ${original_row}
    Collections.Lists Should Be Equal    ${content}[3]     ${original_row_2}
    Collections.Lists Should Be Equal    ${content}[4]     ${row_list_2}

    Tables.Count Table    ${uuid}    Columns    ==    ${2}
    Tables.Count Table    ${uuid}    Rows    ==    ${5}

Modify Parquet Column
    [Setup]   Reset Parquet Table
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2

    VAR    @{expected_column} =    month    day
    VAR    @{expected_row} =    june    1
    VAR    @{expected_row_2} =    july    2

    ${uuid} =    Tables.Open Table    ${parquet_path}
    Tables.Insert Column    ${column_list}        1
    Tables.Append Column    ${column_list_2}
    Tables.Remove Column    0
    Tables.Remove Column    temp

    @{content}    Tables.Get Table
    Collections.Lists Should Be Equal    ${content}[0]     ${expected_column}
    Collections.Lists Should Be Equal    ${content}[1]     ${expected_row}
    Collections.Lists Should Be Equal    ${content}[2]     ${expected_row_2}
    Tables.Count Table    ${uuid}    Columns    ==    ${2}
    Tables.Count Table    ${uuid}    Rows    ==    ${3}

########################################################################################
# Excel
########################################################################################
Set Excel - Cell - Without Read Table
    [Setup]    Reset Excel Table
    VAR    ${xlsx_path} =   ${CURDIR}/results/test_writer.xlsx

    Tables.Open Table    ${xlsx_path}
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp   header=True
    Tables.Set Table Cell    not temp    0    1    header=False

    @{content}    Tables.Get Table
    Tables.Set Table Cell    first column    0    1    header=False
    ${result} =    BuiltIn.Evaluate    "${content}[0][1]" == "not temp"
    BuiltIn.Should Be True    ${result}
    ${result} =    BuiltIn.Evaluate    ${content}[1][1] == 25
    BuiltIn.Should Be True    ${result}
    ${result} =    BuiltIn.Evaluate    ${content}[2][1] == 10
    BuiltIn.Should Be True    ${result}

Set Excel - Row
    [Setup]    Reset Excel Table
    VAR    ${xlsx_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    VAR   @{row_list_2}    column 1    column 2

    Tables.Open Table    ${xlsx_path}
    Tables.Set Table Row    ${row_list}    1    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=False
    Tables.Set Table Row    ${row_list_2}    0    header=False

    @{content}    Tables.Get Table
    Collections.Lists Should Be Equal    ${content}[0]     ${row_list_2}
    Collections.Lists Should Be Equal    ${content}[1]     ${row_list_1}
    Collections.Lists Should Be Equal    ${content}[2]     ${row_list}

Set Excel - Column
    [Setup]    Reset Excel Table
    VAR    ${xlsx_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march

    Tables.Open Table    ${xlsx_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    year    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False

    @{content}    Tables.Get Table    List of dicts
    @{first_column_list} =    Evaluate    [row["year"] for row in ${content}]
    @{second_column_list} =    Evaluate    [row["month"] for row in ${content}]
    Collections.Lists Should Be Equal    ${first_column_list}     ${column_list}
    Collections.Lists Should Be Equal    ${second_column_list}     ${column_list_1}[1:]

Modify Excel Row
    [Setup]    Reset Excel Table
    VAR    ${xlsx_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    VAR    @{column_list} =   column 1    column 2

    VAR    @{original_column} =     year    temp
    VAR    @{original_row} =    2025    30
    VAR    @{original_row_2} =   2024    29

    ${uuid} =    Tables.Open Table    ${xlsx_path}
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Insert Row    ${column_list}    0    header=False
    Tables.Append Row    ${row_list_2}
    Tables.Remove Row    0    header=True

    @{content}    Tables.Get Table
    Collections.List Should Not Contain Value    ${content}[0]    ${original_column}[0]
    Collections.List Should Not Contain Value    ${content}[0]    ${original_column}[1]
    Collections.Lists Should Be Equal    ${content}[0]     ${column_list}
    Collections.Lists Should Be Equal    ${content}[1]     ${row_list}
    Collections.Lists Should Be Equal    ${content}[2]     ${original_row}
    Collections.Lists Should Be Equal    ${content}[3]     ${original_row_2}
    Collections.Lists Should Be Equal    ${content}[4]     ${row_list_2}

    Tables.Count Table    ${uuid}    Columns    ==    ${2}
    Tables.Count Table    ${uuid}    Rows    ==    ${5}

Modify Excel Column
    [Setup]    Reset Excel Table
    VAR    ${xlsx_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2

    VAR    @{expected_column} =    month    day
    VAR    @{expected_row} =    june    1
    VAR    @{expected_row_2} =    july    2

    ${uuid} =    Tables.Open Table    ${xlsx_path}
    Tables.Insert Column    ${column_list}        1
    Tables.Append Column    ${column_list_2}
    Tables.Remove Column    0
    Tables.Remove Column    temp

    @{content}    Tables.Get Table
    Collections.Lists Should Be Equal    ${content}[0]     ${expected_column}
    Collections.Lists Should Be Equal    ${content}[1]     ${expected_row}
    Collections.Lists Should Be Equal    ${content}[2]     ${expected_row_2}
    Tables.Count Table    ${uuid}    Columns    ==    ${2}
    Tables.Count Table    ${uuid}    Rows    ==    ${3}

Quoting Characters - Double Quotes - Always
    [Setup]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    ALL
    [Teardown]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    MINIMAL

    VAR    @{headers} =    name    age
    ${uuid} =    Create Table    ${headers}

    VAR    @{data}    marvin    26
    Tables.Append Row    ${data}

    Tables.Write Table    ${uuid}    ${CURDIR}/results/test_writer_new_table.csv

    ${raw_content} =    OperatingSystem.Get File    ${CURDIR}/results/test_writer_new_table.csv
    BuiltIn.Should Contain    ${raw_content}    "marvin"
    BuiltIn.Should Contain    ${raw_content}    "26"

Quoting Characters - Single Quotes - Always
    [Setup]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    '
    ...    AND
    ...    Tables.Configure Quoting    ALL
    [Teardown]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    MINIMAL

    VAR    @{headers} =    name    age
    ${uuid} =    Create Table    ${headers}

    VAR    @{data}    marvin    26
    Tables.Append Row    ${data}

    Tables.Write Table    ${uuid}    ${CURDIR}/results/test_writer_new_table.csv

    ${raw_content} =    OperatingSystem.Get File    ${CURDIR}/results/test_writer_new_table.csv
    BuiltIn.Should Contain    ${raw_content}    'marvin'
    BuiltIn.Should Contain    ${raw_content}    '26'

Quoting Characters - Double Quotes - Non Numeric
    [Setup]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    NONNUMERIC
    [Teardown]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    MINIMAL

    VAR    @{headers} =    name    age
    ${uuid} =    Create Table    ${headers}

    VAR    @{data}    marvin    ${26}
    Tables.Append Row    ${data}

    Tables.Write Table    ${uuid}    ${CURDIR}/results/test_writer_new_table.csv

    ${raw_content} =    OperatingSystem.Get File    ${CURDIR}/results/test_writer_new_table.csv
    BuiltIn.Should Contain    ${raw_content}    "marvin"
    BuiltIn.Should Contain    ${raw_content}    26
    BuiltIn.Should Not Contain    ${raw_content}    "26"

Quoting Characters - Double Quotes - Minimal
    [Setup]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    MINIMAL
    [Teardown]    BuiltIn.Run Keywords
    ...    Tables.Configure Quoting Character    "
    ...    AND
    ...    Tables.Configure Quoting    MINIMAL

    VAR    @{headers} =    name    age
    ${uuid} =    Create Table    ${headers}

    VAR    @{data}    marvin,sergej    ${26}
    Tables.Append Row    ${data}

    Tables.Write Table    ${uuid}    ${CURDIR}/results/test_writer_new_table.csv

    ${raw_content} =    OperatingSystem.Get File    ${CURDIR}/results/test_writer_new_table.csv
    BuiltIn.Should Contain    ${raw_content}    "marvin,sergej"
    BuiltIn.Should Contain    ${raw_content}    26


*** Keywords ***
Reset CSV Table
    VAR    ${file_path} =    ${CURDIR}/results/test_writer.csv
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${file_path}
    RETURN    ${file_path}
Reset CSV Table 2
    VAR    ${file_path} =    ${CURDIR}/results/test_writer_2.csv
    VAR    @{data_00} =    2026    31
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${data_00}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${file_path}
    RETURN    ${file_path}

Reset Both Csv Tables
    Reset CSV Table
    Reset CSV Table 2
    
Reset Parquet Table
    VAR    ${file_path} =    ${CURDIR}/results/test_writer.parquet
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${file_path}
    RETURN    ${file_path}

Reset Excel Table
    VAR    ${file_path} =    ${CURDIR}/results/test_writer.xlsx
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${file_path}
    RETURN    ${file_path}