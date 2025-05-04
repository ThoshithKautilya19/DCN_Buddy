from flask import Flask, redirect, url_for, request, Response, render_template, send_file
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote_plus
import os
from datetime import  datetime


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Don@sonu19'
app.config['MYSQL_DB'] = 'proj'

mysql = MySQL(app)

#db credentials for upload/import
# DEFINE THE DATABASE CREDENTIALS
user = 'root'
host = "localhost"
password = 'Don@sonu19'
encoded_password = quote_plus(password)
port = 3306  # Default MySQL port
database = 'proj'

#Function to set up connection bw sql and py
def get_connection():
    return create_engine(
        url=f"mysql+pymysql://root:{encoded_password}@localhost:3306/proj"
    
    )

@app.route('/', methods = ["POST", "GET"])
def home_page():
    return render_template("index.html")

@app.route('/access_page', methods=['POST'])
def access_page():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        print("pls")
        cursor = mysql.connection.cursor()
        

        cursor.execute(f"SELECT * FROM `employee_data` WHERE `Employee ID`='{username}' AND `Pass`='{password}'")

        data = cursor.fetchall()

        cursor.execute(f"SELECT `Circle` FROM `employee_data` WHERE `Employee ID`='{username}'")
        circle_tuple = cursor.fetchall()

        cursor.close()

        if len(data) > 0:
            circle = circle_tuple[0][0] if circle_tuple else None
            print(circle)  # Ensure circle is fetched correctly
            print(username)
            return render_template("add.html", user=username, circle=circle)
        else:
            return render_template("index.html", acc_info="Not Valid")

        
@app.route('/add', methods = ["POST", "GET"])
def add_row():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')

        return render_template("add.html", circle=circle, user=user)

@app.route('/del', methods = ["POST", "GET"])
def del_row():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("del.html", circle=circle, user=user )

@app.route('/modify', methods = ["POST", "GET"])
def modify_row():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("modify.html", circle=circle, user=user)

@app.route('/search', methods = ["POST", "GET"])
def search_row():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("search.html", circle=circle, user=user)
    
@app.route('/upload', methods = ["POST", "GET"])
def upload():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("upload.html", circle=circle, user=user)
    
@app.route('/export', methods = ["POST", "GET"])
def export():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("export.html", circle=circle, user=user)
    
@app.route('/logout', methods = ["POST", "GET"])
def logout():
    if request.method=='POST':
        return render_template("logout.html")
    
@app.route('/admin_access', methods = ["POST", "GET"])
def admin_page_redirection():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        
        cursor=mysql.connection.cursor()
        cursor.execute(f"select `Privilege` from `employee_data` where `Employee ID`={user}")

        privileges=list(cursor.fetchall())
        privilege=privileges[0][0]
        print(privilege)
        cursor.close()

        if privilege=="Admin":
            return render_template("admin_add.html", circle=circle, user=user )
        
        else:
            return render_template("error.html", error_msg="NOT AN ADMIN", circle=circle, user=user )

#within admin page
@app.route('/add_user', methods = ["POST", "GET"])
def admin_add_page():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("admin_add.html", circle=circle, user=user )

@app.route('/del_user', methods = ["POST", "GET"])
def admin_del_page():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("admin_del.html", circle=circle, user=user )
    
#Adding user
@app.route('/add_user_db', methods = ["POST", "GET"])
def user_add():
    if request.method=='POST':

        circle=request.form.get('circle')
        user=request.form.get('user')



        user_a=request.form['user_id']
        passw=request.form['user_pass']
        circ=request.form['user_circle']
        priv=request.form['user_privilege']

        print(user_a,passw,circ,priv)

        cursor=mysql.connection.cursor()
        cursor.execute(f"insert into `employee_data`(`Employee ID`, `Pass`, `Circle`, `Privilege`) values ('{user_a}', '{passw}', '{circ}', '{priv}')")
        mysql.connection.commit()
        cursor.close()

        return render_template("admin_add.html", circle=circle, user=user)

   #deleting users
@app.route('/del_user_db', methods = ["POST", "GET"])
def user_del():
    if request.method=='POST': 
        circle=request.form.get('circle')
        user=request.form.get('user')

        user_del=request.form['user_id']

        cursor=mysql.connection.cursor()
        cursor.execute(f"delete from `employeee_data` where `Employee_ID`='{user_del}'")
        mysql.connection.commit()
        cursor.close()

        return render_template("admin_del.html", circle=circle, user=user)






