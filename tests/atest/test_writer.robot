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