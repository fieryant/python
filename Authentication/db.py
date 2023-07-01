# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:39:34 2023

@author: BlinkerBoy
"""

import sqlite3 as sq

con = sq.connect('db.sqlite')

cur = con.cursor()