import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def testtype(scores):
    """
    input: csv with raw score data
    output: cleaned dataframe, removes values without email or test, creates new boolean test column
    """
    scores.columns = scores.columns.str.lstrip()
    scores.loc[:,"Test Type"] = pd.Series(np.where(scores['Test name'].str.contains('Test'), 'SAT', 'ACT'))
    scores = scores.dropna(subset=['Email', 'Test name'])
    return scores

def ACTonly(cleanscores):
    ACT = cleanscores[cleanscores["Test Type"] == "ACT"]
    ACT = ACT.drop(columns=['SAT Total Score', 'SAT Reading Score',
       'SAT Writing & Language Score', 'SAT Math Score', 'SAT Reading Omitted',
       'SAT Reading Missed', 'SAT Writing & Language Omitted',
       'SAT Writing & Language Missed', 'SAT Math Omitted', 'SAT Math Missed',
       'SAT Math Calc Omitted', 'SAT Math Calc Missed'])
    ACT = ACT.dropna(subset = ['ACT Total Score'])
    ACT["Test"] = ACT['Test name'] + ", " + ACT['Test taken']
    ACT['Test taken']= pd.to_datetime(ACT['Test taken']).dt.strftime('%m-%d-%Y')
    return ACT.sort_values(by=['Email', 'Test taken'])

def clean(csv):
    df = testtype(csv)
    return ACTonly(df) # returns only ACT entires

def classgroup(ACT):
    ACT_clean = ACT[["Email", "Test name", "Test taken", "ACT Total Score", 
                 "ACT English Score", "ACT Math Score", "ACT Reading Score", "ACT Science Score"]]
    ACT_clean = ACT_clean.reset_index(drop = True).sort_values(by=['Test taken'])
    ACT_clean["Test Number"] = ACT_clean.groupby('Email').cumcount()
    ACT_clean = ACT_clean.drop(columns = ["Test name", "Test taken"])
    grouped = ACT_clean.groupby(["Email", "Test Number"]).mean()
    grouped = grouped.reset_index()
    grouped["Test Number"] = grouped["Test Number"] + 1
    grouped = grouped.drop(columns = ["Email"])
    return grouped.groupby(["Test Number"]).mean().reset_index().round(2)

def groupbar(group):
    fig = px.bar(group, x="Test Number", y=["ACT English Score", "ACT Math Score", "ACT Reading Score", "ACT Science Score"], 
                 title= "Class ACT Scores",
                 hover_name = "ACT Total Score",
                 labels=dict(variable="Section", value="Score"),
                 barmode = "group") 
    return fig

def main():
    st.title("ACT Class Progress")
    uploaded_file = st.file_uploader("Choose a file", ["csv"])
    if uploaded_file is not None:
        df = clean(pd.read_csv(uploaded_file))
        group = classgroup(df)
        st.plotly_chart(groupbar(group))
