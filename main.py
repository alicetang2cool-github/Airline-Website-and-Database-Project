from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime
from datetime import date
import json

## start website
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Enter your database connection details 
app.config['MYSQL_HOST'] = 'cis221projectdb.ckdslcdwovmx.us-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'masterpasswordforteamrumilehanalice'
app.config['MYSQL_DB'] = 'cis221projectdb'

# Intialize MySQL
mysql = MySQL(app)






###------------------------------------------------------------------------------------------------------------------###
#HOMEPAGE, LOGIN, REGISTRATION





@app.route("/")
@app.route("/homepage")
def home():
    return render_template('homepage.html', title = "HomePage")

@app.route("/customer_homepage")
def customer_homepage():
    email = session['email'] 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers WHERE Customers.Email_Address = "{}"'.format(email))
    customer = cursor.fetchone()
    cursor.execute('SELECT * FROM People WHERE People.SSN = "{}"'.format(customer["SSN"]))
    person = cursor.fetchone()
    return render_template('customer_homepage.html', title = "HomePage", person=person)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        #check if admin
        if email == "manager@admin.com" and password == "admin":
            return redirect(url_for('manager_dashboard'))
        # Check if user table exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Accounts WHERE Email = %s AND Password = %s', (email, password))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If user exists in user table in out database
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = user['Email']
            # Redirect to home page
            flash('You have successfully logged in', 'success')
            return redirect(url_for('customer_homepage'))
    # Show the login form        
    return render_template('login.html', title = "HomePage") 

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('email', None)
   # Redirect to homepage
   flash('You have successfully logged out', 'success')
   return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'First Name' in request.form and 'Last Name' in request.form and 'SSN' in request.form and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        ssn = request.form['SSN']
        email = request.form['email']
        password = request.form['password']
        # Check if user exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Accounts WHERE email = %s', (email,))
        user = cursor.fetchone()
        # If account exists let them login
        if user:
            return render_template('login.html', title = "Login")
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO Accounts (Email, Password) VALUES (%s, %s)', (email, password))
            cursor.execute('INSERT INTO People (SSN, Last_Name, First_Name) VALUES (%s, %s, %s)', (ssn, last_name, first_name))
            cursor.execute('INSERT INTO Customers (SSN, Email_Address) VALUES (%s, %s)', (ssn, email))
            mysql.connection.commit()
            flash('You have successfully created an account, log in!', 'success')
            return redirect(url_for('login'))
    # Show registration form
    return render_template('register.html', title = "Register")







##-----------------------------------------------------------------------------------------------------------------##
#ADMIN





#See All Flights
@app.route('/listing_all_flights')
def listing_all_flights():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cis221projectdb.Flights;')
    result = cursor.fetchall()
    return render_template('listing_all_flights.html', data=result)

#Monthly_Sales_report
@app.route('/manager_dashboard', methods=['GET', 'POST'])
def manager_dashboard():
	# Check if the customer filled form
    if request.method == 'POST':
		#take the date from the form, turn it to an interger of day of the week
		#take the values of the from and turn it to variables 
        Sale_report_date = request.form["Sale_report_date"]
        print(type(Sale_report_date))
        print(Sale_report_date)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(Total_Fare) FROM cis221projectdb.Reservations WHERE Reservations.Date LIKE "%{}%"'.format(Sale_report_date))
        result = cursor.fetchall()
        print(result)
		#put the flights into a html page, which lets the customer select which he wants
        return render_template('monthly_sales_report.html', data=result[0].get('SUM(Total_Fare)'), str = str)
    else:
        return render_template('manager_dashboard.html')
    # Show the  form   
    return render_template('manager_dashboard.html')

#Manager_Customer_dashboard
@app.route('/manager_customer_dashboard', methods=['GET', 'POST'])
def manager_customer_dashboard():
    return render_template('manager_customer_dashboard.html')

#Manager_Employee_dashboard
@app.route('/manager_employee_dashboard', methods=['GET', 'POST'])
def manager_employee_dashboard():
    return render_template('manager_employee_dashboard.html')

