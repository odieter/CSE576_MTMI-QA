import json
import pandas as pd
from tabulate import tabulate

def visualize_schema(path):
    # load json file
    with open(path, 'r')as file:
        df = pd.json_normalize(json.load(file))
    tables = df.loc[0,"tables"]
    print("Tables:",tables)

    table_names = [t['name'] for t in tables]
    print(table_names)

    # Iterate through all tables and display them
    for i in range(len(tables)):
        table = tables[i]
        #print("Table ",i,":", table)
        #print("Column names: ",table['columns'])
        #print("Data: ", table['data'])
        print(table['name'])
        tabledf = pd.DataFrame(table['data'], columns=table['columns'])
        print(tabulate(tabledf, headers = 'keys', tablefmt = 'psql'))


def visualize_questions(path):
    # load json file
    with open(path, 'r') as file:
        df = pd.json_normalize(json.load(file))
    questions = df.loc[0,"questions"]
    for j in range(len(questions)):
        question = questions[j]
        print("Question: ",question['question'])
        print("Hops: ", question["num_hops"])
        challenge_types = question['challenge_types']
        print(challenge_types)
        # for i in range(len(challenge_types)):
        #     print(challenge_types[i])
        reasoning = question['intermediate_reasoning_steps']
        # for i in range(len(reasoning)):
        #     print('Step ',reasoning[i]['step'],":",reasoning[i]['description'])
        #     print("\tUse table ",reasoning[i]['tables'])
        #     print("\tUse columns ",reasoning[i]['columns'])
        # print("Primary keys:",question['primary_keys'])
        # print("Foreign keys:",question['foreign_keys'])
        print("Answer: ", question['answer'])
        print("\n")

def analyze_benchmark(path):
    # load json file
    with open(path, 'r') as file:
        df = pd.json_normalize(json.load(file))
    tables = df.loc[0,"tables"]
    questions = df.loc[0,"questions"]
    print("Number of tables: ",len(tables))
    #print("Number of questions: ", len(questions))

    # Data values to collect
    num_1hop = 0
    num_2hop = 0
    num_3hop = 0
    num_4hop = 0
    num_1table = 0
    num_2table = 0
    num_3table = 0
    num_4table = 0
    num_5table = 0
    num_6table = 0

    for j in range(len(questions)):
        question = questions[j]
        #print("Question: ",question['question'])
        num_hops = question['num_hops']
        if num_hops == 1: num_1hop+=1
        if num_hops == 2: num_2hop+=1
        if num_hops == 3: num_3hop+=1
        if num_hops == 4: num_4hop+=1

        num_tables = len(question['table_names'])
        if num_tables == 1: num_1table+=1
        if num_tables == 2: num_2table+=1
        if num_tables == 3: num_3table+=1
        if num_tables == 4: num_4table+=1
        if num_tables == 5: num_5table+=1
        if num_tables == 6: num_5table+=1

    print("Number of 1-hop Q's: ",num_1hop)
    print("Number of 2-hop Q's: ",num_2hop)
    print("Number of 3-hop Q's: ",num_3hop)
    print("Number of 4-hop Q's: ",num_4hop)
    print("Number of 1-table Q's: ",num_1table)
    print("Number of 2-table Q's: ",num_2table)
    print("Number of 3-table Q's: ",num_3table)
    print("Number of 4-table Q's: ",num_4table)
    print("Number of 5-table Q's: ",num_5table)
    print("Number of 6-table Q's: ",num_6table)



benchmark_path = 'Benchmarks/benchmark_ss004.json'
#visualize_schema(benchmark_path)
visualize_questions(benchmark_path)
#analyze_benchmark(benchmark_path)




