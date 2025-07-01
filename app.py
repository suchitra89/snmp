from flask import Flask,request,redirect,url_for,render_template,flash,session,send_file
from otp import genotp
from cmail import send_mail
from stoken import entoken,dctoken
import mysql.connector
from io import BytesIO
import flask_excel as excel
import re
app=Flask(__name__)
app.secret_key='codegnan@123'
excel.init_excel(app)
mydb=mysql.connector.connect(user='root',host='localhost',password='admin',db='snmp')
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['useremail']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(useremail) from users where useremail=%s',[useremail])
        email_count=cursor.fetchone()
        print(email_count)
        if email_count[0]==0:
            gotp=genotp()#server generated otp
            userdata={'username':username,'useremail':useremail,'password':password,'gotp':gotp}
            subject='OTP for SNM app'
            body=f'use this otp for SNM registration{gotp}'
            send_mail(to=useremail,subject=subject,body=body)
            flash('OTP has been to given email')
            return redirect(url_for('verifyotp',endata=entoken(data=userdata)))
        elif email_count[0]==1:
            flash(f'{useremail} already existed')    
    return render_template('register.html')    
@app.route('/verifyotp/<endata>',methods=['GET','POST'])
def verifyotp(endata):
    if request.method=='POST':
        uotp=request.form['userotp']#user given otp
        dcdata=dctoken(data=endata)
        if dcdata['gotp']==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into users(useremail,username,password) values(%s,%s,%s)',[dcdata['useremail'],dcdata['username'],dcdata['password']])
            mydb.commit()#tcl command
            cursor.close()
            flash('Details registerd sucessfully')
            return redirect(url_for('login'))
        else:
            flash('otp was wrong')    
    return render_template('verifyotp.html')  
@app.route('/login',methods=['GET','POST'])
def login():
    if not session.get('user'):
        if request.method=='POST':
            uemail=request.form['useremail']
            password=request.form['userpwd']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(useremail) from users where useremail=%s',[uemail])
            email_count=cursor.fetchone()
            if email_count[0]==1:
                cursor.execute('select password from users where useremail=%s',[uemail])
                stored_password=cursor.fetchone()
                if stored_password[0]==password:
                    print(session)
                    session['user']=uemail
                    print(session)
                    return redirect(url_for('dashboard'))
                else:
                    flash('password wrong')
                    return redirect(url_for('login'))
            elif email_count[0]==0:
                flash('No email found')
                return redirect(url_for('login'))
            else:
                return 'something wrong'
        return render_template('login.html') 
    else:
        return redirect(url_for('dashboard'))    

   
@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        flash('pls login first')
        return redirect(url_for('login'))    

@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if session.get('user'):
        if request.method=='POST':
            utitle=request.form['title']
            udescription=request.form['description']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into notes(title,description,added_by) values(%s,%s,%s)',[utitle,udescription,
            session.get('user')])
            mydb.commit()
            cursor.close()
            flash(f"{utitle} notes added sucesfully")

        return render_template('addnotes.html')
    else:
        flash('pls login first')
        return redirect(url_for('login'))    
    
@app.route('/viewallnotes')
def viewallnotes():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from notes where added_by=%s',[session.get('user')])
        allnotes=cursor.fetchall()#[(1,'python','fdfdccd','nsuchi3@gmail.com)]
        print(allnotes)
        return render_template('viewallnotes.html',allnotes=allnotes)
    else:
        flash('pls login first')
        return redirect(url_for('login'))    
   
@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from notes where n_id=%s and added_by=%s',[nid,session.get('user')])
        notesdata=cursor.fetchone()
        return render_template('viewnotes.html',notesdata=notesdata)
    else:
        flash('pls login first')
        return redirect(url_for('login'))      

@app.route('/updatenotes/<nid>',methods=['GET','POST']) 
def updatenotes(nid):
    if sessoin.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from notes where n_id=%s and added_by=%s',[nid,session.get('user')])
        notesdata=cursor.fetchone() #(1,'python','guyg')
        if request.method=='POST':
            utitle=request.form['title']
            udescription=request.form['description']
            cursor.execute('update notes set title=%s,description=%s where n_id=%s and added_by=%s',[utitle,
            udescription,nid,session.get('user')])
            mydb.commit()
            cursor.close()
            return redirect(url_for('viewnotes',nid=nid))

        return render_template('updatenotes.html',notesdata=notesdata)    
    else:
        flash('pls login first')
        return redirect(url_for('login'))    
    

    
