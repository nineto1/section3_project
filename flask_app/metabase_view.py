from flask import Blueprint, render_template
import requests
import time

import jwt

METABASE_SITE_URL = "http://127.0.0.1:3000"
METABASE_SECRET_KEY = "daae3a3ddd1581c319e63963af7e80cb6c8dec93916701e06c648fc8f1789799"

print(__name__)
metabase_bp = Blueprint('metabase',__name__)

@metabase_bp.route('/dashboard')
def index() :
    payload1 = {
        "resource": {"dashboard": 4},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token1 = jwt.encode(payload1, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl1 = METABASE_SITE_URL + "/embed/dashboard/" + token1 + "#bordered=true&titled=true"
  
    payload2 = {
        "resource": {"dashboard": 3},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token2 = jwt.encode(payload2, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl2 = METABASE_SITE_URL + "/embed/dashboard/" + token2 + "#bordered=true&titled=true"
    return render_template('dashboard1.html', iframeUrl1=iframeUrl1, iframeUrl2=iframeUrl2), 200

@metabase_bp.route('/feature_importance')
def feature_importance() :
    payload = {
        "resource": {"dashboard": 5},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
    return render_template('feature_importance.html', iframeUrl=iframeUrl)

@metabase_bp.route('/detail_graph')
def graph_detail() :
    payload1 = {
        "resource": {"question": 16},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token1 = jwt.encode(payload1, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl1 = METABASE_SITE_URL + "/embed/question/" + token1 + "#bordered=true&titled=true"

    payload2 = {
        "resource": {"question": 19},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token2 = jwt.encode(payload2, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl2 = METABASE_SITE_URL + "/embed/question/" + token2 + "#bordered=true&titled=true"

    payload3 = {
        "resource": {"question": 18},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token3 = jwt.encode(payload3, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl3 = METABASE_SITE_URL + "/embed/question/" + token3 + "#bordered=true&titled=true"

    payload4 = {
        "resource": {"question": 14},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token4 = jwt.encode(payload4, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl4 = METABASE_SITE_URL + "/embed/question/" + token4 + "#bordered=true&titled=true"

    payload5 = {
        "resource": {"question": 15},
        "params": {},
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token5 = jwt.encode(payload5, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl5 = METABASE_SITE_URL + "/embed/question/" + token5 + "#bordered=true&titled=true"
    return render_template('detail.html', iframeUrl1=iframeUrl1, iframeUrl2=iframeUrl2, 
    iframeUrl3=iframeUrl3, iframeUrl4=iframeUrl4, iframeUrl5=iframeUrl5)

