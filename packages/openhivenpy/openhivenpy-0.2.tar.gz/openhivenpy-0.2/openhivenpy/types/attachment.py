"""
Attachment File which implements the Hiven Attachment type and its methods
(endpoints)

---

Under MIT License

Copyright © 2020 - 2021 Luna Klatzer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Used for type hinting and not having to use annotations for the objects
from __future__ import annotations

import logging
# Only importing the Objects for the purpose of type hinting and not actual use
from typing import TYPE_CHECKING

from .hiven_type_schemas import AttachmentSchema, get_compiled_validator
from ..base_types import DataClassObject
from ..utils import log_type_exception

if TYPE_CHECKING:
    from .. import HivenClient

logger = logging.getLogger(__name__)

__all__ = ['Attachment']


class Attachment(DataClassObject):
    """ Represents a Hiven Message Attachment containing a file """
    _json_schema: dict = AttachmentSchema
    json_validator = get_compiled_validator(_json_schema)

    @log_type_exception('Attachment')
    def __init__(self, data: dict, client: HivenClient):
        """
        Represents a Hiven Message Attachment containing a file

        :param data: Data that should be used to create the object
        :param client: The HivenClient
        """
        super().__init__()
        self._filename = data.get('filename')
        self._media_url = data.get('media_url')
        self._raw = data.get('raw')
        self._client = client

    @classmethod
    def format_obj_data(cls, data: dict) -> dict:
        """
        Validates the data and appends data if it iis missing that would be
        required for the creation of an instance.

        :param data: Data that should be validated and used to form the object
        :return: The modified dictionary, which can then be used to create a 
         new class instance
        """
        data['raw'] = {**data.pop('raw', {}), **data}
        return cls.validate(data)

    @property
    def filename(self) -> str:
        """ Name of the file """
        return getattr(self, '_filename', None)

    @property
    def media_url(self) -> str:
        """ Media-url to access the file """
        return getattr(self, '_media_url', None)

    @property
    def raw(self) -> dict:
        """ The raw data dictionary received over the Swarm """
        # Different files have different attribs
        return getattr(self, '_raw', None)
