
from abc import ABC, abstractmethod
import streamlit as st


# class Person(ABC):
#     def __init__(self, name, age, weight, height):
#         self.name = name
#         self.age = age
#         self._weight = weight
#         self._height = height

#     @property
#     def weight(self):
#         return self._weight

#     @weight.setter
#     def weight(self, value):
#         if value < 0:
#             raise ValueError("Weight cannot be negative")
#         self._weight = value

#     @property
#     def height(self):
#         return self._height

#     @height.setter
#     def height(self, value):
#         if value < 0:
#             raise ValueError("Height cannot be negative")
#         self._height = value

#     @abstractmethod
#     def calculate_bmi(self):
#         pass

#     @abstractmethod
#     def get_bmi_category(self):
#         pass

#     def print_info(self):
#         st.markdown(
#             f"### {self.name} (Age: {self.age})\n"
#             f"- Weight: {self.weight} kg\n"
#             f"- Height: {self.height} m\n"
#             f"- **BMI:** {self.calculate_bmi():.2f}\n"
#             f"- **Category:** {self.get_bmi_category()}"
#         )


# # ===== Adult and Child Classes =====
# class Adult(Person):
#     def calculate_bmi(self):
#         return self.weight / (self.height ** 2)

#     def get_bmi_category(self):
#         bmi = self.calculate_bmi()
#         if bmi < 18.5:
#             return "Underweight"
#         elif 18.5 <= bmi < 24.9:
#             return "Normal weight"
#         elif 24.9 <= bmi < 29.9:
#             return "Overweight"
#         else:
#             return "Obese"


# class Child(Person):
#     def calculate_bmi(self):
#         return (self.weight / (self.height ** 2)) * 1.3

#     def get_bmi_category(self):
#         bmi = self.calculate_bmi()
#         if bmi < 14:
#             return "Underweight"
#         elif 14 <= bmi < 18:
#             return "Normal weight"
#         elif 18 <= bmi < 24:
#             return "Overweight"
#         else:
#             return "Obese"


# class BMIApp:
#     def __init__(self):
#         if 'people' not in st.session_state:
#             st.session_state.people = []

#     def add_person(self, person):
#         st.session_state.people.append(person)

#     def collect_user_data(self):
#         st.header("Enter Person Information")

#         name = st.text_input("Name", value="")
#         age = st.number_input("Age", min_value=0, max_value=120, value=18)
#         weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
#         height = st.number_input("Height (m)", min_value=0.0, step=0.01)

#         if st.button("Add Person"):
#             st.write(f"Debug: name={name}, age={age}, weight={weight}, height={height}")

#             if not name:
#                 st.error("Name is required.")
#             elif weight <= 0.0 or height <= 0.0:
#                 st.error("Weight and height must be greater than 0.")
#             else:
#                 if age >= 18:
#                     person = Adult(name, age, weight, height)
#                 else:
#                     person = Child(name, age, weight, height)

#                 self.add_person(person)
#                 st.success(f"{name} added successfully!")

#     def print_results(self):
#         st.header("BMI Results")
#         if not st.session_state.people:
#             st.info("No people added yet.")
#         else:
#             for person in st.session_state.people:
#                 person.print_info()
#                 st.markdown("---")

#     def run(self):
#         st.title("BMI Calculator App")
#         self.collect_user_data()
#         self.print_results()


# if __name__ == "__main__":
#     app = BMIApp()
#     app.run()


col1,col2,col3,col4,col5=st.columns(5,gap="small",vertical_alignment="center")

with col1:
    st.header("Colum 1")
    st.write("This is colum 1")
with col2:
    st.header("Colum 2")
    st.write("This is colum 2")
with col3:
    st.header("Colum 3")
    st.write("This is colum 3")
with col4:
    st.header("Colum 4")
    st.write("This is colum 4")
with col5:
    st.header("Colum 5")
    st.write("This is colum 5")

with st.container():
    st.header("Header inside the container")
    st.write("This is inside the container")

st.sidebar.header("Sidebar")
st.sidebar.write("This is sidebar")
# st.sidebar.selectbox("Chose an option",["Option1","Option2","Option3"])
st.sidebar.radio("Chose an option",["Home","Contact us","About us"])

with st.form("My form", clear_on_submit=True):
    name=st.text_input("Name")
    surname=st.text_input("Surname")
    age=st.slider("Age",min_value=0,max_value=100)
    email=st.text_input("Email")
    terms=st.checkbox("I agree to the terms and conditions")
    submit_button=st.form_submit_button(label="Submit")
if submit_button:
    st.write(f"Name:{name}")
    st.write(f"Surname:{surname}")
    st.write(f"Age:{age}")
    st.write(f"Email:{email}")
    if terms:
        st.write("You agreed to the terms and conditions")
    else:
        st.write("You did not agree to the terms and conditions")
