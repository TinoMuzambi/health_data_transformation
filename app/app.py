import streamlit as st
import pandas as pd
import json
import os

def generate_mapping_from_json(json_file, mapping_file):
    """_summary_
    """

    # Use the file directly instead of opening it.
    data = json.load(json_file)
    results = {}
    header = ''
    for prop in data['properties']:
        if data['properties'][prop]['type'] == 'object':
            if prop in data['required']:
                variables = data['properties'][prop]['properties']
                variables['record_id'] = {
                    'description': 'Record ID', 'type': 'autonumber'}
                for var in variables:
                    if 'enum' in variables[var]:
                        options = variables[var]['enum']
                        variables[var]['coding'] = '|'.join(
                            [f'{options.index(it)+1},{it}' for it in variables[var]['enum']])
                        variables[var]['enum'] = 'single_choice'
                    else:
                        variables[var]['coding'] = ''
                    for it in variables[var]:
                        if 'type' in variables[var]:
                            if 'string' in variables[var]['type']:
                                variables[var]['type'] = 'text'
                    study_format = ''
                    mapping = f'{var}='
                    if 'record_id' in var:
                        study_format = 'automated'
                    results[f'{list(variables.keys()).index(var)+1}'] = ['',
                                                                        '', '', study_format, var]+[val for val in variables[var].values()]
                    results[f'{list(variables.keys()).index(var)+1}'].append(mapping)
                    if header == '':
                        header = ['Study Variable Name', 'Study Variable Description', 'Study Variable Coding',
                                'Study Variable Format', 'NEW Variable Name']+list(variables[var].keys())
                        for h in range(len(header)):
                            if header[h] == 'type':
                                header[h] = 'NEW Variable Format'
                            if header[h] == 'description':
                                header[h] = 'NEW Variable Description'
                            if header[h] == 'coding':
                                header[h] = 'NEW Variable Coding'   
                        header.append('NEW to Study Mapping')

    res = pd.DataFrame.from_dict(results, orient='index', columns=header)
    # Return result
    return res.to_excel(f'{mapping_file}', index=None, header=True)
    


# Web page header setup.
st.title("eLwazi Phenotype Harmonisation Tool")
st.subheader("Description")
st.write("This tool was designed for the purposes of automating the transformation of data in a single dataset to fit the requirements for a harmonised dataset. It ingests two files: 	a .csv metadata mapping file a .csv dataset for transformation It generates a spreadsheet to facilitate the mapping of the dataset metadata to the harmonisation codebook. *")

# Web page body
st.divider()
# Need a way to specify the path to the folder as well as the file name. st.file_uploader doesn't provide that functionality.
filename = st.text_input(".csv dataset for transformation")
# Temporarily accept csv and JSON, eventually drop JSON.
mapping_file = st.file_uploader(".csv metadata mapping file", type=["csv", "json"])

if mapping_file and filename:
    # When harmonise button is clicked, generate the mapping file and save it to the bin directory.
    if st.button("Harmonise"):
        transformed_dataset = generate_mapping_from_json(mapping_file, os.path.join(os.getcwd(), "./bin/" + filename))

        # Download the file.
        with open(os.path.join(os.getcwd(), "./bin/" + filename), "rb") as file:
            btn = st.download_button(
                    label="Download data as xlsx",
                    data=file,
                    file_name=filename,
                    mime="application/vnd.ms-excel"
                )