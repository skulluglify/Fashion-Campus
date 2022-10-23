#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import re

class Validation:

    EMAIL_ADDRESS_REGEX: re.Pattern
    EMAIL_ADDRESS_REGEX = re.compile("""^[a-zA-Z0-9.\-_+]+@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])(?!\.)$""")

    PHONE_NUMBER_REGEX: re.Pattern
    PHONE_NUMBER_REGEX = re.compile("""^(\+\d{1,2}|0)(\s|)?\(?\d{3,4}\)?(\s|[.-]|)\d{3,4}(\s|[.-]|)\d{3,4}((\s|[.-]|)\d{3,4}|)$""")

    @classmethod
    def email_address(cls, email: str) -> bool:

        return re.match(cls.EMAIL_ADDRESS_REGEX, email) is not None

    @classmethod
    def phone_number(cls, phone: str) -> bool:

        return re.match(cls.PHONE_NUMBER_REGEX, phone) is not None
