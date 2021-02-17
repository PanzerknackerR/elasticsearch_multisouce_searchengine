#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import libraries to generate data
import random, uuid, time, json, sys
from psycopg2 import sql, Error, connect

ENV_NUMBEROFENTRIES = 1000;
ENV_NUMEROFRUNS = 50;
ENV_DBUSERNAME = "unicorn_user";
ENV_DBPASSWORD = "magical_password";
ENV_DBNAME = "rainbow_database";
ENV_DBHOST = "postgres"; # here postgres because we use a docker-compose, whitout we have to use ip
# requires 'random' library
def get_random_words(words_list, total=1):
    ran_words = []

    # enumerate over specified number of words
    while len(ran_words) < total:
        ran_words += [words_list[random.randint(0, len(words_list)-1)]]

    # return a string by joining the list of words
    return ' '.join(ran_words)

def create_postgres_json(size):

    # list to store JSON records
    records = []

    # random words to inject into records
    words = ["ObjectRocket's tutorials", 'orkb', "orkb's tutorials",
    "Postgres' psycopg2 adapter", "data's positronic brain", 'type', 'examples', 'foo', 'bar']

    # iterate over the number of records being created
    for rec_id in range(size):

        # create a new record dict
        new_record = {}

        # input a value for each table column
        new_record[ 'id' ] = uuid.uuid4().hex
        new_record[ 'str_col' ] = get_random_words( words, random.randint(1, len(words)) )
        new_record[ 'int_col' ] = random.randint(1, 6000)
        new_record[ 'bool_col' ] = [True, False][random.randint(0, 1)]
        new_record[ 'float_col' ] = random.uniform(1.5, 99.9)

        # append the new record dict to the list
        records += [ new_record ]

    # return the list of JSON records
    return records

def create_insert_records( json_array, table_name ):

    # get the columns for the JSON records
    columns = json_array[0].keys()

    # SQL column names should be lowercase using underscores instead of spaces/hyphens
    columns = [str(col).lower().replace(" ", "_") for col in columns]
    columns = [str(col).lower().replace("-", "_") for col in columns]
    print ("\ncolumns:", columns)

    # concatenate a string for the SQL 'INSERT INTO' statement
    sql_string = "INSERT INTO {}".format(table_name)
    sql_string = sql_string + " (" + ', '.join(columns) + ")\nVALUES "

    record_list = []
    for i, record in enumerate( json_array ):

        keys = record.keys()
        values = record.values()

        # use map() to cast all items in record list as a string
        #record = list(map(str, values))
        record = list(values)
        print (record)

        # fix the values in the list if needed
        for i, val in enumerate(record):

            if type(val) == str:
                if "'" in val:
                    # posix escape string syntax for single quotes
                    record[i] = "E'" + record[i].replace("'", "''") + "'"

        # cast record as string and remove the list brackets []
        record = str(record).replace("[", '')
        record = record.replace("]", '')

        # remove double quotes as well
        record = record.replace('"', '')

        # ..now append the records to the list
        record_list += [ record ]

    # enumerate() over the records and append to SQL string
    for i, record in enumerate(record_list):

        # use map() to cast all items in record list as a string
        #record = list(map(str, record))

        # append the record list of string values to the SQL string
        sql_string = sql_string + "(" + record + "),\n"

    # replace the last comma with a semicolon
    sql_string = sql_string[:-2] + ";"

    return sql_string

print ("\n")

#create one run an insert entrys in db
def insertRecords():
    # generate records for Postgres
    json_records = create_postgres_json(ENV_NUMBEROFENTRIES);
    
    # use the JSON library to convert JSON array into a Python string
    json_records_str = json.dumps(json_records, indent=4)
    
    print ("\nPostgres records JSON string:")
    print (json_records_str)
    
    # convert the string back to a dict (JSON) object
    json_records = json.loads(json_records_str)
    
    # allow the table name to be passed to the script
    if len(sys.argv) > 1:
        table_name = '_'.join(sys.argv[1:])
    else:
        # otherwise use a default table name
        table_name = 'python_test'
    
    # call the function to create INSERT INTO SQL string
    sql_str = create_insert_records( json_records, table_name )
    
    print ('\nsql_str:')
    print (sql_str)
    
    
    # save the generated Postgres records in a JSON file
    with open('postgres-records.json', 'w') as output_file:
        output_file.write(str(json_records))
    
    try:
        # declare a new PostgreSQL connection object
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
        print ("\ncreated cursor object:", cur)
    
    except Error as err:
        print ("\npsycopg2 connect error:", err)
        conn = None
        cur = None
    
    # only attempt to execute SQL if cursor is valid
    if cur != None:
    
        try:
            sql_resp = cur.execute( sql_str )
            conn.commit()
            print ('finished INSERT INTO execution')
    
        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()
    
        # close the cursor and connection
        cur.close()
        conn.close()
        
#interate the runs
def run():
    i = 1;
    while i <= ENV_NUMEROFRUNS:
      insertRecords();
      i += 1;
#to start the Programm      
run();