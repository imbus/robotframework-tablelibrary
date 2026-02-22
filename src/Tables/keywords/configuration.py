from dataclasses import asdict, dataclass

from robot.api import logger
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
from ..utils.settings_stack import Scope


@dataclass
class ConfigCtx:
    file_type: FileType
    separator: Delimiter
    quoting: Quoting
    quoting_character: QuotingCharacter
    line_terminator: LineTerminator
    file_encoding: FileEncoding
    ignore_header: bool


class Configuration(LibraryAttributes):
    @keyword(tags=["Configuration"])
    def get_library_configuration(self) -> dict:
        """
        Keyword returns the current internal library configuration.

        Return value is type ``ConfigCtx`` and contains all relevant configuration parameters.
        """
        return asdict(
            ConfigCtx(
                file_type=self.file_type,
                separator=self.separator,
                quoting=self.quoting,
                quoting_character=self.quoting_character,
                line_terminator=self.line_terminator,
                file_encoding=self.file_encoding,
                ignore_header=self.ignore_header,
            )
        )

    @keyword(tags=["Configuration"])
    def configure_file_type(self, file_type: FileType, scope: Scope = Scope.Suite):
        """
        Change the internal file type during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``file_type`` | Choose the new file type |

        == Example ==
        | Configure File Type    CSV
        | Configure File Type    Excel
        | Configure File Type    Parquet
        """
        old_config = self.file_type
        self.file_type_stack.set(file_type, scope)
        logger.debug(f"'file_type': old value: {old_config} - new value: {file_type}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_separator(self, separator: Delimiter, scope: Scope = Scope.Suite):
        """
        Change the internal separator during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``separator`` | Define a new separator |

        == Example ==
        | Configure Delimiter    ;
        | Configure Delimiter    ,
        | Configure Delimiter    \\t
        """
        old_config = self.separator
        self.separator_stack.set(separator, scope)
        logger.debug(f"'file_type': old value: {old_config} - new value: {separator}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_quoting(self, quoting: Quoting, scope: Scope = Scope.Suite):
        """
        Change the internal quoting mode during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``quoting`` | Define a new quoting mode |

        == Example ==
        | Configure Quoting    MINIMAL
        | Configure Quoting    NONNUMERIC
        | Configure Quoting    NONE
        """
        old_config = self.quoting
        self.quoting_stack.set(quoting, scope)
        logger.debug(f"'file_type': old value: {old_config} - new value: {quoting}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_quoting_character(self, quoting_character: QuotingCharacter, scope: Scope = Scope.Suite):
        """
        Change the internal quoting character during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``quoting`` | Define a new quoting mode |

        == Example ==
        | Configure Quoting Character    "
        | Configure Quoting Character    '
        """
        old_config = self.quoting_character
        self.quoting_character_stack.set(quoting_character, scope)
        logger.debug(f"'file_type': old value: {old_config} - new value: {quoting_character}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_line_terminator(self, line_terminator: LineTerminator, scope: Scope = Scope.Suite):
        """
        Change the internal line terminator during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``line_terminator`` | Define a new line_terminator |

        == Example ==
        | Configure Line Terminator    LF
        | Configure Line Terminator    CRLF
        """
        old_config = self.line_terminator
        self.line_terminator_stack.set(line_terminator, scope)
        logger.debug(f"'file_type': old value: {old_config} - new value: {line_terminator}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_file_encoding(self, file_encoding: FileEncoding | str, scope: Scope = Scope.Suite):
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
        old_config = self.file_encoding
        self.file_encoding_stack.set(
            file_encoding.value if isinstance(file_encoding, FileEncoding) else file_encoding, scope
        )
        logger.debug(f"'file_type': old value: {old_config} - new value: {file_encoding}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_ignore_header(self, ignore_header: bool, scope: Scope = Scope.Suite):
        """
        Change the internal setting to (not) ignore the data header lines during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``ignore_header`` | Ignore / recognize header columns |

        == Example ==
        | Configure Ignore Header    True
        | Configure Ignore Header    False
        """

        old_config = self.ignore_header
        self.ignore_header_stack.set(ignore_header, scope)
        logger.debug(f"'ignore_header': old value: {old_config} - new value: {ignore_header}")
        return old_config

    @keyword(tags=["Configuration"])
    def configure_streaming(self, enable_streaming: bool, scope: Scope = Scope.Suite):
        """
        Enable / disable the direct streaming of data into the given table file.

        = Default Behaviour =
        By default, you can open a table, modify the content in the internal cache of the Table library and afterwards to write it into a table file.

        = Behaviour using Streaming =
        Using the streaming behaviour enables you to write e.g. rows directly into the table file instead of the internal cache.
        This can be required in case you need the data immediately in the file, and not in the cache.

        | =`Arguments`= | =`Description`= |
        | ``enable_streaming`` | Set to ``True`` to enable the streaming - default: ``False`` |

        == Example ==
        | Configure Streaming    True
        | Configure Streaming    False
        """
        old_config = self.enable_streaming
        self.enable_streaming_stack.set(enable_streaming, scope)
        logger.debug(f"'file_type': old value: {old_config} - new value: {enable_streaming}")
        return old_config
