*** Settings ***
Library     Tables    file_type=CSV
Library     Collections


*** Test Cases ***
Write CSV File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv

Write CSV File - Without Header
    VAR    @{headers} =    2026    31
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer_2.csv

Write Excel File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Configure File Type    Excel
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.xlsx

Write Parquet File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Configure File Type    Parquet
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.parquet

Write CSV - Cell - With Header
    Tables.Configure Ignore Header    False
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    Tables.Write Table Cell    25    0    1
    Tables.Write Table Cell    2029    1    0
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Cell - Without Header
    Tables.Configure Ignore Header    True
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    Tables.Write Table Cell    2010    0    0
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Row - With Header
    Tables.Configure Ignore Header    False
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    VAR   @{row_list}    2004    04
    Tables.Write Table Row    ${row_list}    0
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Row - Without Header
    Tables.Configure Ignore Header    True
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    VAR   @{row_list}    2030    30
    Tables.Write Table Row    ${row_list}    0
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Column - With Header
    Tables.Configure Ignore Header    False
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    VAR   @{column_list}    2006    2007
    Tables.Write Table Column    ${column_list}    0
    ${content_new} =    Tables.Read Table    ${csv_path}

Write CSV - Column - Without Header
    Tables.Configure Ignore Header    True
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    VAR   @{column_list}    2000    2001
    Tables.Write Table Column    ${column_list}    0
    ${content_new} =    Tables.Read Table    ${csv_path}

## TODO: add more paqrquet tests across writing tests