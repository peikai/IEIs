import pandas as pd 

table = pd.read_csv('tables/Li_candidates_calc.csv')

table.to_html('Li_candidates_calc.html')