#Customer That produced the most revenue
@app.route('/customer_most_revenue')
def customer_most_revenue():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT First_name, Last_name FROM cis221projectdb.People, cis221projectdb.Customers, cis221projectdb.Reservations WHERE People.SSN = Customers.SSN AND Customers.Email_Address = Reservations.Email ;')
    result = cursor.fetchall()
    result_name = []
    firstname = result[0].get('First_name')
    lastname = result[0].get('Last_name')
    result_name.append(firstname)
    result_name.append(lastname)
    return render_template('customer_most_revenue.html', data=result_name)

#Most active flights
@app.route('/most_active_flights')
def most_active_flights():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Flights.Flight_Number, Flights.Airline_ID FROM cis221projectdb.Flights;')
    result = cursor.fetchall()
    return render_template('most_active_flights.html', data=result)

#List of Reservations
@app.route('/list_of_reservations', methods=['GET', 'POST'])
def list_of_reservations():
    if request.method == 'POST':
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Reservations.Reservation_Number FROM cis221projectdb.Reservations, cis221projectdb.Customers, cis221projectdb.People WHERE Reservations.Email = Customers.Email_Address AND Customer.SSN = People.SSN AND People.First_Name LIKE "%{}%" AND People.Last_Name LIKE "%{}%"'.format(firstname,lastname))
        result = cursor.fetchall()
        print(result)
    return render_template('list_of_reservations.html', data=result)

#List of Flights
@app.route('/list_of_flights', methods =['GET','POST'])
def list_of_flights():
    if request.method == 'POST':
        airport = request.form['airport']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Flight_Number FROM cis221projectdb.Flights WHERE From_Airport = "{}"'.format(airport))
        result = cursor.fetchall()
        print(result)
    return render_template('list_of_flights.html', data=result)

#Reserved Customers
@app.route('/reserved_customers',methods=['GET','POST'])
def reserved_customers():
    if request.method == 'POST':
        flight = request.form["flight"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT People.First_Name, People.Last_Name FROM cis221projectdb.Legs, cis221projectdb.Reservations, cis221projectdb.Customers, cis221projectdb.People WHERE Legs.Reservation_Number = Reservations.Reservation_Number AND Reservation.Email = Customers.Email_Address AND Customers.SSN = People.SSN AND Legs.Flight_Number = "{}"'.format(flight))
        result = cursor.fetchall()
        return render_template('reserved_customers.html', data=result)

#Revenue Summary
@app.route('/revenue_summary', methods=['GET','POST'])
def revenue_summary():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT SUM(Reservations.Total_Fare), Legs.Flight_Number FROM cis221projectdb.Reservations, cis221projectdb.Legs WHERE Reservations.Reservation_Number = Legs.Reservation_Number GROUP BY Legs.Flight_Number')
    result = cursor.fetchall()
    return render_template('revenue_summary.html', data=result)





##----------------------------------------------------------------##
#CUSTOMER FLIGHT RESERVATION






#search flight function
def searchFlight(from_country, from_city, to_country, to_city, date):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}" AND Airports.City= "{}" '.format(from_country, from_city))
	from_airport = cursor.fetchone()
	cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}" AND Airports.City= "{}" '.format(to_country, to_city))
	to_airport = cursor.fetchone()
	cursor.execute('SELECT * FROM Flights WHERE Flights.Days_of_Week LIKE "%{}%" AND Flights.From_airport = "{}" AND Flights.To_airport = "{}"'.format(date, from_airport['Airport_ID'], to_airport['Airport_ID']))
	result = cursor.fetchall()
	return result

#DIRECT_FLIGHT
@app.route('/direct_flight', methods=['GET', 'POST'])
def direct_flight():
	# Check if the customer filled direct_flight.html form
    if request.method == 'POST':
		#take the date from the form, turn it to an interger of day of the week
        date_going_out = datetime.datetime.strptime(request.form["Date"], "%Y-%m-%d").weekday() + 1
        #find today's date, and if customer can have discount
        date_of_flight = datetime.datetime.strptime(request.form["Date"], "%Y-%m-%d")
        today_date = datetime.datetime.now()
        a = ((date_of_flight - today_date).days)
        if a >= 5:
            session["discount"] = True
        else: 
            session["discount"] = False
		#take the values of the from and turn it to variables 
        from_country = request.form["from_country"]
        from_city = request.form["from_city"]
        to_country = request.form["to_country"]
        to_city = request.form["to_city"]
		#find the rows in Flights table for the flights that the customer wants, denoted as result
        result = searchFlight(from_country, from_city, to_country, to_city, date_going_out)
		#put the flights into a html page, which lets the customer select which he wants
        return render_template('select_direct_flight.html', data=result, str = str)
    else:
        return render_template('direct_flight.html')
    # Show the direct_flight form   
    return render_template('direct_flight.html')

