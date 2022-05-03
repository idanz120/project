from flask import Blueprint, Flask,render_template,redirect,url_for,session,flash,request

from app import mydatabase

customers = Blueprint('customers',__name__, url_prefix='/customers')
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='library.sqlite')




# SING UP ROUTE
@customers.route('/singup', methods = ['POST','GET'])
def add_new_customer():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        age = request.form['age']
        var = dbms.get_data_by('email',mydatabase.CUSTOMERS,'email',email)
        print(var)
        if var == []:
            dbms.insert_new_customer(name,email,password,city,age)
            return redirect(url_for('customers.login'))
        else: flash(' Email Already Exists')
              
    return render_template('singup.html')  


# LOG IN ROUTE
@customers.route("/login", methods = ['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        check = dbms.check_login(email,password)

        print(f'the result is {check}')
        if check != [] :
            session['email'] = email
            session['password'] = password
            print(session)
            name = dbms.get_data_by('name',mydatabase.CUSTOMERS,'email',email)
            for n in name:
                var = str(n).strip('(').strip(')').strip("'").strip(',').strip("'")
            session['name'] = var
            return redirect(url_for('home'))

        else: 
            flash('Not Correct! Try again','info')
            return render_template('login.html')       
    else:
        return render_template('login.html')    


# FIND CUST BY NAME
@customers.route('/find', methods=["POST",'GET'])
def find_customer():
    
    if request.method == "POST":
        data = request.form['search']
        res = dbms.get_data_by('*',mydatabase.CUSTOMERS,'name',data)
        if res ==[]:flash('No results')
        return render_template('find_cust.html',res=res)
    return render_template('find_cust.html')
    

# LOG OUT ROUTE
@customers.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect(url_for('customers.login'))