import numpy as np
from flask import Flask,render_template,request,jsonify
import pickle
import requests


import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Ivs8Ix9Pkwz2gnW9alUtCeSQkrNtxT8ZdeJHd9ZuAL_o"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line



app = Flask(__name__)
models = pickle.load(open('wqi.pkl','rb'))
@app.route('/')
def home() :
    return render_template("predict.html")

@app.route('/login',methods=['POST'])
def login() :
    # year = request.form["year"]
    do = request.form["do"]
    ph = request.form["ph"]
    co = request.form["co"]
    bod = request.form["bod"]
    na = request.form["na"]
    tc = request.form["tc"]
    total = [[float(do),float(ph),float(co),float(bod),float(na),float(tc)]]
    y_pred = models.predict(total)
    y_pred =y_pred[[0]]
    if(y_pred >= 95 and y_pred <= 100) :
        return render_template("predict.html",showcase = 'Excellent,The predicted value is '+ str(y_pred)+' No Purification or Treatment of Water is needed.')
    elif(y_pred >= 89 and y_pred <= 94) :
        return render_template("predict.html",showcase = 'Very good,The predicted value is '+str(y_pred)+' Minor Purification or Treatment of Water is needed.')
    elif(y_pred >= 80 and y_pred <= 88) :
        return render_template("predict.html",showcase = 'Good,The predicted value is'+str(y_pred)+' Conventional Purification or Treatment of Water is needed.')
    elif(y_pred >= 65 and y_pred <= 79) :
        return render_template("predict.html",showcase = 'Fair,The predicted value is '+str(y_pred)+' Extensive Purification or Treatment of Water is needed.')
    elif(y_pred >= 45 and y_pred <= 64) :
        return render_template("predict.html",showcase = 'Marginal,The predicted value is '+str(y_pred)+' Doubtful in purifying and treating the water so as to get Pure Water.')
    else :
        return render_template("predict.html",showcase = 'Poor,The predicted value is '+str(y_pred)+' The Water is not fit for to be used for Drinking.')
    payload_scoring = {"input_data": [{"field": [["do","ph","co","bod","tc","na"]], "values": [[6.7, 7.5, 203, 2, 0.1, 27.0]]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a5f82bd9-6344-4f87-946f-7bee58fdc061/predictions?version=2022-11-26')
    
    
    print(y_pred)
    return render_template('predict.html',prediction_text=pred)


if __name__ == '__main__' :    
      app.run(debug=True,port=5000)