import streamlit as st
# %%
import argparse,sys
import csv
import traceback
import logging
from inspect import currentframe
import pandas as pd

# %%
def get_linenumber():
    """Print code line in logging

    Returns:
        _type_: _description_
    """
    cf = currentframe()
    return cf.f_back.f_lineno

# %%
def isfloat(num):
    """
    Check if string is float
    
    Args:
        num (_type_): string

    Returns:
        _type_: True is float or Flase if not
    """
    try:
        float(num)
        return True
    except ValueError:
        return False
   
# %% 


def error_message(code, format='', record='', options='', cline='', var='', var1='', format1='', format2='', format3='', format4='', format5='', mapfile='', var_value='', dline='', nfields='', nfields_1='', CRED='\033[91m', CEND='\033[0m', CGREEN='\033[9'):
    """Print error message

    Args:
        code (_type_): _description_
        format (str, optional): _description_. Defaults to ''.
        record (str, optional): _description_. Defaults to ''.
        options (str, optional): _description_. Defaults to ''.
        cline (str, optional): _description_. Defaults to ''.
        var (str, optional): _description_. Defaults to ''.
        var1 (str, optional): _description_. Defaults to ''.
        format1 (str, optional): _description_. Defaults to ''.
        format2 (str, optional): _description_. Defaults to ''.
        format3 (str, optional): _description_. Defaults to ''.
        format4 (str, optional): _description_. Defaults to ''.
        format5 (str, optional): _description_. Defaults to ''.
        mapfile (str, optional): _description_. Defaults to ''.
        var_value (str, optional): _description_. Defaults to ''.
        dline (str, optional): _description_. Defaults to ''.
        nfields (str, optional): _description_. Defaults to ''.
        nfields_1 (str, optional): _description_. Defaults to ''.
        CRED (str, optional): _description_. Defaults to '\033[91m'.
        CEND (str, optional): _description_. Defaults to '\033[0m'.
    """
    
    record = f'{record[:150]} ...'
    line = f'{CRED}(Code line{CEND} {cline}{CRED}){CEND}'

    ## Mapping file
    message = {
        18: f'{CRED}\nError: Incosistent number of fields ({nfields_1} vs {nfields} expected) for Study Variable "{var}" and New Variable "{var1}" record -- "{record}" {CEND} (Record No {dline}, Code line {cline})\n',
        4: f'{CRED}\nError_4_{cline}: Wrong option "{options}" for record -- "{record}" {CEND}\n',
        ### Format
        8: f'{CRED}\nError: Empty Variable Format "{format}" for Study Variable "{var}" and New Variable "{var1}" record -- "{record}" {CEND} (Record No {dline}, Code line {cline})\n',
        9: f'{CRED}\nError: Duplicate Study Variable Name "{var}" for record -- "{record}" {CEND} (Code line {cline})\n',
        1: f'{CRED}\nError: "NEW Variable Name" variable missing on Study Variable{CEND} "{var1}" {CRED}for record --{CEND} "{record}" {line}\n',
        2: f'{CRED}\nError: "Study Variable Format" variable missing for record -- "{record}" {CEND} (Code line {cline})\n',
        3: f'{CRED}\nError: "Study Variable Name" or "Study Variable Format" variable missing for record -- "{record}" {CEND} (Code line {cline})\n',
        5: f'{CRED}\nError: Coding{CEND} "{var}" {CRED}not included in mapping{CEND} "{options}" {CRED}in record{CEND} "{record}" {CRED}(Code line{CEND} {cline}{CRED}){CEND}\n',
        6: f'{CRED}\nError: Wrong Variable Format "{format}" in mapping file "{mapfile}" for record -- "{record}" {CEND} (Code line {cline})\n',
        7: f'{CRED}\nError: Unrecognized format of mapping file "{mapfile}" {CEND} (Code line {cline})\n',
        
        
        10: f'{CRED}\nError: Study Variable Name "{var}" not included in mapping file "{mapfile}" for record "{record}" {CEND} (Code line {cline})\n',
        11: f'{CRED}\nError_11_{cline} (Data/Mapping files):{CEND} Study Variable Name {CRED}"{var}"{CEND} not included "NEW to Study Mapping" field for record {CRED}"{record}" {CEND} (Record No {dline})\n',
        12: f'{CRED}\nError: Empty "Study Variable Name" for record "{record}" {CEND} (Code line {cline})\n',
        13: f'{CRED}\nError_13_{cline}: Empty "New to Study Mapping" for "{var}" for record "{record}" {CEND}\n',

        ### Variable
        15: f'{CRED}\nError: Wrong Variable{CEND} "{var}" {CRED}type for record --{CEND} "{record}" {line}\n',

        ## No Exit
        101: f'{CRED}\nWarning_101_{cline} (Data file): Study Variable Name {CEND}"{var}"{CRED} not included in mapping file {CEND}"{mapfile}" {CRED}for record "{record}", and will be ignored.{CEND} (Record No {dline})\n',
        102: f'{CRED}\nError: Invalid "New to Study Mapping": "{var}" for record "{record}" {CEND} (Code line {cline})\n',
        ## Value
        17: f'{CRED}\nError (Data file): Invalid value "{var_value}" for variable "{var}" of type "{format}" for record "{record}" {CEND} (Record No {dline}, Code line {cline})\n',
    }
    
    try:
        print(message[code])
    except KeyError as e:
        print(e)
    # except IndexError as e:
    #     print(e)
    finally:
        if code < 100:
            sys.exit(0)

