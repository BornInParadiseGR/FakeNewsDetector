#!/usr/bin/env python
# coding: utf-8

# In[33]:


import mysql.connector
from datetime import datetime
# βιβλιοθήκες για καθυστέρηεη στην "ψεύτικη ανάλυση" και τυχαίο true ή false Στο fake
import random
import time


# In[57]:


# Σύνδεση με τη βάση
def connect():
    conn = mysql.connector.connect(
        host="db",
        user="wordpress",
        password="wordpress",
        database="wordpress",
        port = 3306
        )
    return conn
# Δημιουργία βάσης
def createDB(cursor):
    cursor.execute("USE wordpress")
# Δημιουργία πινάκων
def createTables(cursor):
    # cursor.execute("CREATE TABLE user "+
    #                  "(id INT AUTO_INCREMENT PRIMARY KEY, "+
    #                  "email VARCHAR(255),"+
    #                  "password VARCHAR(255),"+
    #                  "fullName VARCHAR(255))")
    cursor.execute("CREATE TABLE NewsArticle "+
                     "(id INT AUTO_INCREMENT PRIMARY KEY, "+
                     "userid BIGINT unsigned,"+
                     "title VARCHAR(255),"+
                     "content text,"+
                     "date VARCHAR(255))")
    cursor.execute("CREATE TABLE AnalyzeArticle "+
                     "(id INT AUTO_INCREMENT PRIMARY KEY, "+
                     "userid BIGINT unsigned,"+
                     "starttime TIMESTAMP,"+
                     "endtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"+
                     "status TINYINT(1))")
    cursor.execute("CREATE TABLE AnalysisResult "+
                     "(id INT AUTO_INCREMENT PRIMARY KEY, "+
                     "articleid INT,"+
                     "analysisid INT,"+
                     "isFake VARCHAR(50))")
    # Ξένα κλειδιά
    cursor.execute("ALTER TABLE AnalyzeArticle ADD FOREIGN KEY (userid) REFERENCES wp_users(ID)")
    cursor.execute("ALTER TABLE NewsArticle ADD FOREIGN KEY (userid) REFERENCES wp_users(ID)")
    cursor.execute("ALTER TABLE AnalysisResult ADD FOREIGN KEY (articleid) REFERENCES NewsArticle(id) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE AnalysisResult ADD FOREIGN KEY (analysisid) REFERENCES AnalyzeArticle(id) ON DELETE CASCADE;")

    
# εισαγωγή χρηστών για δοκιμές
# def populateUsers(conn,cursor):
#     sql = "INSERT INTO user (email, password, fullName) VALUES (%s, %s, %s)"
#     val = ("test1@gmail.com","test1","tt")
#     cursor.execute(sql, val)
#     conn.commit()
#     sql = "INSERT INTO user (email, password, fullName) VALUES (%s, %s, %s)"
#     val = ("test2@gmail.com","test1","tt")
#     cursor.execute(sql, val)
#     conn.commit()
# εισαγωγή άρθρων για δοκιμές
def populateArticles(conn,cursor,user,title,content,date):
    sql = "INSERT INTO NewsArticle (userid, title, content, date) VALUES (%s, %s, %s, %s)"
    val = (user, title,content,date)
    cursor.execute(sql, val)
    conn.commit()
    return cursor.lastrowid
    # sql = "INSERT INTO NewsArticle (userid, title, content) VALUES (%s, %s, %s)"
    # val = ("1", "title 2","content of title2")
    # cursor.execute(sql, val)
    # conn.commit()
    # sql = "INSERT INTO NewsArticle (userid, title, content) VALUES (%s, %s, %s)"
    # val = ("2", "title 3","content of title3")
    # cursor.execute(sql, val)
    # conn.commit()
def selectAnalyzeArticle(conn,cursor,userID):
    sql = """SELECT * FROM AnalyzeArticle WHERE userid=%s"""
    cursor.execute(sql, userID)
    results = cursor.fetchall()
    res = []
    for row in results:
        analysisid = row[0]
        userid = row[1]
        starttime = row[2]
        endtime = row[3]
        status = row[4]
        analysis = {
            "analysisId": analysisid,
            "startTime": starttime,
            "endTime": endtime,
            "status": status,
        }
        res.append(analysis)
    return res

