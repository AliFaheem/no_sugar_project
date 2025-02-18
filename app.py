import streamlit as st
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeRegressor

def get_recommendation(category):
    recommendations = {
        "Simple": ["16-8 (Daily)", "2 meals + 1 snack (Low carbs, balanced diet)", "30 min brisk walk (5x per week)"],
        "Mild": ["16-8 (Daily) progressing to 18-6", "2 meals (Low carbs, high protein)", "30 min brisk walk + resistance training (2x per week)"],
        "Complex": ["14-10 progressing to 18-6 (After 2 weeks)", "3 small meals (Strict low carbs)", "20 min light walk progressing to resistance training (after 4 weeks)"]
    }
    return recommendations.get(category, ["No recommendation available"] * 3)

def categorize_diabetes(hba1c, diabetes_duration):
    if hba1c <= 6.5 and diabetes_duration <= 5:
        return "Simple"
    elif 6.5 < hba1c <= 8.0 or 5 < diabetes_duration <= 10:
        return "Mild"
    else:
        return "Complex"

def predict_days(age, weight, duration, hba1c, category):
    # Load the saved model
    model = joblib.load("diabetes_model.pkl")

    # Convert category to numerical value
    category_mapping = {"Mild": 0, "Simple": 1, "Complex": 2}
    category_num = category_mapping.get(category, -1)  # Default to -1 if unknown

    if category_num == -1:
        raise ValueError("Invalid category. Choose from 'Mild', 'Simple', or 'Complex'.")

    # Create a DataFrame for the new input
    new_data = pd.DataFrame({
        "Age": [age],
        "Weight": [weight],
        "duration": [duration],
        "HbA1c": [hba1c],
        "Category": [category_num]
    })

    # Predict
    prediction = model.predict(new_data)
    return int(prediction[0])

def main():
    st.title("Diabetes Reversal Recommendations")
    
    age = st.number_input("Age", min_value=0, step=1)
    weight = st.number_input("Weight (kg)", min_value=0, step=1)
    diabetes_duration = st.number_input("Diabetes Duration (years)", min_value=0, step=1)
    hba1c = st.number_input("HbA1c (%)", min_value=0.0, step=0.1, format="%.1f")
    
    if st.button("Get Recommendation and Prediction"):
        category = categorize_diabetes(hba1c, diabetes_duration)
        st.write(f"### Category: {category}")
        
        recommendations = get_recommendation(category)
        df = pd.DataFrame(
            {"Aspect": ["Intermittent Fasting", "Meals", "Exercise"], "Recommendation": recommendations}
        )
        st.table(df)
        
        try:
            predicted_days = predict_days(age, weight, diabetes_duration, hba1c, category)
            st.write(f"### Estimated Number of Days for Reversal: {predicted_days} days")
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