#once the form in select_direct_flight.html is filled, it goes here
@app.route('/reserve_direct_flight', methods=['GET', 'POST'])
def reserve_direct_flight():
	#take the values of the select_direct_flight.html form and turn it to variables 
    flight_number, airline_ID = request.form["flight"].split("_")
    number_of_people = int(request.form["number"])
    class_of_seats = request.form["class"]
    meal = request.form["meal"]
    seat_type = request.form["seat"]
	#find the row in Flights table for the flight that the customer selected, denoted as info
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Flights WHERE Flight_Number = "{}" AND Airline_ID = "{}"'.format(flight_number, airline_ID))
    flight_info = cursor.fetchone()
	#make a Reservation_ID for this reservation
    cursor.execute('SELECT MAX(Reservation_Number) AS C FROM Reservations')
    ID = cursor.fetchone()["C"] + 1
	#find today's date
    today_date = date.today().strftime('%Y-%m-%d')
	#insert the info into Reservations, Booking, and Legs table
    if session["discount"]:
        cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, (number_of_people * flight_info["Associated_Fare"])/2, session['email']))
    else:
        cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, number_of_people * flight_info["Associated_Fare"], session['email']))
    cursor.execute('INSERT INTO Legs (Reservation_Number, Flight_Number, Airline_ID, Seat_type, Class, Departure_Time, Arrival_Time, Special_Meal) VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(ID, flight_info['Flight_Number'], flight_info['Airline_ID'], seat_type, class_of_seats, flight_info['Local_departure'], flight_info['Local_arrivial'], meal))
    mysql.connection.commit()
	# send customer back to his homepage
    flash('You successfully reserved a flight!', 'success')
    return redirect(url_for('customer_homepage'))

#ROUND_TRIP
@app.route('/round_trip', methods=['GET', 'POST'])
def round_trip():
	# Check if the customer filled round_trip.html form
    if request.method == 'POST':
		#take the dates from the form, turn it to an interger of day of the week
        day_of_week_there = datetime.datetime.strptime(request.form["Date_to_there"], "%Y-%m-%d").weekday()+1
        day_of_week_back = datetime.datetime.strptime(request.form["Date_coming_back"], "%Y-%m-%d").weekday()+1
        #get the difference betweent the two days to see the customers length of stay
        d1 = datetime.datetime.strptime(request.form["Date_to_there"], "%Y-%m-%d")
        d2 = datetime.datetime.strptime(request.form["Date_coming_back"], "%Y-%m-%d")
        lenght_of_stay = abs((d2 - d1).days)
		#take the values of the from and turn it to variables 
        from_country = request.form["from_country"]
        from_city = request.form["from_city"]
        to_country = request.form["to_country"]
        to_city = request.form["to_city"]
        #find today's date, and if customer can have discount
        date_of_flight = datetime.datetime.strptime(request.form["Date_to_there"], "%Y-%m-%d")
        today_date = datetime.datetime.now()
        a = ((date_of_flight - today_date).days)
        if a >= 5:
            session["discount"] = True
        else: 
            session["discount"] = False
		#find the rows in Flights table for the flights going out that the customer wants, denoted as going_out_flights
        going_out_flights = searchFlight(from_country, from_city, to_country, to_city, day_of_week_there)
        #find the rows in Flights table for the flights coming back home that the customer wants, denoted as coming_home_flights
        coming_home_flights = searchFlight(to_country, to_city, from_country, from_city, day_of_week_back)
		#put the flights into a html page, which lets the customer select which he wants
        return render_template('select_round_trip.html', lenght_of_stay=lenght_of_stay, going_out_flights_data=going_out_flights, coming_home_flights_data=coming_home_flights, str = str)
    else:
        return render_template('round_trip.html')
    # Show the round_trip form   
    return render_template('round_trip.html')

#once the form in round_trip.html is filled, it goes here
@app.route('/reserve_round_trip', methods=['GET', 'POST'])
def reserve_round_trip():
	#take the values of the select_round_trip.html form and turn it to variables 
    going_out_flight_number, going_out_airline_ID = request.form["going_out_flight"].split("_")
    coming_home_flight_number, coming_home_airline_ID = request.form["coming_home_flight"].split("_")
    number_of_people = int(request.form["number"])
    class_of_seats = request.form["class"]
    meal = request.form["meal"]
    seat_type = request.form["seat"]
	#find the row in Flights table for the flight that the customer selected for going out, denoted as going_out_flight_info
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Flights WHERE Flight_Number = "{}" AND Airline_ID = "{}"'.format(going_out_flight_number, going_out_airline_ID))
    going_out_flight_info = cursor.fetchone()
    #find the row in Flights table for the flight that the customer selected for coming home, denoted as coming_home_flight_info
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Flights WHERE Flight_Number = "{}" AND Airline_ID = "{}"'.format(coming_home_flight_number, coming_home_airline_ID))
    coming_home_flight_info = cursor.fetchone()
    #make a Reservation_ID for this reservation 
    cursor.execute('SELECT MAX(Reservation_Number) AS C FROM Reservations')
    ID = cursor.fetchone()["C"] + 1
    #find today's date
    today_date = date.today().strftime('%Y-%m-%d')
    #insert the going_out_flight_info into Reservations, Booking, and Legs table
    if session["discount"]:
        cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, (number_of_people * going_out_flight_info["Associated_Fare"])/2 + (number_of_people * coming_home_flight_info["Associated_Fare"])/2, session['email']))
    else: 
        cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, (number_of_people * going_out_flight_info["Associated_Fare"]) + (number_of_people * coming_home_flight_info["Associated_Fare"]), session['email']))
    cursor.execute('INSERT INTO Booking (Reservation_Number, Email, Booking_Fee) VALUES ({}, "{}", {})'.format(ID, session['email'], 10))
    cursor.execute('INSERT INTO Legs (Reservation_Number, Flight_Number, Airline_ID, Seat_type, Class, Departure_Time, Arrival_Time, Special_Meal) VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(ID, going_out_flight_info['Flight_Number'], going_out_flight_info['Airline_ID'], seat_type, class_of_seats, going_out_flight_info['Local_departure'], going_out_flight_info['Local_arrivial'], meal))
    cursor.execute('INSERT INTO Legs (Reservation_Number, Flight_Number, Airline_ID, Seat_type, Class, Departure_Time, Arrival_Time, Special_Meal) VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(ID, coming_home_flight_info['Flight_Number'], coming_home_flight_info['Airline_ID'], seat_type, class_of_seats, coming_home_flight_info['Local_departure'], coming_home_flight_info['Local_arrivial'], meal))
    mysql.connection.commit()
    # send customer back to his homepage
    flash('You successfully reserved a round trip flight!', 'success')
    return redirect(url_for('customer_homepage'))

#MULTI_CITY
@app.route('/multi_city', methods=['GET', 'POST'])
def multi_city():
    # result as an empty list, and set c as 1
    result = []
    c = 1
    # Check if the customer filled multi_city.html form
    if request.method == 'POST':
        #find today's date, and if customer can have discount
        date_of_flight = datetime.datetime.strptime(request.form["Date1"], "%Y-%m-%d")
        today_date = datetime.datetime.now()
        a = ((date_of_flight - today_date).days)
        if a >= 5:
            session["discount"] = True
        else: 
            session["discount"] = False
        #basically this runs the number of city the cusomter wants, each city has a date, and for its date its calld date1, date2, ... date10
        while "Date" + str(c) in request.form:
            #take the dates from the form, turn it to an interger of day of the week
            date = datetime.datetime.strptime(request.form["Date" + str(c)], "%Y-%m-%d").weekday()+1
			#if we are regarding the first segment
            if c == 1:
                from_country = request.form["from_country1"]
                from_city = request.form["from_city1"]
            #if we are regarding the second or more segment
            else:
                from_country = request.form["to_country" + str(c-1)]
                from_city = request.form["to_city" + str(c-1)]
            to_country = request.form["to_country" + str(c)]
            to_city = request.form["to_city" + str(c)]
            #search the flights in the Flights table, then append the rows to the result list
            result.append(searchFlight(from_country, from_city, to_country, to_city, date))
            c += 1
        #when done with loop, go to the select_multi_city.html and bring along the result list
        return render_template('select_multi_city.html', result=result, str = str, range=range, len=len)
    return render_template('multi_city.html')    

#once the form in multi_city.html is filled, it goes here
@app.route('/reserve_multi_city', methods=['GET', 'POST'])
def reserve_multi_city():
    #take the values of the select_multi_city.html form and turn it to variables 
    number_of_people = int(request.form["number"])
    class_of_seats = request.form["class"]
    meal = request.form["meal"]
    seat_type = request.form["seat"]
	#find today's date
    today_date = date.today().strftime('%Y-%m-%d')
    #set c to 1, total fare to 0, and make an empty insert statement
    c = 1
    total_fare = 0
    insertStatement = ''
    #make an ID for the reservation ID
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)	
    cursor.execute('SELECT MAX(Reservation_Number) AS C FROM Reservations')
    ID = cursor.fetchone()["C"] + 1
    #loops through each chosen flight 
    while "flight" + str(c) in request.form:
        #take the values of the select_multi_city.html form for the chosen flight
        flight_number, airline_ID = request.form["flight" + str(c)].split("_")
        #find the row in flights table for the flight chosen
        cursor.execute('SELECT * FROM Flights WHERE Flight_Number = "{}" AND Airline_ID = "{}"'.format(flight_number, airline_ID))
        flight_info = cursor.fetchone()
        #take the price of the chosen flight mulitply the number of people and add it to the total fare
        total_fare += number_of_people * flight_info['Associated_Fare']
        #make a leg for the chosen flight
        insertStatement += 'INSERT INTO Legs (Reservation_Number, Flight_Number, Airline_ID, Seat_type, Class, Departure_Time, Arrival_Time, Special_Meal) VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(ID, flight_info['Flight_Number'], flight_info['Airline_ID'], seat_type, class_of_seats, flight_info['Local_departure'], flight_info['Local_arrivial'], meal)
        c += 1
    #when loop is done, insert te info for reservations, booking, legs table
    if session["discount"]:
        cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, total_fare/2, session['email']))
    else:
        cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, total_fare, session['email']))
    cursor.execute('INSERT INTO Booking (Reservation_Number, Email, Booking_Fee) VALUES ({}, "{}", {})'.format(ID, session['email'], 10))
    cursor.execute(insertStatement)
    cursor.close()
    mysql.connection.commit()
    # send customer back to his homepage
    flash('You successfully reserved a multi-city flight!', 'success')
    return redirect(url_for('customer_homepage'))
    	
