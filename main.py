from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import user

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer,primary_key=True,)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    phno = db.Column(db.Integer)
    gender = db.Column(db.Text)
    stream = db.Column(db.Text)
    address = db.Column(db.Text)
    yop = db.Column(db.Text)


    def __init__(self, name, email, phno, gender, stream, address, yop ):
        self.name = name
        self.email = email
        self.phno = phno
        self.gender = gender
        self.stream = stream
        self.address = address
        self.yop = yop


    def __repr__(self):
        return "{} {} {} ".format(self.name, self.email, self.phno, self.gender,  self.stream, self.address, self.yop,)
db.create_all()

class Marks(db.Model):
    __tablename__ = "marks"

    id = db.Column(db.Integer,primary_key=True,)
    name = db.Column(db.Text, nullable=False)
    sem1 = db.Column(db.Integer)
    sem2 = db.Column(db.Integer)
    sem3 = db.Column(db.Integer)
    sem4 = db.Column(db.Integer)
    sem5 = db.Column(db.Integer)
    sem6 = db.Column(db.Integer)
    sem7 = db.Column(db.Integer)
    sem8 = db.Column(db.Integer)

    def __init__(self,id, name,  sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8 ):
        self.id = id
        self.name = name
        self.sem1 = sem1
        self.sem2 = sem2
        self.sem3 = sem3
        self.sem4 = sem4
        self.sem5 = sem5
        self.sem6 = sem6
        self.sem7 = sem7
        self.sem8 = sem8

    def __repr__(self):
        return "{} {} {} ".format(self.id, self.name, self.sem1, self.sem2, self.sem3, self.sem4,  self.sem5, self.sem6, self.sem7, self.sem8)
db.create_all()

@app.route("/")
@app.route("/index")
def index():
    all = Student.query.all()
    return render_template('index.html',all=all)

@app.route("/add_student", methods=["GET","POST"])
def add_student():
    if request.method=="POST":
        name = request.form['name']
        phno = request.form['phonenumber']
        email = request.form['email']
        gender = request.form['gender']
        stream = request.form['stream']
        address = request.form['address']
        yop = request.form['yop']

        total = Student(name, email, phno, gender, stream, address, yop)
        db.session.add(total)
        db.session.commit()
        flash("Student created successfully","success")
        return redirect(url_for("index"))

    return render_template('add_student.html')

@app.route("/edit_student/<int:id>",methods=["GET","POST"])
def edit_student(id):
    student_to_update = Student.query.get(id)
    if request.method == "POST":
        student_to_update.name = request.form['name']
        student_to_update.phno = request.form['phonenumber']
        student_to_update.email = request.form['email']
        student_to_update.gender = request.form['gender']
        student_to_update.stream = request.form['stream']
        student_to_update.address = request.form['address']
        student_to_update.yop = request.form['yop']

        try:
            db.session.commit()
            flash("Student updated successfully", "success")
            return redirect(url_for("index"))
        except:
            return "NOT UPDATED"
    else:
        return render_template('edit_student.html', student_to_update = student_to_update)

@app.route("/delete_student",methods=["GET","POST"])
def delete_student():
    if request.method == "POST":
        name = request.form['name']
        d = Student.query.filter_by(name=name).first()
        db.session.delete(d)
        db.session.commit()
        # all = Student.query.all()
        flash("Student Deleted successfully", "warning")
        return redirect(url_for("index"))
    else:
        flash("Student Not Found","dark")
    return render_template('delete_student.html')

@app.route("/list.html")
def list():
    all = Student.query.all()
    return render_template('list.html', all=all)


@app.route("/student_marks")
def student_marks():
    # all = Marks.query.all()
    # sorting sem-wise marks, I tried to sort all the but I couldn't do
    page = request.args.get('page',1,type=int)
    all = Marks.query.order_by(Marks.sem1).paginate(page=page, per_page=3)
    all = Marks.query.order_by(Marks.sem2).paginate(page=page, per_page=3)
    all = Marks.query.order_by(Marks.sem3).paginate(page=page, per_page=3)
    return render_template('student_marks.html',all=all, page=page,)


@app.route("/add_marks", methods=["GET","POST"])
def add_marks():
    if request.method=="POST":
        id = request.form['id']
        name = request.form['name']
        sem1 = request.form['sem1']
        sem2 = request.form['sem2']
        sem3 = request.form['sem3']
        sem4 = request.form['sem4']
        sem5 = request.form['sem5']
        sem6 = request.form['sem6']
        sem7 = request.form['sem7']
        sem8 = request.form['sem8']
        total = Marks(id, name, sem1, sem2, sem3,sem4, sem5, sem6, sem7, sem8)
        db.session.add(total)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template('add_marks.html')


@app.route("/edit_add_marks/<int:id>",methods=["GET","POST"])
def edit_add_marks(id):
    edit_add_marks_to_update = Marks.query.get(id)
    if request.method == "POST":
        # edit_add_marks_to_update.id = request.form['id']
        edit_add_marks_to_update.name = request.form['name']
        edit_add_marks_to_update.sem1 = request.form['sem1']
        edit_add_marks_to_update.sem2 = request.form['sem2']
        edit_add_marks_to_update.sem3 = request.form['sem3']
        edit_add_marks_to_update.sem4 = request.form['sem4']
        edit_add_marks_to_update.sem5 = request.form['sem5']
        edit_add_marks_to_update.sem6 = request.form['sem6']
        edit_add_marks_to_update.sem7 = request.form['sem7']
        edit_add_marks_to_update.sem8 = request.form['sem8']

        try:
            db.session.commit()
            flash("Student marks updated successfully", "success")
            return redirect("/index")
        except:
            return "NOT UPDATED"
    else:
        return render_template('edit_add_marks.html', edit_add_marks_to_update = edit_add_marks_to_update)


@app.route("/search",methods=["post","GET"])
def search():
    if request.method == "POST":
        a = request.form.get('searched')
        ab=a
        all = Student.query.filter(Student.name.ilike(f"%{a}%")).all()
        return render_template("search.html", all=all, ab=ab)
    return render_template("list.html")

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)