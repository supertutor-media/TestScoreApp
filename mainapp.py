import info, actapp, actclass, satapp, satclass
import streamlit as st


Pages = {"Site Info": info, "ACT: Individual Student Progress": actapp, "ACT: Class Progress": actclass ,"SAT: Individual Student Progress": satapp, "SAT: Class Progress": satclass}

st.sidebar.title('ACT/SAT Score Analysis')
selection = st.sidebar.radio("Go to", list(Pages.keys()))

Pages[selection].main()