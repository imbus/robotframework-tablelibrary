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

Set CSV - Cell - Without Read Table
    [Teardown]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp    header=True
    Tables.Set Table Cell    2029    1    0    header=False
    Tables.Set Table Cell    first column    0    1    header=False
    Tables.Get Table

Set CSV - Row
    [Teardown]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    VAR   @{row_list_2}    column 1    column 2
    Tables.Set Table Row    ${row_list}    0    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=False
    Tables.Set Table Row    ${row_list_2}    0    header=False
    Tables.Get Table

Set CSV - Column
    [Teardown]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False
    Tables.Get Table

Modify CSV Row - With Header
    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    VAR    @{column_list} =   column 1    column 2
    Tables.Open Table    table 1    ${csv_path}
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Insert Row    ${column_list}    0    header=False
    Tables.Append Row    ${row_list_2}    header=True
    Tables.Remove Row    0    header=True

Modify CSV Column
    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2
    VAR    @{column_list_3} =    2010     2008
    Tables.Open Table    table 1    ${csv_path}
    Tables.Insert Column    ${column_list}        1    header=False
    Tables.Append Column    ${column_list_2}      header=True
    Tables.Remove Column    0     header=False
    Tables.Remove Column    day     header=True
    Tables.Get Table
    
## Parquet tests #########################################################
Write Parquet File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.parquet

Set Parquet - Cell
    Reset Parquet Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    Tables.Open Table    table 1    ${parquet_path}
    Tables.Get Table
    Tables.Set Table Cell    25          0    1     header=True
    Tables.Set Table Cell    2029        1    0     header=False
    Tables.Set Table Cell    column 1    0    0    header=False  

Write Parquet - Cell - Without Read Table
    Reset Parquet Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    Tables.Set Table Cell    100    0    1    ${parquet_path}

Set Parquet - Row
    Reset Parquet Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    VAR   @{row_list_2}    column 1    column 2
    Tables.Open Table    table 1    ${parquet_path}
    Tables.Get Table
    Tables.Set Table Row    ${row_list}      0    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=True
    Tables.Set Table Row    ${row_list_2}    0    header=False

Set Parquet - Column
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Open Table    table 1    ${parquet_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False
    Tables.Get Table


Modify Parquet Row - With Header
    Reset Parquet Table
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    VAR    @{column_list} =   column 1    column 2
    Tables.Open Table    table 1    ${parquet_path}
    Tables.Get Table
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Insert Row    ${column_list}    0    header=False
    Tables.Append Row    ${row_list_2}    header=True
    Tables.Remove Row    0    header=True

Modify Parquet Column
    Reset Parquet Table
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2
    VAR    @{column_list_3} =    2010     2008
    Tables.Open Table    table 1    ${parquet_path}
    Tables.Insert Column    ${column_list}        1    header=False
    Tables.Append Column    ${column_list_2}      header=True
    Tables.Remove Column    0     header=False
    Tables.Remove Column    day     header=True
    Tables.Get Table


*** Keywords ***
Reset CSV Table
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    ${file_path} =    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv
    RETURN    ${CURDIR}/results/test_writer.csv
    
Reset Parquet Table
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.parquet
    RETURN    