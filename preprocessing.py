#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


# In[3]:


path = "MIS ELPMAS DATA.csv"
global df
df = pd.read_csv(path)
df.head()


# In[4]:


df.dtypes


# In[5]:


df["DATE"]=(pd.to_datetime(df['YEAR'].astype(str)  + df['MONTH'], format='%Y%B')) 


# In[6]:


df.dtypes


# In[7]:


for col in [' SALES SERVICE ',
       ' LESS ORC ', ' NET SALES ', ' COST OF GOODS SOLD ',
       ' TRANSACTION MARGIN ', ' BACKEND INCOME ', ' ESTIMATE INCOME ',
       ' TOTAL BACKEND INCOME ', ' DEPRECIATION INVENTORY ',
       ' SALES COMMISSION ', ' GROSS MARGIN ', ' CASH DISCOUNT ',
       ' GROSS MARGIN CD ', ' OTHER INCOME ', ' FREIGHT ', ' INSURANCE ',
       ' COMMERCIAL TAX ', ' DRIECT EXPENSES ', ' COMPENSATION ',
       ' STAFF WELFATE ', ' OUTSOURCED RESOURCE ', ' TRAVEL ', ' CONVEYANCE ',
       ' COMMUNICATION ', ' UTILITIES ', ' REPAIRS MAINTENANCE ',
       ' PRINTING STATIONERY ', ' RENT ', ' RENT WAREHOUSE ',
       ' WAREHOUSE EXPENSES ', ' ENTERTAINMENT ', ' TRAINING ',
       ' ADVERTISMENT EXPENSES ', ' BAD DEBTS ', ' BANK CHARGES ',
       ' RATE TAXES ', ' CONSULTANCY BROKER ', ' AUDIT FEE ',
       ' FALSE GAIN OR LOSS ', ' EXCHANGE GAIN OR LOSS ',
       ' DIRECT SITTING FEE ', ' CSR ', ' FACTORING ', ' OTHER EXPENSES ',
       ' TOTAL TRADING EXPENSES ', ' EBITDA ', ' WORKING CAPITAL INTEREST ',
       ' DEPRECIATION ON ASSET ', ' PROFIT BEFORE TAX ', ' TAX EXPENSES ',
       ' PROFIT AFTER TAX ', ' EBIT ', ' NON CASH ITEM ', ' INTEREST COVER ',
       ' OPEN_WC ', ' CLOSE_WC ', ' AVG_WC ', ' ROCE ', ' WCTURNS ',
       ' WCDAYS ']:
        df[col] = df[col].str.replace(',', '', regex=True)
        df[col] = df[col].str.replace(' -   ', '', regex=True)
        df[col] = pd.to_numeric(df[col])


# In[8]:


df.columns


# ## Calculations for required rows:
# 
# * Revenue = net sales - sales commision + other income
# 
# * Gross margin = gross margin + cash discount + other income
# 
# * Man power cost = compensation + staff welfare + outsourced resource
# 
# * Biz trading cost = frieght + insurance + rent warehouse + warehouse expenses
# 
# * EBITDA = gross margin - man power cost - biz trading cost - other opex
# 
# * EBIT = EBITDA - depreciation
# 
# * PBT = EBIT - intrest cost
# 
# * PAT = PBT - Tax
# 

# In[9]:


# Revenue 

df["C_Revenue"] = df[" NET SALES "]-df[" SALES COMMISSION "]+df[" OTHER INCOME "]


# In[10]:


# Gross margin

df["C_Gross_Margin"] = df[" GROSS MARGIN "]+df[" CASH DISCOUNT "]+df[" OTHER INCOME "]


# In[11]:


# EBITDA

df["Man_power_cost"] = df[" COMPENSATION "]+df[" STAFF WELFATE "]+df[" OUTSOURCED RESOURCE "]
df["Biz_trading_cost"] = df[" FREIGHT "]+df[" INSURANCE "]+df[" RENT WAREHOUSE "]+df[" WAREHOUSE EXPENSES "]
df["A"] = df[" TRAVEL "]+df[" CONVEYANCE "]+df[" COMMUNICATION "]+df[" UTILITIES "]+df[" REPAIRS MAINTENANCE "]+df[" PRINTING STATIONERY "]+df[" RENT "]
df["B"] = df[" ENTERTAINMENT "]+df[" TRAINING "]+df[" ADVERTISMENT EXPENSES "]+df[" BAD DEBTS "]+df[" BANK CHARGES "]+df[" RATE TAXES "]+df[" CONSULTANCY BROKER "]+df[" AUDIT FEE "]+df[" FALSE GAIN OR LOSS "]+df[" EXCHANGE GAIN OR LOSS "]+df[" DIRECT SITTING FEE "]+df[" CSR "]+df[" OTHER EXPENSES "]
df["Other_opex"] = df["A"]+df["B"]
df.drop(columns=["A","B"])

df["C_EBITDA"] = df["C_Gross_Margin"]-df["Man_power_cost"]-df["Biz_trading_cost"]-df["Other_opex"]


# In[12]:


#EBIT

df["C_EBIT"] = df["C_EBITDA"] - df[" DEPRECIATION ON ASSET "]


# In[13]:


#PBT

df["Intrest_cost"] = df[" FACTORING "]+df[" WORKING CAPITAL INTEREST "]

df["C_PBT"] = df["C_EBIT"]-df["Intrest_cost"]


# In[14]:


#PAT

df["C_PAT"] = df["C_PBT"]-df[" TAX EXPENSES "]


# In[ ]:





# ## DATA PREPROCESSING

# In[15]:


df.columns


# In[16]:


#checking nulls

df.isnull().sum().sort_values(ascending=False)


# In[19]:


#filling null values with mean

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

#checkin for nulls

df.isnull().sum().sort_values(ascending=False)


# In[ ]:




