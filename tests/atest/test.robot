*** Settings ***
Library   TableLibrary    CSV    UTF8    ,    True


*** Test Cases ***
Configuration
    TableLibrary.Set File Type    Parquet
    TableLibrary.Set Delimiter    ,
    TableLibrary.Set File Encoding    UTF16