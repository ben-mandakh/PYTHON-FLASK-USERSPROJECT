from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)


##################    READ INDEX  ###################################
@app.route('/')
@app.route("/users")
def index():
    mysql = connectToMySQL('all_users')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template("index.html", all_us=users)


################## ADD A NEW USER PAGE    ###########################
@app.route("/users/new")
def users_new():
    return render_template("create.html")


################## ADD A NEW USER FUNCTION ##########################
@app.route("/process", methods=["POST"])
def add_newUser_to_db():
    mysql = connectToMySQL("all_users")
    
    query = "INSERT INTO users(full_name, email, created_at, updated_at) VALUES (%(fn)s, %(email)s, NOW(), NOW());"
    data = {
        'fn': request.form['fname'] + ' '+ request.form['lname'],
        'email': request.form['eml'],
    }
    new_user_id = mysql.query_db(query, data)
    return redirect("/users")

##################    SHOW   #########################################
@app.route("/users/<num>")
def user_one(num):
    mysql = connectToMySQL('all_users')
    users = mysql.query_db('SELECT * FROM users WHERE id =' + num)
    print(users)
    return render_template("one.html", one_us = users )


################## ADD UPDATE PAGE    ################################
@app.route("/users/edit/<num>")
def users_edit(num):
    return render_template("update.html", userId = num)

##################    UPDATE FUNCTION   ##############################
@app.route("/editInfo", methods=["POST"])
def user_edit():
    mysql = connectToMySQL("all_users")
    
    query = "UPDATE users SET full_name = %(fn)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
    data = {
        'fn': request.form['fname'] + ' '+ request.form['lname'],
        'email': request.form['eml'],
        'id':request.form['id'],
    }
    new_user_id = mysql.query_db(query, data)
    return redirect("/users")

#################    DELETE    ######################################
@app.route("/users/delete/<num>")
def delete(num):
    print(num)
    mysql = connectToMySQL('all_users')
    query = "DELETE FROM users WHERE id =" + num
    mysql.query_db(query)
    return redirect('/users')

#################    END    #########################################
if __name__ == "__main__":
    app.run(debug=True)