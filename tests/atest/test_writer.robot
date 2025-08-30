*** Settings ***
Library     Tables    file_type=CSV


*** Test Cases ***
Write CSV File
    VAR    @{headers} =    year    temp
    VAR    @{data_01} =    2025    30
    VAR    @{data_02} =    2024    29    
    VAR    @{object} =    ${headers}    ${data_01}    ${data_02}
    Tables.Write Table    ${object}    ${CURDIR}/results/test_writer.csv

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

Write CSV cell With Header
    Tables.Configure Ignore Header    False
    VAR    ${csv_path} =   ${CURDIR}/results/test_writer.csv
    ${content_old} =    Tables.Read Table    ${csv_path}
    Tables.Write Table Cell    25    1    1
    Tables.Write Table Cell    2029    2    0
    ${content_new} =    Tables.Read Table    ${csv_path}