import streamlit as st

def main():
    st.title("Diabetes Input Form")
    
    age = st.number_input("Age", min_value=0, step=1)
    weight = st.number_input("Weight", min_value=0, step=1)
    diabetes_duration = st.number_input("Diabetes Duration (years)", min_value=0, step=1)
    hba1c = st.number_input("HbA1c (%)", min_value=0.0, step=0.1, format="%.1f")
    
    category = ""
    if hba1c <= 6.5 and diabetes_duration <= 5:
        category = "Simple"
    elif 6.5 < hba1c <= 8.0 or 5 < diabetes_duration <= 10:
        category = "Mild"
    else:
        category = "Complex"
    
    if st.button("Submit"):
        st.write(f"Received Inputs: Age={age}, Weight={weight}, Diabetes Duration={diabetes_duration} years, HbA1c={hba1c}%")
        st.write(f"Category: {category}")

if __name__ == "__main__":
    main()
