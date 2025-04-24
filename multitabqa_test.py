from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd
import numpy as np
import json

# Using the MultiTabQA-base model
tokenizer = AutoTokenizer.from_pretrained("vaishali/multitabqa-base")
model = AutoModelForSeq2SeqLM.from_pretrained("vaishali/multitabqa-base")

# EXAMPLE QUESTION AND TABLE FORMAT PROVIDED BY MULTITABQA-BASE
# NOT TO BE USED WITH MTMI-QA

# question = "How many departments are led by heads who are not mentioned?"
# table_names = ['department', 'management']
# tables=[{"columns":["Department_ID","Name","Creation","Ranking","Budget_in_Billions","Num_Employees"],
#                   "index":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
#                   "data":[
#                           [1,"State","1789",1,9.96,30266.0],
#                           [2,"Treasury","1789",2,11.1,115897.0],
#                           [3,"Defense","1947",3,439.3,3000000.0],
#                           [4,"Justice","1870",4,23.4,112557.0],
#                           [5,"Interior","1849",5,10.7,71436.0],
#                           [6,"Agriculture","1889",6,77.6,109832.0],
#                           [7,"Commerce","1903",7,6.2,36000.0],
#                           [8,"Labor","1913",8,59.7,17347.0],
#                           [9,"Health and Human Services","1953",9,543.2,67000.0],
#                           [10,"Housing and Urban Development","1965",10,46.2,10600.0],
#                           [11,"Transportation","1966",11,58.0,58622.0],
#                           [12,"Energy","1977",12,21.5,116100.0],
#                           [13,"Education","1979",13,62.8,4487.0],
#                           [14,"Veterans Affairs","1989",14,73.2,235000.0],
#                           [15,"Homeland Security","2002",15,44.6,208000.0]
#                         ]
#                   },
#                   {"columns":["department_ID","head_ID","temporary_acting"],
#                     "index":[0,1,2,3,4],
#                     "data":[
#                             [2,5,"Yes"],
#                             [15,4,"Yes"],
#                             [2,6,"Yes"],
#                             [7,3,"No"],
#                             [11,10,"No"]
#                           ]
#                   }]


# helper function to flatten tables from example format, not useful with MTMI-QA
def linearize_table_base(table):
    # col: <columns> row 1 : <r | o | w | 1> row 2 : <r | o | w | 2 > ...
    #print(table.columns)
    flat = "col : "
    for col in table.columns:
        flat += col + " | "
    flat = flat[:-2]
    #print(flat)
    #print("Table Length:", table.shape[0])
    for i in range(table.shape[0]):
        flat += "row "+ str(i+1) + " : "
        for item in table.loc[i]:
            flat += str(item) + " | "
        flat = flat[:-2]
    #print(flat)
    return flat


# helper function to linearize MTMI-QA tables
def linearize_table_mtmiqa(table):
    # col: <columns> row 1 : <r | o | w | 1> row 2 : <r | o | w | 2 > ...
    flat = "col : "
    for col in table['columns']:
        flat += str(col) + " | "
    flat = flat[:-2]
    data = table['data']
    for i in range(len(data)):
        flat += "row "+ str(i+1) + " : "
        for item in data[i]:
            flat += str(item) + " | "
        flat = flat[:-2]
    return flat

# example from MultiTabQA-base
#input_tables = [pd.read_json(json.dumps(table), orient="split") for table in tables]

# specify MTMI-QA benchmark file here
benchmark_path = 'benchmark_od001.json'
with open(benchmark_path, 'r') as file:
    benchmark = pd.json_normalize(json.load(file))
input_tables = benchmark.loc[0, "tables"] # get tables from benchmark

# MultiTabQA-base requires the following input format:
# query + " " + <table_name> : table_name1 + flattened_table1 + <table_name> : table_name2 + flattened_table2 + ...
# If using their example data, would look like:
# model_input_string = """How many departments are led by heads who are not mentioned? <table_name> : department col : Department_ID | Name | Creation | Ranking | Budget_in_Billions | Num_Employees row 1 : 1 | State | 1789 | 1 | 9.96 | 30266 row 2 : 2 | Treasury | 1789 | 2 | 11.1 | 115897 row 3 : 3 | Defense | 1947 | 3 | 439.3 | 3000000 row 4 : 4 | Justice | 1870 | 4 | 23.4 | 112557 row 5 : 5 | Interior | 1849 | 5 | 10.7 | 71436 row 6 : 6 | Agriculture | 1889 | 6 | 77.6 | 109832 row 7 : 7 | Commerce | 1903 | 7 | 6.2 | 36000 row 8 : 8 | Labor | 1913 | 8 | 59.7 | 17347 row 9 : 9 | Health and Human Services | 1953 | 9 | 543.2 | 67000 row 10 : 10 | Housing and Urban Development | 1965 | 10 | 46.2 | 10600 row 11 : 11 | Transportation | 1966 | 11 | 58.0 | 58622 row 12 : 12 | Energy | 1977 | 12 | 21.5 | 116100 row 13 : 13 | Education | 1979 | 13 | 62.8 | 4487 row 14 : 14 | Veterans Affairs | 1989 | 14 | 73.2 | 235000 row 15 : 15 | Homeland Security | 2002 | 15 | 44.6 | 208000 <table_name> : management col : department_ID | head_ID | temporary_acting row 1 : 2 | 5 | Yes row 2 : 15 | 4 | Yes row 3 : 2 | 6 | Yes row 4 : 7 | 3 | No row 5 : 11 | 10 | No"""

# Get table names and flatten the tables for input
table_names = [t['name'] for t in input_tables]
flattened_tables = ''.join([f"<table_name> : {table_name} " + linearize_table_mtmiqa(table)
                            for table_name, table in zip(table_names, input_tables)])

# Run MultiTabQA-base on each question in the benchmark
questions = benchmark.loc[0,"questions"] # get questions from benchmark
for q in questions:
    question = q["question"]
    print("Question " + q['question_id'] + ": ",question)
    answer = q["answer"]
    print("Gold Answer: ",answer)
    flattened_input = question + " " + flattened_tables
    inputs = tokenizer(flattened_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    print("Model Answer")
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True))