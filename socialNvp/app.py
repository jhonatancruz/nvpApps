from flask import Flask, render_template, request, session, redirect, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from flask.ext.login import LoginManager
from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user , logout_user , current_user , login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nvp'
db = SQLAlchemy(app)
app.secret_key= os.urandom(24)
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Create our database model
class Members(UserMixin, db.Model):
    __tablename__ = "Members"
    id = db.Column(db.Integer, primary_key=True)
    firstName= db.Column(db.String(20))
    lastName= db.Column(db.String(20))
    company= db.Column(db.String(50))
    phoneNumber= db.Column(db.VARCHAR(15),unique=True)
    email = db.Column(db.String(120), unique=True)
    emailGroup= db.Column(db.String(120))
    password= db.Column(db.VARCHAR(15), unique=True)
    # registered_on= db.Column(db.DateTime)
    is_active= db.Column(db.Boolean, default=False)
    has_slack= db.Column(db.Boolean, default=False)
    has_kisi= db.Column(db.Boolean, default=False)
    has_agreement= db.Column(db.Boolean, default=False)
    has_mailbox= db.Column(db.Boolean, default=False)
    lockerNum= db.Column(db.VARCHAR(15),unique=True)


    def __init__(self, firstName, lastName, company, phoneNumber, email,password, is_active, has_slack,has_kisi, has_agreement,has_mailbox, lockerNum):
        self.firstName = firstName
        self.lastName= lastName
        self.company= company
        self.phoneNumber= phoneNumber
        self.email= email
        self.password= password
        # self.registered_on= registered_on
        self.is_active= is_active
        self.has_slack= has_slack
        self.has_kisi= has_kisi
        self.has_agreement= has_agreement
        self.has_mailbox= has_agreement
        self.lockerNum= lockerNum

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)

#--------------------------------------------------------------------------------------------#
# landing page
    @app.route('/')
    def homepage():
        return render_template('index.html')

    #routes to the sign up page
    @app.route('/SignUp.html', methods=['POST'])
    def SignUp():
        return render_template('SignUp.html')

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
            # registered_on= db.DateTime
            is_active= False
            has_slack= False
            has_kisi= False
            has_agreement= False
            has_mailbox= False
            lockerNum= 0


            # Check that email does not already exist (not a great query, but works)
            if not db.session.query(Members()).filter(Members().phoneNumber == phoneNumber).count():
                user= Members(firstName, lastName, company, phoneNumber, email, password, is_active, has_slack, has_kisi, has_agreement, has_mailbox, lockerNum)
                db.session.add(user)
                db.session.commit()
                return render_template('success.html')
            else:
                return render_template('error.html')
        return render_template('index.html')

    #routes to the login page
    @app.route('/login.html', methods=['POST'])
    def login():
        return render_template('login.html')

    #verifies email and password for user login
    # @app.route('/login', methods=['POST'])
    # def loginVerify():
    #     email= request.form['email']
    #     password= request.form['password']
    #     registered_user = Members.query.filter_by(email=email,password=password).first()
    #     if request.method== 'POST':
    #         if registered_user:
    #             login_user(registered_user)
    #             flash('Successful login')
    #         else:
    #              flash('Username or Password is invalid' , 'error')
    #              return redirect(url_for('login'))
    #     return render_template('login.html')
    #
    #         # if request.form['email']== 'jcruz3@drew.edu' & request.form['password']=='password123':
    #         #     em= Members.query.filter_by(email= email).first()
    #         #     pas= Members.query.filter_by(password= password).first()
    #         #     login_user(em)
    #         #     return render_template('profile.html', members=em)
    #         # return render_template('error.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('homepage'))

    @app.route('/profile')
    @login_required
    def profile():
        if g.Members:
            return render_template('profile.html')
        return redirect(url_for('login'))

    # global variable for use
    @app.before_request
    def before_request():
        g.Members= None
        if 'Members' in session:
            g.Members= session['Members']

    # @app.route('/getsession')
    # def getsession():
    #     if 'Members' in session:
    #         return session['Members']
    #     return 'Not Logged in'
    #
    # @app.route('/dropsession')
    # def dropsession():
    #     session.pop('Members', None)
    #     return 'Dropped'

    #routes to the admin dashboard
    @app.route('/dashboard.html', methods=['POST', 'GET'])
    @login_required
    def dashboard():
        members= Members.query.all()
        user='jcruz3@drew.edu'
        # members= db.session.query(Members).filter(Members.password).first()
        return render_template('dashboard.html', members=members)

    if __name__ == '__main__':
        app.debug = True
        app.run()
