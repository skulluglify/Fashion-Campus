#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import rt.regis

rt.regis.module_registry(".modules.sqlx")

from sqlx import *
from schema.meta import db_init

if str(__name__).upper() in ("__MAIN__",):

    ## Copyright (C) 2022 By Ahmad Asy Syafiq
        
    e, m = db_init()

    if os.path.exists("migration.db"):
        if os.path.isfile("migration.db"):

            os.remove("migration.db")

    sqlx_migration(e, sqlx.create_engine("sqlite:///migration.db"))