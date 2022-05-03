
from flask import Blueprint, Flask,render_template,redirect,url_for,session,flash,request
from app import mydatabase

helper = Blueprint('helper',__name__, url_prefix='/helper')
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='library.sqlite')





#DELETE CUSTOMER ROUTE
@helper.route('/delcustomer/<i>')
def del_cust_by_id(i):
    print(i)
    dbms.delete_by_id(mydatabase.CUSTOMERS,'custID',i)
    return redirect('/display/customers')

#DELETE BOOK ROUTE
@helper.route('/delbook/<i>')  
def del_book_by_id(i):
    print(i)
    dbms.delete_by_id(mydatabase.BOOKS,'BookID',i)
    return redirect('/display/books')


