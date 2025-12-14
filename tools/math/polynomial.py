# tools/math/polynomial.py

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def gen_linear_chart():
    x = np.linspace(-10, 10, 100)
    y = x
    fig, ax = plt.subplots()
    ax.plot(x, y, label="y = x")
    ax.set_title("Linear Function")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid()
    st.pyplot(fig)


def gen_quadratic_chart():
    x = np.linspace(-10, 10, 100)
    y = x**2
    fig, ax = plt.subplots()
    ax.plot(x, y, label="y = x^2")
    ax.set_title("Quadratic Function")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid()
    st.pyplot(fig)


def gen_cubic_chart():
    x = np.linspace(-10, 10, 100)
    y = x**3
    fig, ax = plt.subplots()
    ax.plot(x, y, label="y = x^3")
    ax.set_title("Cubic Function")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid()
    st.pyplot(fig)


def gen_quartic_chart():
    x = np.linspace(-10, 10, 100)
    y = x**4
    fig, ax = plt.subplots()
    ax.plot(x, y, label="y = x^4")
    ax.set_title("Quartic Function")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid()
    st.pyplot(fig)


def gen_quintic_chart():
    x = np.linspace(-10, 10, 100)
    y = x**5
    fig, ax = plt.subplots()
    ax.plot(x, y, label="y = x^5")
    ax.set_title("Quintic Function")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
