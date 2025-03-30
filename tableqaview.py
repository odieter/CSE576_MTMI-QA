import json
import pandas as pd
from tabulate import tabulate

def visualize_schema(schema_path):
    # load json file
    with open(schema_path, 'r')as file:
        df = pd.json_normalize(json.load(file))
    tables = df.loc[0,"tables"]
    #print("Tables:",tables)

    # Iterate through all tables and display them
    for i in range(len(tables)):
        table = tables[i]
        #print("Table ",i,":", table)
        #print("Column names: ",table['columns'])
        #print("Data: ", table['data'])
        print(table['name'])
        tabledf = pd.DataFrame(table['data'], columns=table['columns'])
        print(tabulate(tabledf, headers = 'keys', tablefmt = 'psql'))


def visualize_questions(question_path):
    # load json file
    with open(question_path, 'r') as file:
        df = pd.json_normalize(json.load(file))
    for j in range(len(df)):
        question = df.loc[j]
        print("Question: ",question['question'])
        reasoning = question['intermediate_reasoning_steps']
        for i in range(len(reasoning)):
            print('Step ',reasoning[i]['step'],":",reasoning[i]['description'])
            print("\tUse table ",reasoning[i]['tables'])
            print("\tUse columns ",reasoning[i]['columns'])
        print("Primary keys:",question['primary_keys'])
        print("Foreign keys:",question['foreign_keys'])
        print("Answer: ", question['answer'])
        print("\n")


schema_path = './schema1.json'
question_path = './schema1questions.json'
visualize_schema(schema_path)
visualize_questions(question_path)



