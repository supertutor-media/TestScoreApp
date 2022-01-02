import streamlit as st

def main():
    st.title("Site Info")

    st.header("Student Progress")
    
    st.markdown("""
                In the Student Progress sections, see how individual students are scoring on their exams. 
                The bar chart highlights the highest scores achieved. The line chart shows how the scores have changed over time. 
                In the legends, click on specific sections to hide them from the graph.
                This graph can be used to see how specific students are scoring and how they are progressing over time.
                """)
    
    st.header("Class Progress")
    
    st.markdown("""
                In the Class Progress sections, see how test scores change over time for the entire class. 
                This graph shows how the class is progressing once students have taken multiple exams. 
                Each column represents the sequential order of tests taken (i.e. first test taken, second test taken) no matter which test it was.
                So the first bar is the average score on the first test taken, the second bar is the average score on the second test taken, etc.
                Thus this graph can be used to see if the class overall is progressing as they take more exams.
                """)
    return 0
