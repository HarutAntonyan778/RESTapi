from bottle import run,get,route,post,request
import sqlite3
import json
import re

conn = sqlite3.connect('databases/users')



@get("/users")
def get_all_users():
    response = []
    try:
        em = request.query['email']
        db = conn.execute("SELECT * FROM accounts WHERE email='{e}'".format(e=em))
    except Exception as e:
        db = conn.execute("SELECT * FROM accounts")
    for row in db:
        response.append({'email': row[0],
        'firstName': row[2],
        'lastName': row[3],
        'age': row[4]})
    return {'items': response}

@get("/emailVerify")
def emailVerify():
    try:
        email = request.query['email']
    except Exception as e:
        return {'errorMessage':'email query parameter is required'}
    return {'exist': verify_email(email)}

@post("/users")
def register():
   post_data = json.loads(request.body.read())
   try:
       firstName = post_data['firstName']
       lastName = post_data['lastName']
       password = post_data['password']
       email = post_data['email']
       age = post_data['age']
   except Exception as e:
       return {'errorMessage': 'Something went wrong, please try again with correct information'}
   if is_valid_email(email) == False:
       return {'errorMessage': 'Invalid email format'}

   if verify_email(email) == True:
       return {'errorMessage': 'Email is exist, Please provide another email address'}


   db = conn.execute("INSERT INTO accounts (email,password,firstName,lastName,age) VALUES ('{e}','{p}','{f}','{l}',{g})".format(e=email,p=password,f=firstName,l=lastName,g=age))
   conn.commit()
   return {'success': True}

@post("/login")
def login():
    post_data = json.loads(request.body.read())
    try:
        email = post_data['email']
        password = post_data['password']
    except Exception as e:
        return {'errorMessage': 'Something went wrong, please try again with correct information'}
    if is_valid_email(email) == False:
        return {'errorMessage': 'Invalid email format'}
    if verify_email(email) == False:
        return {'errorMessage': "Emailaddress doesn't exist"}
    user = conn.execute("SELECT * FROM accounts WHERE email='{e}' AND password='{p}'".format(e=email,p=password))
    for row in user:
        return {'email': row[0],'firstName':row[2],'lastName':row[3],'age':row[4]}
    return {'errorMessage': 'Invalid password'}

def verify_email(email):
    db = conn.execute("SELECT * FROM accounts WHERE email='{e}'".format(e=email))
    for row in db:
        return True
    return False

def is_valid_email(email):
        if re.match("^([a-z]{1}[a-zA-Z-_]{3,16}){1}@([a-z]{2,7}\.[a-z]{2,4}){1}(\.[a-z]{2,4})?$",email) == None:
            return False
        return True

run(reLoader=True, debug=True,host='localhost',port=8080)
