#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import rt.regis
rt.regis.module_registry(".modules.sqlx")

from utils import call_engine, call_local_engine

from sqlx import sqlx_migration

if str(__name__).upper() in ("__MAIN__",):

    ## Copyright (C) 2022 By Ahmad Asy Syafiq

    mode = "push"

    migration_db = os.path.join(os.path.dirname(__file__), "migration.db")

    if mode == "pull":

        if os.path.exists(migration_db):
            if os.path.isfile(migration_db):

                os.remove(migration_db)

        sqlx_migration(call_engine(), call_local_engine())
    
    elif mode == "push":

        sqlx_migration(call_local_engine(), call_engine())
    