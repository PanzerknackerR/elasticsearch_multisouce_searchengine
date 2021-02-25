## How to use the prototype

For comfort, we first open three terminals and navigate to the repository in each case.
The first [1] terminal is for controlling the docker-compose. The second [2] is for the PostgreSQL-DB and the third [3] is for the MySQL-DB.
And now to the procedure:

1. [1]: ```docker-compose up -d postgres mysql elasticsearch kibana``` First, we provide the infrastructure.
   - For this purpose, the two databases are started. Elasticsearch (single node) and Kibana are prepared. The PostgreSQL database is initialized completely empty. The MySQL database is filled with three sample tables and associated sample data during initialization. In addition, triggers are inserted, which are later used for a continuous update of the Elasticsearch database. 
2. [2]: ```docker-compose run postgres bash``` Open a bash to login into the DB
   - ```psql --host=postgres --username=unicorn_user --dbname=rainbow_database``` Login into the DB
     - (PW: magical_password) 
   - ```\d``` Show Tables
   - You have to see, that the Database is empty. In the next steps we create an table, and fill this table with example data. We used this way, so that it is easy to customize the data to be created. Also, everyone can adjust the amount of data to be inserted accordingly.
3. [1]: ```docker-compose up create_table-postgres``` To create the table
   - [2]: ```\d``` Show Tables
   - [2]: ```select count(*) from python_test;``` Show Entries
   - Now we see that the table has been created but no data is contained yet.
4. [1]: ```docker-compose up generate_data-postgres```now we generate data and insert them into the PostgreSQL-DB
   - Here you can change the amount of data and also the appearance of the data arbitrarily on the basis of the script. After a change do not forget to rebuild the container.
     -```docker-compose build generate_data-postgres``` the same applies to the create_table script
   - [2]: ```select count(*) from python_test;``` Verify that the number of data is there
   - [2]: ```select * from python_test LIMIT 5;``` Verify that the data looks as expected
5. http://localhost:5601/app/dev_tools#/console now we can also look in Kibana in the Dev Tools
   -  ```
      GET python_test/_search{
      "query": {
         "match": {
           "str_col": "Bestsellerlisten"
           }
         }
       }
      ```
      With this query we can see that there are no entries yet. The value can be changed as desired.
6. ```docker-compose up logstash_postgres``` Now we start Logstash to bring our data into elasticsearch. Here we have provided only one initialization pipeline.
7. Repeat step 5 and look at the results. The data was successfully brought into Elasticsearch and can be processed using Kibana.
8. [3]: ```docker exec -it demo_mysql bash```Now we start the second part of the demo, now we look at the MySQL DB. 
   -  ```mysql -uavid_reader -pi_love_books``` Login into the DB 
   -  ```use books;``` Choose DB.
   -  ```show tables;``` look at the Tables
   -  ```show TIGGERS \G;``` look at the Triggers
   -  ```select * from books Limit 5;``` look at some entries 
   -  We have here a continuous adjustment by the Tigger, which is efficient, in contrast to a "Full Diff Compare". Continuous insertion strategy is defined in the pipeline.
9. http://localhost:5601/app/dev_tools#/console now we can again look in Kibana in the Dev Tools
   -  ```
      GET books/_search{
      "query": {
         "match": {
           "isbn": "9780001000391"
           }
         }
       }
      ```
      With this query we can see that there are no entries yet. The value can be changed as desired.
10. [1]: ```docker-compose up -d logstash_mysql``` Now we start the pipelines, here are two defined one for initializing and one for continuous changes.
    - Repeat step 9 and look at the results.
    - [3]: ```delete from books where isbn='9780001000391';``` Delete this entry
    - [3]: ```select * from books Limit 5;``` Verity that its gone
    - Repeat step 9 and look at the results.
    - [3] ```update books set title ='NEW TITLE' where isbn='9780006482079';``` Modify one Entry
    - [3]: ```select * from books Limit 5;``` Verity that the modifications are correct
    - Repeat step 9, but change the isbn value to ```"9780006482079"```
    - We have only ensured that a denominalization and also a continuous adjustment is possible.
11. [1]: ```docker-compose up eventdata``` Here now runs a python script that pushes all always 10 entries into Elasticsearch. Time intervals from 0.0 always 0.01 second more pause, at 10 seconds it stops.
12. http://localhost:5601/app/dev_tools#/console now we can again look in Kibana in the Dev Tools
   -  ```
      GET event_data/_search{
      "query": {
         "match": {
           "str_col": "Bestsellerlisten"
           }
         }
       }
      ```
      With this query we can see that there are some Results, which change over time, the more often we make the request
   - Thereby we see that also the direct insertion of data into Elasticsearch is possible. 
  
         

	  		  
          
