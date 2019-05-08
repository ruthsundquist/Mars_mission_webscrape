import scrape_mars

from flask import Flask
from flask import render_template
import pymongo
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
clientconnection = pymongo.MongoClient(conn)
#this is the Mongo database connection and the db is called mars_scrape
db = clientconnection.mars_scrape
app= Flask(__name__)
@app.route("/scrape")
#marsnews is the collection of scraped results for Web page
def scrapemongo():
    variable =  scrape_mars.scrape()
    db.marsnews.insert(variable)
    return ("success")
@app.route("/")
# marsite is the function that returns the website as a dictionary cast as a string is called index
def marsite():
    index = db.marsnews.find_one()
    return render_template('index.html', index=index)
    #return str(index)
if __name__ == "__main__":
    app.run(debug=True)

# copy http into a browser to view contents call index stored in Mongo mars_scrape