@app.route('/return_page', methods = ["POST", "GET"])
def admin_return():
    if request.method=='POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        return render_template("add.html", circle=circle, user=user )

@app.route('/re_access', methods = ["POST", "GET"])
def re_access():
    if request.method=='POST':
        return render_template("index.html")


    
    
# Addng data retrieved from the user

@app.route('/add_row', methods = ["POST", "GET"])
def adding_rows():
    if request.method == 'POST':
        data = {}
        columns =["`Circle`", "`Site NSS ID`","`MW Hop ID`","`MW Node ID`","`MW Node Name`","`VLAN`","`Node IP`","`Subnet Mask`","`GNE ID`","`GNE Name`","`GNE IP`","`GNE Subnet`","`MUX ID@GNE`","`MUX Name@GNE`","`MUX Port@GNE`","`MUX ID@Router`","`MUX Name@Router`","`MUX Port@Router`","`Main path Service ID`","`Protect path Service ID`","`Router host name`","`Router Loopback IP`","`Router Port`","`Router VLAN`","`Gateway IP`","`Gateway Subnet`","`Router VRF`","`Server Name`","`Server IP`","`Node Status`","`Updated Date/Time`","`User updated`"]
        vars=["Circle", "Site NSS ID","MW Hop ID","MW Node ID","MW Node Name","VLAN","Node IP","Subnet Mask","GNE ID","GNE Name","GNE IP","GNE Subnet","MUX ID@GNE","MUX Name@GNE","MUX Port@GNE","MUX ID@Router","MUX Name@Router","MUX Port@Router","Main path Service ID","Protect path Service ID","Router host name","Router Loopback IP","Router Port","Router VLAN","Gateway IP","Gateway Subnet","Router VRF","Server Name","Server IP","Node Status","Updated Date/Time","User updated"]

        for var_name in vars:
            data[var_name] = request.form.get(var_name)
        
        #auto circle mapping
        circle=request.form["circle"]
        data["Circle"]=circle
        print(circle)

        #auto date-time
        date_time=datetime.now()
        date_time = date_time.strftime("%d/%m/%Y, %H:%M:%S")
        data["Updated Date/Time"]=date_time

        #auto-user mapping
        user_updated=request.form['user']
        data["User updated"]=user_updated
        print(user_updated)


        req_data={}

        #Removing none values
        for i in range(len(vars)):
            if data[vars[i]]==None or data[vars[i]]=='':
                continue
            else:
                req_data[columns[i]]=data[vars[i]]
        
        
        q_list=[]

        for i in req_data.keys():
            q_list.append(f"{i}='{req_data[i]}'")
        
        vals=list(req_data.values())
        val_query=','.join(vals)
        val_query = ','.join([f"'{val}'" for val in vals])
        req_col=list(req_data.keys())
        req_col_query=','.join(list(req_data.keys()))


        cursor = mysql.connection.cursor()
        #validation of data

        uniq_cols=["Site NSS ID","MW Node ID","MW Node Name","Node IP","GNE IP","Gateway IP"]
        
        dup_cols=[]

        for col in uniq_cols:
            cursor.execute(f"select * from node_data where `Site NSS ID`='{data[col]}'")
            if len(cursor.fetchall())>0:
                dup_cols.append(col)
            else:
                continue
        
        if len(dup_cols)>0:
            msg=','.join(dup_cols)

            return render_template("error.html", error_msg=f"Duplicate values detected in columns: [{msg}]", circle=circle,user=user)
        
        else:

            print(f"insert into `node_data`({req_col_query}) values ({val_query})")
            cursor.execute(f"insert into `node_data`({req_col_query}) values ({val_query})")
            
            cursor.execute("select * from `node_data`")
            data1=cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return render_template("add.html", confirmation="YES, DATA RECEIVED AND ADDED", info=data1, circle=circle, user=user_updated)


#Add data using an excel file.
@app.route('/upload_file', methods = ["POST", "GET"])
def uploading_file():
    if request.method == 'POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
        
        upload_folder="D:/My_Website"
        app.config['upload_folder']=upload_folder

        import os
        from werkzeug.utils import secure_filename

        if 'file' not in request.files:
            return render_template('upload.html', msg='No')
        
        file=request.files['file']

        if file.filename=='':
            return render_template('upload.html', msg='No file sent', circle=circle, user=user)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_folder'], filename))

            try:
                # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
                engine = get_connection()
                df = pd.read_excel(f"{upload_folder}/{filename}")  # Use pd.read_excel() for Excel files
                df.to_sql('node_data', con=engine, if_exists='append', index=False)
                print(f"Connection to the MySQL server on {host} as user {user} created successfully.")
            except Exception as ex:
                print("Connection could not be made due to the following error: \n", ex)



            return render_template('upload.html', msg='File sent and received, and uploaded', circle=circle,user=user)
        
