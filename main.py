from flask import Flask, render_template, request
import requests
#import cgi, cgitbuu
import json
import APICalls as tmdb
import psycopg2 as db

try:
    connection = db.connect(user = "postgres",
                                  password = "password",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")
    cursor = connection.cursor()

    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    '''
    cursor.execute("select * from userdata;")
    record = cursor.fetchone()
    print("Records : ", record,"\n")
    record = cursor.fetchone()
    print("Records : ", record,"\n")

    '''
    #app = Flask(__name__)

    
except (Exception, db.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

'''    
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
'''


app = Flask(__name__)           

@app.route("/")
def home():
    
    ids=[]
    j=0
    k=0
    l=0
    moviesR=[]
    moviesT=[]
    moviesF=[]
    movies = []
    ids = tmdb.getRecommend()
    for i in ids: 
        
        mTitle=tmdb.getTitle(i)
        #print(mTitle)
        mDescr=tmdb.getOverview(i)
        mPoster=tmdb.getPosterPath(i)
        mUrl=tmdb.getURL(i)
        mRat=tmdb.getRatings(i)
        movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
        moviesR.append(movie)
        j=j+1
        if(j>3):
            break
    
    ids = tmdb.getTrending()
    for i in ids: 
        
        mTitle=tmdb.getTitle(i)
        #print(mTitle)
        mDescr=tmdb.getOverview(i)
        mPoster=tmdb.getPosterPath(i)
        mUrl=tmdb.getURL(i)
        mRat=tmdb.getRatings(i)
        movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
        moviesT.append(movie)
        k=k+1
        if(k>3):
            break
        
    ids = tmdb.getUpcoming()
    for i in ids: 
        
        mTitle=tmdb.getTitle(i)
        #print(mTitle)
        mDescr=tmdb.getOverview(i)
        mPoster=tmdb.getPosterPath(i)
        mUrl=tmdb.getURL(i)
        mRat=tmdb.getRatings(i)
        movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
        moviesF.append(movie)
        l=l+1
        if(l>3):
            break    
        
         
    movies.append(moviesT)
    movies.append(moviesR)
    movies.append(moviesF)
    
    return render_template('welcome.html', response=movies)

  
@app.route('/search',methods=['POST','GET']) 
def search():
    if(request.method=='POST'):
        title=request.form['search']
    else:
        title=request.args.get('search')
    '''print("blabla")
    print(title)
    print("blabla")
    '''
    ids=[]
    movies=[]  
    ids=tmdb.getIdsfromQuery(title)
    for i in ids: 
        
        mTitle=tmdb.getTitle(i)
        print(mTitle)
        mDescr=tmdb.getOverview(i)
        mPoster=tmdb.getPosterPath(i)
        mUrl=tmdb.getURL(i)
        mRat=tmdb.getRatings(i)
        movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
        movies.append(movie)

    return render_template('search.html', response=movies)



@app.route("/getregpage") 
def getregpage():
    return render_template('register.html')

@app.route("/register",methods=['POST','GET']) 
def register():
    if(request.method=='POST'):
        undata=request.form['uname']
        pwddata=request.form['pwd']
        edata=request.form['mail']
    else:
        undata=request.args.get('uname')
        pwddata=request.args.get('pwd')
        edata=request.args.get('mail')

    #print(undata,pwddata,edata)
    
    try:
        insert_udata_query = """ INSERT INTO userdata (username, email, password) VALUES (%s,%s,%s)"""
        #insert_mdata_query = """ INSERT INTO moviedata (username, movielist) VALUES (%s,%s)"""
        urecord_to_insert = (undata,pwddata,edata)
        cursor.execute(insert_udata_query, urecord_to_insert)
        connection.commit()

        '''
        record = cursor.fetchone()
        print("Records : ", record,"\n")
        record = cursor.fetchone()
        print("Records : ", record,"\n")
        '''

    except (Exception, db.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return render_template('userlogin.html')




@app.route("/getloginpage")

def getloginpage():
    return render_template('userlogin.html')
    

@app.route("/login", methods=['POST','GET'])
def login():
    print("inside login \n")
    authenticate=0
    if(request.method=='POST'):
        undata=request.form['uname']
        pwddata=request.form['pwd']
        
    else:
        undata=request.args.get('uname')
        pwddata=request.args.get('pwd')
        
    print(undata,pwddata)
    
    try:
        select_udata_query = """ select * from userdata where username=%s and password=%s"""
        #insert_mdata_query = """ INSERT INTO moviedata (username, movielist) VALUES (%s,%s)"""
        condition_fields=(undata,pwddata)
        cursor.execute(select_udata_query,condition_fields)
        usermatch = cursor.fetchall()

        if(len(usermatch) == 1):
            authenticate = 1

    except (Exception, db.Error) as error :
        print ("Error while fetching in PostgreSQL", error)
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    if(authenticate==1):
        ids=[]
        j=0
        k=0
        l=0
        moviesR=[]
        moviesT=[]
        moviesF=[]
        movies = []

        select_mdata_query = """ select movielist from moviedata where username=%s"""
        condition_fields=(undata)
        cursor.execute(select_mdata_query,[undata])
        m_id_match = cursor.fetchall()
        if(len(m_id_match)>0):
            ids = tmdb.getRecommend(int(m_id_match[0]))
        else:
            ids = tmdb.getRecommend()
        for i in ids: 
               
            mTitle=tmdb.getTitle(i)
            #print(mTitle)
            mDescr=tmdb.getOverview(i)
            mPoster=tmdb.getPosterPath(i)
            mUrl=tmdb.getURL(i)
            mRat=tmdb.getRatings(i)
            movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
            moviesR.append(movie)
            j=j+1
            if(j>3):
                break
            
        ids = tmdb.getTrending()
        for i in ids: 
            
            mTitle=tmdb.getTitle(i)
            #print(mTitle)
            mDescr=tmdb.getOverview(i)
            mPoster=tmdb.getPosterPath(i)
            mUrl=tmdb.getURL(i)
            mRat=tmdb.getRatings(i)
            movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
            moviesT.append(movie)
            k=k+1
            if(k>3):
                break
            
        ids = tmdb.getUpcoming()
        for i in ids: 
            
            mTitle=tmdb.getTitle(i)
            #print(mTitle)
            mDescr=tmdb.getOverview(i)
            mPoster=tmdb.getPosterPath(i)
            mUrl=tmdb.getURL(i)
            mRat=tmdb.getRatings(i)
            movie={"Title": mTitle, "Info": mDescr, "Poster": mPoster, "Url": mUrl, "Rating": mRat}
            moviesF.append(movie)
            l=l+1
            if(l>3):
                break    
            
         
        movies.append(moviesT)
        movies.append(moviesR)
        movies.append(moviesF)
        

        return render_template('welcome.html',response=movies)
    else:
        return render_template('userlogin.html')

    '''
    """
    j=0
    trending=[[]]
    for i in tmdb.getTrending():
        trending.append(tmdb.getTitle(i), tmdb.getPosterPath(i))
        j=j+1
        if(j>3):
            break
    
 
        
    upcoming=[[]]
    j=0
    for i in tmdb.getUpcoming():
        upcoming.append(tmdb.getTitle(i), tmdb.getPosterPath(i))
        j=j+1
        if(j>3):
            break
        
    
        
    recommendation=[[]]
    j=0
    for i in tmdb.getRecommendation():
        recommendation.append(tmdb.getTitle(i), tmdb.getPosterPath(i))
        j=j+1
        if(j>3):
            break
        
    
    """
    '''
    response = requests.get('http://www.omdbapi.com/?apikey=aa44e6ff&t=blade')
    response = response.json()
    response = json.dumps(rating, sort_keys = True, indent = 40)
    #response = response.replace(",","***********\n")
    return render_template('welcome.html', response=final)



if __name__ == "__main__":
    app.run(debug=True)            
