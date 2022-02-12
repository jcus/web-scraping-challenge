from flask import Flask, render_template, redirect
#, url_for F
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

## Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/Mission_to_Mars_app")

# Use flask pymongo to set up the connection to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.marsData.find_one()

    # Return template and data
    return render_template("index.html", data = mars_data)
   ##print(mars_data)
   # return "Flas data loaded success"    


# Route that will trigger the scrape function and run app
@app.route("/scrape")
def scrape():
    # direct the collection data from mongo database 
    marsTable = mongo.db.marsData
    # drop the table if it exist
    mongo.db.marsData.drop()
    # Update the Mongo database using update and upsert=True
    #mongo.db.collection.insert_one(mars_data)
    
    # call scrape mars all scrape
    mars_data = scrape_mars.scrape_all()
    
    # take the dictionary and load into mongoDB
    marsTable.insert_one(mars_data)
    
    # go to the index route
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