#DOMESTIC FLIGHT
@app.route('/domestic_flight', methods=['GET', 'POST'])
def domestic_flight():
    if request.method == 'POST':
        #take the values of the domestic_flight.html form and turn it to variables 
        domestic_country = request.form["domestic_country"]
        domestic_city = request.form["domestic_city"]
        date = datetime.datetime.strptime(request.form["Date"], "%Y-%m-%d").weekday() + 1
        #find today's date, and if customer can have discount
        date_of_flight = datetime.datetime.strptime(request.form["Date"], "%Y-%m-%d")
        today_date = datetime.datetime.now()
        a = ((date_of_flight - today_date).days)
        if a >= 5:
            session["discount"] = True
        else: 
            session["discount"] = False
        #make a string of airports thats in the same country as cusomter
        string_of_to_airports = ''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}" AND Airports.City= "{}" '.format(domestic_country, domestic_city))
        from_airport = cursor.fetchone()
        cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}"'.format(domestic_country))
        to_airports = cursor.fetchall()
        for i in range(len(to_airports) - 1):
            to_airport_ID = to_airports[i]['Airport_ID']
            string_of_to_airports += "'" + str(to_airport_ID) + "'" + ", "
        string_of_to_airports_1 = string_of_to_airports + "'" + str(to_airports[len(to_airports)-1]['Airport_ID']) + "'"
        string_of_to_airports_2 = "("+ string_of_to_airports_1 + ")"
        cursor.execute('SELECT * FROM Flights, Airports WHERE Flights.To_airport = Airports.Airport_ID AND Flights.Days_of_Week LIKE "%{}%" AND Flights.From_airport = "{}" AND Flights.To_airport IN {}'.format(date, from_airport['Airport_ID'], string_of_to_airports_2))
        flights = cursor.fetchall()
        return render_template('select_domestic_flight.html', data=flights, str = str)
    else:
        return render_template('domestic_flight.html')
    return render_template('domestic_flight.html')

