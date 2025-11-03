from robot.api.deco import keyword

from ..general.library_attributes import LibraryAttributes
from ..utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
)


class Configuration(LibraryAttributes):
    @keyword(tags=["Configuration"])
    def configure_file_type(self, file_type: FileType):
        """
        Change the internal file type during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``file_type`` | Choose the new file type |

        == Example ==
        | Configure File Type    CSV
        | Configure File Type    Excel
        | Configure File Type    Parquet
        """
        self.file_type = file_type

    @keyword(tags=["Configuration"])
    def configure_separator(self, separator: Delimiter):
        """
        Change the internal separator during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``separator`` | Define a new separator |

        == Example ==
        | Configure Delimiter    ;
        | Configure Delimiter    ,
        | Configure Delimiter    \\t
        """
        self.separator = separator

    @keyword(tags=["Configuration"])
    def configure_quoting(self, quoting: Quoting):
        """
        Change the internal quoting mode during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``quoting`` | Define a new quoting mode |

        == Example ==
        | Configure Quoting    MINIMAL
        | Configure Quoting    NONNUMERIC
        | Configure Quoting    NONE
        """
        self.quoting = quoting

    @keyword(tags=["Configuration"])
    def configure_quoting_character(self, quoting_character: QuotingCharacter):
        """
        Change the internal quoting character during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``quoting`` | Define a new quoting mode |

        == Example ==
        | Configure Quoting Character    "
        | Configure Quoting Character    '
        """
        self.quoting_character = quoting_character

    @keyword(tags=["Configuration"])
    def configure_line_terminator(self, line_terminator: LineTerminator):
        """
        Change the internal line terminator during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``line_terminator`` | Define a new line_terminator |

        == Example ==
        | Configure Line Terminator    LF
        | Configure Line Terminator    CRLF
        """
        self.line_terminator = line_terminator

    @keyword(tags=["Configuration"])
    def configure_file_encoding(self, file_encoding: FileEncoding | str):
        """
        Change the internal file encoding during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``file_encoding`` | Define a new file encoding |

        == Example ==
        | Configure File Encoding    UTF_8
        | Configure File Encoding    UTF_16
        | Configure File Encoding    LATIN_1

        see [Python Encoding Names|https://docs.python.org/3/library/codecs.html#standard-encodings]
        """
        self.file_encoding = (
            file_encoding.value if isinstance(file_encoding, FileEncoding) else file_encoding
        )

    @keyword(tags=["Configuration"])
    def configure_ignore_header(self, ignore_header: bool):
        """
        Change the internal setting to (not) ignore the data header lines during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``ignore_header`` | Ignore / recognize header columns |

        == Example ==
        | Configure Ignore Header    True
        | Configure Ignore Header    False
        """
        self.ignore_header = ignore_header