#Delete rows using the specific info given
@app.route('/del_row', methods = ["POST", "GET"])
def del_rows():
    if request.method == 'POST':
        circle=request.form.get('circle')
        user=request.form.get('user')
    
        data = {}
        columns =["`Circle`", "`Site NSS ID`","`MW Hop ID`","`MW Node ID`","`MW Node Name`","`VLAN`","`Node IP`","`Subnet Mask`","`GNE ID`","`GNE Name`","`GNE IP`","`GNE Subnet`","`MUX ID@GNE`","`MUX Name@GNE`","`MUX Port@GNE`","`MUX ID@Router`","`MUX Name@Router`","`MUX Port@Router`","`Main path Service ID`","`Protect path Service ID`","`Router host name`","`Router Loopback IP`","`Router Port`","`Router VLAN`","`Gateway IP`","`Gateway Subnet`","`Router VRF`","`Server Name`","`Server IP`","`Node Status`","`Updated Date/Time`","`User updated`"]
        vars=["Circle", "Site NSS ID","MW Hop ID","MW Node ID","MW Node Name","VLAN","Node IP","Subnet Mask","GNE ID","GNE Name","GNE IP","GNE Subnet","MUX ID@GNE","MUX Name@GNE","MUX Port@GNE","MUX ID@Router","MUX Name@Router","MUX Port@Router","Main path Service ID","Protect path Service ID","Router host name","Router Loopback IP","Router Port","Router VLAN","Gateway IP","Gateway Subnet","Router VRF","Server Name","Server IP","Node Status","Updated Date/Time","User updated"]

        for var_name in vars:
            data[var_name] = request.form.get(var_name)
        

        req_data={}

        #Removing none values
        for i in range(len(vars)):
            if data[vars[i]]==None or data[vars[i]]=='':
                continue
            else:
                req_data[columns[i]]=data[vars[i]]
        
        
        q_list=[]

        for i in req_data.keys():
            q_list.append(f"{i}='{req_data[i]}'")
        
        cursor=mysql.connection.cursor()

        cond=' and '.join(q_list)
        print(cond)
        print(f'select * from `node_data` where {cond}')

        if cond=='':
            return render_template("error.html", error_msg="No parameters filled")
        
        else:
            cursor.execute(f'select * from `node_data` where {cond}')

            data=cursor.fetchall()
            print(data)

            if len(data)>1:
                print("mass")
                return render_template('del_mass_result.html', del_dat=data, cols=vars, circle=circle, user=user)

            elif len(data)==0:
                return render_template("error.html", error_msg="No such records found", circle=circle, user=user)
            else:
                print("unique")
                return render_template('del_unique_result.html', item=data[0], cols=vars,circle=circle, user=user)

        

@app.route('/del_conf', methods = ["POST", "GET"])
def del_rows_CONF():
    if request.method == 'POST':

        circle=request.form.get('circle')
        user=request.form.get('user')

        node_id=request.form['node_id']
        print(node_id)

        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM node_data WHERE `Site NSS ID` = %s", (node_id,))
        print("DELETE FROM node_data WHERE `Site NSS ID` = %s", (node_id,))
        mysql.connection.commit()
        cursor.close()





        return render_template("del.html", conf_msg="Data successfully removed", circle=circle, user=user)


