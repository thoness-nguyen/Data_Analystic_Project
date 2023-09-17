#!/usr/bin/env python
# coding: utf-8

# # Retail dataset analyze practice

# In[1]:


import numpy as np
import pandas as pd


# ## Use pandas to extract data frame 

# ### Dataset features

# In[2]:


df_features = pd.read_csv ("C:/Users/HP/Downloads/retail dataset/Features data set.csv")


# In[3]:


df_features.tail(5)


# In[4]:


df_features.shape


# In[5]:


df_features.info()


# In[6]:


df_features.describe()


# ### dataset sales

# In[7]:


df_sales = pd.read_csv ("C:/Users/HP/Downloads/retail dataset/sales data-set.csv")
df_sales.head(6)


# In[8]:


df_sales.shape


# In[9]:


df_features.info()


# In[10]:


df_features.describe(include = 'all')


# ### dataset stores

# In[55]:


df_stores = pd.read_csv ("C:/Users/HP/Downloads/retail dataset/stores data-set.csv")
df_stores.head(6)


# In[12]:


df_stores.shape


# In[13]:


df_stores.info()


# In[14]:


df_stores.describe(include = "all")


# ## 1. Handle missing data:

# Features

# In[15]:


missed_values_features = df_features.isna().sum()
missed_values_features


# In[16]:


df_features['CPI'].fillna(df_features['CPI'].mean(), inplace = True)


# In[17]:


df_features ['Unemployment'].fillna (df_features ['Unemployment'].mean(), inplace = True)


# In[18]:


df_features['MarkDown1'].fillna(0, inplace = True)


# In[19]:


df_features[['MarkDown2','MarkDown3','MarkDown4','MarkDown5']] = df_features[['MarkDown2','MarkDown3','MarkDown4','MarkDown5']].fillna(0)


# Sale

# In[20]:


df_sales.isna().sum()


# Stores

# In[21]:


df_stores.isna().sum()


# In[22]:


df_stores.info


# ## 2. Change suitable type of values:

# Features

# In[23]:


df_features.dtypes


# In[24]:


# convert date from datetime of pyhton ('%d/%m/%y')
df_features['Date'] = pd.to_datetime (df_features['Date'], format = '%d/%m/%Y')


# In[25]:


df_features.head(6)


# In[26]:


# Change the temperature from F to C
df_features['Temperature']=(df_features['Temperature'] - 32) / 1.8


# In[27]:


# change the value True False to Yes No
df_features ['IsHoliday'].replace ({True: 'Yes', False: 'No'}, inplace = True)


# In[28]:


# Round the number to 1 
df_features[['Temperature','Fuel_Price','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','Unemployment']] = df_features[['Temperature','Fuel_Price','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','Unemployment']].round(1)


# Sales

# In[29]:


df_sales.head()


# In[30]:


# Convert date to datetime in python
df_sales ['Date'] = pd.to_datetime (df_sales ['Date'], format = '%d/%m/%Y')


# In[31]:


df_sales['IsHoliday'] = df_sales['IsHoliday'].replace({True: 'Yes', False: 'No'})


# Stores

# In[32]:


df_stores.head()


# In[33]:


df_stores['Type'] = df_stores['Type'].astype ('category')


# ## Analyze

# **Bài tập phân tích cho bảng df_features:**
# 
# Phân tích nhiệt độ (Temperature):
# 1. Tính giá trị trung bình, median, độ lệch chuẩn và phương sai của cột nhiệt độ.
# Phân tích tỷ lệ thất nghiệp (Unemployment):
# 2. Tính tỷ lệ thất nghiệp trung bình của tất cả các cửa hàng.
# Phân tích ngày lễ (IsHoliday):
# 3. Đếm số lượng ngày lễ có trong dữ liệu.
# 
# **Bài tập phân tích cho bảng df_sales:**
# 
# Phân tích doanh số bán hàng (Weekly_Sales):
# 1. Tính tổng doanh số bán hàng trung bình của mỗi cửa hàng.
# 2. Tính tổng doanh số bán hàng trung bình của mỗi cửa hàng cho các ngày lễ và các ngày không phải ngày lễ.
# Phân tích cửa hàng (Store) và phòng (Dept):
# 3. Đếm số lượng cửa hàng và phòng khác nhau có trong dữ liệu.
# 
# **Bài tập phân tích cho bảng df_stores:**
# 
# Phân tích loại cửa hàng (Type) và kích thước (Size):
# 1. Đếm số lượng cửa hàng thuộc mỗi loại.
# 2. Tính kích thước trung bình của cửa hàng mỗi loại.
# 3. Phân tích kích thước cửa hàng (Size) theo loại (Type):
# Phân tích kích thước cửa hàng (Size) theo loại cửa hàng và ngày lễ (IsHoliday):
# 4. Tính kích thước trung bình của cửa hàng mỗi loại cho các ngày lễ và các ngày không phải ngày lễ.

