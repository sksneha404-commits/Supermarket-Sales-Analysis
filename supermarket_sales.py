import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

print(os.getcwd())
# df=pd.read_csv(r"C:\Users\sksne\Desktop\my\python\supermarket_sales.csv",encoding="utf-8")
# df=pd.read_csv(r"C:\Users\sksne\Desktop\my\python\Supermarket_Sales_Analysis/supermarket_sales.csv",encoding="utf-8")
df=pd.read_csv("supermarket_sales.csv",encoding="utf-8")

df.info()

'''[checking the missing value]'''
print(df[df["Invoice ID"].isnull()])
print(df[df["City"].isnull()])
print(df[df["Time"].isnull()])
print(df.isnull().any(axis=1).sum())

'''[check duplicate row]'''
print(df.duplicated().sum())

'''[handling hte missing value by replaceing it from "unknown"]'''
df["Time"]=df["Time"].fillna("Unknown")
df["City"]=df["City"].fillna("Unknown")
df["Invoice ID"]=df["Invoice ID"].fillna("Unknown")


'''[converting dtype of date and time into datetime type]'''
print(df.isnull().sum())
df["Date"]=pd.to_datetime(df["Date"])
print(df["Date"].dtype)
df["Time"]=pd.to_datetime(df["Time"].replace("Unknow",pd.NA),
                          format="%H:%M",errors="coerce")
print(df["Time"].head(10))
print(df["Time"].dtype)

'''[checking the valid value in the data set]'''
print(df.isnull().sum())
print(df.describe())
print((df["Quantity"]<=0).sum())
print((df["Unit price"]<=0).sum())
print((df["Total"]<=0).sum())
print(((df["Rating"]<0) | (df["Rating"]>10)).sum())

''' checking  the relation b/w columns to avoid further error in data and understand the columns '''
print(df[["Unit price","Quantity","Tax 5%","Total","cogs",
        "gross income"]].head())
print((~np.isclose(df["cogs"]+df["Tax 5%"],df["Total"])).sum())


'''creating new colunms extracting day ,month from date '''
df["Month"]=df["Date"].dt.month
print(df[["Date","Month"]].head())
df["Day"]=df["Date"].dt.day_name()
print(df[["Day","Date"]].head())

'''finding the sales and product that has high or low sale'''
df["Sale Category"]=np.where((df["Total"]>=500),"high sale" ,"low sale")
print(df[["Total","Sale Category"]].head())
print(df.groupby("Sale Category")["Total"].sum())
product_sales=df.groupby("Product line")["Total"].sum()
print(df.groupby("Product line")["Total"].sum().sort_values(ascending=(False)))
print(df.groupby("Product line")["Total"].mean().sort_values(ascending=(False)))
print(df.groupby("Product line")["Total"].size().sort_values(ascending=(False)))

'''finding sales per branch '''
branch_sales=df.groupby("Branch")["Total"].sum()
print(df.groupby("Branch")["Total"].sum().sort_values(ascending=(False)))
print(df.groupby("Branch")["Total"].size().sort_values(ascending=(False)))
print(df.groupby("Branch")["Total"].mean().sort_values(ascending=(False)))

'''payment method that use in transection '''
payment_sales=df.groupby("Payment")["Total"].sum()
payment_count=df.groupby("Payment")["Total"].size()
print(df.groupby("Payment")["Total"].size().sort_values(ascending=(False)))
print(df.groupby("Payment")["Total"].sum().sort_values(ascending=(False)))
print(df.groupby("Payment")["Total"].mean().sort_values(ascending=(False)))

'''finding the days that have high or low sales'''
daily_sales=df.groupby("Day")["Total"].sum()
print(df.groupby("Day")["Total"].sum().sort_values(ascending=(False)))

'''finding the monthly sales that have high or low sales'''
monthly_sales=df.groupby("Month")["Total"].sum()
print(df.groupby("Month")["Total"].sum().sort_values(ascending=(False)))

'''finding the  which customer type  have high or low sales'''
customer_type=df.groupby("Customer type")["Total"].sum()
print(df.groupby("Customer type")["Total"].sum().sort_values(ascending=(False)))
print(df.groupby("Customer type")["Total"].mean().sort_values(ascending=(False)))
print(df.groupby("Customer type")["Total"].size().sort_values(ascending=(False)))

'''finding the  which customer (gender)  have high or low sales'''
print(df.groupby("Gender")["Total"].sum().sort_values(ascending=(False)))
print(df.groupby("Gender")["Total"].mean().sort_values(ascending=(False)))
print(df.groupby("Gender")["Total"].size().sort_values(ascending=(False)))



'''creating vertical bar chart for product sales'''
plt.figure(figsize=(8,6))
bars=plt.bar(product_sales.index,product_sales.values)
plt.title("Total sales by Product Line")
plt.xlabel("Product Line")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.bar_label(bars,fmt='%.0f')
plt.savefig("charts/Product_sales.png")
plt.show()

# '''creating horizontal bar chart for product sales'''
# product_sales_sort=product_sales.sort_values(ascending=True)
# bars=plt.barh(product_sales_sort.index,product_sales_sort.values)
# plt.title("Total sales by Product Line")
# plt.ylabel("Product Line")
# plt.xlabel("Total Sales")
# plt.bar_label(bars,fmt='%.0f')
# plt.savefig("charts/Product_sales.png")
# plt.grid(axis="x",linestyle="--",alpha=0.9)
# plt.show()



'''creating bar chart for branch sales'''
bars=plt.bar(branch_sales.index,branch_sales.values)
plt.title("Total sales by Branch")
plt.xlabel("Branch")
plt.ylabel("Total sales")
plt.bar_label(bars,fmt='%.0f')
plt.savefig("charts/Branch_sales.png")
plt.show()




'''creating pie chart for transection way sales'''
plt.pie(payment_count.values,labels=payment_sales.index,autopct='%1.1f%%')
plt.title(" Transection by Payment Method ")
plt.savefig("charts/Transection_method.png")
plt.show()



'''creating line chart for monthly sales'''
plt.plot(monthly_sales.index,monthly_sales.values,marker='o')
plt.title("Monthly sales")
plt.xlabel("Month")
plt.ylabel("Total sales")
plt.savefig("charts/Monthly_sales.png")
plt.show()


'''creating bar chart for custoner type sales'''
plt.figure(figsize=(8,6))
bars=plt.barh(customer_type.index,customer_type.values)
plt.title(" Type of customer")
plt.ylabel("Customer")
plt.xlabel("Total sales")
plt.bar_label(bars,fmt='%.0f')
plt.savefig("charts/Customer_type.png")
plt.show()


'''creating line chart for daily sales '''
plt.figure(figsize=(8,6))
days_order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
daily_sales_index=daily_sales.reindex(days_order)
plt.plot(daily_sales_index.index,daily_sales_index.values,marker='o')
plt.title("Daily Sales")
plt.xlabel("Days")
plt.ylabel("Total sales")
plt.savefig("charts/Daily_sales.png")
plt.show()
