#! /bin/env python

import streamlit as st
import numpy as np

# Write a title and a bit of a blurb
st.title('Distribution Tester')
st.write('Pick a distribution from the list and we shall draw the a line chart from a random sample from the distribution')

# Make some choices for a user to select
keys = ['Normal','Uniform']
dist_key = st.selectbox('Which Distribution do you want to plot?', keys)

# Logic of our program
if dist_key == 'Normal':
    nums = np.random.randn(1000)
elif dist_key == 'Uniform':
    nums = np.array([np.random.randint(100) for i in range(1000)])

# Display User
st.linechart(nums)