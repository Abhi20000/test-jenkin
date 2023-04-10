from flask import *
import mysql.connector

def sql_connection():   
    mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="root",
    db="abhishek"
    )
    conn= mydb.cursor()
    return mydb, conn

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=['GET','POST'])
def home():
    
    return render_template("home.html")


@app.route("/customer",methods=['GET','POST'])
def customer():
    mydb, conn = sql_connection()
    if request.method == 'POST':
        c_id = request.form.get('c_id')
        c_name = request.form.get('c_name')
        c_cellno = request.form.get('c_cellno')
        c_mail = request.form.get('c_mail')
        conn.execute(f"SELECT cust_id from customer where cust_id = { request.form.get('c_id') } ")
        if conn.fetchall() :
          flash('Customer Is Already Present in database . Try With Unique Customer Id')
          conn.execute("SELECT * FROM customer")
          p_cust_data = conn.fetchall()
          mydb.commit()
          mydb.close()
          conn.close()
          return render_template("customer.html", cs_d=p_cust_data)
        else:
          conn.execute("INSERT INTO customer VALUES ({}, '{}', {}, '{}')".format(c_id, c_name, c_cellno, c_mail))
          conn.execute("SELECT * FROM customer")
          p_cust_data = conn.fetchall()
          mydb.commit()
          mydb.close()
          conn.close()
          return render_template("customer.html", cs_d=p_cust_data)

    else:
        conn.execute("SELECT * FROM customer")
        p_cust_data = conn.fetchall()
        mydb.commit()
        mydb.close()
        conn.close()
        return render_template("customer.html", cs_d=p_cust_data)


@app.route("/courses",methods=['GET','POST'])
def courses():
    mydb, conn = sql_connection()
    if request.method == 'POST':
       
        course_id = request.form.get('course_id')
        course_name = request.form.get('course_name')
        course_price = request.form.get('course_price')
        conn.execute(f"SELECT course_id from courses where course_id = { request.form.get('course_id') } ")
        if conn.fetchall() :
          flash('Course id already Present. Try with unique id')
          conn.execute("SELECT * FROM courses")
          p_course_data = conn.fetchall()
          mydb.commit()
          mydb.close()
          conn.close()
          return render_template("courses.html", co_d=p_course_data)
        else:
         conn.execute("INSERT INTO courses VALUES ({}, '{}', {})".format(course_id, course_name, course_price))
         conn.execute("SELECT * FROM courses")
         course_data = conn.fetchall()
         mydb.commit()
         mydb.close()
         conn.close()
         return render_template("courses.html", co_d=course_data)
    

    else:
        mydb, conn = sql_connection()
        conn.execute("SELECT * FROM courses")
        p_course_data = conn.fetchall()
        mydb.commit()
        mydb.close()
        conn.close()
        return render_template("courses.html", co_d=p_course_data)



@app.route("/sales",methods=['GET','POST'])
def sales():
    mydb, conn = sql_connection()
    if request.method == 'POST':
        s_id = request.form.get('s_id')
        s_custid = request.form.get('s_custid')
        s_courseid = request.form.get('s_courseid')
        s_qty_order = request.form.get('s_qty_order')
        conn.execute(f"SELECT s_id from sales where s_id = { request.form.get('s_id') } ")
        if conn.fetchall():
          flash('S-ID Already Present. Try With Unique Sales Id')
          conn.execute("SELECT * FROM sales")
          sales_data = conn.fetchall()
          mydb.commit()
          mydb.close()
          conn.close()
          return render_template("sales.html", sa_d=sales_data)
        conn.execute(f"SELECT cust_id from customer where cust_id = { request.form.get('s_custid') } ")
        if conn.fetchall():
          conn.execute("INSERT INTO sales VALUES ({}, {}, {}, {})".format(s_id, s_custid, s_courseid, s_qty_order))
          conn.execute("SELECT * FROM sales")
          sales_data = conn.fetchall()
          mydb.commit()
          mydb.close()
          conn.close()
          return render_template("sales.html", sa_d=sales_data)
        else:
          flash('Customer Id Is Not Maching. Customer Should Present In Customer Table')
          conn.execute("SELECT * FROM sales")
          sales_data = conn.fetchall()
          mydb.commit()
          mydb.close()
          conn.close()
          return render_template("sales.html", sa_d=sales_data)
        

    else:
        mydb, conn = sql_connection()
        conn.execute("SELECT * FROM sales")
        p_sales_data = conn.fetchall()
        mydb.commit()
        mydb.close()
        conn.close()
        return render_template("sales.html", sa_d=p_sales_data)

@app.route("/report")
def report():
        mydb, conn = sql_connection()
        conn.execute("""
           select customer.cust_name, customer.cust_email, customer.cust_cellno,
           case 
           when customer.cust_id in (select sales.s_custid from sales,customer 
           where customer.cust_id= sales.s_custid ) and sales.s_courseid in 
          (select courses.course_id  from courses , sales  where courses.course_id=sales.s_courseid ) 
           then 
          (select sum( sales.s_qty_order * courses.course_price)  from sales,courses
           where courses.course_id=sales.s_courseid and customer.cust_id = sales.s_custid )
           else 0
          END AS total_sales
          from customer,courses,sales
          group by customer.cust_id
          order by customer.cust_id asc;""")
        p_sales_report = conn.fetchall()
        
        mydb.commit()
        mydb.close()
        conn.close()
        print(p_sales_report)
        return render_template("report.html", sa_report=p_sales_report)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
