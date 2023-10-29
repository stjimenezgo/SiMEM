# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 20:08:13 2023

@author: StevenJG
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.cm as cm
from matplotlib import rcParams

# Configuración de entrada

dFec = "2023-10-26"

# Conexión a la información de SiMEM

url = "https://www.simem.co/backend-files/api/PublicData?startdate=" + dFec + "&enddate=" + dFec + "&datasetId=2bff14"
response = requests.get(url)

# Organización de información en una tabla Pandas

data = pd.read_json(response.text)
aportes_hidr = pd.json_normalize(data.loc['records']['result'])

# Configuración de la información por región

aportes_hidr_grp = aportes_hidr.groupby(by='RegionHidrologica').sum()
aportes_hidr_grp['PorcentajeHidricoEnergia'] = 100 * aportes_hidr_grp['AportesHidricosEnergia'] / aportes_hidr_grp['MediaHistoricaEnergia']
aportes_sv = aportes_hidr_grp['PorcentajeHidricoEnergia'].sort_values(ascending = False)

# Configuración de imagen

rcParams['font.sans-serif'] = ['Calibri']

ax = aportes_sv.plot.barh(color = cm.rainbow(np.linspace(0, 1, len(aportes_hidr_grp))))
ax.set_title('Aportes de energía agregados por Región en Porcentaje')
ax.set_xlabel('Porcentaje [%]')
ax.set_ylabel('')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

for i, v in enumerate(aportes_sv.tolist()):
    ax.text(v + np.max(aportes_sv)*0.05, i, '{:1.1f}'.format(v), va = 'center')
