from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# initialize flask
app = Flask(__name__)

#  start server before executing
client = pymongo.MongoClient('mongodb://localhost:27017/')

############################## ROUTES ##############################
# default route that renders index.html template
@app.route("/")
def index():
    # find data 
    mars = client.db.mars.find_one()
    # return template
    return render_template("index.html", mars=mars)

# scrape route
@app.route("/scrape")
def scrape():
    mars = client.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)