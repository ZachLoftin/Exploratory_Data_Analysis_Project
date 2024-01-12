# First step is to import pandas and matplotlib. 
# Then I'll load the datasets by using pd.read_csv and look at the information regarding each dataset.

import pandas as pd
from matplotlib import pyplot as plt


# In[2]:

# Next, import all the datasets

instacart_orders = pd.read_csv('/datasets/instacart_orders.csv', sep=';')

products = pd.read_csv('/datasets/products.csv', sep=';')

aisles = pd.read_csv('/datasets/aisles.csv', sep=';')

departments = pd.read_csv('/datasets/departments.csv', sep=';')

order_products = pd.read_csv('/datasets/order_products.csv', sep=';')

# In[7]:

# Look at each dataset

instacart_orders.info()
print()
products.info()
print()
aisles.info()
print()
departments.info()
print()
order_products.info(show_counts=True)

# In[8]:

# Check for duplicated orders

print(instacart_orders.duplicated().sum())


# In[9]:

# Check for all orders placed Wednesday at 2:00 AM

wed_2am_order = instacart_orders[(instacart_orders['order_dow'] == 3) & (instacart_orders['order_hour_of_day'] == 2)]
print(wed_2am_order)


# In[10]:

# Remove duplicate orders

instacart_orders['order_id'] = instacart_orders['order_id'].drop_duplicates()


# In[11]:

# Double check for duplicate rows

print(instacart_orders['order_id'].duplicated().sum())

# In[12]:

# Double check for duplicate order IDs only

print(instacart_orders[instacart_orders.duplicated(subset='order_id')])

# First, I checked the orders dataframe for duplicates.
# Second, I used query on the instacart orders to a variable called wednesday orders to check which orders were on wednesday.
# Then I used query() to find which orders were placed at 2AM.
# Then I got rid of the duplicates with the drop_duplicates function, and placed each column in the subset.
# I double checked if there were any duplicates, then checked the "order_id" column only.

# In[13]:

# Check for fully duplicate rows

print(products.duplicated().sum())

# In[14]:

# Check for just duplicate product IDs

dup_id = products['product_id'].duplicated()
print(dup_id.sort_values())

# In[15]:

print(dup_id.sum())

# In[16]:

# Check for just duplicate product names (convert names to lowercase to compare better)

print(products['product_name'].str.lower().value_counts())

# In[17]:

# Check for duplicate product names that aren't missing

duplicate_products = products['product_name'].duplicated(keep=False) & products['product_name'].notna()
print(duplicate_products.sum())

# First I checked for obvious duplicates. Then checked for duplicates within the product_id column.
# Not finding any, I made all the strings in lowercase and checked again, 
# finding several duplicates and then getting rid of them.

# In[18]:

print(departments['department_id'].duplicated().sum())

# In[19]:

print(aisles['aisle_id'].duplicated().sum())

# In[20]:

# Check for fully duplicate rows

print(order_products['order_id'].duplicated().sum())
dup_order_products = order_products['order_id'].duplicated(keep=False)
print(dup_order_products.sum())

# In[21]:


other_dups = order_products[order_products.duplicated(subset=['order_id', 'product_id'], keep=False)]
display(other_dups)


# In[23]:


products.info()
print()
print(products.isna().sum())
print()
print(products['product_name'].value_counts(dropna=False))


# In[24]:

# Are all of the missing product names associated with aisle ID 100?

missing_values = products['product_name'].isna()
correlation = missing_values.astype(int).corr(products['aisle_id'] == 100)
print(correlation)

# In[25]:

# Are all of the missing product names associated with department ID 21?

missing_values = products['product_name'].isna()
correlation = missing_values.astype(int).corr(products['department_id'] == 21)
print(correlation)

# In[26]:

# What is this ailse and department?

print(aisles['aisle'])
row_index = 99
print()
print(aisles.iloc[row_index])
print()
print(departments['department'])
row_index2 = 20
print()
print(departments.iloc[row_index2])


# In[27]:

# Fill missing product names with 'Unknown'

products['product_name'] = products['product_name'].fillna('Unknown')
print(products.isna().sum())