#INTERNATIONAL FLIGHT
@app.route('/international_flight', methods=['GET', 'POST'])
def international_flight():
    if request.method == 'POST':
        #take the values of the domestic_flight.html form and turn it to variables 
        domestic_country = request.form["domestic_country"]
        domestic_city = request.form["domestic_city"]
        date = datetime.datetime.strptime(request.form["Date"], "%Y-%m-%d").weekday() + 1
        #find today's date, and if customer can have discount
        date_of_flight = datetime.datetime.strptime(request.form["Date"], "%Y-%m-%d")
        today_date = datetime.datetime.now()
        a = ((date_of_flight - today_date).days)
        if a >= 5:
            session["discount"] = True
        else: 
            session["discount"] = False
        #find the airport of customer
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}" AND Airports.City= "{}" '.format(domestic_country, domestic_city))
        domestic_airport = cursor.fetchone()
        #find the airports not in the country of customer
        cursor.execute('SELECT * FROM Airports WHERE Airports.Country != "{}"'.format(domestic_country))
        international_airports = cursor.fetchall()
        #make a string of airports thats are not the same country as cusomter
        string_of_to_airports = ''
        for i in range(len(international_airports) - 1):
            international_airports_ID = international_airports[i]['Airport_ID']
            string_of_to_airports += "'" + str(international_airports_ID) + "'" + ", "
        string_of_to_airports_1 = string_of_to_airports + "'" + str(international_airports[len(international_airports)-1]['Airport_ID']) + "'"
        string_of_to_airports_2 = "("+ string_of_to_airports_1 + ")"
        cursor.execute('SELECT * FROM Flights, Airports WHERE Flights.To_airport = Airports.Airport_ID AND Flights.Days_of_Week LIKE "%{}%" AND Flights.From_airport = "{}" AND Flights.To_airport IN {}'.format(date, domestic_airport['Airport_ID'], string_of_to_airports_2))
        flights = cursor.fetchall()
        return render_template('select_international_flight.html', data=flights, str = str)
    else:
        return render_template('international_flight.html')
    return render_template('international_flight.html')

