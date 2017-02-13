from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nvp'
db = SQLAlchemy(app)

# Create our database model
class Members(db.Model):
    __tablename__ = "Members"
    id = db.Column(db.Integer, primary_key=True)
    firstName= db.Column(db.String(20))
    lastName= db.Column(db.String(20))
    company= db.Column(db.String(50))
    phoneNumber= db.Column(db.VARCHAR(15),unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, firstName, lastName, company, phoneNumber, email):
        self.firstName = firstName
        self.lastName= lastName
        self.company= company
        self.phoneNumber= phoneNumber
        self.email= email

    def __repr__(self, email):
        return '< Email %s>' % (self.email)

# Set "homepage" to index.html
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/SignUp.html', methods=['POST'])
def index():
    return render_template('SignUp.html')

@app.route('/dashboard.html', methods=['POST'])
def dashboard():
    return render_template('dashboard.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    if request.method == 'POST':
        email = request.form['email']
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        fullName= firstName+lastName
        company = request.form['company']
        phoneNumber= request.form['phoneNumber']

        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(Members).filter(Members.firstName+Members.lastName== firstName+lastName).count():
        #em = Users(email)
            user= Members(firstName, lastName, company, phoneNumber, email)
            db.session.add(user)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
