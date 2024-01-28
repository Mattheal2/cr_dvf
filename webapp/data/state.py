import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
from urllib.request import urlopen
import json


#Le 'state' est une variable globale accessible dans toute l'application. Le dataframe doit se trouver à l'intérieur pour être accessible partout. 


def get_default_data():
    data = pd.read_csv("webapp/data/valeursfoncieres-2022.txt", delimiter='|', decimal=',', low_memory=False)
    data = data.dropna(axis=1, how='all')
    data = data.drop_duplicates()
    for col in data.columns:
        if data[col].dtype == "object":
            data[col].fillna('None')
        elif col == 'Valeur fonciere':
            data[col].fillna(data[col].mean())
        else :
            data[col].fillna(0)
            
    data['Date mutation']=pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')
    data['Code departement']=data['Code departement'].astype(str)
    
    return data