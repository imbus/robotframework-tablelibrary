*** Settings ***
Library   Tables    file_type=CSV    file_encoding=UTF8    delimiter=,    ignore_header=True


*** Test Cases ***
File Type
    Tables.Set File Type    Parquet
    ${file_type} =    Tables.Get File Type
    Should Be Equal As Strings    ${file_type}    parquet
    
    Tables.Set File Type    CSV
    ${file_type} =    Tables.Get File Type
    Should Be Equal As Strings    ${file_type}    csv

Delimiter
    Tables.Set Delimiter    ,
