
from flask import Blueprint, Flask,render_template,redirect,url_for,session,flash,request
from app.customers import customers
from app import mydatabase
from datetime import date


books = Blueprint('books',__name__, url_prefix='/books')
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='library.sqlite')

books.register_blueprint(customers)

#ADD BOOK ROUTE
@books.route('/new_book', methods = ['POST','GET'])
def add_new_book():
    if request.method == "POST":
        name = request.form['name']
        author = request.form['author']
        year_published = request.form['year_published']
        type = request.form['type']
        dbms.insert_new_book(name,author,year_published,type)

        return redirect(url_for('books.add_new_book'))
    return render_template('add_new_book.html')    

#GET LOAN ROUTE
@books.route('/loans/<i>')
def loan(i):
    try:
        var=dbms.get_data_by('custID',mydatabase.CUSTOMERS,'email',session['email'])
        for x in var:
            b = str(x).strip('(').strip(')').strip(',')
        custID = b
        bookID = str(i).strip("'")
        loandate = date.today()
        returndate ='Not yet'
        dbms.insert_loan(custID,bookID,loandate,returndate)
        flash('SUCSSES')
        return render_template('display_books.html')
    except Exception as x:
        print(x)    

        return render_template('display_books.html')

#RETURN BOOK ROUTHE
@books.route('/return/<i>')
def return_a_book(i):
    today_date = date.today()
    dbms.update(mydatabase.LOANS,'returndate',today_date,"bookID",i )
    flash('SUCSSES')
    return render_template('display_books.html')