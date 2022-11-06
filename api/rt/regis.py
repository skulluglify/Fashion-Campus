#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import pathlib
import platform

## REGISTRY MODULE .PYZ
def module_registry(package: str, fail_exit: bool = True) -> bool:

    SEPARATOR: str = ""

    for sep in (".", "/", "\\"):

        if sep in package:

            ## MULTIPLE SEPARATOR
            if SEPARATOR != "":

                if sep != SEPARATOR:

                    if fail_exit:

                        raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

                    return False

            SEPARATOR = sep
            continue

    ## SEPARATOR NOT FOUND
    if SEPARATOR == "":

        if fail_exit:

            raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

        return False

    if package.startswith(SEPARATOR):

        ## FAKE ROOTDIR
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

    files = [
        os.path.join(os.path.dirname(__file__), *PATH, f"{MODULE_NAME}.{MODULE_VERSION}.pyz"),
        os.path.join(os.path.dirname(__file__), *PATH, f"{MODULE_NAME}.pyz"),
    ]

    # platform.system().lower().startswith("linux")
    # platform.system().lower().startswith("darwin")
    # platform.system().lower().startswith("java")
    # platform.system().lower().startswith("windows")

    for file in files:

        path = pathlib.Path(file)

        if path.exists():
            if path.is_file():
                
                sys.path.insert(0, path.as_posix())
                return True

    if fail_exit:

        raise ModuleNotFoundError("Couldn`t find package '%s'!" % package)

    return False