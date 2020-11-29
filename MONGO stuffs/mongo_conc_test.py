from pymongo import MongoClient

# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# client = MongoClient(<<MONGODB URL>>)
client = MongoClient('mongodb://localhost:27017')

# db=client.pymongo_test
db = client['pymongo_test']

# Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

# Insert data to mongodb schema pymongo_test
posts = db.posts

post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}
new_result = posts.insert_many([post_1, post_2, post_3])

# print _id of inserted documents
# print('Multiple posts: {0}'.format(new_result.inserted_ids))

# print detailed documents
for i in posts.find({}):
    pprint(i)