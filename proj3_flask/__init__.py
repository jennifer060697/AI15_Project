from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def create_app() :
    model = None
    with open('xgb_bas.pkl','rb') as pickle_file:
        model = pickle.load(pickle_file)

    if request.method == 'POST' :
        SEX = int(request.form['SEX'])
        AGE = int(request.form['AGE'])
        VA_LT = float(request.form['VA_LT'])
        VA_RT = float(request.form['VA_RT'])
        HTN = int(request.form['HTN'])
        DM = int(request.form['DM'])
        DR = int(request.form['DR'])

        if AGE < 25 : AGE_G = 1
        elif AGE >= 75 : AGE_G = 27
        else : AGE_G = int((AGE-21)/2)

        raw = {
            'SEX' : [SEX],
            'AGE_G' : [AGE_G],
            'VA_LT': [VA_LT],
            'VA_RT': [VA_RT],
            'HTN': [HTN],
            'DM': [DM],
            'DR' : [DR],
        }

        y_pred = model.predict_proba(pd.DataFrame(raw))
        proba = y_pred[0][1]

        if proba > 0.7 : PROBA = '녹내장 위험도 매우 높음'
        elif proba > 0.6 : PROBA = '녹내장 위험도 높음'
        elif proba > 0.4 : PROBA = '녹내장 위험도 보통'
        elif proba > 0.3 : PROBA = '녹내장 위험도 낮음'
        else : PROBA = '녹내장 위험도 매우 낮음'

        return render_template('pred.html', PROBA = PROBA)
    
    else :
        return render_template('proj3.html')
