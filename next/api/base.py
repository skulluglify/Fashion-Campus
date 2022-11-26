#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class UnicornException(Exception):
    
    message = "error, something went wrong"
    status_code = 400
    
    def __init__(self, message: str, status_code: int = 400):

        self.message = message
        self.status_code = status_code