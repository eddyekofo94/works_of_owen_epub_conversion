import re

with open('qa/bug_regression_baselines.json', 'r') as f:
    text = f.read()

# I will just write a python script to load the base JSON, then add the new volumes manually
