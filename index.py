import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import re
import string
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from flask import Flask, request, jsonify, render_template, Response
import requests
from bs4 import BeautifulSoup
import re
from flask_cors import CORS, cross_origin
import pickle
import time
from datetime import datetime
import db
from db import populateArticles, connect, selectAnalyzeArticle, selectNewsArticleAnalysis, deleteCompleteAnalysis, selectArticleContent



pd.options.mode.chained_assignment = None  # default='warn

df_fake = pd.read_csv("Fake.csv")
df_true = pd.read_csv("True.csv")


df_fake["class"] = 0
df_true["class"] = 1

df_fake.shape, df_true.shape


df_merge = pd.concat([df_fake, df_true], axis =0 )


df = df_merge.drop(["title", "subject","date"], axis = 1)



df = df.sample(frac = 1)  #mix data



df.reset_index(inplace = True)
df.drop(["index"], axis = 1, inplace = True)




# Creating a function to process the texts
# takes out point capitals and more things

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

df["text"] = df["text"].apply(wordopt)


x = df["text"]
y = df["class"]

# we now split the text, with 25 percent of dataset to test and 75 to train
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)


#lets vectorize the text
vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)


# dt_pkl_victorized = "victorizer.pkl"
# with open(dt_pkl_victorized,"wb") as dt_pkl_victor:
#     pickle.dump(vectorization, dt_pkl_victor)



# dt_pkl_victor = open(dt_pkl_victorized,"rb")
# vectorization = pickle.load(dt_pkl_victor)


#lets deploy a machine learning classifier
DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)
   
# dt_pkl_filename = "trained_classifier.pkl"
# with open(dt_pkl_filename,"wb") as dt_pkl_file:
#     pickle.dump(DT, dt_pkl_file)

# dt_pkl_file = open(dt_pkl_filename,"rb")
# DT = pickle.load(dt_pkl_file)

pred_dt = DT.predict(xv_test)

DT.score(xv_test, y_test)


# -----------------------------------------------------------------------

# lets create some manual testing

# Removing last 10 rows for manual testing
df_fake_manual_testing = df_fake.tail(10)
for i in range(23480,23470,-1):
    df_fake.drop([i], axis = 0, inplace = True)

df_true_manual_testing = df_true.tail(10)
for i in range(21416,21406,-1):
    df_true.drop([i], axis = 0, inplace = True)

df_fake_manual_testing["class"] = 0
df_true_manual_testing["class"] = 1

df_fake_manual_testing.head(10)
df_true_manual_testing.head(10)

df_manual_testing = pd.concat([df_fake_manual_testing,df_true_manual_testing], axis = 0)

df_manual_testing.to_csv("manual_testing.csv")

df_manual_testing = df_manual_testing.drop(["class"], axis = 1)



#results of the test
# ---------------------------------------------------------

# lets create some functions that will help us determine the actual
# test of the model we created



def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"

import validators
app = Flask(__name__)
CORS(app)
@app.route('/dataForm', methods=['GET','POST'])
def dataForm():
    try:
        json_data = request.get_json()
        userid = json_data['user_id']
        content=json_data['data']
        title = json_data["title"]
        date = json_data["date"]
        # Process the received JSON data here
        # For example, you can print it to the console
        #print("Received JSON data:", json_data)
        y = str(json_data)
        
        #data = extract_publication_date_data(str(y))
        conn = db.connect()
        cursor = conn.cursor()
        
        
        #content = data["Body"]
        #date = data["Date"]
        print("id:",userid,"\nTitle:",title,"\nContent",content,"\nDate:",date)
        if userid != 0:
            articleid = populateArticles(conn,cursor,userid,title,content,date)
            
        starttime = datetime.now()
        if json_data is not None:
            testing_news = {"text":[y]}
            new_def_test = pd.DataFrame(testing_news)
            new_def_test["text"] = new_def_test["text"].apply(wordopt)
            new_x_test = new_def_test["text"]
            new_xv_test = vectorization.transform(new_x_test)
            pred_DT = DT.predict(new_xv_test)
            print(output_lable(pred_DT[0]))
            result = "\n DT Prediction: {}".format(output_lable(pred_DT[0]))
            isFake = output_lable(pred_DT[0])
            endtime = datetime.now()
            status = 1
            if userid != 0:
                db.analysis(conn,cursor,userid,articleid,starttime,endtime,status,isFake)
    
            
            return jsonify(result)
        
           # return render_template('frontend.html', result="\n DT Prediction: {}".format(output_lable(pred_DT[0])))

        return jsonify({"message": "Data received successfully."}), 200
    except Exception as e:
        return jsonify({"error": "Failed to process data.", "details": str(e)}), 400
    

