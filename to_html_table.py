import pandas as pd 

table_calc = pd.read_csv('tables/K/K_candidates_calc.csv')
table_exp = pd.read_csv('tables/K/K_candidates_exp.csv')
table_all = pd.read_csv('tables/K/K_candidates_all.csv')

table_calc.to_html('tables/K/K_candidates_calc.html')
table_exp.to_html('tables/K/K_candidates_exp.html')
table_all.to_html('tables/K/K_candidates_all.html')