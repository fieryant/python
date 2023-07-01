# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:36:54 2023

@author: BlinkerBoy
"""

from db import cur, con
import bcrypt as bc
from sqlite3 import IntegrityError

"""User Model"""


class user:
    table_name = 'users'

    primary_key = 'id'

    attributes = [primary_key, 'username', 'password']

    # relational_operators = ['=','!=', '>', '<', '<=','>=', '<>']

    def __init__(self):
        self.where_args = []

    def __str__(self):
        formated_string = ''.join(
            [f"{item}: "+"{}\n" for item in self.attributes])
        return formated_string.format(*[getattr(self, name) for name in self.attributes])

    def __repr__(self):
        return self.__str__()

    @classmethod
    def __get_create_query(cls):
        # get a list of attributes without the primary key
        attrs = [i for i in cls.attributes if i != cls.primary_key]
        attr = ', '.join(attrs)
        values = '?,'*len(attrs)
        values = values.removesuffix(',')
        return f"insert into {cls.table_name}({attr}) values({values})"

    # @classmethod
    def __get_fetch_query(self, *cols):
        temp_cols = ', '
        if len(cols) == 0:
            temp_cols = '*'
        else:
            temp_cols = temp_cols.join(cols)
        query = f"select {temp_cols} from {self.table_name}"
        query += self.__get_where_args()
        return query

    def __get_delete_query(self):
        query = f"delete from {self.table_name} where id = ?"
        return query

    def __get_where_args(self):
        query = ''
        # track how many where condition is applied
        where_count = 0
        if len(self.where_args) != 0:
            query += ' where '
            for arg in self.where_args:
                if where_count:
                    # if there is more that one condition then use and or
                    query += f" {arg['logic']} "
                # filter the dictionary: get all items without the logic
                values = {x: arg[x] for x, y in arg.items() if x != 'logic'}
                query += ' '.join(values.values())
                # simplified version of above two line
                # query += f" {arg['col_name']} {arg['operator']} '{arg['value']}'"
                where_count += 1
        return query

    def __make_object(self, obj, *cols):
        temp_obj = self.__class__()
        if len(cols) == 0:
            cols = tuple(self.attributes)
        for item, value in zip(cols, obj):
            setattr(temp_obj, item, value)
        return temp_obj

    @classmethod
    def create(cls, name, password):
        try:
            # run the sql query with value
            cur.execute(cls.__get_create_query(), [
                        name, cls.get_hashed_pass(password)])
            # commit is required when inserting value into the databse
            con.commit()
        except IntegrityError:
            print('this username is taken')
        except:
            print('Unable to create user')

    """Get a collection of users"""

    def get(self, *cols):
        try:
            res = cur.execute(self.__get_fetch_query(*cols))
        except:
            raise Exception(self.__get_fetch_query(*cols))
        collection = []
        # make a collection of user object
        for u in res:
            collection.append(self.__make_object(u, *cols))
        return collection

    def first(self):
        objects = self.get()
        if(len(objects)) == 0:
            return None
        else:
            return objects[0]

    """Apply some condition on the query"""

    def where(self, column, operator, value, logic='and'):
        self.where_args.append({
            'col_name': column,
            'operator': operator,
            'value': f"'{value}'",
            'logic': logic
        })
        return self

    """Where helper with = by defalut"""

    def where_equal(self, column, value, logic='and'):
        self.where(column, '=', value, logic)
        return self

    @staticmethod
    def get_hashed_pass(password):
        return bc.hashpw(password.encode('utf-8'), bc.gensalt())

    @staticmethod
    def check_hashed_pass(password, hashed_password):
        return bc.checkpw(password.encode('utf-8'), hashed_password)

    """Delete the current object"""

    def delete(self):
        cur.execute(self.__get_delete_query(), [self.id])
        con.commit()
        return True

    """Find a model with given primary key"""
    @classmethod
    def find(cls, id):
        res = cur.execute(cls().__get_fetch_query() +
                          f' where {cls.primary_key} = ? limit 1', [id])
        obj = res.fetchone()
        # check if the value was found or not.
        # res.fetchone() returns
        if obj == None:
            raise Exception(f'Model not found! with {cls.primary_key} = {id}')
        return cls.__make_object(obj)

    """Count the number of model ib db
    can be chained with where condition
    """

    def count(self):
        query = f'select count(*) from {self.table_name}'
        res = cur.execute(query + self.__get_where_args())
        return res.fetchone()[0]
# print(user().count())
# user().create('anis', 'password')
