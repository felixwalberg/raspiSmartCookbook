from flask import *
import mysql.connector
import json
import sys
import time

# for probe
import Probe.probeIS as probeFunc
import threading

# boolean to run probe loop
probe = False
#test

app = Flask(__name__)


# load folder for database credentials
credentials = json.load(open("credentials.json", "r"))

# all routes for different recipe categories

@app.route('/breakfast', methods=['GET'])
def breakfast():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )
    cursor = database.cursor()

    # Query to return recipes from the Breakfast category
    query = "SELECT * FROM recipesNew_data WHERE category = 'Breakfast' ORDER BY Name;"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("breakfast.html", data = data, name="Felix Walberg", Title="Breakfast")

@app.route('/baking', methods=['GET'])
def baking():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )

    cursor = database.cursor()

    # Query to return recipes from the Baking category
    query = "SELECT * FROM recipesNew_data WHERE Category = 'Baking' ORDER BY Name;"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("baking.html", data = data, Name="Felix Walberg", Title="Baking")

@app.route('/meat', methods=['GET'])
def meat():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )

    cursor = database.cursor()

    # Query to return recipes from the Meat category
    query = "SELECT * FROM recipesNew_data WHERE Category = 'Meat' ORDER BY Name;"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("meat.html", data = data, Name="Felix Walberg", Title="Meat")

@app.route('/soupsnstews', methods=['GET'])
def soupsnstews():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )

    cursor = database.cursor()

    # Query to return recipes from the Soups/Stews category
    query = "SELECT * FROM recipesNew_data WHERE Category = 'Soups&Stews' ORDER BY Name;"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("soupsnstews.html", data = data, Name="Felix Walberg", Title="Soups/Stews")

@app.route('/sideDishes', methods=['GET'])
def sideDishes():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )

    cursor = database.cursor()

    # Query to return recipes from the Side Dishes category
    query = "SELECT * FROM recipesNew_data WHERE Category = 'Side Dishes' ORDER BY Name;"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("sideDishes.html", data = data, Name="Felix Walberg", Title="Side Dishes")

@app.route('/pasta', methods=['GET'])
def pasta():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )

    cursor = database.cursor()

    # Query to return recipes from the Pasta category
    query = "SELECT * FROM recipesNew_data WHERE Category = 'Pasta' ORDER BY Name;"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("pasta.html", data = data, Name="Felix Walberg", Title="Pasta")



# page within "recipes" where user can select category 
@app.route('/categories', methods=['GET'])
def categories():
    return render_template("categories.html", Title="Categories", Name="Felix Walberg")

# route to live temperature data, sends info to initial state
# starts thread to run infinite loop on probe until shut off
@app.route('/probe', methods=['GET'])
def probe():
    t1= threading.Thread(target=probeSetup)
    t1.start()
    return render_template("probe.html", Title="Internal Temp", Name="Felix Walberg")

# function to run infinite loop recording probe temperature data and sending it to initial state
@app.route('/runProbe', methods=['POST'])
def runProbe():
    while probe:
        val = probeFunc.getTemp()
        temp = probeFunc.convertToF(val)
        probeFunc.sendData(temp)
    return "ok"

# function I used to call with multithreads in order to start infinite loop
@app.route('/probeSetup', methods=['POST'])
def probeSetup():
    global probe
    probe = True
    runProbe()
    return "ok"

# function that takes in the recipe name as a parameter and renders a template that displays ingredients and instructions from database based on custom query
@app.route('/recipe/<id>')
def recipe(id):
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
         )

    cursor = database.cursor()

    #Query to return recipe that was clicked on
    query = "SELECT * FROM recipesNew_data WHERE Name  = '" + id + "';"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("recipe.html", data = data, Title=id, Name="Felix Walberg")

# function that takes in the category of the recipe list as a parameter and generates a random recipe based on that and passes it to the recipe route
@app.route('/surpriseMe/<cat>')
def surpriseMe(cat):
        database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
            )
        cursor = database.cursor()

        # Query to return random recipe from category
        query = "SELECT Name FROM recipesNew_data WHERE Category = '" + cat + "'ORDER BY RAND () LIMIT 1;"

        cursor.execute(query)
        data = cursor.fetchall()

        # manipulating output
        string = str(data).strip('[]')
        string = string.strip('()')
        string = string[:-1]
        string = string[:-1]
        string = string[1:]

        cursor.close()
        database.close()
        return redirect('/recipe/' + string)

# route to render the home template and stop the probe from collecting data
@app.route('/goHome', methods=["GET"])
def goHome():
    global probe
    probe = False
    runProbe()
    return render_template("home.html", Title="Raspberry Pi Smart Cookbook", Name="Felix Walberg")

@app.route('/', methods=["GET"])
def home():
    return render_template("home.html", Title="Raspberry Pi Smart Cookbook", Name="Felix Walberg")
