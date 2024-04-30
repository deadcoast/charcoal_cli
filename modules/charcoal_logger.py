import logging
from typing import Optional

from colorama import init

# Initialize colorama for colored CLI output
init()
# Initialize colorama
init(autoreset=True)

# Setup a logger
logger = logging.getLogger('CodeExtractor')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('code_extractor.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Setup logger for error logging
logging.basicConfig(filename='charcoal_error.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Setup logger
logging.basicConfig(filename='error_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Setup logger for info logging
logging.basicConfig(filename='charcoal_info.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def charcoal_info_logger(message: str):
    logger.info(message)


# Exception for handling extraction related errors
class ExtractionError(Exception):
    """Exception raised for errors that occur during code extraction."""

    def __init__(self, message: str, details: Optional[str] = None) -> None:
        """
        Initialize the class instance.

        Args:
            message (str): The message to be passed to the superclass.
            details (Optional[str]): Additional details for the instance.

        Returns:
            None
        """
        super().__init__(message)
        self._details = details

    @property
    def extraction_details(self):
        return self._details

    @extraction_details.setter
    def extraction_details(self, value):
        if value is not None:
            # Perform validation logic here
            self._details = value

    def __str__(self):
        return f"An error occurred during code extraction. Details: {self._details}"

    def log_error_details(self):
        logger = logging.getLogger(__name__)
        logger.error(str(self))

    def log_info_details(self):
        logger = logging.getLogger(__name__)
        logger.info(str(self))

    def log_debug_details(self):
        logger = logging.getLogger(__name__)
        logger.debug(str(self))

    def log_warning_details(self):
        logger = logging.getLogger(__name__)
        logger.warning(str(self))

    def log_critical_details(self):
        logger = logging.getLogger(__name__)
        logger.critical(str(self))

    def log_exception_details(self):
        logger = logging.getLogger(__name__)
        logger.exception(str(self))

    def log_fatal_details(self):
        logger = logging.getLogger(__name__)
        logger.fatal(str(self))


# Exception for handling extraction related errors
class CriticalError(Exception):
    """Exception raised for errors that occur during code extraction."""

    def __init__(self, message: str, details: Optional[str] = None) -> None:
        """
        Initialize the class instance.

        Args:
            message (str): The message to be passed to the superclass.
            details (Optional[str]): Additional details for the instance.

        Returns:
            None
        """
        super().__init__(message)
        self._details = details

    @property
    def extraction_details(self):
        return self._details

    @extraction_details.setter
    def extraction_details(self, value):
        if value is not None:
            # Perform validation logic here
            self._details = value

    def __str__(self):
        return f"An error occurred during code extraction. Details: {self._details}"

    def log_error_details(self):
        logger = logging.getLogger(__name__)
        logger.error(str(self))