# In[34]:


df_features.head(6)


# In[35]:


df_features['Temperature'].mean()


# In[36]:


np.median(df_features['Temperature'])


# In[37]:


np.std(df_features['Temperature'])


# In[38]:


np.var(df_features['Temperature'])


# In[1]:


# Tính tỷ lệ thất nghiệp trung bình của tất cả các cửa hàng
# merge table with 'on' and 'how'
b = df_features.merge(df_stores[['Store','Size']],on = 'Store', how = 'inner')

a = b[['Unemployment','Size']].groupby (b['Store']).mean('Unemployment').sort_values(by = 'Size',ascending = False)
round(a,2)


# #### There is no correlation between unemployment rate and size store

# In[40]:


df_features['IsHoliday'].value_counts()['Yes']


# In[41]:


df_sales.head(5)


# In[42]:


# Tính tổng doanh số bán hàng trung bình của mỗi cửa hàng.
c = df_sales.merge(df_stores [['Size','Store']], on = 'Store', how ='inner')

d = c[['Weekly_Sales','Size']].groupby(c['Store']).mean('Weekly_Sales').sort_values(by = 'Weekly_Sales',ascending = False)
round (d,1)


# #### There is a relationship between Weeky_sale and size of store
# 
# #### --> The bigger of the store, the higher profit achievement

# In[43]:


# Tính tổng doanh số bán hàng trung bình của mỗi cửa hàng cho các ngày lễ và các ngày không phải ngày lễ.
df_sales ['Weekly_Sales'].groupby(df_features['IsHoliday']).mean().round(2)


# In[46]:


# Đếm số lượng ngày lễ và số lượng ngày bình thường
num_holidays = df_features['IsHoliday'].value_counts()['Yes']
num_normal_days = df_features['IsHoliday'].value_counts()['No']

# Tính tỷ lệ ngày lễ so với ngày bình thường
holiday_ratio = num_holidays / (num_holidays + num_normal_days) * 100

print("Tỷ lệ ngày lễ: {:.2f}%".format(holiday_ratio))


# In[47]:


df_sales.tail(10)


# In[52]:


# Đếm số lượng cửa hàng và phòng khác nhau có trong dữ liệu.
df_sales[['Store','Dept']].nunique()


# In[57]:


df_stores.head(10)


# In[69]:


# Đếm số lượng cửa hàng thuộc mỗi loại.
df_stores[['Type','Size']].value_counts('Type')


# In[72]:


# Phân tích kích thước cửa hàng (Size) theo loại cửa hàng và ngày lễ (IsHoliday):
df_stores[['Size','Type']].groupby('Type').mean('Size').round(2)


# In[76]:


# Tính kích thước trung bình của cửa hàng mỗi loại cho các ngày lễ và các ngày không phải ngày lễ.
g = df_features.merge(df_stores[['Size','Store']], on = 'Store', how = 'inner')

h = g[['Size','IsHoliday']].groupby('IsHoliday').mean()
h


# ### Analystic practice

# 1. Predict the department-wide sales for each store for the following year
# 2. Model the effects of markdowns on holiday weeks
# 3. Provide recommended actions based on the insights drawn, with prioritization placed on largest business impact

# In[77]:


df_features.head(6)


# In[82]:


df_sales.head(6)


# In[79]:


df_stores.head(6)


# In[81]:


# Use "dt" to extract the datatime 
df_sales['Year'] = df_sales['Date'].dt.year


# In[94]:


sale_2010 = df_sales.query('Year == 2010')['Weekly_Sales'].sum()
print ("Tổng doanh thu năm 2010:",sale_2010)


# In[95]:


sale_2011 = df_sales.query('Year == 2011')['Weekly_Sales'].sum()
print ("Tổng doanh thu năm 2011:",sale_2011)


# In[96]:


sale_2012 = df_sales.query('Year == 2012')['Weekly_Sales'].sum()
print ("Tổng doanh thu năm 2012:",sale_2012)


# In[103]:


sale_rate = ((sale_2011 - sale_2010)/ sale_2010) * 100
sale_rate


# In[100]:


# "pct_change" dùng để tính phần trăm giá trị liên tiếp của các giá trị liền kề
yearly_revenue = df_sales.groupby('Year')['Weekly_Sales'].sum()
revenue_growth_rate = yearly_revenue.pct_change() * 100
print (revenue_growth_rate)


# In[ ]:


markdown, isholiday, sale_week


# In[ ]:




