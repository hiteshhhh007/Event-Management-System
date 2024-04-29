from flask import Flask,render_template,request,redirect,url_for,render_template_string
from flaskext.mysql import MySQL
from datetime import datetime, timedelta
from flask import jsonify
import random
import string
app=Flask(__name__)
mysql=MySQL()
import uuid

current_time=datetime.now()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='Hitesh@MySQL'
app.config['MYSQL_DATABASE_DB']='dbms_project'
mysql.init_app(app)



# data = cursor.fetchone()
# print(data)

def generate_random_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


#Default Route
@app.route('/')
def default_route():
    return render_template('index.html')

# organiserid=random.randint(1,1000)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username-s']
        email = request.form['email-s']
        password = request.form['password-s']
        level = request.form['level']
        conn = mysql.connect()
        cur = conn.cursor()
        if level == 'User':
            cur.execute("INSERT INTO signup_user(useruniq, passwordset, email) VALUES (%s, %s, %s)", (username, password, email))
        elif level == 'Organizer':
            cur.execute("INSERT INTO organiser_signup(organiserid, passwordset, email) VALUES (%s, %s, %s)", (username, password, email))
            # cur.execute("INSERT INTO  event_organise_belongs_hasvenue(organiserid) VALUES (%s) ",(username))
        conn.commit()
        cur.close()
        conn.close()
        if level == 'User':
            return render_template('index.html')
        elif level == 'Organizer':
            return render_template('index.html')
        
# Login route
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username-l']
        password = request.form['password-l']
        level = request.form['level']
        conn = mysql.connect()
        cur = conn.cursor()
        if level=="User":
            cur.execute("SELECT * FROM signup_user WHERE useruniq = %s AND passwordset = %s", (username, password))
        else:
            cur.execute("SELECT * FROM organiser_signup WHERE organiserid = %s AND passwordset = %s", (username, password))
        user = cur.fetchone()
        user_details=user
        cur.close()
        conn.close()
        if user:
            if level == 'User':
                return render_template('user.html')
            elif level == 'Organizer':
                return render_template('homepage.html',user_details=user_details)
        else:
            error_message='!!Account does not exist!!'
            return render_template('index.html', login_error=error_message)


@app.route('/newevent', methods=['GET','POST'])
def newevent():
    if request.method == 'POST':
        event_id = request.form['eventId']
        event_description = request.form['eventDescription']
        event_title = request.form['eventTitle']
        event_date = request.form['eventDate']
        event_S_Time=request.form['eventSTime']
        event_E_Time=request.form['eventETime']
        event_capacity = request.form['eventCapacity']
        registration_deadline = request.form['registrationDeadline']
        creation_date = request.form['creationDate']
        event_category = request.form['eventCategory']
        # time_left=registration_deadline-current_time
        # time_left_str = str(timedelta(seconds=int(time_left.total_seconds())))
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT organiserid from organiser_signup")
        organiser_id=cur.fetchone()
        cur.execute("INSERT INTO event (organiserid,eventid, eventdescription, eventtitle, starttimeevent, endtimeevent,capacity, registrationdeadline, createddate,categoryname) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s)", (organiser_id,event_id, event_description, event_title, event_S_Time,event_E_Time, event_capacity, registration_deadline, creation_date, event_category))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('venue.html')
    return render_template('newevent.html')
@app.route('/previousevent', methods=['GET','POST'])
def previousevent():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT eventtitle, eventid, createddate, capacity FROM event")
    events = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('previousevent.html', events=events)


@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_id = request.form['event_id']  
    conn = mysql.connect()
    cursor = conn.cursor()
    # Delete the record with the corresponding event ID
    cursor.execute("DELETE FROM event WHERE eventid = %s", (event_id,))
    conn.commit()  # Commit the transaction
    cursor.close()
    conn.close()
    return redirect(url_for('previousevent'))
@app.route('/attendees', methods=['GET', 'POST'])
def attendees():
    # Connect to MySQL
    conn = mysql.connect()
    cur = conn.cursor()
    query = """
        SELECT username, eventid
        FROM attendee
    """
    cur.execute(query)
    attendees_data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('attendees.html', attendees=attendees_data)

@app.route('/delete_attendee', methods=['POST'])
def delete_attendee():
    event_id = request.form['eventid']
    conn = mysql.connect()
    cur = conn.cursor()
    # Delete the attendee from the database
    cur.execute("DELETE FROM attendee WHERE eventid = %s", (event_id,))
    conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

    # Return a success response
    return jsonify({'success': True})
