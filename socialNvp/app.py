from flask import Flask, render_template, request, session, redirect, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nvp'
db = SQLAlchemy(app)
app.secret_key= os.urandom(24)
# login_manager= LoginManager()
# login_manager.init_app(app)


# Create our database model
class Members(UserMixin, db.Model):
    __tablename__ = "Members"
    id = db.Column(db.Integer, primary_key=True)
    firstName= db.Column(db.String(20))
    lastName= db.Column(db.String(20))
    company= db.Column(db.String(50))
    phoneNumber= db.Column(db.VARCHAR(15),unique=True)
    email = db.Column(db.String(120), unique=True)
    password= db.Column(db.VARCHAR(15), unique=True)

    def __init__(self, firstName, lastName, company, phoneNumber, email,password):
        self.firstName = firstName
        self.lastName= lastName
        self.company= company
        self.phoneNumber= phoneNumber
        self.email= email
        self.password= password

    # def __repr__(self, email):
    #     return '< Email %s>' % (self.email)


# @login_manager.user_loader
# def load_user(Members_id):
#     return Members.query.get(int(members_id))
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return 'You are now logged out'

#--------------------------------------------------------------------------------------------#
# landing page
@app.route('/')
def homepage():
    return render_template('index.html')

#routes to the sign up page
@app.route('/SignUp.html', methods=['POST'])
def SignUp():
    return render_template('SignUp.html')

#routes to the login pages
@app.route('/login.html', methods=['POST'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginVerify():
    if request.method== 'POST':
        session.pop('Members', None)
        if request.form['password']== 'password123':
            session['Members']= request.form['email']
            return redirect(url_for('profile'))
    return render_template('login.html')

        # if request.form['email']== 'jcruz3@drew.edu' & request.form['password']=='password123':
        #     em= Members.query.filter_by(email= email).first()
        #     pas= Members.query.filter_by(password= password).first()
        #     login_user(em)
        #     return render_template('profile.html', members=em)
        # return render_template('error.html')

@app.route('/profile')
def profile():
    if g.Members:
        return render_template('profile.html')
    return redirect(url_for('login'))

#global variable for use
@app.before_request
def before_request():
    g.Members= None
    if 'Members' in session:
        g.Members= session['Members']

@app.route('/getsession')
def getsession():
    if 'Members' in session:
        return session['Members']
    return 'Not Logged in'

@app.route('/dropsession')
def dropsession():
    session.pop('Members', None)
    return 'Dropped'

#routes to the admin dashboard
@app.route('/dashboard.html', methods=['POST'])
@login_required
def dashboard():
    members= Members.query.all()
    return render_template('dashboard.html', members=members)

# Save e-mail to database and send to success page
@app.route('/registering', methods=['POST'])
def registering():
    if request.method == 'POST':
        email = request.form['email']
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        fullName= firstName+lastName
        company = request.form['company']
        phoneNumber= request.form['phoneNumber']
        password= request.form['password']

        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(Members).filter(Members.phoneNumber == phoneNumber).count():
            user= Members(firstName, lastName, company, phoneNumber, email, password)
            db.session.add(user)
            db.session.commit()
            return render_template('success.html')
        else:
            return render_template('error.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
