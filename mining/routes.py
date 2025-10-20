from mining import app,db
from flask import render_template,flash,redirect,url_for,request, jsonify
from flask_login import login_user,login_required,logout_user
from mining.forms import LoginForm,RegisterForm
from mining.models import User
from .predict import make_prediction
import json

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login_page():
    form =LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            next_page=request.args.get('next')
            flash(f'Success! You are logged in as : {attempted_user.username}',category='success')
            return redirect(next_page or url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! you are now logged in as {user_to_create.username}',category="success")
        return redirect(url_for('prediction_page'))
    
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
    return render_template('register.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category="info")
    return redirect(url_for('home_page'))

@app.route('/prediction',methods=['GET','POST'])
@login_required
def prediction_page():
    return render_template('prediction.html')



@app.route('/api/predict', methods=['POST'])
@login_required
def get_prediction():
    """
    Handles the AJAX request from the frontend, runs the ML model, 
    and returns the prediction result as JSON.
    """
    # Ensure the request contains JSON data
    if not request.is_json:
        return jsonify({"success": False, "error": "Missing JSON in request"}), 400

    try:
        data = request.get_json()
        input_list = data.get('input_data')

        # Basic input validation
        if not input_list or not isinstance(input_list, list):
            return jsonify({"success": False, "error": "Invalid or missing 'input_data' list"}), 400

        # --- Call the prediction function ---
        # NOTE: make_prediction returns a NumPy array, so we must convert it.
        prediction_result = make_prediction(input_list)
        
        # Return success with the prediction result
        return jsonify({
            'success': True,
            'prediction': float(prediction_result[0])
        }), 200

    except Exception as e:
        # Catch any errors (e.g., model loading failure, array shape mismatch)
        print(f"Prediction Error: {e}")
        return jsonify({
            'success': False,
            'error': f'Prediction failed due to server error: {str(e)}'
        }), 500