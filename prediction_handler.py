import pandas as pd
from joblib import load

model_old = load("artifacts/model_old.joblib")
model_young = load("artifacts/model_young.joblib")


scaler_old = load("artifacts/scaler_old.joblib")
scaler_young = load("artifacts/scaler_young.joblib")

def calculatenormalisedriskscore(medical_history):
    riskscores = {
    'diabetes': 6,
    'heart disease': 8,
    'high blood pressure': 6,
    'thyroid': 5,
    'no disease': 0,
    'none': 0
    }

    diseases = medical_history.lower().split(" & ")

    total_risk_score = sum(riskscores.get(disease, 0) for disease in diseases)

    max_score = 14
    min_score = 0

    normalisedriskscore = (total_risk_score - min_score)/(max_score - min_score)

    return normalisedriskscore



def preprocessing(input_data):
    df = pd.DataFrame(columns=[
        'Age', 'Number Of Dependants', 'Income_Lakhs', 'Insurance_Plan', 
        'Genetical_Risk', 'normalisedriskscore', 'Gender_Male', 
        'Region_Northwest', 'Region_Southeast', 'Region_Southwest', 
        'Marital_status_Unmarried', 'BMI_Category_Obesity', 
        'BMI_Category_Overweight', 'BMI_Category_Underweight', 
        'Smoking_Status_Occasional', 'Smoking_Status_Regular', 
        'Employment_Status_Salaried', 'Employment_Status_Self-Employed'
    ])

    df.loc[0] = 0

    print(df.shape)

    df['Age'] = input_data['Age']
    df['Number Of Dependants'] = input_data['Number of Dependents']
    df['Income_Lakhs'] = input_data['Income (in Lakhs)'] 

    if input_data['Region'] == 'Northeast':
        pass
    elif input_data['Region'] == 'Northwest':
        df['Region_Northwest'] = 1
        df['Region_Southwest'] = 0
        df['Region_Northeast'] = 0
    elif input_data['Region'] == 'Southwest':
        df['Region_Northwest'] = 0
        df['Region_Southwest'] = 1
        df['Region_Northeast'] = 0
    elif input_data['Region'] == 'Northeast':
        df['Region_Northwest'] = 0
        df['Region_Southwest'] = 0
        df['Region_Northeast'] = 1

    if input_data['Insurance Plan'] == 'Bronze':
        df['Insurance_Plan'] = 1
    elif input_data['Insurance Plan'] == 'Silver':
        df['Insurance_Plan'] = 2
    elif input_data['Insurance Plan'] == 'Gold':
        df['Insurance_Plan'] = 3

    if input_data['Gender'] == 'Male':
        df['Gender_Male'] = 1

    if input_data['BMI Category'] == 'Normal':
        df['BMI_Category_Obesity'] = 0
        df['BMI_Category_Overweight'] = 0
        df['BMI_Category_Underweight'] = 0
    elif input_data['BMI Category'] == 'Overweight':
        df['BMI_Category_Obesity'] = 0
        df['BMI_Category_Overweight'] = 1
        df['BMI_Category_Underweight'] = 0
    elif input_data['BMI Category'] == 'Underweight':
        df['BMI_Category_Obesity'] = 0
        df['BMI_Category_Overweight'] = 0
        df['BMI_Category_Underweight'] = 1
    elif input_data['BMI Category'] == 'Obesity':
        df['BMI_Category_Obesity'] = 1
        df['BMI_Category_Overweight'] = 0
        df['BMI_Category_Underweight'] = 0

    if input_data['Smoking Status'] == 'No Smoking':
        df['Smoking_Status_Occasional'] = 0
        df['Smoking_Status_Regular'] = 0
    elif input_data['Smoking Status'] == 'Occasional':
        df['Smoking_Status_Occasional'] = 1
        df['Smoking_Status_Regular'] = 0
    elif input_data['Smoking Status'] == 'Regular':
        df['Smoking_Status_Occasional'] = 0
        df['Smoking_Status_Regular'] = 1

    if input_data['Employment Status'] == 'Self-Employed':
        df['Employment_Status_Self-Employed']=1
        df['Employment_Status_Salaried']=0
    elif input_data['Employment Status'] == 'Salaried':
        df['Employment_Status_Self-Employed']=0
        df['Employment_Status_Salaried']=1
    elif input_data['Employment Status'] == 'Freelancer':
        df['Employment_Status_Self-Employed']=0
        df['Employment_Status_Salaried']=0

    if input_data['Genetical Risk']:
        df['Genetical_Risk'] = input_data['Genetical Risk']
    else:
        df['Genetical_Risk'] = 0



    df['normalisedriskscore'] = calculatenormalisedriskscore(input_data['Medical History'])
    handlescaling(input_data['Age'], df)
    return df

def handlescaling(age ,df):
    if age<=25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_old

    colstoscale = scaler_object['columns_to_scale']    
    scaler = scaler_object['scaler']

    df['Income_Level'] = 0

    df[colstoscale] = scaler.transform(df[colstoscale])
    df.drop('Income_Level',axis=1,inplace=True)


    return df


def predict(input_data):
    print(input_data)

    testinputdf = preprocessing(input_data)

    if input_data['Age']<25:
        prediction = model_young.predict(testinputdf)
    else:
        prediction = model_old.predict(testinputdf)

    return int(prediction)


    



    

    



    
