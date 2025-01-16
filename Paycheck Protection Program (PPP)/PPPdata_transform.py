# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 16:16:44 2022

@author: ytao4
"""
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.io as pio
#pio.renderers.default = 'svg'
import seaborn as sns
pio.renderers.default = 'browser'

import pandas as pd

df = pd.read_csv('public_up_to_150k_12_220102.csv')

df.columns

df_flag=pd.DataFrame()
df_flag

df_flag['LoanNumber'] =df['LoanNumber']


"""D_address"""
df_flag['D_BorrowerAddress'] = df["BorrowerAddress"].duplicated(keep=False)


df_flag["D_BorrowerAddress"] = df_flag["D_BorrowerAddress"].astype(int)

df_flag["D_BorrowerAddress"].hist(bins=2)


"""D_BorrowerName"""
"""D_BorrowerName"""

df_flag['D_BorrowerName'] = df["BorrowerName"].duplicated(keep=False)

df_flag["D_BorrowerName"] = df_flag["D_BorrowerName"].astype(int)
df_flag["D_BorrowerName"].sum()

df_flag["D_BorrowerName"].hist(bins=2)

"""Forgiveness"""
df_flag["Forgiveness"] = (df["ForgivenessAmount"] > 0).astype(int)



"""LoanStatus"""
df1 = pd.concat([pd.get_dummies(df[['LoanStatus']] , drop_first=True), df], axis=1)
df1.columns

df_flag['LoanStatus_Paid in Full']= df1['LoanStatus_Paid in Full']
df_flag['LoanStatus_Paid in Full'].hist(bins=2)


"""BusinessAgeDescription"""
df_flag["No_BusinessAgeDescription"] = (df["BusinessAgeDescription"] == 'Unanswered').astype(int)
df_flag["No_BusinessAgeDescription"].sum()

df_flag["LT2_BusinessAgeDescription"] = (df["BusinessAgeDescription"] == 'New Business or 2 years or less').astype(int)
df_flag["LT2_BusinessAgeDescription"].sum()



"""HubzoneIndicator"""
df_flag["HubzoneIndicator"] = (df["HubzoneIndicator"] == 'Y').astype(int)
df_flag["HubzoneIndicator"].sum()


"""RuralUrbanIndicator"""
df_flag["RuralUrbanIndicator"] = (df["RuralUrbanIndicator"] == 'R').astype(int)
df_flag["RuralUrbanIndicator"].sum()

"""df["JobsReported"]"""
df_flag["No_JobsAmount"] =  (df["JobsReported"] == 0).astype(int)
df_flag["No_JobsAmount"].sum()

df["JobsReported"].describe()
df["JobsReported"] = df["JobsReported"].replace(0,1)
#df["JobsReported"] = df["JobsReported"].replace(-6,6)


"""avg_amountPerEmployee"""
#df["CurrentApprovalAmount"].describe()
#df["JobsReported"].describe()
#df["CurrentApprovalAmount"].hist(bins=2)


df["avg_amountPerEmployee"] = df["CurrentApprovalAmount"] / df["JobsReported"]
df["avg_amountPerEmployee"].isnull().sum()
df["avg_amountPerEmployee"].hist(bins=100)

df_flag["avg_amountPerEmployee"] = (df["avg_amountPerEmployee"] >25000).astype(int)
df_flag["avg_amountPerEmployee"].sum()


df["avg_amountPerEmployee"].describe()

df_flag.to_csv('flag_public_up_to_150k_12_220102.csv',index=False)

####
is_2002 =  df['avg_amountPerEmployee'] < 25000
gapminder_2002 = df[is_2002]
gapminder_2002["avg_amountPerEmployee"].hist(bins=100)



plt.boxplot(df["avg_amountPerEmployee"])


sns.boxplot(df["avg_amountPerEmployee"])
sns.boxplot(gapminder_2002["avg_amountPerEmployee"])



#heat map read indicator only
import pandas as pd

df1 = pd.read_csv('flag_public_150k_plus_220102.csv')
df2 = pd.read_csv('flag_public_up_to_150k_1_220102.csv')
df3 = pd.read_csv('flag_public_up_to_150k_2_220102.csv')
df4 = pd.read_csv('flag_public_up_to_150k_3_220102.csv')
df5 = pd.read_csv('flag_public_up_to_150k_4_220102.csv')
df6 = pd.read_csv('flag_public_up_to_150k_5_220102.csv')
df7 = pd.read_csv('flag_public_up_to_150k_6_220102.csv')
df8 = pd.read_csv('flag_public_up_to_150k_7_220102.csv')
df9 = pd.read_csv('flag_public_up_to_150k_8_220102.csv')
df10 = pd.read_csv('flag_public_up_to_150k_9_220102.csv')
df11 = pd.read_csv('flag_public_up_to_150k_10_220102.csv')
df12 = pd.read_csv('flag_public_up_to_150k_11_220102.csv')
df13 = pd.read_csv('flag_public_up_to_150k_12_220102.csv')
frames = [df1, df2, df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13]

df = pd.concat(frames)
df.columns

#df.iloc[:, 1:].describe().to_csv("my_description.csv")
df.describe()


import numpy as np
from matplotlib.ticker import PercentFormatter

input_df = df["Forgiveness"]

plt.hist(input_df,bins=[0,0.5,1], 
         weights=np.ones(len(input_df)) / len(input_df))
plt.xticks((0,1))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

"""
import pandas as pd
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 11)
pd.set_option('display.width', 100)
"""



#heat map

df.iloc[:, 1:] 
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(16, 10))
# Store heatmap object in a variable to easily access it when you want to include more features (such as title).
# Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
heatmap = sns.heatmap(df.iloc[:, 1:].corr(), vmin=-1, vmax=1, annot=True)
# Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);



#geo map


df1 = pd.read_csv('public_150k_plus_220102.csv')
df2 = pd.read_csv('public_up_to_150k_1_220102.csv')
df3 = pd.read_csv('public_up_to_150k_2_220102.csv')
df4 = pd.read_csv('public_up_to_150k_3_220102.csv')
df5 = pd.read_csv('public_up_to_150k_4_220102.csv')
df6 = pd.read_csv('public_up_to_150k_5_220102.csv')
df7 = pd.read_csv('public_up_to_150k_6_220102.csv')
df8 = pd.read_csv('public_up_to_150k_7_220102.csv')
df9 = pd.read_csv('public_up_to_150k_8_220102.csv')
df10 = pd.read_csv('public_up_to_150k_9_220102.csv')
df11 = pd.read_csv('public_up_to_150k_10_220102.csv')
df12 = pd.read_csv('public_up_to_150k_11_220102.csv')
df13 = pd.read_csv('public_up_to_150k_12_220102.csv')
frames = [df1, df2, df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13]

df = pd.concat(frames)
df.columns
df = df[['CurrentApprovalAmount','BorrowerState','JobsReported']]

"""
df = pd.read_csv('public_150k_plus_220102.csv')
df.columns
"""
df = df.dropna(subset=['BorrowerState'])

df["JobsReported"].describe()

#df_group['avg_amountPerEmployee'].describe()
# replace value 0 to 1, -6 to 6
df["JobsReported"] = df["JobsReported"].replace(0,1)
df["JobsReported"] = df["JobsReported"].replace(-6,6)

df["avg_amountPerEmployee"] = df["CurrentApprovalAmount"] / df["JobsReported"]
df_group = df.groupby(['BorrowerState']).mean()
df_group.index.astype(str)

#drop Guam, American Samoa, Puerto Rico,Northern Mariana Islands,	Armed Forces
df_group = df_group.drop(['AS','GU','PR','MP','AE'])

#Avg per employee
fig = go.Figure(data=go.Choropleth(
    locations=df_group.index.astype(str), # Spatial coordinates
    z = df_group['avg_amountPerEmployee'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "USD",
))

fig.update_layout(
    title_text = 'Average approved amount per employee ($)',
    geo_scope='usa', # limite map scope to USA
)

fig.show()

#Avg approval amount
fig = go.Figure(data=go.Choropleth(
    locations=df_group.index.astype(str), # Spatial coordinates
    z = df_group['CurrentApprovalAmount'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "USD",
))

fig.update_layout(
    title_text = 'Average approved amount ($ in thousands)',
    geo_scope='usa', # limite map scope to USA
)

fig.show()


"""
import plotly.graph_objects as go

df.columns

import pandas as pd
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

fig = go.Figure(data=go.Choropleth(
    locations=♠.unique().astype(str), # Spatial coordinates
    z = df['CurrentApprovalAmount'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "USD",
))

fig.update_layout(
    title_text = 'Average amount per employee',
    geo_scope='usa', # limite map scope to USA
)

fig.show()
"""

