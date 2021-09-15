import pandas as pd 

key_element = 'Li'
table = pd.read_csv('Tables/{element}/fullwindow.csv'.format(element=key_element))
table.to_html('fullwindow.html')