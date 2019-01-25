from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def list():
   con = sql.connect("flowers.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from FLOWERS")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/enternew')
def new_flower():
   con = sql.connect("flowers.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from FLOWERS")
   rows = cur.fetchall();

   return render_template('insertFlower.html', rows=rows)

@app.route('/flowerSight/', methods=['GET', 'POST'])
def flowerSight():

   commonName = request.form['COMNAME']
   con = sql.connect("flowers.db")
   con.row_factory = sql.Row

   
   cur = con.cursor()
   cur.execute("SELECT * FROM SIGHTINGS WHERE NAME = ?  order by SIGHTED desc LIMIT 10", (commonName,))
   
   rows = cur.fetchall();
   return render_template('recentSightings.html', rows=rows)

@app.route('/editFlower/', methods=['GET', 'POST'])
def editFlower():

   commonName = request.form['COMNAME']
   con = sql.connect("flowers.db")
   con.row_factory = sql.Row

   
   cur = con.cursor()
   cur.execute("SELECT * FROM FLOWERS WHERE COMNAME = ?", (commonName,))
   
   rows = cur.fetchall();
   return render_template('edit.html', rows=rows)

@app.route('/addrec/',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         fname = request.form['FNAME']
         pname = request.form['PNAME']
         l = request.form['LOCATION']
         s = request.form['SIGHTED']
         
         with sql.connect("flowers.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO SIGHTINGS (NAME,PERSON,LOCATION,SIGHTED) VALUES (?,?,?,?)",(fname,pname,l,s) )

            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()



@app.route('/update_entry/', methods = ['POST', 'GET'])
def update_entry():
   if request.method == 'POST':
      try:
         o = request.form['original']
         g = request.form['genus']
         s = request.form['species']
         c = request.form['cname']

         with sql.connect("flowers.db") as con:
             cur = con.cursor()
            
             cur.execute("UPDATE FLOWERS SET GENUS=?, SPECIES=?, COMNAME=? WHERE COMNAME = ?",(g,s,c,o))
             msg = "Successfully added"
             
      except:
         con.rollback()
         msg = "Error in the Addition"
      finally: 
         return render_template("result.html", msg=msg)
         con.close()


if __name__ == '__main__':
   app.run(debug = True)