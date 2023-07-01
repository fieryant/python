# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:35:45 2023

@author: BlinkerBoy
"""

import sqlite3 as sq

con = sq.connect('db.sqlite')

cur = con.cursor()

cur.execute("drop table if exists users")

cur.execute("""CREATE TABLE "users" (
	"id"	INTEGER,
	"username"	,
	"password"	,
	PRIMARY KEY("id" AUTOINCREMENT)
    UNIQUE("username")
)""")
