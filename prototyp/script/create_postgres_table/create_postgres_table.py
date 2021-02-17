#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import libraries to generate data
import random, uuid, time, json, sys
from psycopg2 import sql, Error, connect

ENV_NUMBEROFENTRIES = 700;
ENV_NUMEROFRUNS = 10;
ENV_DBUSERNAME = "unicorn_user";
ENV_DBPASSWORD = "magical_password";
ENV_DBNAME = "rainbow_database";
ENV_DBHOST = "postgres"; # here postgres because we use a docker-compose, whitout we have to use ip
def create_table():
    """ create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE python_test(
            id UUID PRIMARY KEY,
            str_col VARCHAR(5000),
            int_col SMALLINT,
            bool_col BOOLEAN,
            float_col DECIMAL)
        """
        )
    try:
        # connect to the PostgreSQL server
        conn = connect(
            dbname = ENV_DBNAME,
            user = ENV_DBUSERNAME,
            host = ENV_DBHOST,
            #port="5436",
            password = ENV_DBPASSWORD,
            # attempt to connect for 3 seconds then raise exception
            connect_timeout = 3
            )
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except Error as err:
        print ("\npsycopg2 connect error:", err)
        conn = None
        cur = None
    # only attempt to execute SQL if cursor is valid
    if cur != None:    
        # close the cursor and connection
        cur.close()
        conn.close()
        
#to start the Programm      
create_table();