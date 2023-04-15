import streamlit as st
import matplotlib.pyplot as plt
import requests
import numpy as np
import streamlit_lottie as st_lottie

def babylonian_method(num):
    """
    Implements the Babylonian method for finding the square root of a number.
    """
    guess = num / 2
    history = [guess]
    while abs(num - guess ** 2) > 1e-6:
        guess = (guess + num / guess) / 2
        history.append(guess)
    return guess, history

def solve_quadratic(a, b, c):
    """
    Solves the quadratic equation ax^2 + bx + c = 0 using the Babylonian method.
    """
    x_guess = max(abs(b/a), abs(c/a))
    guess_list = [(x_guess,)]
    while True:
        x = (x_guess + c/(a*x_guess)) / 2
        guess_list.append((x,))
        if abs(x - x_guess) < 1e-6:
            break
        x_guess = x
    x1, x2 = None, None
    if a != 0:
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            x1 = (-b + np.sqrt(discriminant)) / (2*a)
            x2 = (-b - np.sqrt(discriminant)) / (2*a)
    return x1, x2, guess_list

def plot_guesses(guess_list, x1, x2):
    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot x1 and x2 as vertical lines
    ax.axvline(x=x1, linestyle='--', color='r', label='x1')
    ax.axvline(x=x2, linestyle='--', color='b', label='x2')

    # Plot all the values in guess_list as points
    x_values = range(len(guess_list))
    y_values = [guess[0] for guess in guess_list]
    ax.plot(x_values, y_values, 'go', label='Guesses')

    # Set the x-axis label and legend
    ax.set_xlabel('Iteration')
    ax.legend()

    # Show the plot
    st.pyplot(fig)


def load_lottieurl(url):
    r = requests.get(url)

    if r.status_code != 200:
        return None
    
    return r.json()

hieroglyphic_nums = {
    1: "𓏭",
    10: "𓍯",
    100: "𓎼",
    1000: "𓍿",
    10000: "𓀀",
}

def to_hieroglyphs(num):
    if (num in hieroglyphic_nums):
        return hieroglyphic_nums[num]
    
    st.write("The number you entered is not in the hieroglyphic set. Choose a power of 10")