# Pulled up the info for the products dataframe to see if any numbers weren't matching.
# Used isna() and sum() to count the amount of missing values in products df
# Using the corr() method, it seems like the missing product names are strongly correlated with aisle 100
# Using the corr() method, it seems like the missing product names are strongly correlated with department id 21
# Using indexing, I found aisle 100 is missing
# Using indexing, I found department 21 is missing
# Filled in all missing values with "Unknown" and then double checked with isna().sum()

# In[28]:

instacart_orders.info()


# In[29]:

# Are there any missing values where it's not a customer's first order?

not_first_order = instacart_orders[(instacart_orders['days_since_prior_order'].isna()) & (instacart_orders['order_number'] != 1)]
print(not_first_order)

# In[30]:

order_products.info(show_counts=True)

# In[31]:

# What are the min and max values in this column?

print(order_products['order_id'].min())
print(order_products['order_id'].max())
print(order_products['product_id'].min())
print(order_products['product_id'].max())
print(order_products['add_to_cart_order'].min())
print(order_products['add_to_cart_order'].max())
print(order_products['reordered'].min())
print(order_products['reordered'].max())

# In[32]:

# Save all order IDs with at least one missing value in 'add_to_cart_order'

missing_values_orders = order_products[order_products['add_to_cart_order'].isna()]
print(missing_values_orders)

# In[33]:

# Do all orders with missing values have more than 64 products?

orders_64 = missing_values_orders.groupby('order_id').size()
print(orders_64)

# In[34]:

# Replace missing values with 999 and convert column to integer type

order_products['add_to_cart_order'] = order_products['add_to_cart_order'].fillna(999).astype(int, errors='ignore')

# In[35]:

hours_of_day_index = instacart_orders['order_hour_of_day'].reset_index(drop=True)
print(hours_of_day_index.value_counts().sort_index())

# In[36]:

dow_index = instacart_orders['order_dow'].reset_index(drop=True)
print(dow_index.value_counts().sort_index())

# In[37]:

instacart_orders.hist(column='order_hour_of_day')
plt.show()

# The graph shows a majority of people shop around the 15th hour of the day.

# In[38]:

instacart_orders['order_dow'].hist()
plt.show()

# In[39]:

instacart_orders['days_since_prior_order'].hist()
plt.show()

# In[40]:

instacart_orders[instacart_orders['order_dow'] == 3]['order_hour_of_day'].plot(kind='hist', bins=40)

# In[41]:

plt.show()

# In[42]:

instacart_orders[instacart_orders['order_dow'] == 6]['order_hour_of_day'].plot(kind='hist', bins=40)

# In[43]:

plt.show()

# There isn't much difference between the graphs when using the default "bins" but when increasing bins to get more detail, 
# we see that both graphs show an increase in shopping around 10am and both begin to decline around the 3pm mark. 
# The biggest difference in the graphs is the dip in shopping around 12pm on Wednesdays, where as on Saturday, 
# that seems to be the busiest shopping time.

# In[44]:

distribution_num_orders = instacart_orders['user_id'].value_counts()

# In[45]:

print(distribution_num_orders.head(20))

# By calling "value_counts()" on the 'user_id' column, you can get an accurate count of the number of orders per customer

# In[46]:

pop_product_name = products['product_name'].value_counts()

# In[47]:

pop_product_id = products['product_id'].value_counts()

# In[48]:

print(pop_product_name.head(20))
print(pop_product_id.head(20))

# By calling "value_counts()" to each column, we can get the most popular products of each column.

# In[49]:

reorder_sum = order_products.groupby('product_id')['reordered'].sum()
order_id_amount = order_products.groupby('product_id')['order_id'].count()
reorder_ratio = reorder_sum / order_id_amount
print(reorder_ratio)

# First, I used groupby('product_id') to group the data by the product id column. 
# Then used ['reordered'].sum() to find the sum
# of the reordered column. Then used ['order_id].count() to count the total number of orders for each product
# and finally dividing them which leaves you with the portion of orders that are reorders.

# In[50]:

order_products.info()

# In[51]:

customer_sum = order_products.groupby('order_id')['reordered'].sum()
product_id_amount = order_products.groupby('order_id')['product_id'].count()
reorder_customer_ratio = customer_sum / product_id_amount
print(reorder_customer_ratio)