def selectNewsArticleAnalysis(conn, cursor, userID, analysisID):
    # # Check if analysis belongs to user
    # sql_analysis = """SELECT AnalyzeArticle.userid FROM AnalyzeArticle WHERE AnalyzeArticle.id=%s"""
    # cursor.execute(sql_analysis, (analysisID,))
    # resultid = cursor.fetchone()[0]
    # if resultid != userID:
    #     return

    articlesRes = []
    # Get all article ids of analysis
    sql_article_ids = """SELECT AnalysisResult.articleid,AnalysisResult.isFake,NewsArticle.title,NewsArticle.content,NewsArticle.date
      FROM AnalysisResult,NewsArticle WHERE AnalysisResult.articleid=NewsArticle.id AND analysisid=%s"""
    cursor.execute(sql_article_ids, (analysisID,))
    results = cursor.fetchall()
    for row in results:
        short_content = "N/A"
        if not row[3] is None:
            short_content = str(row[3].decode())[:50]
            #short_content = str(row[3].decode())[:150]

        date = "N/A"
        if not row[4] is None:
            date = str(row[4].decode())

        title = "N/A"
        if not row[2] is None:
            title = str(row[2].decode())
        
        articlesRes.append(
            {
                "articleId": row[0],
                "isFake": row[1].decode(),
                "title": title,
                "content": short_content,
                "date": date
            }
        )
    return articlesRes

def selectArticleContent(conn, cursor, articleId):
    sql = """SELECT content FROM NewsArticle WHERE id=%s"""
    cursor.execute(sql, (articleId,))
    results = cursor.fetchall()
    row = results[0]
    content = str(row[0].decode())
    return content

# αναζήτηση άρθρου με βάση το όνομα
def selectArticleTitle(conn,cursor,q):
    cursor.execute("SELECT * FROM NewsArticle WHERE title like '%"+q+"%'")
    results = cursor.fetchall()
    found = False
    for row in results:
        found = True
        print(row)
    if not found:
        print ("No article with " + q + " in title")
# αναζήτηση άρθρου με βάση την ημερομηνία
def selectArticleDate(conn,cursor,datefrom,dateto):
    #timestampfrom = int(datefrom.timestamp())
    #timestampto = int(dateto.timestamp())
    fromdatestr = datefrom.strftime("%Y-%m-%d %H:%M:%S")
    todatestr = dateto.strftime("%Y-%m-%d %H:%M:%S")
    #print(str(timestampfrom)+"-"+str(timestampto))
    cursor.execute("SELECT * FROM NewsArticle WHERE inputdate BETWEEN %s AND %s", (fromdatestr, todatestr))
    
    results = cursor.fetchall()
    found = False
    for row in results:
        found = True
        print(row)
    if not found:
        print ("No article between days "+datefrom.strftime("%d-%m-%Y")+" - "+dateto.strftime("%d-%m-%Y"))
def selectAnalysis(conn,cursor,userid,articleID):
    cursor.execute("SELECT AnalysisResult.id AS ResultID, "+
                   "NewsArticle.title AS ArticleTitle, AnalysisResult.isFake AS IsFake "+
                   "FROM AnalysisResult "+
                   "INNER JOIN NewsArticle ON AnalysisResult.articleid = NewsArticle.id "+
                   "WHERE NewsArticle.id ="+articleID+";")
    results = cursor.fetchall()
    found = False
    for row in results:
        found = True
        print(row)
    if not found:
        print ("No analysis for article with id "+articleID)
# Διαγραφή άρθρου
def deleteArticle(conn,cursor,userid,id):
    # πρέπει να ελεγχθεί αν το id είναι του χρήστη που είναι logged in και υπάρχει και το id του άρθρου
    cursor.execute("SELECT * FROM NewsArticle WHERE userid='"+str(userid)+"' and id='"+str(id)+"'")
    results = cursor.fetchall()
    num_rows = cursor.rowcount
    if num_rows==0:
        return False
    else:
        # διαγραφή όλων των αναλύσεων που αφορούν το άρθρο σύμφωνα με τον πίνακα AnalysisResult
        cursor.execute("SELECT * FROM AnalysisResult WHERE articleid = '"+str(id)+"'")
        results = cursor.fetchall()
        for row in results:
            analysisid = row[2]
            cursor.execute("DELETE FROM AnalyzeArticle WHERE id = '"+str(analysisid)+"'")
            conn.commit()
        cursor.execute("DELETE FROM NewsArticle WHERE id = '"+str(id)+"'")
        conn.commit()
        
        
        return True
# Διαγραφή ανάλυσης
def deleteAnalysis(conn,cursor,userid,id):
    # πρέπει να ελεγχθεί αν το id είναι του χρήστη που είναι logged in και υπάρχει και το id της ανάλυσης
    cursor.execute("SELECT * FROM AnalyzeArticle WHERE userid='"+str(userid)+"' and id='"+str(id)+"'")
    results = cursor.fetchall()
    num_rows = cursor.rowcount
    if num_rows==0:
        return False
    else:
        cursor.execute("DELETE FROM AnalyzeArticle WHERE id = '"+str(id)+"'")
        conn.commit()
        return True

