from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nvc66176;PWD=mJ8bip8lv31naRX3",'','')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reco')
def recomender():
    return render_template('recomender.html')

@app.route('/login')
def login():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')



@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    mail = request.form['email']
    password = request.form['pass']
    password2 = request.form['pass2']

    sql = "SELECT * FROM login WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('list.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO login VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, mail)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, password2)
      ibm_db.execute(prep_stmt)
    
    return render_template('result.html', msg="Register successfuly..")


@app.route('/auth',methods=['GET','POST'])
def auth():
    
    if request.method=='POST':
        email=request.form['your_name']
        
        password=request.form['your_pass']
        sql="SELECT * FROM login WHERE mail=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return redirect(url_for('recomender'))
        else:
            return render_template('result.html', msg="incorrect username or password")
    elif request.method=='GET':
        return render_template('signin.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)