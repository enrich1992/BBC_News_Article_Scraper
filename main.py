'''
Code written to query a keyword from a Hosted Mongo Database and return all articles containing keyword

Created on 18 April 2021
by Enrich Braz
'''


import pymongo     # to connect to hosted MongoDB
from fastapi import FastAPI  # FastAPI is preferred to flask as its easier and faster
from fastapi.encoders import jsonable_encoder  # encode final output in JSON format
import uvicorn  # for ASGI (Asynchronous Server Gateway Interface) implementation


# Create the App object
app = FastAPI()

# Connect to MongoDB database and access the stored database
connection_url = "mongodb+srv://enrich:enrich@cluster0.mri6u.mongodb.net/Articledatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_url)

Database = client.get_database('Articledatabase')
Article_tb = Database.Article_tb

# Create a Route which accepts a single parameter which will be the keyword you want to search
@app.get('/findbykeyword')
def findbykeyword(keyword: str):

    # Create a Text index for our article_body field using the create_index function of pymongo.
    # This breaks the field down into a series of strings to make search easier
    Article_tb.create_index([('article_body','text')])
    # Use the find function of pymongo to search for the string we want i.e. keyword
    query = Article_tb.find({"$text": { "$search" : keyword} })

    #  Extract all the docs that contain the keyword by referring to their id
    output = {}
    i = 0
    for x in query:
        output[i] = x
        output[i].pop('_id')
        i += 1

    # Return our final output as a JSON object
    return jsonable_encoder(output)




# Run the API with uvicorn. This wil run on the local host and port (http://127.0.0.1:8000)
if __name__ == '__main__':
    uvicorn.run(app)


#
# To execute the API type in the terminal $: uvicorn main:app --reload
# Once the connection is made go to http://127.0.0.1:8000/docs for the SWAGGER UI and enter keyword

# If you don't want to run the SWAGGER UI, then do not enter any parameter in the def findbykeyword() function
# a define a variable keyword with whatever word you want to search.
# On executing the API in terminal and once connection is made. Go to http://127.0.0.1:8000/findbykeyword


