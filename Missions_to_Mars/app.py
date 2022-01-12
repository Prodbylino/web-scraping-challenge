from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Get the Latest Mars information
    mars_data = mongo.db.collection.find_one()
    # If no record is found in mongodb, return a dictionary of empty values
    if (mars_data == None):
        mars_data = { "Most_Recent_News": {"title": "","paragraph": ""},
        "Featured_Image_URL": "", "Planet_Profile_Table_HTML_String": "",
        "Hemisphere_Image_URLs": [{"title": "","image_url": ""}, 
        {"title": "", "image_url": ""}, {"title": "","image_url": ""}, 
        {"title": "","image_url": ""}]}
    
    print(mars_data)

    # Return template and data
    return render_template("index.html", mission=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data_new = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data_new, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)




