# CSE576_MTMI-QA

Code repository for the MTMI-QA Dataset Benchmark.

The benchmark files are located in the Benchmarks folder. Data in MTMI-QA is stored in a JSON format containing the tables and corresponding annotated QA pairs.

tableqaview.py contains code to visualize the tables and QA pairs from a specified JSON benchmark file.

multitabqa_test.py contains code to run the MultiTabQA-base model on a benchmark file and report its answers for each question. gemini_batch_benchmark.py contains code for running Gemini end-to-end QA. The Binder file and TableCoT folder contains code to run those respective methods as well.

kaggle.ipynb contains code for the dataset generation pipeline.



