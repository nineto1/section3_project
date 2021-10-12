from flask import Blueprint, render_template, request
import xgb_model
import dbmanager
import json
import pandas as pd


print(__name__)
model_bp = Blueprint('model',__name__)

@model_bp.route('/')
def index() :
    model = xgb_model.get_model()
    best_estimator = model.best_estimator_    
    return render_template('model_info.html', model=best_estimator, R2=xgb_model.R2_score)

@model_bp.route('/predict', methods = ['POST'])
def predict() :
    content = request.json
    x_train = pd.DataFrame(content)
    model = xgb_model.get_model()
    y_pred = model.predict(x_train)
    x_train['자치구명'] = x_train['시군구코드'].apply(lambda x : dbmanager.find_name_by_code('시군구코드', x))
    x_train['법정동명'] = x_train['법정동코드'].apply(lambda x : dbmanager.find_name_by_code('법정동코드', x))
    x_train["예상물건금액"] = y_pred
    print(x_train.head(5))
    dbmanager.insert_user_prediction(x_train)
    return x_train.to_dict(), 200

