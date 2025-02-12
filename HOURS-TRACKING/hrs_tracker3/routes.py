from flask import render_template, redirect, url_for, flash
from app import app, session  # Import app and session
from forms import LoginForm, RegistrationForm, RecordHoursForm
from models import Teacher, HoursRecord  # Ensure HoursRecord is defined
from routes import manage_classes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        
        # Replace with actual authentication logic
        if username == 'admin' and password == 'password':
            flash('Login successful!', 'success')
            return redirect(url_for('app'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # Clear the session or perform any necessary logout logic
    session.clear()  # This will remove all session data
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))  # Redirect to the login page after logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Logic to save the user in the database goes here
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/record_hours', methods=['GET', 'POST'])
def record_hours():
    form = RecordHoursForm()
    if form.validate_on_submit():
        teacher_id = form.teacher_id.data
        class_subject_id = form.class_subject_id.data  # Adjust as necessary
        hours_taught = form.hours_taught.data
        date = form.date.data

        new_record = HoursRecord(teacher_id=teacher_id, class_subject_id=class_subject_id, hours_taught=hours_taught, date=date)
        session.add(new_record)
        session.commit()

        flash('Hours recorded successfully!', 'success')
        return redirect(url_for('view_hours'))
    
    return render_template('record_hours.html', form=form)

@app.route('/view_hours', methods=['GET'])
def view_hours():
    records = session.query(HoursRecord).all()  # Fetch hours records
    return render_template('view_hours.html', records=records)

@manage_classes_bp.route('/manage_classes', methods=['GET', 'POST'])
def manage_classes():
    form = ManageClassForm()  # Create an instance of the form
    if form.validate_on_submit():  # Check if the form is submitted and valid
        subject = form.subject.data
        class_name = form.class_name.data
        date = form.date.data
        hours = form.hours.data
        
        # Create a new class record in the database
        new_class = ClassRecord(subject=subject, class_name=class_name, date=date, hours=hours)
        db.session.add(new_class)
        db.session.commit()
        
        flash('Class managed successfully!', 'success')  # Flash success message
        return redirect(url_for('dashboard'))  # Redirect to the same page

    return render_template('manage_classes.html', form=form)  # Render the form on GET request
@app.route('/app')
def app():
    teacher_name = session.get('teacher_name')  # Adjust based on how you store the teacher's name
    return render_template('app.html', teacher_name=teacher_name)

if __name__ == '__main__':
    app.run(debug=True)