import pandas as pd
data=pd.read_csv(r'mining\data\MiningProcess_Flotation_Plant_Database.csv')

def dropDuplicate(data):
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)
    return data


def changeDataType(data):
    data['date']=pd.to_datetime(data['date'])
    data=data.set_index('date')
    return data


def formatNum_And_Resample(data):
    for col in data.columns:
        if col != "date":
            data[col] = (
                data[col]
                .astype(str)             
                .str.replace(',', '.', regex=False)   
                .str.replace('%', '', regex=False)   
                .str.strip()           
            )
            data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.resample('1h').mean()
    return data


def feature_engineer(data):
    #derived features
    data['Starch_to_Pulp']=data['Starch Flow']/data['Ore Pulp Flow']
    data['Amina_to_Pulp']=data['Amina Flow']/data['Ore Pulp Flow']
    data.dropna(inplace=True)
    return data


def pipeline_building(data):
    from sklearn.preprocessing import FunctionTransformer
    from sklearn.pipeline import Pipeline
    
    drop_duplicate_tf = FunctionTransformer(dropDuplicate)
    change_dtype_tf = FunctionTransformer(changeDataType)
    format_resample_tf = FunctionTransformer(formatNum_And_Resample)
    feature_engineer_tf = FunctionTransformer(feature_engineer)
    
    preprocess_pipeline=Pipeline([('drop_duplicates', drop_duplicate_tf),
        ('change_dtype', change_dtype_tf),
        ('format_resample', format_resample_tf),
        ('feature_engineer', feature_engineer_tf)])    
    data_processed=preprocess_pipeline.fit_transform(data)
    return data_processed, preprocess_pipeline


def model_training(data_processed):
    x=data_processed.drop(columns=['% Silica Concentrate'])
    y=data_processed['% Silica Concentrate']
    
    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=42)
    
    from catboost import CatBoostRegressor
    cat_model = CatBoostRegressor(
        iterations=300,
        learning_rate=0.05,
        depth=5,
        random_seed=20,
        subsample=0.8,
        rsm=0.8,               # random subspace method (like colsample)
        verbose=0              # silent training
    )   
    cat_model.fit(x_train, y_train)
    return cat_model,x_train, x_test, y_train, y_test



def save_model(data):
    import joblib
    
    data_processed,preprocess_pipeline = pipeline_building(data)
    model, x_train, x_test, y_train, y_test = model_training(data_processed)
    
    joblib.dump(model,'cat_model.pkl')
    joblib.dump(preprocess_pipeline, 'preprocess_pipeline.pkl')

save_model(data)








