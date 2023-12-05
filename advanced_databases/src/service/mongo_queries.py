import pandas as pd
from pymongo import MongoClient
import time

mongo_client = MongoClient('mongodb://root:rootpassword@localhost:27017/admin')
db = mongo_client.admin

salaries_collection = db.salaries
jobs_collection = db.job_postings
query1 = [{"$group": {
    "_id": "$salary_id",
    "avg_max_salary": {"$avg": "$max_salary"}
}
},
    {"$sort": {"avg_max_salary": -1}
     }]

doc = salaries_collection.aggregate(query1)
result = list(doc)
print(len(result))
for row in doc:
    print(row)

# ---------------------------


query2 = [
    {"$group": {"_id": {"company_id": "$company_id", "location": "$location"},
                "count": {"$sum": 1}
                }
     },
    {"$sort": {"_id.location": 1, "count": -1}},
    {"$group": {"_id": "$_id.location",
                "topCompany": {"$first": "$_id.company_id"}}
     },
    {"$project": {"_id": 0, "company_id": "$topCompany", "location": "$_id"}}
]

doc = jobs_collection.aggregate(query2)
result = list(doc)
print(len(result))
for row in doc:
    print(row)

# Similar to LIKE '%er%'
query3 = [
    {"$match": {'title': {'$regex': '/er$/'}}
     },
    {'$lookup': {'from': "companies",
                 'localField': "company_id",
                 'foreignField': "company_id",
                 'as': "company"}
     },
    {'$unwind': "$company"},
    {'$lookup': {'from': "benefits",
                 'localField': "job_id",
                 'foreignField': "job_id",
                 'as': "benefits"}
     },
    {'$lookup': {'from': "employee_counts",
                 'localField': "company.company_id",
                 'foreignField': "company_id",
                 'as': "employee_counts"}
     },
    {'$group': {'_id': {'company_id': "$company.company_id",
                        'company_name': "$company.name",
                        'employee_count': {'$ifNull': ["$employee_counts.employee_count", 0]}
                        },
                'job_count': {'$sum': 1}}
     },
    {'$match': {'job_count': {'$gt': 5}}
     },
    {'$sort': {'job_count': -1}
     },
    {'$project': {'_id': 0,
                  'company_id': "$_id.company_id",
                  'company_name': "$_id.company_name",
                  'employee_count': "$_id.employee_count",
                  'job_count': "$job_count"}
     }]

print("QUERY3 1")
doc = jobs_collection.aggregate(query3)
result = list(doc)
print(len(result))
for row in result:
    print(row)

query3 = [
    {"$match": {'title': {'$regex': 'er$'}}},
    {'$lookup': {'from': "companies",
                 'localField': "company_id",
                 'foreignField': "company_id",
                 'as': "company"}},
    {'$unwind': "$company"},
    {'$lookup': {'from': "benefits",
                 'localField': "job_id",
                 'foreignField': "job_id",
                 'as': "benefits"}},
    {'$lookup': {'from': "employee_counts",
                 'localField': "company.company_id",
                 'foreignField': "company_id",
                 'as': "employee_counts"}},
    {'$group': {'_id': {'company_id': "$company.company_id",
                        'company_name': "$company.name",
                        'employee_count': {'$ifNull': ["$employee_counts.employee_count", 0]}
                        },
                'job_count': {'$sum': 1}}},
    {'$match': {'job_count': {'$gt': 5}}},
    {'$sort': {'job_count': -1}},
    {'$project': {'_id': 0,
                  'company_id': "$_id.company_id",
                  'company_name': "$_id.company_name",
                  'employee_count': "$_id.employee_count",
                  'job_count': "$job_count"}}
]

print("QUERY3 2")
#doc = jobs_collection.aggregate(query3)
##print(len(result))
#counter = 0
#for row in result:
    #for ec in row['employee_count']:
        #print(row['company_id'], ",", row['company_name'], ",", ec, ",", row['job_count'])
        #counter += 1
#print(counter)


query3 = [
    {"$match": {'title': {'$regex': 'er$'}}},
    {'$lookup': {'from': "companies",
                 'localField': "company_id",
                 'foreignField': "company_id",
                 'as': "company"}},
    {'$unwind': "$company"},
    {'$lookup': {'from': "benefits",
                 'localField': "job_id",
                 'foreignField': "job_id",
                 'as': "benefits"}},
    {'$lookup': {'from': "employee_counts",
                 'localField': "company.company_id",
                 'foreignField': "company_id",
                 'as': "employee_counts"}},
    {'$group': {'_id': {'company_id': "$company.company_id",
                        'company_name': "$company.name",
                        'employee_count': {'$ifNull': ["$employee_counts.employee_count", 0]}
                        },
                'job_count': {'$sum': 1},
                'job_ids': {'$addToSet': "$job_id"}}},
    {'$match': {'job_count': {'$gt': 5}}},
    {'$sort': {'job_count': -1}},
    {'$project': {'_id': 0,
                  'company_id': "$_id.company_id",
                  'company_name': "$_id.company_name",
                  'employee_count': "$_id.employee_count",
                  'job_count': "$job_count",
                  'job_ids': "$job_ids"}}
]


print("QUERY3 3")
#doc = jobs_collection.aggregate(query3)
#result = list(doc)
#print(len(result))
#counter = 0
#for row in result:
    #for ec in row['employee_count']:
        #print(row['company_id'], ",", row['company_name'], ",", ec, ",", row['job_count'])
        #counter += 1
#print(counter)


query_aux = [
    {"$match": {"company_id" : 163139} },
    {"$match": {'title': {'$regex': 'er$'}}
     }
]
doc = jobs_collection.aggregate(query_aux)
counter = 0
for row in doc:
    print(row)
    counter += 1
print(counter)