@app.route('/deletenotes/<nid>')
def deletenotes(nid):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('delete from notes where n_id=%s and added_by=%s',[nid,session.get('user')])
        mydb.commit()
        flash(f'{nid} delete sucessfully')
        return redirect(url_for('viewallnotes')) 
    else:
            flash('pls login first')
            return redirect(url_for('login'))    
           
@app.route('/fileupload',methods=['GET','POST'])
def fileupload():
    if session.get('user'):
        if request.method=='POST':
            file_data=request.files['uploadfile']
            fdata=file_data.read()
            filename=file_data.filename
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into filedata(f_name,fdata,added_by) values(%s,%s,%s)',[filename,fdata,session.
            get('user')])
            mydb.commit()
            cursor.close()
            flash(f'{filename} added succesfully')
        return render_template('fileupload.html')
    else:
            flash('pls login first')
            return redirect(url_for('login'))    
        
@app.route('/viewfiles')
def viewfiles():
    if session.get('user'):
        cursor=mydb.cursor()
        cursor.execute('select f_id,f_name,create_at from filedata where added_by=%s',[session.get('user')])
        allfile_data=cursor.fetchall()
        return render_template('viewallfiles.html',allfile_data=allfile_data)  
    else:
            flash('pls login first')
            return redirect(url_for('login'))    
         
@app.route('/view_file/<fid>')
def view_file(fid):
    if session.get('user'):
        cursor=mydb.cursor()
        cursor.execute('select f_name,fdata from filedata where f_id=%s and added_by=%s',[fid,session.get('user')])
        file_info=cursor.fetchone()
        array_data=BytesIO(file_info[1])
        print(array_data)
        return send_file(array_data,as_attachment=False,download_name=file_info[0])
    else:
            flash('pls login first')
            return redirect(url_for('login'))    
       
@app.route('/download_file/<fid>')
def download_file(fid):
    if session.get('user'):
        cursor=mydb.cursor()
        cursor.execute('select f_name,fdata from filedata where f_id=%s and added_by=%s',[fid,session.get('user')])
        file_info=cursor.fetchone()
        array_data=BytesIO(file_info[1])
        print(array_data)
        return send_file(array_data,as_attachment=True,download_name=file_info[0])
    else:
            flash('pls login first')
            return redirect(url_for('login'))    
        
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    else:
        flash('pls login first')
        return redirect(url_for('login'))  
@app.route('/getexceldata') 
def getexceldata():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True) 
        cursor.execute('select * from notes where added_by=%s',[session.get('user')])
        notesdata=cursor.fetchall()
        data=[list(i) for i in notesdata]
        columns=['Notesid','Title','Description','created_at']
        data.insert(0,columns)
        return excel.make_response_from_array(data,'xlsx',filename='notesdata')
    else:
        flash('pls login first')
        return redirect(url_for('login'))           
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        searchdata=request.form['s_data']
        strg=['a-zA-Z0-9']
        pattern=re.compile(f'^{strg}',re.IGNORECASE)#defining pattern that can starts with small letters,capital letters or numbers user can type anything
        if pattern.match(searchdata):#checking that user given some value
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select * from notes where title like %s or description like %s or created_at like %s',
            [searchdata+'%',searchdata+'%',searchdata+'%'])
            sdata=cursor.fetchall()#fetching selected records
            return render_template('dashboard.html',sdata=sdata)  
        else:
            flash('pls give valid search')
            return redirect(url_for('dashboard'))    
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='POST':
        useremail=request.form['mail']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where useremail=%s',[useremail])
        email_count=cursor.fetchone()[0]
        if email_count==1:
            subject='reset link for SNM ap forgot password'
            body=f"click thelink reset password: {url_for('newpassword',data=entoken(useremail),_external=True)}"
            send_mail(to=useremail,subject=subject,body=body)
            flash(f'reset link hasbeen sent to given mail{useremail}')
            return redirect(url_for('forgotpassword'))
            
        elif email_count==0:
            flash('pls create account first')
            return redirect(url_for('register'))
        else:
            return 'something went wrong'        
    return render_template('forgotpwd.html')
@app.route('/newpassword/<data>',methods=['GET','POST'])
def newpassword(data):
    if request.method=='POST':
        newpassword=request.form['npwd']
        conpassword=request.form['cpwd']
        if newpassword==conpassword:
            useremail=dctoken(data)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('update users set password=%s where useremail=%s',
            [newpassword,useremail])
            mydb.commit()
            cursor.close()
            flash('password updates sucessfully')
            return redirect(url_for('login'))
        else:
            flash('password mismatch')    
            return redirect(url_for('newpassword',data=data))
    else:
        return render_template('newpassword.html')
app.run(debug=True,use_reloader=True)    