#!/bin/bash

# MySQL Configuration
MYSQL_SERVER=127.0.0.1
MYSQL_DATABASE=mysql
MYSQL_USERNAME=admin
MYSQL_PASSWORD=admin

echo "Dropping tables and collections..."

# Drop MySQL tables
mysql -h $MYSQL_SERVER -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "DROP TABLE IF EXISTS benefits"
mysql -h $MYSQL_SERVER -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "DROP TABLE IF EXISTS salaries"
mysql -h $MYSQL_SERVER -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "DROP TABLE IF EXISTS employee_counts"
mysql -h $MYSQL_SERVER -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "DROP TABLE IF EXISTS job_postings"
mysql -h $MYSQL_SERVER -u $MYSQL_USERNAME -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "DROP TABLE IF EXISTS companies"



# MongoDB Configuration
MONGO_HOST=127.0.0.1
MONGO_PORT=27017
MONGO_DATABASE=admin
MONGO_USERNAME=root
MONGO_PASSWORD=rootpassword

# Drop MongoDB collections
mongo $MONGO_HOST:$MONGO_PORT/$MONGO_DATABASE -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin --eval "db.benefits.drop()"
mongo $MONGO_HOST:$MONGO_PORT/$MONGO_DATABASE -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin --eval "db.salaries.drop()"
mongo $MONGO_HOST:$MONGO_PORT/$MONGO_DATABASE -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin --eval "db.employee_counts.drop()"
mongo $MONGO_HOST:$MONGO_PORT/$MONGO_DATABASE -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin --eval "db.job_postings.drop()"
mongo $MONGO_HOST:$MONGO_PORT/$MONGO_DATABASE -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin --eval "db.companies.drop()"

echo "Tables and collections dropped successfully."
