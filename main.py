from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired,Length
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.secret_key = "9505082-84-19-919-157028"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Myform(FlaskForm):
    firstname = StringField("firstname",validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])
    email = StringField("email", validators=[Email(message="Email id required")])
    password = PasswordField("password", validators=[InputRequired(message="Password required"),Length(min=5,max=10,message="length should be between 5 and 10")])
    submit = SubmitField("submit")

class Student(db.Model):
    id = db.Column("id",db.Integer,primary_key = True)
    firstname = db.Column("firstname",db.String(255))
    lastname = db.Column("lastname",db.String(255))
    email  = db.Column("email",db.String(255))
    password = db.Column("password",db.String(255))

    def __init__(self,firstname,lastname,email,password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

db.create_all()


@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/signup",methods = ["GET","POST"])
def signingUp():
    form = Myform()
    if form.validate_on_submit():
        fname = form.firstname.data
        lname = form.lastname.data
        email = form.email.data
        password = form.password.data
        student = Student(fname, lname, email, password)
        db.session.add(student)
        db.session.commit()
        return render_template("welcomeStudent.html",name = fname)
    return render_template("signup.html", form=form)

@app.route("/allStudents")
def allStudentsMethod():
    students = db.session.query(Student).all()
    return render_template("viewall.html",students = students)
#**** returning json
@app.route("/<int:id>")
def studbyid(id):
    student = Student.query.get(id)
    return jsonify(studentName= student.firstname,studentLastName=student.lastname,studentEmail=student.email,studentPassword=student.password)

@app.route("/allStudentsJson")
def all():
    studentList =[]
    students = Student.query.all()
    for item in students:
        studentList.append({"firstname":item.firstname,"lastname":item.lastname,"email":item.email,"password":item.password})
    print(studentList)
    return jsonify(studentList)
@app.route("/delete/<int:id>")
def deleteStudent(id):
    student_to_delete = Student.query.get(id)
    db.session.delete(student_to_delete)
    db.session.commit()
    return redirect("/allStudents")

@app.route("/edit/<int:id>",methods = ["POST","GET"])
def editStudent(id):
    student_to_edit = Student.query.get(id)
    if request.method=="POST":
        student_to_edit = Student.query.get(id)
        student_to_edit.firstname = request.form["firstname"]
        student_to_edit.lastname = request.form["lastname"]
        student_to_edit.email = request.form["email"]
        student_to_edit.password = request.form["password"]
        db.session.commit()
        return redirect("/allStudents")
    return render_template("update.html",stu = student_to_edit)

if __name__ == "__main__":
    app.run(debug = True)

"""Read All Records
all_books = session.query(Book).all()


Read A Particular Record By Query
book = Book.query.filter_by(title="Harry Potter").first()


Update A Particular Record By Query
book_to_update = Book.query.filter_by(title="Harry Potter").first()
book_to_update.title = "Harry Potter and the Chamber of Secrets"
db.session.commit()  


Update A Record By PRIMARY KEY
book_id = 1
book_to_update = Book.query.get(book_id)
book_to_update.title = "Harry Potter and the Goblet of Fire"
db.session.commit()  


Delete A Particular Record By PRIMARY KEY
book_id = 1
book_to_delete = Book.query.get(book_id)
db.session.delete(book_to_delete)
db.session.commit()
You can also delete by querying for a particular value e.g. by title or one of the other properties.

"""