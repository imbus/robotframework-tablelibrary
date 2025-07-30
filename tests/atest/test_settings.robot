*** Settings ***
Library   Tables    file_type=CSV    file_encoding=UTF8    delimiter=,    ignore_header=True


*** Test Cases ***
File Type
    Tables.Configure File Type    Parquet
    Tables.Configure File Type    Excel
    Tables.Configure File Type    CSV

Delimiter
    Tables.Configure Delimiter    ,
    Tables.Configure Delimiter    ;

File Encoding
    Tables.Configure File Encoding    UTF8
    Tables.Configure File Encoding    LATIN1
    Tables.Configure File Encoding    UTF16
