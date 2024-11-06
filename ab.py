from datetime import timedelta
from flask import Flask,render_template,redirect, request, session, url_for,flash
from werkzeug.utils import secure_filename
from dbconnection.datamanipulation import *
import os

app=Flask(__name__)
upload_folder='./static'
app.config['UPLOAD_FOLDER']=upload_folder
app.config['MAX_CONTENT_LENGTH']=16*1024*1024
ALLOWED_EXTENSIONS={'jpg','png','PNG'}
def is_allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
app.secret_key='supersecretkey'
app.secret_key="superadmin"
app.permanent_session_lifetime=timedelta(minutes=30)


@app.route('/')
def home():
    if 'id' in session:
        return redirect('home_page')
   
    return render_template('ab.html')

@app.route('/home_page')
def home_page():
    return render_template('home.html')

@app.route('/register')
def register():
    if 'id' in session:
        return redirect('home_page')
    return render_template('register.html')

@app.route('/register_action',methods=['POST'])
def register_action():
    name=request.form['name']
    age=request.form['age']
    address=request.form['address']
    username=request.form['username']
    password=request.form['password']
    user=sql_edit_insert('insert into register values(NULL,?,?,?,?,?)',(name,address,age,username,password))
    flash('inserted succefully')

    return redirect(url_for('register'))


@app.route('/login')
def login():
    if 'id' in session:
        return redirect('home_page')

    return render_template('login.html')

@app.route('/login_action',methods=['POST'])
def login_action():
    username=request.form['username']
    password=request.form['password']
    user=sql_query2('select * from register where username=? and password=?',(username,password))
    if len(user)>0:
        session['id']=user[0][0]
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('login'))
    
@app.route('/display')    
def display():
    m=sql_query('select * from register')
    return render_template('display.html',a=m)


@app.route('/logout')
def logout():
    if 'id' in session:
      session.clear()
      return redirect(url_for('login'))

@app.route('/delete')
def delete():
      user=request.args.get('uid')
      m=sql_edit_insert('delete from register where id=?',[user])
      return redirect(url_for('display'))

@app.route('/edit')
def edit():
    user=request.args.get('eid')
    m=sql_query2('select * from register where id=?',[user])
    return render_template('edit.html',p=m)

@app.route('/edit_action',methods=['POST'])
def edit_action():
    id=request.form['id']
    name=request.form['name']
    age=request.form['age']
    address=request.form['address']
    username=request.form['username']
    password=request.form['password']
    user=sql_edit_insert('update register set name=?,age=?,address=?,username=?,password=? where id=?',(name,age,address,username,password,id))
    
    return redirect(url_for('display'))

@app.route('/dropdown')
def dropdown():
    m=sql_query('select * from country')
    return render_template('dropdown.html',n=m)

@app.route('/getstate')
def getstate():
    m=request.args.get('co')
    p=sql_query2('select * from state where cid=?',[m])
    print(p)
    return render_template('getstate.html',c=p)

@app.route('/update')
def update():
    m=sql_query('select * from place')
    return redirect(url_for('dropdown'))


@app.route('/update_action',methods=['POST'])
def update_action():
    country=request.form['country']
    state=request.form['state']
    place=request.form['place']
    user=sql_edit_insert('insert into place values(NULL,?,?,?)',(country,state,place))
    flash('inserted sucessfully')
    return redirect(url_for('update'))

@app.route("/fileupload")
def fileupload():
    return render_template('upload.html')

@app.route("/uploadAction", methods=["post"])
def uploadAction():
    if request.method=='POST':
        if len(request.files)>0:
            file=request.files['file']
        if file and is_allowed(file.filename): 
            filename=secure_filename(file.filename)
            r=sql_edit_insert('insert into file_tb values(NULL,?,?)',(filename,request.form['name'])) 
        if(r>0):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) 
            flash('inserted sucessfully')
        else:
            msg='uploading failed'
            return render_template('upload.html',msg=msg) 
    return redirect(url_for('fileupload'))      

@app.route('/viewimage')
def viewimage():
    image=sql_query('select * from file_tb')
    return render_template('viewimage.html',a=image)

if __name__=='__main__':
    app.run(debug=True)

    