#FLEXIBLE_FLIGHT
@app.route('/flexible_flight', methods=['GET', 'POST'])
def flexible_flight():
	# Check if the customer filled flexible_flight.html form
    if request.method == 'POST':
		#take the values of the from and turn it to variables 
        from_country = request.form["from_country"]
        from_city = request.form["from_city"]
        to_country = request.form["to_country"]
        to_city = request.form["to_city"]
		#find the rows in Flights table for the flights that the customer wants, denoted as result
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}" AND Airports.City= "{}" '.format(from_country, from_city))
        from_airport = cursor.fetchone()
        cursor.execute('SELECT * FROM Airports WHERE Airports.Country = "{}" AND Airports.City= "{}" '.format(to_country, to_city))
        to_airport = cursor.fetchone()
        print(from_airport)
        print(to_airport)
        cursor.execute('SELECT * FROM Flights WHERE Flights.From_airport = "{}" AND Flights.To_airport = "{}"'.format(from_airport['Airport_ID'], to_airport['Airport_ID']))
        result = cursor.fetchall()
		#put the flights into a html page, which lets the customer select which he wants
        return render_template('select_flexible_flight.html', data=result, str = str)
    else:
        return render_template('flexible_flight.html')
    # Show the direct_flight form   
    return render_template('flexible_flight.html')

