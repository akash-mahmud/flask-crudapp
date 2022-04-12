# from logging import debug
from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskproject.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id        = db.Column(db.Integer , primary_key = True)
    firstName = db.Column(db.String(100) , nullable = False)
    lastName = db.Column(db.String(100) , nullable = False)
    userName = db.Column(db.String(20) , nullable = False)
    city = db.Column(db.String(200) , nullable = False)
    data_created = db.Column(db.DateTime , default= datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.firstName}"


@app.route("/" , methods=['GET' , 'POST'])
def hello_world():
    if request.method== 'POST':
        # print(request.form.get('firstName'))
    
        firstName = request.form.get('firstName')
  
        lastName =  request.form.get('lastName')
        userName =  request.form.get('userName')
        city =  request.form.get('city')
        user = User(firstName=firstName, lastName=lastName, userName= userName, city=city)
        db.session.add(user)
        db.session.commit()
    allUser = User.query.all()
    # print(allUser)
    return render_template('index.html' , allUser =allUser)

@app.route("/users")
def products():
    allUser = User.query.all()
    print(allUser)
    return "<p>Products</p>"


@app.route("/update/<int:id>"  , methods=['GET' , 'POST'])
def update(id):
    if request.method== 'POST':
        # print(request.form.get('firstName'))
    
        firstName = request.form.get('firstName')
  
        lastName =  request.form.get('lastName')
        userName =  request.form.get('userName')
        city =  request.form.get('city')
        user = User.query.filter_by(id=id).first()
        user.firstName =firstName
        user.lastName = lastName
        user.userName = userName
        user.city = city
        db.session.add(user)
        db.session.commit()
        return redirect("/")

    user = User.query.filter_by(id=id).first()
   
    return render_template('update.html' , user =user)


@app.route("/delete/<int:id>")
def delete(id):

    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    print(user)
    
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)