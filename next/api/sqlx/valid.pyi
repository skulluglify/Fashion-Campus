import re

class Validation:
    EMAIL_ADDRESS_REGEX: re.Pattern
    ENSURE_PASSWORD_HAS_FOUR_DIGITS_OR_MORE_REGEX: re.Pattern
    ENSURE_PASSWORD_HAS_LENGTH_EIGHT_OR_MORE_REGEX: re.Pattern
    ENSURE_PASSWORD_HAS_ONE_SPECIALCASE_OR_MORE_REGEX: re.Pattern
    ENSURE_PASSWORD_HAS_ONE_UPPERCASE_OR_MORE_REGEX: re.Pattern
    ENSURE_PASSWORD_HAS_TWO_LOWERCASE_OR_MORE_REGEX: re.Pattern
    PHONE_NUMBER_REGEX: re.Pattern
    STRONG_PASSWORD_REGEX: re.Pattern
    @classmethod
    def strong_password(cls, password: str) -> bool: ...
    @classmethod
    def ensure_password_has_two_lowercase_or_more(cls, password: str) -> bool: ...
    @classmethod
    def ensure_password_has_one_uppercase_or_more(cls, password: str) -> bool: ...
    @classmethod
    def ensure_password_has_four_digits_or_more(cls, password: str) -> bool: ...
    @classmethod
    def ensure_password_has_one_specialcase_or_more(cls, password: str) -> bool: ...
    @classmethod
    def ensure_password_has_length_eight_or_more(cls, password: str) -> bool: ...
    @classmethod
    def email_address(cls, email: str) -> bool: ...
    @classmethod
    def phone_number(cls, phone: str) -> bool: ...