#searching
@app.route('/search_row', methods = ["POST", "GET"])
def sear_rows():
    if request.method == 'POST':

        circle=request.form.get('circle')
        user=request.form.get('user')
    
        data = {}
        columns =["`Circle`", "`Site NSS ID`","`MW Hop ID`","`MW Node ID`","`MW Node Name`","`VLAN`","`Node IP`","`Subnet Mask`","`GNE ID`","`GNE Name`","`GNE IP`","`GNE Subnet`","`MUX ID@GNE`","`MUX Name@GNE`","`MUX Port@GNE`","`MUX ID@Router`","`MUX Name@Router`","`MUX Port@Router`","`Main path Service ID`","`Protect path Service ID`","`Router host name`","`Router Loopback IP`","`Router Port`","`Router VLAN`","`Gateway IP`","`Gateway Subnet`","`Router VRF`","`Server Name`","`Server IP`","`Node Status`","`Updated Date/Time`","`User updated`"]
        vars=["Circle", "Site NSS ID","MW Hop ID","MW Node ID","MW Node Name","VLAN","Node IP","Subnet Mask","GNE ID","GNE Name","GNE IP","GNE Subnet","MUX ID@GNE","MUX Name@GNE","MUX Port@GNE","MUX ID@Router","MUX Name@Router","MUX Port@Router","Main path Service ID","Protect path Service ID","Router host name","Router Loopback IP","Router Port","Router VLAN","Gateway IP","Gateway Subnet","Router VRF","Server Name","Server IP","Node Status","Updated Date/Time","User updated"]

        for var_name in vars:
            data[var_name] = request.form.get(var_name)
        

        req_data={}

        #Removing none values
        for i in range(len(vars)):
            if data[vars[i]]==None or data[vars[i]]=='':
                continue
            else:
                req_data[columns[i]]=data[vars[i]]
        
        
        q_list=[]

        for i in req_data.keys():
            q_list.append(f"{i}='{req_data[i]}'")
        
        cursor=mysql.connection.cursor()

        cond=' and '.join(q_list)
        print(cond)
        print(f'select * from `node_data` where {cond}')
        cursor.execute(f'select * from `node_data` where {cond}')

        data=cursor.fetchall()

        if len(data)>1:
            print("mass")
            return render_template('search_mass_result.html', del_dat=data, cols=vars, circle=circle, user=user)

        elif len(data)==0:
            print("None")
            return render_template('error.html',  error_msg="No such records found",circle=circle, user=user)

        else:
            print("unique")
            return render_template('search_result.html', item=data[0], cols=vars,circle=circle, user=user)


#Exporting csv  files

@app.route('/export_db', methods = ["POST", "GET"])
def exp():
    if request.method == 'POST':
        circle=request.form.get('circle')
        user=request.form.get('user')

    
        data = {}
        columns =["`Circle`", "`Site NSS ID`","`MW Hop ID`","`MW Node ID`","`MW Node Name`","`VLAN`","`Node IP`","`Subnet Mask`","`GNE ID`","`GNE Name`","`GNE IP`","`GNE Subnet`","`MUX ID@GNE`","`MUX Name@GNE`","`MUX Port@GNE`","`MUX ID@Router`","`MUX Name@Router`","`MUX Port@Router`","`Main path Service ID`","`Protect path Service ID`","`Router host name`","`Router Loopback IP`","`Router Port`","`Router VLAN`","`Gateway IP`","`Gateway Subnet`","`Router VRF`","`Server Name`","`Server IP`","`Node Status`","`Updated Date/Time`","`User updated`"]
        vars=["Circle", "Site NSS ID","MW Hop ID","MW Node ID","MW Node Name","VLAN","Node IP","Subnet Mask","GNE ID","GNE Name","GNE IP","GNE Subnet","MUX ID@GNE","MUX Name@GNE","MUX Port@GNE","MUX ID@Router","MUX Name@Router","MUX Port@Router","Main path Service ID","Protect path Service ID","Router host name","Router Loopback IP","Router Port","Router VLAN","Gateway IP","Gateway Subnet","Router VRF","Server Name","Server IP","Node Status","Updated Date/Time","User updated"]

        for var_name in vars:
            data[var_name] = request.form.get(var_name)
        

        req_data={}

        #Removing none values
        for i in range(len(vars)):
            if data[vars[i]]==None or data[vars[i]]=='':
                continue
            else:
                req_data[columns[i]]=data[vars[i]]
        
        
        q_list=[]

        for i in req_data.keys():
            q_list.append(f"{i}='{req_data[i]}'")
        
        cursor=mysql.connection.cursor()

        cond=' and '.join(q_list)
        print(cond)

        if cond=='':
            return render_template("export.html", circle=circle, user=user)
        
        else:

            print(f'select * from `node_data` where {cond}')
            cursor.execute(f'select * from `node_data` where {cond}')


            data=cursor.fetchall()
            print(request.form.get('circle'))


            # if request.form.get('all_circle')!="all":
            #     circle=request.form['circle']
            #     user=request.form['user']
            #     cursor=mysql.connection.cursor()
            #     cursor.execute(f"select * from `node_data` where `Circle`='{circle}'")
            #     data=cursor.fetchall()
                
            
            # else:
            #     cursor=mysql.connection.cursor()
            #     cursor.execute("select * from `node_data`")
            #     data=cursor.fetchall()

            
            df=pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

            cursor.close()
            ex_fil='dcnb.xlsx'
            upload_folder="D:/My_Website"
            df.to_excel(f"{upload_folder}/{ex_fil}", index=False)

            ret_val=send_file(f"{upload_folder}/{ex_fil}", as_attachment=True)

            return ret_val
    

