from flask import Flask, render_template, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from forms import LoginForm, RegistrationForm, RecordHoursForm  # Adjust as needed
from forms import ManageClassForm 
from models import Base , Teacher , Record , ClassRecord # Adjust as needed
from models import Teacher
from forms import RecordHoursForm  
from models import ClassSubject

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/hrs_tracker"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.metadata.create_all(engine)

# Create a scoped session
Session = scoped_session(sessionmaker(bind=engine))

app.secret_key = 'your_secret_key'  # Change this to a secure key


@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session.get('username')  # Get username from session
    hrs = session.get('hrs')
    data = [username, hrs]
    if data:
        return render_template('app.html', data=data)
    return render_template('app.html')

@app.route('/manage_classes', methods=['GET', 'POST'])
def manage_classes():
    form = ManageClassForm()
    
    session = Session()  
    # Fetch subjects from the database to populate the SelectField
    subjects = session.query(ClassSubject).all()
    form.subject.choices = [(subject.subject_id, subject.name) for subject in subjects]

    if form.validate_on_submit():  # Check if the form is submitted and valid
        subject_id = form.subject.data
        class_name = form.class_name.data
        date = form.date.data
        number_of_hours = form.hours.data
        
        
        # Store class details in session (if needed)
        session['class_details'] = [subject_id, class_name, date, number_of_hours]
        
        flash('Class managed successfully!', 'success')  # Flash success message
        return redirect(url_for('dashboard'))  # Redirect to the dashboard

    session.close()  # Close the session for GET requests
    return render_template('manage_classes.html', form=form)  # Render the form on GET request

@app.route('/record_hours', methods=['GET', 'POST'])
def record_hours():
    form = RecordHoursForm()
    print('before form validation')
    if form.validate_on_submit():
        hours = form.hours.data
        date = form.date.data
        
        # Create a new record in the database
        # new_record = HoursRecord(hours=hours, date=date)
        # db.session.add(new_record)
        # db.session.commit()
        session['hrs'] = [hours, date]
        # print(new_record)
        flash('Hours recorded successfully!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the dashboard view

    return render_template('record_hours.html', form=form)

@app.route('/view_hours', methods=['GET'])
def view_hours():
    
    hours_data = session.get('hrs')  # Replace Record with your actual model class
    return render_template('view_hours.html', data=hours_data)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        session['username'] = username
        
        flash('Login successful!', 'success')
        return redirect(url_for('record_hours'))
    else:
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# @app.route('/app')
# def app_dashboard():
#     teacher_name = "Teacher Name"  # Replace with logic to get the teacher's name
#     return render_template('app.html', teacher_name=teacher_name)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Cleanup session on shutdown
@app.teardown_appcontext
def cleanup_session(exception=None):
    Session.remove()

if __name__ == '__main__':
    app.run(debug=True)