@app.route('/urlForm', methods=['GET','POST'])
def urlForm():
    try:
        status = 0
        json_data = request.get_json()
        y=json_data['data']
        
        # Process the received JSON data here
        # For example, you can print it to the console
        print("Received URL JSON data:", y)
        data = extract_publication_date(y)
        conn = db.connect()
        cursor = conn.cursor()
        userid = json_data['user_id']
        title = data["Title"]
        content = data["Body"]
        date = data["Date"]
        print("id:",userid,"\nTitle:",title,"\nContent",content,"\nDate:",date)
        if userid != 0:
            articleid = populateArticles(conn,cursor,userid,title,content,date)
            

        str_data = str(data)
        starttime = datetime.now()
        if y is not None:
            testing_news = {"text":[str_data]}
            new_def_test = pd.DataFrame(testing_news)
            new_def_test["text"] = new_def_test["text"].apply(wordopt)
            new_x_test = new_def_test["text"]
            new_xv_test = vectorization.transform(new_x_test)
            pred_DT = DT.predict(new_xv_test)
            isFake = output_lable(pred_DT[0])
            endtime = datetime.now()
            status = 1
            if userid != 0:
                db.analysis(conn,cursor,userid,articleid,starttime,endtime,status,isFake)
    
            # sql = "INSERT INTO AnalyzeArticle (userid,starttime,endtime,status) VALUES (%s, %s, %s, %s)"
            # val = (str(userid),str(starttime),str(endtime),str(status))
            # cursor.execute(sql, val)
            # conn.commit()
            # analysisid = cursor.lastrowid
            # sql = "INSERT INTO AnalysisResult (articleid,analysisid,isFake) VALUES (%s, %s, %s)"
            # val = (str(articleid),str(analysisid),str(isFake))
            # cursor.execute(sql, val)
            # conn.commit()

            result = "\n DT Prediction: {}".format(output_lable(pred_DT[0]))
            
            return jsonify(result)
        
           # return render_template('frontend.html', result="\n DT Prediction: {}".format(output_lable(pred_DT[0])))

        return jsonify({"message": "Data received successfully."}), 200
    except Exception as e:
        return jsonify({"error": "Failed to process data.", "details": str(e)}), 400
    
