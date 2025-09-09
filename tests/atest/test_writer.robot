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
    
## Csv tests #########################################################
Write CSV File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv

Write CSV File - Without Header
    VAR    @{data_00} =    2026    31
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${data_00}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer_2.csv

Write CSV - Cell
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    Tables.Write Table Cell    25    0    1    header=True
    Tables.Write Table Cell    10    1    temp    header=True
    Tables.Write Table Cell    2029    1    0    header=False
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Cell - Without Read Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    Tables.Write Table Cell    100    0    1    ${csv_path}

Write CSV - Row
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    Tables.Write Table Row    ${row_list}    0    header=True
    Tables.Write Table Row    ${row_list_1}    1    header=False
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Row - Without Read Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR   @{row_list}    2004    04
    Tables.Write Table Row    ${row_list}    0    ${csv_path}

Write CSV - Column
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    month    august    march
    Tables.Write Table Column    ${column_list}    0    header=True
    Tables.Write Table Column    ${column_list_1}    1    header=False
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Column - Without Read Table
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    VAR   @{column_list}    2006    2007
    Tables.Write Table Column    ${column_list}    0    ${csv_path}

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
    Tables.Write Table Cell    25    0    1
    Tables.Write Table Cell    2029    1    0

Write Parquet - Cell - Without Read Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    Tables.Write Table Cell    100    0    1    ${parquet_path}

Write Parquet - Row
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    ${content_old} =    Tables.Read Table    ${parquet_path}
    VAR   @{row_list}    2004    04
    VAR   @{row_list_1}    2030    30
    Tables.Write Table Row    ${row_list}    0
    Tables.Write Table Row    ${row_list_1}    1
    ${content_new} =    Tables.Read Table    ${parquet_path}

Write Parquet - Row - Without Read Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{row_list}    2004    04
    Tables.Write Table Row    ${row_list}    0    ${parquet_path}

Write Parquet - Column
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    ${content_old} =    Tables.Read Table    ${parquet_path}
    VAR   @{column_list}    2006    2007
    VAR   @{column_list_1}    august    march
    Tables.Write Table Column    ${column_list}    0    header=True
    Tables.Write Table Column    ${column_list_1}    1    header=False
    ${content_new} =    Tables.Read Table    ${parquet_path}

Write Parquet - Column - Without Read Table
    VAR    ${parquet_path} =   ${CURDIR}/results/test_writer.parquet
    VAR   @{column_list}    2009    2008
    Tables.Write Table Column    ${column_list}    0    ${parquet_path}