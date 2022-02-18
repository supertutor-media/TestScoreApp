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
    scores.loc[:,"Test Type"] = pd.Series(np.where(scores["Test name"].str.contains("Test"), "SAT", "ACT"))
    scores = scores.dropna(subset=['Email', 'Test name'])
    return scores

def SATonly(cleanscores):
    SAT = cleanscores[cleanscores["Test Type"] == "SAT"]
    SAT = SAT.drop(columns=['ACT Total Score',
       'ACT English Score', 'ACT Math Score', 'ACT Reading Score',
       'ACT Science Score', 'ACT Essay Score', 'ACT English Omitted',
       'ACT English Missed', 'ACT Math Omitted', 'ACT Math Missed',
       'ACT Reading Omitted', 'ACT Reading Missed', 'ACT Science Omitted',
       'ACT Science Missed'])
    SAT = SAT.dropna(subset = ['SAT Total Score']) # remove entries w/o total score
    SAT["SAT English Score"] = SAT['SAT Reading Score'] + SAT['SAT Writing & Language Score']
    SAT["Test"] = SAT['Test name'] + ", " + SAT['Test taken']
    SAT['Test taken']= pd.to_datetime(SAT['Test taken'])
    return SAT.sort_values(by=['Email', 'Test taken'])

def classgroup(csv):
    SAT = SATonly(testtype(csv))
    SAT_clean = SAT[["Email", "Test name", "Test taken", "SAT Total Score",
               "SAT Reading Score", "SAT Writing & Language Score", "SAT Math Score"]]
    SAT_clean = SAT_clean.reset_index()
    SAT_clean["Test Number"] = SAT_clean.reset_index().groupby('Email').cumcount()
    SAT_clean = SAT_clean.drop(columns = ["Test name", "Test taken", "index"])
    grouped = SAT_clean.groupby(["Email", "Test Number"]).mean()
    grouped = grouped.reset_index()
    grouped["Test Number"] = grouped["Test Number"] + 1
    grouped.drop(columns = ["Email"])
    
    return grouped.groupby(["Test Number"]).mean().reset_index().round(2)

def groupbar(group):
    fig = px.bar(group, x="Test Number", y=["SAT Reading Score", "SAT Writing & Language Score", "SAT Math Score"], 
                 title= "Class SAT Scores",
                 hover_name = "SAT Total Score",
                 labels=dict(variable="Section", value="Score"))
   
    return fig

def main():
    st.title("SAT Class Progress")
    uploaded_file = st.file_uploader("Choose a file", ["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        group = classgroup(df)
        st.plotly_chart(groupbar(group))
        
