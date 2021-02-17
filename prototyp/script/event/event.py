# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import random, uuid, time, json, sys
import time
# Connect to the elastic cluster
es=Elasticsearch([{'host':'elasticsearch','port':9200}])

e1={

}

def get_random_words(words_list, total=1):
    ran_words = []

    # enumerate over specified number of words
    while len(ran_words) < total:
        ran_words += [words_list[random.randint(0, len(words_list)-1)]]

    # return a string by joining the list of words
    return ' '.join(ran_words)

def create_event_json(size):
    # list to store JSON records
    records = []
    # random words to inject into records
    words = ["ObjectRocket's tutorials", 'orkb', "orkb's tutorials",
    "Postgres' psycopg2 adapter", "data's positronic brain", 'type', 'examples', 'foo', 'bar']
    # iterate over the number of records being created
    for rec_id in range(size):
        # input a value for each table column
        id_col=uuid.uuid4().hex
        string_col = get_random_words( words, random.randint(1, len(words)) )
        bool_col = [True, False][random.randint(0, 1)]
        int_col = random.randint(1, 6000)
        float_col = random.uniform(1.5, 99.9)
        doc= {
            "id": id_col,
            "str_col": string_col,
            "int_col": int_col,
            "bool_col": bool_col,
            "float_col" : float_col,
        }
        res = es.index(index='event_data',id=id_col,body=doc)
        print(res)
        
        
def run():
    x=0
    while x<10:
        print(x)
        create_event_json(10)
        time.sleep(x)
        x+=0.01
        
run()