#once the form in select_flexible_flight.html is filled, it goes here
@app.route('/reserve_flexible_flight', methods=['GET', 'POST'])
def reserve_flexible_flight():
	#take the values of the select_direct_flight.html form and turn it to variables 
    flight_number, airline_ID = request.form["flight"].split("_")
    number_of_people = int(request.form["number"])
    class_of_seats = request.form["class"]
    meal = request.form["meal"]
    seat_type = request.form["seat"]
	#find the row in Flights table for the flight that the customer selected, denoted as info
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Flights WHERE Flight_Number = "{}" AND Airline_ID = "{}"'.format(flight_number, airline_ID))
    flight_info = cursor.fetchone()
	#make a Reservation_ID for this reservation
    cursor.execute('SELECT MAX(Reservation_Number) AS C FROM Reservations')
    ID = cursor.fetchone()["C"] + 1
	#find today's date
    today_date = date.today().strftime('%Y-%m-%d')
	#insert the info into Reservations, Booking, and Legs table
    cursor.execute('INSERT INTO Reservations (Reservation_Number, Date, Passengers, Total_Fare, Email) VALUES ({}, "{}", {}, {}, "{}")'.format(ID, today_date, number_of_people, number_of_people * flight_info["Associated_Fare"], session['email']))
    cursor.execute('INSERT INTO Legs (Reservation_Number, Flight_Number, Airline_ID, Seat_type, Class, Departure_Time, Arrival_Time, Special_Meal) VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(ID, flight_info['Flight_Number'], flight_info['Airline_ID'], seat_type, class_of_seats, flight_info['Local_departure'], flight_info['Local_arrivial'], meal))
    mysql.connection.commit()
	# send customer back to his homepage
    flash('You successfully reserved a flight!', 'success')
    return redirect(url_for('customer_homepage'))







###----------------------------------------------------------------------------------------###
#CUSOMTER NAV BAR
#RESERVATION AND PROFILE AND BEST SELLERS






#GET RESERVATIONS OF THE CUSTOMER
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    #get email of cusomter
    email = session['email'] 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Reservations WHERE Reservations.Email = "{}"'.format(email))
    reservations_rows = cursor.fetchall()
    return render_template('reservations.html', reservations_rows=reservations_rows, str = str)

#once the cusomter picks a reservation to delete in reservations form it comes here
@app.route('/delete_reservation', methods=['GET', 'POST'])
def delete_reservation():
    if request.method == 'POST':
        #take the deleted value of the reservations.html form and turn it to variables 
        reservation_number = int(request.form["reservation_number"])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Reservations WHERE Reservations.Reservation_Number = {}'.format(reservation_number))
        mysql.connection.commit()
        flash('You successfully deleted a reservation!', 'success')
        return redirect(url_for('reservations'))

#if customer picks a reservation but wants to see the info of it
@app.route('/flight_details', methods=['GET', 'POST'])
def flight_details():
    if request.method == 'POST':
        reservation_number = request.form["reservation_number"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Legs WHERE Legs.Reservation_Number = {}'.format(reservation_number))
        legs = cursor.fetchall()
        return render_template('flight_details.html', legs=legs, str = str)

#PROFILE OF CUSTOMER
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    email = session['email'] 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers WHERE Customers.Email_Address = "{}"'.format(email))
    customer = cursor.fetchone()
    cursor.execute('SELECT * FROM People WHERE People.SSN = "{}"'.format(customer["SSN"]))
    person = cursor.fetchone()
    return render_template('profile.html', person=person, str = str)

#BEST SELLERS
@app.route('/best_sellers', methods=['GET', 'POST'])
def best_sellers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Legs.Flight_Number, count(*), Flights.From_airport, Flights.To_airport, Flights.Associated_Fare FROM Legs, Flights WHERE Legs.Flight_Number=Flights.Flight_Number GROUP BY Legs.Flight_Number HAVING COUNT(*) > 3') 
    best_flights = cursor.fetchall()
    return render_template('best_sellers.html', best_flights=best_flights, str = str)






###----------------------------------------------------------------------------------------###
#hope this is understandable guys :/





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

