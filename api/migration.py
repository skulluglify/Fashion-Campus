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

    migration_db = os.path.join(os.path.dirname(__file__), "migration.db")

    if os.path.exists(migration_db):
        if os.path.isfile(migration_db):

            os.remove(migration_db)

    sqlx_migration(e, sqlx.create_engine("sqlite:///" + migration_db))