st_lottie.st_lottie(load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_xrq4wyy3.json"), height=300) 
 
# Streamlit app
st.title("Explore mathematical processes based on Babylonian or Egyption Practices!")
st.write("Ihsaan Yasin | MIDEAST 341")


# Centers all buttons
st.write("<style>div.row-widget.stButton > button:first-child {margin: 0 auto; display: block;}</style>", unsafe_allow_html=True)



# Babylonian method
st.header("The Babylonian Method")
st.write("The Babylonian method finds the square root of a number. It is based on approximating the square root by dividng a number by two, looking at its square, and then going to the upper or lower half of the number. If you're familiar with Comptuer Science, then this is essentially a binary search!")
num1 = st.number_input("Enter a number:")
if st.button("Find Square Root"):
    result, history = babylonian_method(num1)
    st.success(f"The square root of {num1} is {result:.6f}")
    # Plot the convergence of the method
    fig, ax = plt.subplots()
    ax.plot(history, label="guess")
    ax.axhline(y=result, color="r", linestyle="--", label="exact value")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Guess")
    ax.set_title("Convergence of Babylonian Method")
    ax.legend()
    st.pyplot(fig)

st.divider()

# Quadratic equation
st.header("Quadratic Equation")
st.write("This is a showcase of an implementation of a quadratic equation solution finder. It uses the babylonians' method of solving a quadratic, which involved continuously calculating guesses. This is very similar to the babylonian method, except now having gesses for the next root")
a = st.number_input("Enter a value for a:")
b = st.number_input("Enter a value for b:")
c = st.number_input("Enter a value for c:")
if st.button("Solve Quadratic Equation"):
    x1, x2, guesses = solve_quadratic(a, b, c)
    if x1 is None:
        st.error("The quadratic equation has no real solutions.")
    else:
        st.write("Here, the guesses are for the approximate method of the solutions obtained at each iteration for the quadratic solution using the babylonian method. This is very similar to the plot of the babylonian method")
        st.success(f"The solutions to the quadratic equation {a}x^2 + {b}x + {c} = 0 are x1 = {x1:.6f} and x2 = {x2:.6f}.")
        plot_guesses(guesses, x1, x2)


# Hieroglyphic numeral calculator
st.header("Hieroglyphic Numeral Calculator")

st.write("Simply enter a number in the hieroglyphic set and press the button below to see the result")
st.write("Note that the caluclations are cumulative. Further, you might ned to double click buttons")
st.write("Challenge: Can you guess the value of each of the hieroglyphic numerals?")

if 'numA' not in st.session_state:
    st.session_state['numA'] = None

if 'result' not in st.session_state:
    st.session_state['result'] = 0

if 'operation' not in st.session_state:
    st.session_state['operation'] = None

if 'string' not in st.session_state:
    st.session_state["string"] = "0"

if 'doOperation' not in st.session_state:
    st.session_state["doOperation"] = 1

st.divider()

# for key in ['numA', 'result', 'operation', 'string', 'doOperation']:
#     if key in st.session_state:
#         st.write(key, st.session_state[key])

if st.session_state["doOperation"] == 1:
    with st.container():
        col11, col22, col33, col44 = st.columns(4)
        with col11: 
            if (st.button("x", key="1")):
                st.session_state["operation"] = 'x'
                st.session_state["doOperation"] = 2

        with col22: 
            if (st.button('＋', key="10")):
                st.session_state["operation"] = '++'
                st.session_state["doOperation"] = 2
        with col33: 
            if (st.button("/", key="100")):
                st.session_state["operation"] = '/'
                st.session_state["doOperation"] = 2

        with col44: 
            if (st.button('−', key="1000")):
                st.session_state["operation"] = '--'
                st.session_state["doOperation"] = 2
    
    

elif st.session_state["doOperation"] == 2: 
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: 
            if (st.button(hieroglyphic_nums[1])):
                st.session_state["numA"] = 1
                st.session_state["doOperation"] = 3

        with col2: 
            if (st.button(hieroglyphic_nums[10])):
                st.session_state["numA"] = 10
        with col3: 
            if (st.button(hieroglyphic_nums[100])):
                st.session_state["numA"] = 100
                st.session_state["doOperation"] = 3

        with col4: 
            if (st.button(hieroglyphic_nums[1000])):
                st.session_state["numA"] = 1000
                st.session_state["doOperation"] = 3
        with col5: 
            if(st.button(hieroglyphic_nums[10000])):
                st.session_state["numA"] = 10000
                st.session_state["doOperation"] = 3
        
        
else: 
    st.write(st.session_state["numA"])
    st.write(st.session_state["operation"])
    operation = st.session_state["operation"]
    st.write(operation)

    if (st.button("Calculator", key="calculator")):
        x = 0
        if operation == 'x':
            x = int(st.session_state["result"]) * int(st.session_state["numA"])
            st.session_state['string'] = st.session_state['string'] + ' x ' + str(st.session_state['numA'])
        if operation == '/':
            x = int(st.session_state["result"]) / int(st.session_state["numA"])
            st.session_state['string'] = st.session_state['string'] + ' / ' + str(st.session_state['numA'])
        if operation == '--':
            x = int(st.session_state["result"]) - int(st.session_state["numA"])
            st.session_state['string'] = st.session_state['string'] + ' - ' + str(st.session_state['numA'])
        if operation == '++':
            x = int(st.session_state["result"]) + int(st.session_state["numA"])
            st.session_state['string'] = st.session_state['string'] + ' + ' + str(st.session_state['numA'])
        
        st.session_state["result"] = x
        st.session_state["doOperation"] = 1

st.write("Current calulation: " + str(st.session_state["string"]))
st.write("Result: " + str(st.session_state["result"]))

if st.button("clear"):
    st.session_state["numA"] = None
    st.session_state["operation"] = None
    st.session_state["result"] = 0
    st.session_state["doOperation"] = 1
    st.session_state["string"] = "0"

