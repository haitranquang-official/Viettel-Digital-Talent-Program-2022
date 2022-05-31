import config
from flask import jsonify, render_template, request, Flask
from flask_mongoengine import MongoEngine
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.get_config()
db = MongoEngine()
db.init_app(app)


class Student(db.Document):
    name = db.StringField()
    email = db.StringField()

    def to_json(self):
        return {"name": self.name,
                "email": self.email}


@app.route('/all', methods=['GET'])
def all():
    students = Student.objects.all()
    return render_template('list.html', students=students)


@app.route('/add', methods=['POST'])
def add():
    record = request.json
    student = Student(name=record['name'], email=record['email'])
    student.save()
    return jsonify(student.to_json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