UPLOAD_FOLDER = 'uploads'
import base64
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/textFileForm', methods=['POST'])
@cross_origin()
def textFileForm():
    json_data = request.get_json()
    y=json_data['contents']
    userid = json_data['user_id']
    string_y = str(y)
    # Decode the Base64 string
    decoded_bytes = base64.b64decode(string_y)
    # Convert the bytes to a string
    decoded_string = decoded_bytes.decode('utf-8')
    # Print the decoded string
    lines = decoded_string.split('\n')
    starttime = datetime.now()
    articleIds = []
    isFakes = {}
    for arg in lines:
        if arg == lines[-1]:
            # This is the last argument
            break
        data = extract_csv_data(str(arg))
        conn = db.connect()
        cursor = conn.cursor()
        userid = json_data['user_id']
        # title = data["Title"]
        # content = data["Body"]
        # date = data["Date"]
        data = str(arg).split(',"')
        if data and isinstance(data[0], str) and data[0]:
            title = data[0]
        if data and isinstance(data[1], str) and data[1]:
            content = data[1]
        if data and isinstance(data[2], str) and data[2]:
            date = data[2]

        print(userid,"\nTitle:",title,"\nContent:",content,"\nDate:",date,"\n\n")
        articleId = 0
        if userid != 0:
            articleId = populateArticles(conn,cursor,userid,title,content,date)
        articleIds.append(articleId)
        testing_news = {"text":[arg]}
        new_def_test = pd.DataFrame(testing_news)
        new_def_test["text"] = new_def_test["text"].apply(wordopt)
        new_x_test = new_def_test["text"]
        new_xv_test = vectorization.transform(new_x_test)
        pred_DT = DT.predict(new_xv_test)
        isFakes[articleId] = output_lable(pred_DT[0])
        endtime = datetime.now()
        status = 1
        # if userid != 0:
        #     db.analysis(conn,cursor,userid,articleIds,starttime,endtime,status,isFake)
        result = "\n DT Prediction: {}".format(output_lable(pred_DT[0]))
    
    if userid != 0:
        db.analysis(conn,cursor,userid,articleIds,starttime,endtime,status,isFakes)
          


    # {
    #    'filename': 
    #    'contents': 'base64 string'
    # }
    #
    #
    #
    #
    # Get file string from json
    # Decode it with base64
    # read it as csv and do yo thing...
        
    responce = Response("File uploaded successfully. Check results in History")
    responce.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    responce.headers['Access-Control-Allow-Credentials'] = 'true'
    return responce

@app.route('/urlFileForm', methods=['POST'])
@cross_origin()
def urlFileForm():
   
    json_data = request.get_json()
    y=json_data['contents']
    string_y = str(y)
    # Decode the Base64 string
    decoded_bytes = base64.b64decode(string_y)

    # Convert the bytes to a string
    decoded_string = decoded_bytes.decode('utf-8')

    # Print the decoded string
    lines = decoded_string.split('\n')
    print("this is my url:",lines)
    starttime = datetime.now()
    articleIds = []
    isFakes = {}
    for arg in lines:
        if arg == lines[-1]:
            # This is the last argument
            break
        data = extract_publication_date(arg)
        conn = db.connect()
        cursor = conn.cursor()
        userid = json_data['user_id']
        title = data["Title"]
        content = data["Body"]
        date = data["Date"]
        print("id:",userid,"\nTitle:",title,"\nContent",content,"\nDate:",date)
        articleid = 0
        if userid != 0:
            articleid = populateArticles(conn,cursor,userid,title,content,date)
        articleIds.append(articleid)

        y = str(data)
        print("the news data",y)
        testing_news = {"text":[y]}
        new_def_test = pd.DataFrame(testing_news)
        new_def_test["text"] = new_def_test["text"].apply(wordopt)
        new_x_test = new_def_test["text"]
        new_xv_test = vectorization.transform(new_x_test)
        pred_DT = DT.predict(new_xv_test)
        isFakes[articleid] = output_lable(pred_DT[0])
        endtime = datetime.now()
        status = 1

    if userid != 0:
        db.analysis(conn,cursor,userid,articleIds,starttime,endtime,status,isFakes)
        #result = "\n DT Prediction: {}".format(output_lable(pred_DT[0]))
        
          


    # {
    #    'filename': 
    #    'contents': 'base64 string'
    # }
    #
    #
    #
    #
    # Get file string from json
    # Decode it with base64
    # read it as csv and do yo thing...
        
    responce = Response("File uploaded successfully. Check results in History")
    responce.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    responce.headers['Access-Control-Allow-Credentials'] = 'true'
    return responce

@app.route('/deleteAnalysis', methods=['POST','GET'])
@cross_origin()
def deleteAnalysis():
    analysis_id = request.args.get("analysis_id")
    response_json = {
        "RESULT": "ERROR"
    }
    if analysis_id is None:
        return jsonify(response_json)
    else:
        conn = db.connect()
        cursor = conn.cursor(prepared=True)
        res = deleteCompleteAnalysis(conn, cursor, analysis_id)
        response_json = {
            "RESULT": res
        }
    return jsonify(response_json)

