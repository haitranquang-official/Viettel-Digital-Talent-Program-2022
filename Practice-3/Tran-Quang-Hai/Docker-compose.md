# **TASK: CREATE A THREE-TIER APPLICATION AND DEPLOY WITH DOCKER AND DOCKER-COMPOSE**

## **1. Overview**
This project sets up a three-tier web application that displays the course
attendees’ information on the browser using docker-compose.
<br>
Base images:
<br>
• nginx:1.22.0-alpine
<br>
• python:3.9
<br>
• mongo:5.0


## **2. MongoDB**

### **2.1.** Populate database
To import a CSV file to mongodb, we use the following command
```
mongoimport --type csv -d student -c student --headerline datasource.csv
```
Explanation:
<br>
--type: file type
<br>
-d: database
<br>
-c: collection (same as database name by default)
<br>
--headerline: specify that first line of CSV file means fields' names
<br>
We would later use this command in docker container's shell


## **3. Python Application**

### **3.1.** Libraries to use
- Flask: a popular framework to develop HTTP application with Python
- Flask_mongoengine: connect to mongodb instances
- DNSPython: a requirement for Flask_mongoengine
- Jinja2: a framework to "Pythonize" HTML
<br>
All will be included in requirements.txt as usual
```
flask
flask_mongoengine
dnspython
Jinja2
```

### **3.2.** Develop a Flask application

### **3.2.1.** Project structure

<img src="imgs/1-Python code structure.png">
<br>
Quite simple structure, but it can be take for granted as our main focus is about Docker.

### **3.2.2.** Database configuration

In config.py file, I specified attributes of mongo database that is going to be used:
```
config = {
    'db': 'student',
    'host': 'mongodb',
    'port': 27017
}

def get_config():
    return config
```

### **3.2.3.** Initial Flask app
In app.py, first I imported necessary libraries and specify application properties:

```
import config
from flask import jsonify, render_template, request, Flask
from flask_mongoengine import MongoEngine
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.get_config()
db = MongoEngine()
db.init_app(app)
```

### **3.2.4.** Define Student class
```
class Student(db.Document):
    number = db.IntField()
    name = db.StringField()
    yob = db.IntField()
    major = db.StringField()
    university = db.StringField()
```
### **3.2.5.** Expose HTTP Request
```
@app.route('/all', methods=['GET'])
def all():
    students = list(Student.objects.all())
    students.sort(key=lambda x: x.number)
    return render_template('list.html', students=students)
```

### **3.2.6.** Display on HTML

As you may notice, there is a method called "render_template" above. By default, it will render HTML file in ./templates folder. Below is the HTML code in list.html:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <table>
        <tr>
            <th>STT</th>
            <th>Tên</th>
            <th>Năm sinh</th>
            <th>Trường</th>
            <th>Chuyên ngành</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student.number }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.yob }}</td>
            <td>{{ student.university }}</td>
            <td>{{ student.major }}</td>
        </tr>  
        
        {% endfor %}
    </table>
</body>
</html>
```
In the for-loop above, Jinja2 library was used to "Pythonize" HTML code

### **3.3.** Dockerfile
```
FROM python:3.9
RUN mkdir /python-app
WORKDIR /python-app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT [ "python", "app.py" ]
EXPOSE 5000
```
- requirements.txt file and pip install command don't usually change the content of the image compare to the last build, so these commands would be run first
## **4. Nginx**

### **4.1.** Custom configuration
To make Nginx listen to Python app instead, we need to add those configurations to nginx.conf file
```
server {
        listen 80;
        proxy_pass_header Server;

        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://pythonapp:5000/;
        }
    }
```
Full nginx file is in nginx folder

### **4.2.** Dockerfile
Since we have a custom conf file, we need to replace the default file with it
```
FROM nginx:1.22.0-alpine
COPY nginx.conf /etc/nginx/nginx.conf
```

## **5. Docker-compose**
### **5.1.** Docker-compose file
Content of docker-compose.yml file:
```
version: '3.0'

services:
  mongodb:
    image: mongo:5.0
    container_name: mongodb_vt
    ports:
      - 27016:27017
  pythonapp:
    build: python-http/
    ports:
      - 5009:5000
  nginx:
    build: nginx/
    restart: always
    ports:
      - 5005:80
    depends_on:
      - pythonapp
```
We can access MongoDB at port 27016, Python Flask app at port 5009 and Nginx at port 5005.
<br>
For mongodb, I use default image on dockerhub, while for pythonapp and nginx I build a custom image on local machine

## **6. Deploy on a cloud server**

### **6.1.** Create a Docker context

### **6.1.1.** Initial SSH connection

### **6.1.2.** Install Docker on remote machine
For this task, I would reuse Ansible playbook from last assignment. [Link to playbooks]("https://github.com/haitranquang-official/Viettel-Digital-Talent-Program-2022/tree/main/Practice-2/Tran-Quang-Hai/playbooks/roles/personal/tasks").

### **6.1.3.** Create Docker context
After finishing step 6.1.1 and 6.1.2, you can create a docker context using command:
```
docker context create <context-name> --docker "host=ssh://<username>@<ip_address>"
```
Show all contexts that have been created:
```
docker context ls
```

### **6.2.** Deploy with docker-compose
First, I switch docker context to the server that I'm going to deploy those applications:
```
docker context use <context_name>
```
Then you are good to go, just run:
```
docker-compose up -d
```

### **6.3.** (Optional) Simple load balancer with nginx
### **6.3.1.** nginx.conf file
```
    upstream flask{
        server 178.128.109.226
        server 178.128.103.48
    }
    server {
        listen 80;
        proxy_pass_header Server;

        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://flask:5000/;
        }
    }
```
Traffic to port 80 nginx host will be distributed to servers 178.128.109.226 and 178.128.103.48 both at port 5000

