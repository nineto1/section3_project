import dbmanager

import pandas as pd
import numpy as np
from eli5.sklearn import PermutationImportance
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from category_encoders import TargetEncoder

from pdpbox.pdp import pdp_isolate, pdp_plot

import pickle

TARGET = '물건금액'
MODEL = 'xgb_model'
MAX_DEPTH = np.arange(1, 10, 2)
N_ESTIMATORS = np.arange(200, 1000, 100)
LEARNING_RATE = np.arange(0.1, 0.5, 0.1)
ACTIVATE = False

def load_DB_data() :
    df = pd.DataFrame.from_records(dbmanager.getTableAll(dbmanager.TABLE_NAME), columns = dbmanager.COLUMNS_LIST)
    df.fillna(value = 0, inplace = True) # 결측치 처리
    df.drop(columns = ['실거래가아이디', '자치구명', '법정동명'], inplace = True)
    return df

def splite_train_test(df) :
    train, test = train_test_split(df, train_size = 0.8, test_size=0.2, random_state=2)

    y_train = train[TARGET]
    y_test = test[TARGET]
    x_train = train.drop(columns = TARGET)
    x_test = test.drop(columns = TARGET)
    return x_train, x_test, y_train, y_test

def train_model(x, y) :
    pipe = make_pipeline(
        TargetEncoder(),    
        StandardScaler(), 
        XGBRegressor(random_state=2, n_jobs=-1)
    )

    dists = {
        'xgbregressor__max_depth' : MAX_DEPTH,
        'xgbregressor__n_estimators' : N_ESTIMATORS,
        'xgbregressor__learning_rate' : LEARNING_RATE
    }
    randomscv = RandomizedSearchCV(
        pipe, 
        param_distributions=dists, 
        n_iter=50, 
        cv=5, 
        scoring='r2',  
        verbose=1,
        n_jobs=-1,
        return_train_score = True
    )
    randomscv.fit(x_train, y_train);

    return randomscv

def get_model() :
    with open(MODEL, 'rb') as file :
        model = pickle.load(file)
    return model

def model_predict(x) : 
    model = get_model()    

    pred = model.predict(x)
    return pred

def feature_importance(x, y) :
    model = get_model()
    pipe = model.best_estimator_

    permuter = PermutationImportance(
        pipe.named_steps['xgbregressor'],
        scoring = 'r2',
        n_iter=5,
        random_state=2
    )

    x_transformed = pipe.named_steps['targetencoder'].transform(x)
    permuter.fit(x_transformed, y)
    data = {'field_name' : x.columns, 'permutation_importance' : permuter.feature_importances_, 
            'feature_importnace' : pipe.named_steps['xgbregressor'].feature_importances_}
    dbmanager.create_feature_importance(pd.DataFrame(data))

x_train, x_test, y_train, y_test = splite_train_test(load_DB_data())

if __name__ == '__main__' and ACTIVATE == True:
    model = train_model(x_train, y_train)
    with open(MODEL, 'wb') as file :
        pickle.dump(model, file)

feature_importance(x_test, y_test)

y_pred = model_predict(x_test)
R2_score = r2_score(y_test, y_pred)