@app.route('/venue', methods=['GET','POST'])
def venue():
    if request.method=='POST':
        venue_name=request.form['venueName']
        venue_id=request.form['venueID']
        venue_location=request.form['venueLocation']
        venue_capacity=request.form['venueCapacity']
        contact_person=request.form['contactPerson']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT eventid from event")
        event_id=cur.fetchone()
        cur.execute("INSERT INTO venue (eventid,venuename,venueid,venuelocation,venuecapacity,contactpersonno) VALUES (%s,%s,%s, %s, %s, %s)", (event_id,venue_name,venue_id, venue_location,venue_capacity,contact_person))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('ticket.html')
    return render_template('venue.html')
@app.route('/ticket', methods=['GET','POST'])
def ticket():
    if request.method=='POST':
        ticket_desc=request.form['ticketDescription']
        ticket_salestart=request.form['ticketSaleStartDate']
        ticket_saleend=request.form['ticketSaleEndDate']
        ticket_price=request.form['ticketPrice']
        ticket_avail=request.form['availableTickets']
        ticket_id=request.form['ticketID']
        ticket_type=request.form['ticketType']
        event_id=request.form['eventID']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO ticket (eventid,ticketdesc,ticketsalestart,ticketsaleend,ticketprice,ticketavail,ticketid,tickettype) VALUES (%s,%s,%s,%s,%s, %s, %s, %s)", (event_id,ticket_desc,ticket_salestart,ticket_saleend,ticket_price,ticket_avail,ticket_id,ticket_type))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('ticket.html')
    return render_template('ticket.html')

@app.route('/user',methods=['GET','POST'])
def user():
    if request.method=='POST':
        name=request.form['name']
        dob=request.form['dob']
        gender=request.form['gender']
        state=request.form['state']
        city=request.form['city']
        zipcode=request.form['zipcode']
        country=request.form['country']
        email=request.form['email']
        phone=request.form['phone']
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("INSERT INTO user(name,dob,gender,state,city,zipcode,country,email,phonenumber) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,dob,gender,state,city,zipcode,country,email,phone))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('eventslive.html')
    return render_template('user.html')


@app.route('/register', methods=['POST'])
def register():
    conn = mysql.connect()
    cur = conn.cursor()
    data = request.get_json()
    event_id = data['eventId']
    useruniq = "hit"  

    
    cur.execute("INSERT INTO attendee (username, eventid) VALUES (%s, %s)", (useruniq, event_id))
    conn.commit()

    # Return a JSON response indicating success
    return jsonify({"status": "success"}), 200

@app.route('/eventslive', methods=['GET','POST'])
def eventslive():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT eventid, eventtitle FROM event")
    events = cur.fetchall()
    return render_template('eventslive.html', events=events) 

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Connect to the MySQL database
        conn = mysql.connect()
        cur = conn.cursor()
        # Generate unique IDs for the transaction and payment
        transaction_id = str(uuid.uuid4())[:8]  # Take first 8 characters
        payment_id = str(uuid.uuid4())[:8] 
        payment_mode = request.form.get('payment_method')  
        # Fetch event information from the database
        cur.execute("SELECT eventid, eventtitle FROM event LIMIT 1")
        event = cur.fetchone()  
        if event is None:
            cur.close()
            conn.close()
            return "Event not found", 404
        event_id, event_title = event
        
        # Payment details
        payment_amount = 100.00  # Example hardcoded amount
        payment_date = datetime.now()  # Current date and time
        
        # Insert the payment record into the database
        cur.execute("INSERT INTO payment (transid, paymentid, eventid, eventname, paymethod, amt, paydaate) VALUES (%s, %s, %s, %s, %s, %s, %s)",(transaction_id, payment_id, event_id, event_title, payment_mode, payment_amount, payment_date))
        conn.commit()  # Commit the transaction
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        
        return redirect('/viewrecipt')  

    
    return render_template('payment.html')  

@app.route('/viewrecipt', methods=['GET','POST'])
def view_receipt():
    conn = mysql.connect()
    cur = conn.cursor()
    query = """
        SELECT
            transid,
            paymentid,
            eventid,
            eventname,
            paymethod,
            amt,
            paydaate
        FROM
            payment
    """
    cur.execute(query)
    payment_record = cur.fetchone()  # Fetch the first record
    if payment_record is None:
        return "Payment record not found", 404  # Handle case where no record is found
    transaction_id, payment_id, event_id, event_name, payment_method, payment_amount, payment_date = payment_record
    cur.close()
    conn.close()
    # Render the template with the payment details
    return render_template(
        'viewrecipt.html',
        payment_amount=payment_amount,
        payment_id=payment_id,
        transaction_id=transaction_id,
        payment_date=payment_date,
        payment_method=payment_method,
        event_name=event_name,
        event_id=event_id
    )

if __name__ == '__main__':
    app.run(debug=True)

