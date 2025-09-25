*** Settings ***
Library     Tables    file_type=CSV
Library     Collections


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
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp    header=True
    Tables.Set Table Cell    2029    1    0    header=False
    Tables.Set Table Cell    first column    0    1    header=False
    @{content}    Tables.Get Table

Set CSV - Row
    [Setup]    Reset CSV Table
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
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False
    Tables.Get Table

Modify CSV Row - With Header
    [Setup]    Reset CSV Table
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
    [Setup]    Reset CSV Table
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

Modify first Table - Write in second table
    [Setup]    Reset Both Csv Tables
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    ${csv_path_2} =   ${CURDIR}/results/test_writer_2.csv

    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2
    VAR    @{column_list_3} =    2010     2008

    Tables.Open Table    table 1    ${csv_path}
    Tables.Open Table    table 2    ${csv_path_2}
    Tables.Switch Table   table 1
    Tables.Insert Column    ${column_list}        1    header=False
    Tables.Append Column    ${column_list_2}      header=True
    Tables.Remove Column    0     header=False
    Tables.Remove Column    day     header=True
    ${new_content}    Tables.Get Table
    Tables.Write Table    ${new_content}    table 2

Modify and Write Table - Without Write Path
    [Setup]    Reset CSV Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR    @{column_list} =    month      june      july
    Tables.Open Table    table 1    ${csv_path}
    Tables.Append Column    ${column_list}
    ${content}    Get Table
    Tables.Write Table    data=${content}


    
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
    [Setup]   Reset Parquet Table
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
    [Setup]   Reset Parquet Table
    VAR   ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Open Table    table 1    ${parquet_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False
    Tables.Get Table


Modify Parquet Row - With Header
    [Setup]   Reset Parquet Table
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
    [Setup]   Reset Parquet Table
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

########################################################################################
# Excel
########################################################################################
Set Excel - Cell - Without Read Table
    [Setup]    Reset Excel Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.xlsx
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Cell    25    0    1    header=True
    Tables.Set Table Cell    10    1    temp    header=True
    Tables.Set Table Cell    2029    1    0    header=False
    Tables.Set Table Cell    first column    0    1    header=False
    Tables.Get Table

Set Excel - Row
    [Setup]    Reset Excel Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.xlsx
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    VAR   @{row_list_2}    column 1    column 2
    Tables.Set Table Row    ${row_list}    0    header=True
    Tables.Set Table Row    ${row_list_1}    1    header=False
    Tables.Set Table Row    ${row_list_2}    0    header=False
    Tables.Get Table

Set Excel - Column
    [Setup]    Reset Excel Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Open Table    table 1    ${csv_path}
    Tables.Get Table
    Tables.Set Table Column    ${column_list}    0    header=True
    Tables.Set Table Column    ${column_list_1}    1    header=False
    Tables.Get Table

Modify Excel Row - With Header
    [Setup]    Reset Excel Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR    @{row_list} =     2001    04
    VAR    @{row_list_2} =    2026    10
    VAR    @{column_list} =   column 1    column 2
    Tables.Open Table    table 1    ${csv_path}
    Tables.Insert Row    ${row_list}    0    header=True
    Tables.Insert Row    ${column_list}    0    header=False
    Tables.Append Row    ${row_list_2}    header=True
    Tables.Remove Row    0    header=True

Modify Excel Column
    [Setup]    Reset Excel Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.xlsx
    VAR    @{column_list} =    month      june      july
    VAR    @{column_list_2} =    day      1      2
    VAR    @{column_list_3} =    2010     2008
    Tables.Open Table    table 1    ${csv_path}
    Tables.Insert Column    ${column_list}        1    header=False
    Tables.Append Column    ${column_list_2}      header=True
    Tables.Remove Column    0     header=False
    Tables.Remove Column    day     header=True
    Tables.Get Table


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