#%%
def read_mapping(mapping_file):
    """_summary_

    Args:
        mapping_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    study_data = {}
    option_formats = ['text', 'integer', 'number', 'single_choice', 'hardcode', 'automated', 'date_y', 'not_recorded'] ## with formula must be computed last
    mapping_variables = []
    if mapping_file.endswith(".xlsx"):
        mapping_f = pd.read_excel(
            mapping_file, keep_default_na=False, dtype=str)
        data = mapping_f.T.to_dict()
        data = list(data.values())
    # TODO support CSV, google sheet
    # with open(mapping_file, newline='') as csvfile:
    #     data = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for item in data:
        item = {k.lower().strip(): v.strip() for k, v in item.items() if k!='' and k!=None}
        item_str = ', '.join([':'.join([key, item[key]]) for key in item if key != None and item[key] != None]) # to use for error logging
        if 'study variable name' in item and 'study variable format' in item and 'new variable name' in item and 'new variable format' in item and 'new to study mapping' in item:
            ## Get expected size for record
            nfields = len(item)
        else:
            error_message(code=3, record=item_str,
                            cline=(get_linenumber()))

        ## Get variables
        study_var = item['study variable name'] #TODO check this is not empty
        study_options = item['study variable coding']
        study_format = item['study variable format']
        new_var = item['new variable name']
        new_options = item['new variable coding']
        new_format = item['new variable format']
        new_to_study_mapping = item['new to study mapping']
        
        ## Check that size of this record is correct
        nfields_1 = len(item)
        if nfields_1 != nfields:
            error_message(code=18, record=item_str,
                            nfields_1=nfields_1, nfields=nfields, var=study_var, var1=new_var, cline=(get_linenumber()))
        
        if item['study variable format'] != '':
            if study_format in [ 'automated', 'hardcode' ] and study_var == '':
                study_var = new_var
                if study_var not in study_data:
                    study_data[study_var] = {}
                else:
                    error_message(code=9, record = item_str, var=study_var, cline=(get_linenumber())) 
            elif study_format in ['not_recorded']:
                study_var = new_var
                if study_var not in study_data:
                    study_data[study_var] = {}
                else:
                    error_message(code=9, record=item_str, var=study_var, cline=(get_linenumber()))
            elif study_format in ['text', 'date_y', 'integer', 'number', 'single_choice']: ## Can not be empty
                if study_var == '':
                    error_message(code=8, var=study_var, var1=new_var, record=item_str, cline=(get_linenumber()))
                if study_var not in study_data:
                    study_data[study_var] = {}
                else:
                    error_message(code=9, record=item_str, var=study_var, cline=(get_linenumber()))
            else:
                error_message(
                    code=6, format=study_format, record=item_str, cline=(get_linenumber()))
                    
            if study_format in ['automated', 'hardcode', 'text', 'date_y', 'integer', 'number', 'single_choice', 'not_recorded']:
                study_data[study_var]['study_var'] = study_var
                study_data[study_var]['study_options'] = study_options
                study_data[study_var]['study_format'] = study_format
                study_data[study_var]['new_var'] = new_var
                study_data[study_var]['new_options'] = new_options
                study_data[study_var]['new_format'] = new_format
                study_data[study_var]['new_to_study_mapping'] = new_to_study_mapping
                
                if study_var not in mapping_variables:  # Store variable to keep order
                    mapping_variables.append(study_var)
                
            if study_format in ['text', 'number', 'integer', 'date_y', 'single_choice']:
                if new_to_study_mapping == '':
                    error_message(code=13, var=study_var, options=new_options,
                                    record=item_str, cline=(get_linenumber()))
                new_options_ = {}
                try:
                    for it in [it for it in new_to_study_mapping.split("|")]:
                        newStr = it.split('=')
                        if len(newStr) < 1:
                            error_message(
                                code=4, options=new_options, record=item_str, cline=(get_linenumber()))
                        try:
                            new_options_[
                                newStr[0].strip()] = newStr[1].strip().replace('\'', '')
                        except:
                            error_message(code=4, options=new_options, record=item_str, cline=(get_linenumber()))
                except:
                    error_message(code=13, var=new_to_study_mapping,
                                    record=item_str, cline=(get_linenumber()))
                study_data[study_var]['new_to_study_mapping'] = new_options_
    # return variables list as well to use during convertion
    return study_data, mapping_variables

# %%
def pheno_mapping(pheno_file, mapping_file, warn=False):
    """_summary_

    Args:
        pheno_file (_type_): _description_
        mapping_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    datas = {}
    variables = []
    mapping,mapping_variables = read_mapping(mapping_file)
    values = {}
    
    if pheno_file.endswith(".xlsx"):
        pheno_f = pd.read_excel(pheno_file, keep_default_na=False, dtype=str)
        data = pheno_f.T.to_dict()
        data = list(data.values())
    
    # print(data)
    record = 1
    new_records = {}
    phenos_1 = []
    phenos_2 = []
    dline = 0
    not_in_mapping = []
    
    for item in data:
        item = {k.strip(): v.strip() for k, v in item.items()}
        item_str = ', '.join([item[key] for key in item])  # Used for error logging
        new_item = {}
        dline += 1
        for var in item:
            if var in mapping_variables:
                if var in mapping and 'new_to_study_mapping' in mapping[var] and 'new_var' in mapping[var] and 'new_format' in mapping[var]:
                    var_format = mapping[var]['study_format']
                    new_var = mapping[var]['new_var']
                    new_format = mapping[var]['new_format']
                    new_to_study_mapping = mapping[var]['new_to_study_mapping']
                    study_value = item[var]
                                        
                    if new_var == '':
                        error_message(code=1, var=new_var, var1=var, record=item_str, cline=(get_linenumber()))
                    
                    if var_format in ['text', 'number', 'integer', 'date_y', 'single_choice']:
                        if new_to_study_mapping == '':
                            error_message(code=13, var=var, record=item_str, cline=(get_linenumber()))
                        if new_var not in new_to_study_mapping:
                            error_message(
                                code=11, var=var, record=item_str, cline=(get_linenumber()))
                        # print(
                            # new_to_study_mapping[new_var.strip().lower()], var.strip().lower())
                        if new_to_study_mapping[new_var.strip()] != var.strip():
                            error_message( code=11, var=var, record=item_str, cline=(get_linenumber()))
                        if new_var not in phenos_2:  # Store variable to keep order
                            phenos_2.append(new_var)
                    
                    if var_format == 'text':  # Case 1
                        if new_var in new_to_study_mapping and (new_format == 'text' or new_format == 'single_choice'): 
                            value = ''
                            if new_format == 'text': ## text -> text
                                # Check that mapping of new variable  = study variable
                                if study_value != '':
                                    value = study_value
                                else:
                                    not_found = True  # To check in value found in new mapping
                                    for new_value in new_to_study_mapping:
                                        if new_to_study_mapping[new_value] == '': ## e.g. 999=''
                                            value = new_value
                                            not_found = False
                                    if not_found:
                                        error_message(code=5, var=study_value, options=new_to_study_mapping,record=item_str, cline=(get_linenumber()))
                            elif new_format == 'single_choice':  # text -> single_choice
                                not_found = True  # To check in value found in new mapping
                                for new_value in new_to_study_mapping:
                                    # e.g. South Africa = South_Africa or 999=''
                                    if new_to_study_mapping[new_value].strip().lower() == study_value.strip().lower():
                                        value = new_value
                                        not_found = False
                                if not_found:
                                    error_message(code=5, var=study_value, options=new_to_study_mapping,
                                                    record=item_str, cline=(get_linenumber()))
                            else:
                                print(new_format, new_to_study_mapping, var, new_var)
                        else:
                            error_message(code=11, var=var, record=item_str, cline=(get_linenumber()))
                                                
                    elif var_format == 'number':
                        if new_format == 'number':  # number -> number
                            # Check that mapping of new variable  = study variable
                            if study_value != '':
                                value = str(study_value)
                                if not isfloat(value): ## Check if not float
                                    error_message(code=16, var=var, var_value=value, format=new_format, options=new_to_study_mapping, record=item_str, cline=(get_linenumber()))
                            else:
                                not_found = True  # To check in value found in new mapping
                                for new_value in new_to_study_mapping:
                                    if new_to_study_mapping[new_value] == '':  # e.g. 999=''
                                        value = new_value
                                        not_found = False
                                if not_found:
                                    error_message(code=5, var=study_value, options=new_to_study_mapping,record=item_str, cline=(get_linenumber()))
                        else:
                            error_message(
                                code=11, var=var, record=item_str, cline=(get_linenumber()))
                                                
                    elif var_format in ['integer', 'date_y']:
                        if new_format == 'integer':  # integer, date_y -> integer
                            # Check that mapping of new variable  = study variable
                            if study_value != '':
                                value = str(study_value)
                                if not value.isdigit():  # check if value is number
                                    error_message(code=17, var=var, var_value=value, format=new_format, options=new_to_study_mapping, record=item_str, dline=dline, cline=(get_linenumber()))
                            else:
                                not_found = True  # To check in value found in new mapping
                                for new_value in new_to_study_mapping:
                                    if new_to_study_mapping[new_value] == '':  # e.g. 999=''
                                        value = new_value
                                        not_found = False
                                if not_found:
                                    error_message(code=5, var=study_value, options=new_to_study_mapping,                                                       record=item_str, cline=(get_linenumber()))
                        else:
                            error_message(
                                code=11, var=var, record=item_str, cline=(get_linenumber()))
                    
                    elif var_format == 'single_choice':  # Case 
                        if new_var in new_to_study_mapping and new_format == 'single_choice':  # single_choice -> single_choice
                            value = ''
                            not_found = True  # To check in value found in new mapping
                            for new_value in new_to_study_mapping:
                                # e.g. South Africa = South_Africa or 999=''
                                if study_value.strip().lower() in new_to_study_mapping[new_value].strip().lower():
                                    value = new_value
                                    not_found = False
                                    continue
                            if not_found:
                                error_message(code=5, var=study_value, options=new_to_study_mapping,
                                                record=item_str, cline=(get_linenumber()))
                        else:
                            error_message(
                                code=11, var=var, record=item_str, cline=(get_linenumber()))

                    if var_format in ['text', 'number', 'integer', 'date_y', 'single_choice']:
                        globals()[new_var] = value
                        new_item[new_var] = value
                        # if 'record_id' in new_var:
                        values[new_var] = value
                    
                else:
                    error_message(code=10, var=var,
                                record=item_str, cline=(get_linenumber()))
            else:
                if var not in not_in_mapping:
                    if warn:
                        error_message(code=101, var=var,
                                        record=item_str, mapfile=mapping_file, dline=dline, cline=(get_linenumber()))
                not_in_mapping.append(var)
        ### Write automated, hardcode records
        for var in mapping_variables:
            if var in mapping:
                study_format = mapping[var]['study_format']
                study_var = mapping[var]['study_var']
                new_var = mapping[var]['new_var']
                new_to_study_mapping = mapping[var]['new_to_study_mapping']
                
                if study_format in ['automated', 'hardcode']:  # Case
                    ## Store variable to keep order
                    if study_var not in phenos_1:
                        phenos_1.append(study_var)
                    if new_to_study_mapping == '':
                        error_message(code=8, format=var_format, var=study_var, var1=new_var, record=item_str, cline=(get_linenumber()))
                    elif study_var in new_to_study_mapping:
                        var_ = [it.strip()
                                for it in new_to_study_mapping.split('=')]
                        if new_var == var_[0].strip() and new_var != 'record_id':
                            value = var_[1]
                            if study_format == 'hardcode':
                                value = value.replace('\'', '')
                            # if '{' in value and '}' in value:
                            #     value = value.format(pid=values['pid'])
                            new_item[new_var] = value
                        elif new_var == 'record_id':
                            new_item[new_var] = record
                            record += 1
                        else:
                            error_message(
                                code=11, var=study_var, record=item_str, dline=dline, cline=(get_linenumber()))
                    else:
                        error_message(
                            code=11, var=study_var, record=item_str, dline=dline, cline=(get_linenumber()))
            else:
                error_message(code=11, var=study_var,
                                record=item_str, dline=dline, cline=(get_linenumber()))
        new_records[new_item['record_id']] = new_item
        
    variables = phenos_1 + phenos_2
    
    if not warn:
        print(
            f'{CRED}|-- {len(not_in_mapping)} warnings found. To print use warn=True{CEND}')
                
    return new_records, variables

