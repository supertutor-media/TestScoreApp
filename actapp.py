import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def testtype(scores):
    """
    input: csv with raw score data
    output: cleaned dataframe, removes values without email or test, creates new boolean test column
    """
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

def groupbar(ACT, email):
    df1 = ACT[ACT['Email'] == email]
    df2 = df1[['Email','Test', 'ACT Total Score','ACT English Score', 
               'ACT Math Score', 'ACT Reading Score', 'ACT Science Score']]
    df3 = df2.groupby(['Email', 'Test']).max().reset_index() # get superscore for day
    fig = px.bar(df3, x="Test", y=['ACT English Score', 'ACT Math Score', 'ACT Reading Score','ACT Science Score'], 
                 title= "ACT scores for " + email,
                 hover_name = 'ACT Total Score',
                 labels=dict(variable = 'Section', value = 'Score'),
                 barmode = 'group')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def linechart(ACT, email):
    df1 = ACT[ACT['Email'] == email]
    df2 = df1[['Email', 'Test taken', 'Test name', 'ACT English Score', 'ACT Math Score', 'ACT Reading Score','ACT Science Score', 'ACT Total Score']]
    df3 = df2.groupby(['Email', 'Test taken', 'Test name']).max().reset_index().sort_values(by=['Test taken'])
    fig = px.line(df3, x='Test taken', y=['ACT English Score', 'ACT Math Score', 'ACT Reading Score','ACT Science Score', 'ACT Total Score'],
                  title = 'ACT scores over time for ' + email,
                  labels=dict(variable = 'Section', value = 'Score'))
    return fig

def displaydf(ACT, email):
    df = ACT[ACT['Email'] == email][['Test taken', 'Test name', 'ACT Total Score', 
       'ACT English Score', 'ACT Math Score', 'ACT Reading Score', 'ACT Science Score']].sort_values(by="Test taken")
    df = df.reset_index().drop(columns= ['index'])
    df = df.rename(columns={'Test taken': 'Date', 'Test name': 'Test', 'ACT Total Score': 'Total Score',
                            'ACT Reading Score': 'Reading','ACT English Score': 'English',
                            'ACT Math Score': 'Math', 'ACT Science Score': 'Science'})
    return df

def main():  
    st.title('ACT: Track Individual Student Progress')
    uploaded_file = st.file_uploader("Choose a file", ["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        newdf = clean(df)
        student = st.selectbox('Select a student', newdf.Email.unique())
        st.plotly_chart((groupbar(newdf, student)))
        if(len(newdf[newdf['Email'] == student]['Test'].unique()) > 1):
            st.plotly_chart((linechart(newdf, student))) # line chart appears only when >1 test entry
        st.dataframe(displaydf(newdf, student))
