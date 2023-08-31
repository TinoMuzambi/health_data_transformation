import streamlit as st

# Header setup.
st.title("eLwazi Phenotype Harmonisation Tool")
st.subheader("Description")
st.write("This tool was designed for the purposes of automating the transformation of data in a single dataset to fit the requirements for a harmonised dataset. It ingests two files: 	a .csv metadata mapping file a .csv dataset for transformation It generates a spreadsheet to facilitate the mapping of the dataset metadata to the harmonisation codebook. *")

# Body
st.file_uploader(".csv metadata mapping file",type="csv,json",)
st.file_uploader(".csv dataset for transformation",type="csv")

st.button("Harmonise")