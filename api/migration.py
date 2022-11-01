#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from api.utils import call_engine, call_local_engine
import rt.regis

rt.regis.module_registry(".modules.sqlx")

from sqlx import sqlx_migration

if str(__name__).upper() in ("__MAIN__",):

    ## Copyright (C) 2022 By Ahmad Asy Syafiq

    migration_db = os.path.join(os.path.dirname(__file__), "migration.db")

    if os.path.exists(migration_db):
        if os.path.isfile(migration_db):

            os.remove(migration_db)

    sqlx_migration(call_engine(), call_local_engine())
    # sqlx_migration(call_local_engine(), call_engine())