import geoviews as gv
import plotly.express as px
gv.extension('bokeh')
import geopandas as gpd
import pandas as pd

#Chaque fonctions renvoie un graphe au format HTML

def get_graph1(data):
  moy_prixdep = data.groupby('Code departement')['Valeur fonciere'].mean().reset_index()

  sf = gpd.read_file('webapp/data/departements-version-simplifiee.geojson')
  jf=sf.merge(moy_prixdep, left_on='code', right_on='Code departement')
  departements=gv.Polygons(jf, vdims=['nom', 'Valeur fonciere'])
  departements.opts(width=500, height=370, tools=['hover'], aspect='equal')

  gv.renderer('bokeh').save(departements, 'webapp/data/graph1')
  return open('webapp/data/graph1.html').read()
  
def get_graph2(data):
  regions = {
    'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
    'Bretagne': ['35', '22', '56', '29'],
    'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
    'Corse': ['2A', '2B'],
    'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    'Hauts-de-France': ['02', '59', '60', '62', '80'],
    'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'Normandie': ['14', '27', '50', '61', '76'],
    'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    'Pays de la Loire': ['44', '49', '53', '72', '85'],
    'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
  }

  def map_departement_region(departement):
    for region, deps in regions.items():
        if departement in deps:
            return region
    return "Outre-Mer"


  data['Region']= data['Code departement'].apply(map_departement_region)

  moy_prixreg = data.groupby('Region')['Valeur fonciere'].mean().reset_index()
  
  sf = gpd.read_file('webapp/data/regions.geojson')
  jf=sf.merge(moy_prixreg, left_on='nom', right_on='Region')
  regions=gv.Polygons(jf, vdims=['nom', 'Valeur fonciere'])
  regions.opts(width=500, height=370, tools=['hover'], aspect='equal')
  
  gv.renderer('bokeh').save(regions, 'webapp/data/graph2')
  return open('webapp/data/graph2.html').read()
  
def get_graph3(data):
  propri_piecesnonnull=data[data["Nombre pieces principales"]>0]
  prix_pieces = propri_piecesnonnull.groupby('Nombre pieces principales')['Valeur fonciere'].mean()
  prix_pieces_df=prix_pieces.reset_index(name='Moyenne valeur fonciere')
  nombre_propri=propri_piecesnonnull.groupby('Nombre pieces principales').size().reset_index(name='Nombre de propriétés avec ce nombre de pièces')
  valnbpiecesfin=pd.merge(prix_pieces_df, nombre_propri, on="Nombre pieces principales")

  valnbpiecesfin=valnbpiecesfin[valnbpiecesfin['Nombre de propriétés avec ce nombre de pièces']>=20]
  
  fig=px.bar(valnbpiecesfin, x='Nombre pieces principales', y='Moyenne valeur fonciere', height=400, width=600)
  #fig=px.box(dvf2022_final, x='Nombre pieces principales', y='Valeur fonciere')
  return fig.to_html()
  