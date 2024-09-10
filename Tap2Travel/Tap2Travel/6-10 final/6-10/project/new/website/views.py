from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
import webbrowser
from . models import BusRoute
from . import db
import json
from datetime import datetime
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/user/<bus_number>', methods=['GET', 'POST'])
@login_required
def user(bus_number):
    matching_route = BusRoute.query.filter_by(busNumber=bus_number).first()
    if matching_route:
        return render_template("user.html", user=current_user, bus_route=matching_route)
    else:
        flash('Bus route not found.', 'error')
        return redirect(url_for('views.user'))

@views.route('/payment', methods=['POST','GET'])
def payment():
    busNumber = request.form.get('busNumber')
    source = request.form.get('source')
    destination = request.form.get('destination')
    stops = request.form.get('stops')
    fare = request.form.get('fare')
    
    return render_template('payment.html', user=current_user, busNumber=busNumber, source=source, destination=destination, stops=stops, fare=fare)




@views.route('/generate_ticket', methods=['POST'])
def generate_ticket():
    # Retrieve data from the form
    busNumber = request.form['busNumber']
    source = request.form['source']
    destination = request.form['destination']
    stops = request.form['stops']
    fare = request.form['fare']
    
    # Get current date and time
    current_datetime = datetime.now()
    date = current_datetime.strftime("%Y-%m-%d")
    time = current_datetime.strftime("%H:%M:%S")
    flash('Ticket Generated!', category='success')
    # Render the generate_ticket.html template with the provided data
    return render_template('generate_ticket.html', user=current_user, busNumber=busNumber, source=source, destination=destination, stops=stops, fare=fare, date=date, time=time)



@views.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        busNumber = request.form['busNumber']
        source = request.form['source']
        destination = request.form['destination']
        stops = request.form['stops']

        # Create a new BusRoute object and save it to the database
        new_route = BusRoute(busNumber=busNumber, source=source, destination=destination, stops=stops)
        db.session.add(new_route)
        db.session.commit()

        return redirect(url_for('views.admin'))  # Redirect back to the form page
    flash('Bus Route is added!', category='success')
    return render_template('admin.html',user=current_user)  # Replace 'your_template.html' with your HTML file path

if __name__ == '__main__':
    db.create_all()
    views.run(debug=True)

@views.route('/open_qr', methods=['POST'])
@login_required
def open_qr():
    if request.method == 'POST':
        data = request.form['data']
        matching_route = BusRoute.query.filter_by(busNumber=data).first()
        if matching_route:
            return redirect(url_for('views.user', bus_number=data))
        else:
            flash('Bus route not found.', 'error')
            return redirect(url_for('views.user'))



