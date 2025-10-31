*** Settings ***
Library   Tables    file_type=CSV    file_encoding=UTF_8    separator=,    ignore_header=True


*** Test Cases ***
File Type
    Tables.Configure File Type    Parquet
    # Tables.Configure File Type    Excel
    Tables.Configure File Type    CSV

Delimiter
    Tables.Configure Separator    ,
    Tables.Configure Separator    ;

File Encoding
    Tables.Configure File Encoding    UTF_8
    Tables.Configure File Encoding    LATIN_1
    Tables.Configure File Encoding    UTF_16

Quoting Characters
    [Teardown]    Tables.Configure Quoting Character    "
    Tables.Configure Quoting Character    "
    Tables.Configure Quoting Character    '
