from flask import Flask, render_template,redirect, url_for, request
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY']= "thisissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nvp'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/imgs' #for uploads
Bootstrap(app)
db= SQLAlchemy(app)
admin= Admin(app)
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class User(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email= db.Column(db.String(50), unique=True)
    company = db.Column(db.String(50))
    phoneNumber= db.Column(db.VARCHAR(15),unique=True)
    password= db.Column(db.String(80))
    img_url= db.Column(db.String(100))
    emailGroup= db.Column(db.String(120))
    is_active= db.Column(db.Boolean, default=True)
    has_slack= db.Column(db.Boolean, default=False)
    has_kisi= db.Column(db.Boolean, default=False)
    has_agreement= db.Column(db.Boolean, default=False)
    has_mailbox= db.Column(db.Boolean, default=False)
    lockerNum= db.Column(db.VARCHAR(15),unique=True)
    admin= db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember= BooleanField('rememeber me')

class RegisterForm(FlaskForm):
    email= StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=4, max=25)])
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    company = StringField('Company', validators=[InputRequired(), Length(min=8, max=25)])
    phoneNumber= IntegerField("Phone Number")

admin.add_view(ModelView(User, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    allForm= User()

    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid email or password</h1>'
        # return '<h1>' + form.username.data + ' '+ form.password.data + '</h1>'

    return render_template('login.html', form=form, allForm=allForm)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form= RegisterForm()

    if form.validate_on_submit():
        filename = photos.save(request.files['photo'])
        hash_password= generate_password_hash(form.password.data, method='sha256')
        new_user= User(firstName= form.firstName.data,lastName= form.lastName.data,  email= form.email.data,company= form.company.data, phoneNumber= form.phoneNumber.data, password= hash_password, img_url= filename)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1> New user has been created</h1>'
        # return '<h1>' + form.username.data + ' '+ form.password.data + ' '+ form.email.data+ '</h1>'
    return render_template('signup.html', form= form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', firstName= current_user.firstName, img_url= current_user.img_url,
                             lastName= current_user.lastName,  email= current_user.email, company= current_user.company,
                             phoneNumber= current_user.phoneNumber, is_active= current_user.is_active, has_slack=current_user.has_slack,
                             has_kisi=current_user.has_kisi, has_agreement= current_user.has_agreement, has_mailbox= current_user.has_mailbox,
                             lockerNum= current_user.lockerNum)
    # current_user.img_url= 'filename'
    # #url= User(current_user.img_url= 'filename')
    # db.session.add(current_user.img_url)
    # db.session.commit()
    # return '<h1>'+ current_user.email+'</h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route('/facebook', methods=['GET', 'POST'])
def facebook():
    users= User.query.all()
    return render_template('facebook.html', users=users, img_url= current_user.img_url)

if __name__ == '__main__':
    app.run(debug=True)