@app.route('/getArticleFullContent', methods=['GET'])
@cross_origin()
def getArticleFullContent():
    article_id = request.args.get("article_id")
    conn = db.connect()
    cursor = conn.cursor(prepared=True)
    content = selectArticleContent(conn, cursor, article_id)
    data_array = {
        "data": content
    }
    return jsonify(data_array)

@app.route('/getDbData', methods=['POST','GET'])
@cross_origin()
def getDbData():
    user_id = request.args.get("user_id")
    analysis_id = request.args.get("analyze_id")
    data_array = {}
    if analysis_id is None:
        conn = db.connect()
        cursor = conn.cursor(prepared=True)
        # data = [{'id': 1, 'starttime': 'John Doe', 'endtime': 'johndoe@example.com', 'status': 0},
        # {'id': 2, 'starttime': 'Jane Doe', 'endtime': 'janedoe@d.com','status': 1}]
        analysis = selectAnalyzeArticle(conn, cursor, user_id)
        data_array = {
            "data": analysis
        }
    else:
        conn = db.connect()
        cursor = conn.cursor(prepared=True)
        articles = selectNewsArticleAnalysis(conn, cursor, user_id, analysis_id)
        data_array = {
            "data": articles
        }
        print(data_array)
    return jsonify(data_array)


def extract_publication_date(y):
    result = {}
    
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(y)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Common date patterns
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # yyyy-mm-dd
                r'\d{2}/\d{2}/\d{4}',  # mm/dd/yyyy
                r'\d{2}-\d{2}-\d{4}',  # dd-mm-yyyy
            ]

            title = soup.title.string
            if title:
                title_with_one_space = ' '.join(title.split())
                #print(f"Page Title with one space: {title_with_one_space}")
                result["Title"] = title_with_one_space
            else:
                print("No page title found")

            # Get the page body with only one space
            body = soup.body
            if body:
                body_text = body.get_text()
                body_with_one_space = ' '.join(body_text.split())
                modified_text = body_with_one_space.replace('\n', ' ') 
                result["Body"] = modified_text
                #print("Page Body with one space:")
                #print(body_with_one_space)
            else:
                print("No page body found")



            # Search for date patterns in the page content
            for pattern in date_patterns:
                date_match = re.search(pattern, response.text)
                if date_match:
                    date = date_match.group(0)
                    result["Date"] = date

            print("No publication date found on the page.")

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
    return result

def extract_publication_date_data(article_text):
    result = {
        "Title": None,
        "Body": None,
        "Date": None
    }

    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # yyyy-mm-dd
        r'\d{2}/\d{2}/\d{4}',  # mm/dd/yyyy
        r'\d{2}-\d{2}-\d{4}',  # dd-mm-yyyy
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}',
    ]


    lines = article_text.split('\n')  # Splits the string by newline characters
    if lines:  # Check if there are any lines in the text
        title = lines[0]  # Return the first line
        result["Title"] = title
    modified_text = article_text.replace('\n', ' ') 
    result["Body"] = modified_text

    for pattern in date_patterns:
        date_match = re.search(pattern, article_text)
        if date_match:
            result["Date"] = date_match.group(0)
            break

    return result

def extract_csv_data(article_text):
    result = {
        "Title": None,
        "Body": None,
        "Date": None
    }

    pattern = r'^(.*?),(.*)$'

    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # yyyy-mm-dd
        r'\d{2}/\d{2}/\d{4}',  # mm/dd/yyyy
        r'\d{2}-\d{2}-\d{4}',  # dd-mm-yyyy
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}',
    ]


    # modified_title = article_text.split(',')[0]
    # result["Title"] = modified_title
    modified_text = article_text.replace('\n', ' ') 
    result["Body"] = modified_text

    match = re.search(pattern, article_text, re.DOTALL | re.MULTILINE)
    if match:
        result["Title"] = match.group(1).strip()

    for pattern in date_patterns:
        date_match = re.search(pattern, article_text)
        if date_match:
            result["Date"] = date_match.group(0)
            break

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)