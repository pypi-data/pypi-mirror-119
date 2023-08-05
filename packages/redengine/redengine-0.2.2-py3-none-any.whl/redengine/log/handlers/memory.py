
import logging
import csv
import io
import os
from logging import Formatter, FileHandler, Handler, LogRecord
from pathlib import Path
from typing import List, Dict
from dateutil.parser import parse as parse_datetime


class MemoryHandler(Handler):
    """
    Logging handler for storing the records in memory.
    """

    def __init__(self, store_as="record", **kwargs):
        """Initialize the class

        Parameters
        ----------
        store_as : str, optional
            How the records are stored.
            Options: [record, dict], 
            by default "record"
        """
        super().__init__(**kwargs)
        self.records = []
        self.store_as = store_as
        
    def emit(self, record:logging.LogRecord):
        msg = self.format(record)

        if self.store_as == "record":
            self.records.append(record)
        elif self.store_as == "dict":
            self.records.append(vars(record))
        else:
            raise ValueError(f"Invalid value: {self.store_as}")

# Extras
    def read(self, **kwargs) -> List[Dict]:
        "Read the logs"
        yield from self.records
        
    def clear_log(self):
        "Empty the logging storage"
        self.records = []