# %%

def main(pheno_file, mapping_file, pheno_output, warn=False):
    """_summary_

    Args:
        pheno_file (_type_): _description_
        mapping_file (_type_): _description_
        pheno_output (_type_): _description_
        warn (bool, optional): _description_. Defaults to False.
    """
    CRED = '\033[91m'
    CGREEN = '\033[92m'
    CEND = '\033[0m'
    print(
        f'Reading mapping file {CGREEN}{mapping_file}{CEND} and phenotype file {CGREEN}{pheno_file}{CEND} ...')
    new_records, phenos = pheno_mapping(pheno_file, mapping_file, warn)
    output = open(pheno_output, 'w')
    output.writelines(','.join([str(it) for it in phenos])+'\n')
    print(
        f'Writing output to {CGREEN}{pheno_output}{CEND} ...')
    for pid in sorted(new_records):
        datas = []
        for cvs_pheno in phenos:
            if cvs_pheno in new_records[pid]:
                datas.append(new_records[pid][cvs_pheno])
        output.writelines(','.join([str(it) for it in datas])+'\n')
    output.close()

## TODO check duplicate variable in data sheet
# %%


# Web page header setup.
st.title("eLwazi Phenotype Harmonisation Tool")
st.header("Perform Mapping")
st.subheader("Description")
st.write("This tool was designed for the purposes of automating the transformation of data in a single dataset to fit the requirements for a harmonised dataset. It ingests two files: 	a .csv metadata mapping file a .csv dataset for transformation It generates a spreadsheet to facilitate the mapping of the dataset metadata to the harmonisation codebook. *")

# Web page body.
# Temporarily accept csv and xlsx, eventually drop xlsx.
mapping_file = st.file_uploader(".csv metadata mapping file", type=["csv", "xlsx"])
# First dataset
first_dataset = st.file_uploader("First dataset", type=["csv", "xlsx"])
# Second dataset
second_dataset = st.file_uploader("Second dataset", type=["csv", "xlsx"])

if mapping_file and first_dataset and second_dataset:
    # When harmonise button is clicked, harmonise the datasets.
    if st.button("Harmonise"):
        main(first_dataset, mapping_file, second_dataset)