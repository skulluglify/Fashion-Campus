#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import pathlib
import platform

from .runtime import RtInit

def module_init():

    ## REGISTRY RUNTIME LIBRARY
    RtInit()

## REGISTRY MODULE .PYZ
def module_registry(package: str, fail_exit: bool = True, verbose: bool = False) -> bool:

    module_init()

    SEPARATOR: str = ""

    for sep in (".", "/", "\\"):

        if sep in package:

            ## SEPARATOR ALREADY SET
            if SEPARATOR != "":

                ## DIFFERENT SEPARATOR
                if SEPARATOR != sep:

                    if fail_exit:

                        raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

                    return False

            SEPARATOR = sep

    ## SEPARATOR NOT FOUND
    if SEPARATOR == "":

        if fail_exit:

            raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

        return False

    ## FAKE ROOTDIR
    if package.startswith(SEPARATOR):

        ## LENGTH OF SEPARATOR EQUAL TO 1 
        package = package[1:]

    PATH = []
    MODULE_NAME: str = ""
    PACKAGE = package.lower().split(SEPARATOR)

    if 2 <= len(PACKAGE):

        *PATH, MODULE_NAME = PACKAGE

    elif len(PACKAGE) == 1:

        MODULE_NAME = PACKAGE[0]

    else:

        if fail_exit:

            raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

        return False

    MODULE_VERSION = "py" + ".".join(platform.python_version_tuple()[:2])

    CURRENT_DIR = os.path.dirname(__file__)

    if CURRENT_DIR.endswith(".pyz/rt"):

        CURRENT_DIR = os.path.dirname(CURRENT_DIR)
        CURRENT_DIR = os.path.dirname(CURRENT_DIR)

    files = [
        os.path.join(CURRENT_DIR, *PATH, f"{MODULE_NAME}.{MODULE_VERSION}.pyz"),
        os.path.join(CURRENT_DIR, *PATH, f"{MODULE_NAME}.pyz"),
    ]

    # if verbose:

    #     for file in files:

    #         print("\033[1;33;40m[ PATH ]\033[0m", file)

    # platform.system().lower().startswith("linux")
    # platform.system().lower().startswith("darwin")
    # platform.system().lower().startswith("java")
    # platform.system().lower().startswith("windows")

    for file in files:

        path = pathlib.Path(file)

        if path.exists():
            if path.is_file():

                if verbose:

                    print("\033[1;33;40m[ LOG ]\033[0m", file)
                
                sys.path.insert(0, path.as_posix())
                return True

    if fail_exit:

        raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

    return False