from pycaret.classification import *
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
def build_classifier(df,label):
    m1 = setup(data = df,target = label)
    best = compare_models()
    table = pull()
    return table, best

def automl(df, label, usecase):
    wip = st.empty()  # Placeholder for the "Please wait" message
            
    wip.text('Building your models, Please Wait....')  # Show "Please wait" message