@app.route('/mod_search', methods = ["POST", "GET"])
def mod_search():
    if request.method == 'POST':
        if "search_nss_id" in request.form:
            circle=request.form.get('circle')
            user=request.form.get('user')   
            print("nss")
            nss_id=request.form["search_nss_id"]
            
            cursor=mysql.connection.cursor()

            cursor.execute(f"select * from `node_data` where `Site NSS ID`='{nss_id}'")

            data=cursor.fetchall()

            cursor.close()

            if len(data)==0:
                print("None")
                return render_template('error.html',  error_msg="No such records found",circle=circle, user=user)

            else:
                return render_template("modify_nss.html", item=data[0], circle=circle, user=user)
        
        if "search_name" in request.form:
            circle=request.form.get('circle')
            user=request.form.get('user')   
            print("name")
            node_name=request.form["search_name"]
            
            cursor=mysql.connection.cursor()

            cursor.execute(f"select * from `node_data` where `MW Node Name`='{node_name}'")

            data=cursor.fetchall()

            cursor.close()

            if len(data)==0:
                print("None")
                return render_template('error.html',  error_msg="No such records found",circle=circle, user=user)

            else:

                return render_template("modify_name.html", item=data[0], circle=circle, user=user)
        



@app.route('/modify_rows', methods = ["POST", "GET"])
def mod_rows():
    if request.method == 'POST':

        circle=request.form.get('circle')
        user=request.form.get('user')
           
        data = {}
        columns =["`Circle`", "`Site NSS ID`","`MW Hop ID`","`MW Node ID`","`MW Node Name`","`VLAN`","`Node IP`","`Subnet Mask`","`GNE ID`","`GNE Name`","`GNE IP`","`GNE Subnet`","`MUX ID@GNE`","`MUX Name@GNE`","`MUX Port@GNE`","`MUX ID@Router`","`MUX Name@Router`","`MUX Port@Router`","`Main path Service ID`","`Protect path Service ID`","`Router host name`","`Router Loopback IP`","`Router Port`","`Router VLAN`","`Gateway IP`","`Gateway Subnet`","`Router VRF`","`Server Name`","`Server IP`","`Node Status`","`Updated Date/Time`","`User updated`"]
        vars=["Circle", "Site NSS ID","MW Hop ID","MW Node ID","MW Node Name","VLAN","Node IP","Subnet Mask","GNE ID","GNE Name","GNE IP","GNE Subnet","MUX ID@GNE","MUX Name@GNE","MUX Port@GNE","MUX ID@Router","MUX Name@Router","MUX Port@Router","Main path Service ID","Protect path Service ID","Router host name","Router Loopback IP","Router Port","Router VLAN","Gateway IP","Gateway Subnet","Router VRF","Server Name","Server IP","Node Status","Updated Date/Time","User updated"]

        for var_name in vars:
            data[var_name] = request.form.get(var_name)
        

        req_data={}

        #Removing none values
        for i in range(len(vars)):
            if data[vars[i]]==None or data[vars[i]]=='':
                continue
            else:
                req_data[columns[i]]=data[vars[i]]
        
        
        q_list=[]

        for i in req_data.keys():
            q_list.append(f"{i}='{req_data[i]}'")

        cond=','.join(q_list)
        print(cond)
        table="node_data"
        nss_id=request.form["nss"]
        print(nss_id)

        if cond=='':
            return render_template("modify.html", circle=circle, user=user)
        
        else:

            cursor=mysql.connection.cursor()
            cursor.execute("SET SQL_SAFE_UPDATES=0")
            cursor.execute(f"update `{table}` set {cond} where `Site NSS ID`='{nss_id}'")
            print(f"update `{table}` set {cond} where `Site NSS ID`='{nss_id}'")


            mysql.connection.commit()
            cursor.close()

            return render_template("modify.html", circle=circle, user=user)
    

        









if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug = True) 
