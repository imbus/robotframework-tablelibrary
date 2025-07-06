*** Settings ***
Library   TableLibrary    CSV    UTF8    ,    True


*** Test Cases ***
File Type
    ${file_type} =    TableLibrary.Get File Type
    Should Be Equal As Strings    ${file_type}    csv
    
    TableLibrary.Set File Type    Parquet
    ${file_type} =    TableLibrary.Get File Type
    Should Be Equal As Strings    ${file_type}    parquet
    
    TableLibrary.Set File Type    CSV
    ${file_type} =    TableLibrary.Get File Type
    Should Be Equal As Strings    ${file_type}    csv