def deleteCompleteAnalysis(conn, cursor, analysisid):
    # find analysis article IDs
    sql_find_articles = """SELECT articleid FROM AnalysisResult WHERE analysisid=%s"""
    cursor.execute(sql_find_articles, (analysisid,))
    rows = cursor.fetchall()
    if cursor.rowcount == 0:
        return
    for row in rows:
        articleid = row[0]

        # DELETE from AnalysisResult
        sql_delete_result = """DELETE FROM AnalysisResult WHERE articleid=%s"""
        cursor.execute(sql_delete_result, (articleid,))

        # DELETE from NewsArticle
        sql_delete_article = """DELETE FROM NewsArticle WHERE id=%s"""
        cursor.execute(sql_delete_article, (articleid,))

    # DELETE from AnalyzeArticle
    sql_delete_analysis = """DELETE FROM AnalyzeArticle WHERE id=%s"""
    cursor.execute(sql_delete_analysis, (analysisid,))

    conn.commit()

def analysis(conn,cursor,userid,articleids,starttime,endtime,status,isFakes):
    if isinstance(articleids, int):
        analysisSingle(conn,cursor,userid,articleids,starttime,endtime,status,isFakes)
        return

    for articleid in articleids:
        # έλεγχος αν υπάρχει το άρθρο με articleid
        cursor.execute("SELECT COUNT(*) FROM NewsArticle WHERE id= '"+str(articleid)+"'")
        rows = cursor.fetchone()[0]
        if rows==0:
            return False;
    
    sql = "INSERT INTO AnalyzeArticle (userid,starttime,endtime,status) VALUES (%s, %s, %s, %s)"
    val = (str(userid),str(starttime),str(endtime),str(status))
    cursor.execute(sql, val)
    conn.commit()
    analysisid = cursor.lastrowid

    for articleid in articleids:
        sql = "INSERT INTO AnalysisResult (articleid,analysisid,isFake) VALUES (%s, %s, %s)"
        val = (str(articleid),str(analysisid),str(isFakes[articleid]))
        cursor.execute(sql, val)
        conn.commit()

def analysisSingle(conn,cursor,userid,articleid,starttime,endtime,status,isFake):
    # έλεγχος αν υπάρχει το άρθρο με articleid
    cursor.execute("SELECT COUNT(*) FROM NewsArticle WHERE id= '"+str(articleid)+"'")
    rows = cursor.fetchone()[0]
    if rows==0:
        return False;

    sql = "INSERT INTO AnalyzeArticle (userid,starttime,endtime,status) VALUES (%s, %s, %s, %s)"
    val = (str(userid),str(starttime),str(endtime),str(status))
    cursor.execute(sql, val)
    conn.commit()
    analysisid = cursor.lastrowid
    sql = "INSERT INTO AnalysisResult (articleid,analysisid,isFake) VALUES (%s, %s, %s)"
    val = (str(articleid),str(analysisid),str(isFake))
    cursor.execute(sql, val)
    conn.commit()



# In[40]:


#createDB(cursor)
#conn = connect()
#cursor = conn.cursor()
# Βγάζω από σχόλια μόνο για δημιουργία πινάκων και πληθύσμωση τους αρχικά
#createTables(cursor)
#populateUsers(conn,cursor)
#populateArticles(conn,cursor)

# έστω συνδεδεμένος ο 1
# userid = 1
# while True:
#     print('1. Αναζήτηση άρθρου')
#     print('2. Ανάλυση άρθρου')
#     print('3. Εμφάνιση Αναλύσεων')
#     print('4. Διαγραφή Άρθρου')
#     print('5. Διαγραφή Ανάλυσης')
#     print('6. Έξοδος')
#     try:
#         choice = int(input('Δώσε επιλογή:'))
#         if choice==1:
#             inp = input('Δώσε μέρος του τίτλου άρθρου (κενό για εμφάνιση όλων):')
#             selectArticleDate(conn,cursor,inp)
#         elif choice==2:
#             articleid = int(input('Δώσε id άρθρου προς ανάλυση:'))
#             if analysis(conn,cursor,userid,articleid):
#                 print('Επιτυχής Ανάλυση')
#             else:
#                 print('Ανεπιτυχής Ανάλυση')
#         elif choice==3:
#             inp = input('Δώσε άρθρο για Εμφάνιση αναλύσεων:')
#             selectAnalysis(conn,cursor,userid,inp)
#         elif choice==4:
#             id = int(input('Δώσε id άρθρου προς διαγραφή:'))
#             if deleteArticle(conn,cursor,userid,id):
#                 print ('Επιτυχής διαγραφή')
#             else:
#                 print ('Δεν διαγράφηκε κάποιο στοιχείο')
#         elif choice==5:
#             id = int(input('Δώσε id ανάλυσης προς διαγραφή:'))
#             if deleteAnalysis(conn,cursor,userid,id):
#                 print ('Επιτυχής διαγραφή')
#             else:
#                 print ('Δεν διαγράφηκε κάποιο στοιχείο')
#         elif choice==6:
#             break
#     except ValueError:
#         print("Παρακαλώ εισαγάγετε αριθμό.")

# # Κλείσιμο cursor και connection
# cursor.close()


# In[ ]:
