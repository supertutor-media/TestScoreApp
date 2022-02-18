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
    SAT['Test taken']= pd.to_datetime(SAT['Test taken']).dt.strftime('%m-%d-%Y')
    return SAT.sort_values(by=['Email', 'Test taken'])

def clean(csv):
    df = testtype(csv)
    return SATonly(df) # returns only SAT entires

def stackedbar(SAT, email):
    df1 = SAT[SAT["Email"] == email]
    df2 = df1[["Email", "Test", "Test taken", "SAT Total Score", "SAT Reading Score", "SAT Writing & Language Score", "SAT Math Score"]]
    df3 = df2.drop(columns=["Test taken"])
    df3 = df3.groupby(["Email", "Test"]).max().reset_index() # get superscore for day
    fig = px.bar(df3, x="Test", y=["SAT Reading Score", "SAT Writing & Language Score", "SAT Math Score"], 
                 title= "SAT scores for " + email,
                 hover_name = "SAT Total Score",
                 labels=dict(variable="Section", value="Score"))
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig
    
def linechart(SAT, email):
    df1 = SAT[SAT["Email"] == email]
    df2 = df1[["Email","Test taken", "Test name", "SAT Total Score", "SAT English Score", "SAT Math Score"]]
    df3 = df2.groupby(["Email", "Test taken", "Test name"]).max().reset_index()
    fig = px.line(df3, x='Test taken', y=["SAT English Score", "SAT Math Score", "SAT Total Score"],
              title = "SAT scores over time for " + email,
              labels=dict(variable="Section", value="Score")
             )
    return fig

def displaydf(SAT, email):
    df = SAT[SAT["Email"] == email][["Test taken", "Test name", "SAT Total Score", 
       "SAT Reading Score", "SAT Writing & Language Score", "SAT Math Score"]].sort_values(by="Test taken")
    df = df.reset_index().drop(columns= ["index"])
    df = df.rename(columns={'Test taken': 'Date', 'Test name': 'Test', 'SAT Total Score': 'Total Score',
                            'SAT Reading Score': 'Reading','SAT Writing & Language Score': 'Writing & Language','SAT Math Score': 'Math'})
    return df
    
def main():  
    st.title("Track Individual Student Progress")
    uploaded_file = st.file_uploader("Choose a file", ["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        newdf = clean(df)
        student = st.selectbox("Select a student", newdf.Email.unique())
        st.plotly_chart((stackedbar(newdf, student)))
        if(len(newdf[newdf["Email"] == student]["Test"].unique()) > 1):
            st.plotly_chart((linechart(newdf, student))) # line chart appears only when >1 test entry
        st.dataframe(displaydf(newdf, student))
        



        


    

    

