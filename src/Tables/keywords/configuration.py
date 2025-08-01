from ..utils.settings import FileEncoding, FileType, Delimiter
from ..general.library_attributes import LibraryAttributes

from robot.api.deco import keyword

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
    def configure_delimiter(self, delimiter: Delimiter):
        """
        Change the internal delimiter during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``delimiter`` | Define a new delimiter |

        == Example ==
        | Configure Delimiter    ;
        | Configure Delimiter    ,
        | Configure Delimiter    \\t
        """
        self.delimiter = delimiter

    @keyword(tags=["Configuration"])
    def configure_file_encoding(self, file_encoding: FileEncoding):
        """
        Change the internal file encoding during your test execution dynamically.

        | =`Arguments`= | =`Description`= |
        | ``file_encoding`` | Define a new file encoding |

        == Example ==
        | Configure File Encoding    UTF8
        | Configure File Encoding    UTF16
        | Configure File Encoding    LATIN1
        """
        self.file_encoding = file_encoding

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
