import streamlit as st

# def calculate(num1,num2,operation):
#     if operation == "Addition":
#         result=num1 + num2
#     elif operation == "Subctration":
#         result=num1 -num2
#     elif operation == "Multiplacation":
#         result=num1 * num2
#     elif operation =="Division":
#         try:
#             result=num1 / num2
#         except ZeroDivisionError:
#             result="Cannot divide by 0"
#     return result

# def main():
#     st.title("Calculater")
#     num1 = st.number_input("enter the first number",step=1)
#     num2 = st.number_input("enter the second number",step=1)

#     operation= st.radio("Choose an operator",["Addition","Subctration","Multiplacation","Division"])

#     result=calculate(num1,num2,operation)

#     st.write(f"The result of {operation} of {num1} and {num2} is {result}")

# if __name__=="__main__":
#     main()


st.title("Hello world")

if st.button("Click here"):
    st.write("Button has been clicked")

if st.checkbox("Remember me"):
    st.write("Your info has been saved")
