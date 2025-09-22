*** Settings ***
Library     Tables    file_type=CSV
Library     Collections


*** Test Cases ***    
Write Excel File
    [Tags]    robot:skip
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Configure File Type    Excel
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.xlsx
    
## Txt tests #########################################################
Write CSV to TXT File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.txt
    BuiltIn.Log    ${file_path}
    BuiltIn.Should Contain    ${file_path}    results${/}test_writer.txt

Write CSV to TXT File - Quoting
    [Tags]    robot:skip
    [Teardown]    Configure Quoting    MINIMAL
    Configure Quoting Character    '
    Configure Quoting    ALL
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.txt
    BuiltIn.Log    ${file_path}
    BuiltIn.Should Contain    ${file_path}    results${/}test_writer.txt
    ${content} =    Tables.Read Table    ${file_path}
    Should Contain    ${content}[1]    '2025'
    Should Contain    ${content}[1]    '30'

    
## Csv tests #########################################################
Write CSV File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv
    BuiltIn.Log    ${file_path}
    BuiltIn.Should Contain    ${file_path}    results${/}test_writer.csv

Write CSV File - Without Header
    VAR    @{data_00} =    2026    31
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${data_00}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer_2.csv

Set CSV - Cell
    Reset Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp    header=True
    Tables.Set Table Cell    2029    1    0    header=False


Set CSV - Cell - Without Read Table
    [Teardown]    Reset Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Cell    100    0    1    header=False

Set CSV - Row
    [Teardown]    Reset Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    Tables.Set Table Row    ${row_list}    0    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=False

Set CSV - Column
    [Teardown]    Reset Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False

Modify CSV Row - With Header
    Reset Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    Tables.Open Table    table 1    ${csv_path}
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Append Row    ${row_list_2}    header=True
    Tables.Remove Row    0    header=True

Modify CSV Column - With Header
    Reset Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2
    Tables.Open Table    table 1    ${csv_path}
    Tables.Insert Column    ${column_list}    1    True
    Tables.Append Column    ${column_list_2}    True
    Tables.Remove Column    0     True
    
## Parquet tests #########################################################
Write Parquet File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.parquet

Write Parquet - Cell
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    ${content_old} =    Tables.Read Table    ${parquet_path}
    Tables.Set Table Cell    25    0    1
    Tables.Set Table Cell    2029    1    0

Write Parquet - Cell - Without Read Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    Tables.Set Table Cell    100    0    1    ${parquet_path}

Write Parquet - Row
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    ${content_old} =    Tables.Read Table    ${parquet_path}
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    Tables.Set Table Row    ${row_list}    0
    Tables.Set Table Row    ${row_list_1}    1
    ${content_new} =    Tables.Read Table    ${parquet_path}

Write Parquet - Row - Without Read Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{row_list}    2004    04
    Tables.Set Table Row    ${row_list}    0    ${parquet_path}

Write Parquet - Column
    [Tags]    robot:skip
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    ${content_old} =    Tables.Read Table    ${parquet_path}
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    august    march
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False
    ${content_new} =    Tables.Read Table    ${parquet_path}

Write Parquet - Column - Without Read Table
    [Tags]    robot:skip
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{column_list}    2009    2008
    Tables.Set Table Column    ${column_list}    0    ${parquet_path}


*** Keywords ***
Reset Table
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv
    