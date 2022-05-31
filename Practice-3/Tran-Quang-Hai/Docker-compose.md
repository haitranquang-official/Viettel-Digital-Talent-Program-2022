# **TASK: CREATE A THREE-TIER APPLICATION AND DEPLOY WITH DOCKER AND DOCKER-COMPOSE**

## **1. Overview**

### **1.1.** 

## **2. MongoDB**

### **2.1.** Populate database

## **3. Python Application**

### **3.1.** Libraries to use
- Flask: a popular framework to develop HTTP application with Python
- Flask_mongoengine: connect to mongodb instances
- DNSPython: a requirement for Flask_mongoengine
- Jinja2: a framework to "Pythonize" HTML
<br>
All will be included in requirements.txt as usual

### **3.2.**
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
## **4. Nginx**

### **4.1.**

## **5. Docker-compose**

## **6. Deploy on a cloud server**

