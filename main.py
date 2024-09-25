import streamlit as st
from prediction_handler import predict

# Streamlit frontend
st.title("Health and Insurance Information Form")

# First row with Age, Number of Dependents, and Income in Lakhs using only manual input
st.write("### Personal Information")
age = st.number_input("Age", min_value=18, max_value=100, value=30)
num_dependents = st.number_input("Number of Dependents", min_value=0, max_value=5, value=2)
income_lakhs = st.number_input("Income (in Lakhs)", min_value=0, max_value=100, value=10)

# Create columns for the dropdowns
st.write("### Additional Information")
col1, col2, col3 = st.columns(3)

with col1:
    region = st.selectbox("Region", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])
    marital_status = st.selectbox("Marital Status", ['Unmarried', 'Married'])
    smoking_status = st.selectbox("Smoking Status", ['No Smoking','Occasional','Regular'])
    
    

with col2:
    gender = st.selectbox("Gender", ['Male', 'Female'])
    bmi_category = st.selectbox("BMI Category", ['Overweight', 'Underweight', 'Normal', 'Obesity'])
    medical_history = st.selectbox("Medical History", ['High blood pressure', 'No Disease', 'Diabetes & High blood pressure', 
                                                       'Diabetes & Heart disease', 'Diabetes', 'Diabetes & Thyroid', 
                                                       'Heart disease', 'Thyroid', 'High blood pressure & Heart disease'])

with col3:
    insurance_plan = st.selectbox("Insurance Plan", ['Silver', 'Bronze', 'Gold'])
    employment_status = st.selectbox("Employment Status", ['Self-Employed', 'Freelancer', 'Salaried'])
    genetical_risk = st.selectbox("Genetical Risk",['0','1','2','3','4','5'])



# Predict button at the bottom
st.markdown("""<hr>""", unsafe_allow_html=True)  # Horizontal line for separation
centered_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        margin: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

input_data = {
    "Age": age,
    "Number of Dependents": num_dependents,
    "Income (in Lakhs)": income_lakhs,
    "Region": region,
    "Marital Status": marital_status,
    "Smoking Status": smoking_status,
    "Insurance Plan": insurance_plan,
    "Medical History": medical_history,
    "Gender": gender,
    "BMI Category": bmi_category,
    "Employment Status": employment_status,
    "Genetical Risk":genetical_risk
}


if st.button("Predict"):
    prediction = predict(input_data)
    st.success(f"Your Healthcare Premium Insurance price is predicted to be {prediction}")
