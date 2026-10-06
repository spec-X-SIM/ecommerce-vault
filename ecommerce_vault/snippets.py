"""
Catalog of all data cleaning, visualization, and dashboard codes
stored as non-executing string templates.
"""

SNIPPETS = {
    "01_data_cleaning_and_duplicates": '''\
# ==========================================
# DATA CLEANING, IMPUTATION & DEDUPLICATION
# ==========================================
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(r"ecommerce_sales_data_5000_with_missing_values.csv")

# Impute Missing Numerical Values with Median
numeric_columns = [
    "Customer_Age", "Quantity", "Unit_Price", "Discount_Percent", 
    "Sales", "Profit", "Delivery_Days", "Rating", "Customer_Satisfaction"
]
for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Impute Missing Categorical Values with Mode
categorical_columns = [
    "Gender", "City", "Region", "Customer_Segment", "Product_Category", 
    "Product", "Payment_Mode", "Shipping_Mode", "Order_Status", 
    "Marketing_Channel", "Return_Flag"
]
for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

# Remove Duplicate Rows
df = df.drop_duplicates()
''',

    "02_eda_basic_exploration": '''\
# ==========================================
# BASIC DATA EXPLORATION & GROUPING
# ==========================================
import pandas as pd

# View structure
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
print(df.describe())

# Convert Order_Date to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Filter transactions
high_sales = df[df["Sales"] > 10000]

# Regional and Category Grouping
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
category_sales = df.groupby("Product_Category")["Sales"].sum().sort_values(ascending=False)
category_profit = df.groupby("Product_Category")["Profit"].sum().sort_values(ascending=False)
''',

    "03_matplotlib_charts": '''\
# ==========================================
# MATPLOTLIB CHARTS
# ==========================================
import matplotlib.pyplot as plt
import pandas as pd

# 1. Monthly Sales Trend (Line Plot)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
monthly_sales = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
months = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 5))
plt.plot(months, monthly_sales.values, marker="s")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=60)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.show()

# 2. Total Sales by Region (Vertical Bar Chart)
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(region_sales.index, region_sales.values)
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# 3. Top 10 Products by Total Sales (Horizontal Bar Chart)
top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_products.index, top_products.values)
plt.gca().invert_yaxis()
plt.title("Top 10 Products by Total Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# 4. Monthly Sales Area Plot
plt.figure(figsize=(12, 5))
plt.fill_between(months, monthly_sales.values, color="red", alpha=0.4)
plt.title("Monthly Sales Area Plot", fontsize=16, fontweight="bold")
plt.xlabel("Month", fontsize=12, fontweight="bold")
plt.ylabel("Total Sales", fontsize=12, fontweight="bold")
plt.xticks(rotation=60, fontsize=10)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.show()

# 5. Profit Distribution (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(df["Profit"], bins=20, color="red", edgecolor="black", linewidth=1.2, alpha=0.7)
plt.title("Distribution of Profit", fontsize=16, fontweight="bold")
plt.xlabel("Profit", fontsize=12, fontweight="bold")
plt.ylabel("Frequency", fontsize=12, fontweight="bold")
plt.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.4)
plt.tight_layout()
plt.show()

# 6. Payment Mode Distribution (Donut Chart)
payment_counts = df["Payment_Mode"].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"width": 0.4},
    shadow=True,
    explode=[0.03] * len(payment_counts),
    colors=["red", "skyblue", "gold"]
)
plt.title("Payment Mode Distribution", fontsize=16, fontweight="bold")
plt.axis("equal")
plt.tight_layout()
plt.show()

# 7. Scatter Plot: Discount Percentage vs Sales
plt.figure(figsize=(10, 6))
plt.scatter(
    df["Discount_Percent"], df["Sales"],
    s=45, alpha=0.6, edgecolors="black", linewidths=0.5
)
plt.title("Discount Percentage vs Sales", fontsize=16, fontweight="bold")
plt.xlabel("Discount Percentage", fontsize=12, fontweight="bold")
plt.ylabel("Sales", fontsize=12, fontweight="bold")
plt.grid(True, linestyle="--", linewidth=0.7, alpha=0.3)
plt.tight_layout()
plt.show()
''',

    "04_seaborn_and_specialized": '''\
# ==========================================
# SEABORN, PYWAFFLE & WORDCLOUD
# ==========================================
import seaborn as sns
import matplotlib.pyplot as plt
from pywaffle import Waffle
from wordcloud import WordCloud

# 1. Average Sales by Region (Bar Plot)
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Region", y="Sales")
plt.title("Average Sales by Region")
plt.xlabel("Region")
plt.ylabel("Average Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Regression Plot: Discount Percentage vs Sales
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x="Discount_Percent", y="Sales", scatter_kws={"alpha": 0.4})
plt.title("Relationship Between Discount Percentage and Sales")
plt.xlabel("Discount Percentage")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# 3. Pair Plot
pair_data = df[["Sales", "Profit", "Quantity", "Delivery_Days", "Customer_Satisfaction"]]
pair_sample = pair_data.sample(n=500, random_state=42)
sns.pairplot(pair_sample)
plt.show()

# 4. Correlation Heatmap
corr_data = df[["Sales", "Profit", "Quantity", "Discount_Percent", "Delivery_Days", "Rating", "Customer_Satisfaction"]]
corr = corr_data.corr()
plt.figure(figsize=(10, 7))
sns.heatmap(corr, annot=True, fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of E-Commerce Variables")
plt.tight_layout()
plt.show()

# 5. Violin Plot: Customer Segments
plt.figure(figsize=(10, 5))
sns.violinplot(data=df, x="Customer_Segment", y="Sales")
plt.title("Sales Distribution by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Waffle Chart
segment_counts = df["Customer_Segment"].value_counts()
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=segment_counts.to_dict(),
    title={"label": "Customer Segment Distribution"}
)
plt.show()

# 7. Word Cloud
text = " ".join(df["Product"].dropna().astype(str))
wordcloud = WordCloud(width=1000, height=500, background_color="white").generate(text)
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Product Word Cloud")
plt.show()
''',

    "05_plotly_charts": '''\
# ==========================================
# PLOTLY INTERACTIVE CHARTS
# ==========================================
import plotly.express as px
import plotly.graph_objects as go

# 1. Plotly Express: Regional Sales Bar Chart
region_sales_df = df.groupby("Region", as_index=False)["Sales"].sum()
fig = px.bar(region_sales_df, x="Region", y="Sales", title="Total Sales by Region")
fig.show()

# 2. Plotly Express: Grouped Sales & Profit Bar Chart
category_summary = df.groupby("Product_Category", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
fig = px.bar(
    category_summary,
    x="Product_Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Product Category"
)
fig.show()

# 3. Plotly Express: Payment Modes Pie Chart
payment_df = df["Payment_Mode"].value_counts().reset_index()
payment_df.columns = ["Payment_Mode", "Orders"]
fig = px.pie(payment_df, names="Payment_Mode", values="Orders", title="Orders by Payment Mode")
fig.show()

# 4. Plotly Express: Scatter Plot
fig = px.scatter(
    df,
    x="Discount_Percent",
    y="Sales",
    color="Product_Category",
    hover_data=["Product", "Region", "Profit"],
    title="Discount Percentage vs Sales"
)
fig.show()

# 5. Plotly Graph Objects: Grouped Bar Chart
cat_go = df.groupby("Product_Category")[["Sales", "Profit"]].sum()
fig = go.Figure()
fig.add_trace(go.Bar(x=cat_go.index, y=cat_go["Sales"], name="Sales"))
fig.add_trace(go.Bar(x=cat_go.index, y=cat_go["Profit"], name="Profit"))
fig.update_layout(
    title="Sales and Profit by Product Category",
    xaxis_title="Product Category",
    yaxis_title="Amount",
    barmode="group"
)
fig.show()
''',

    "06_full_dash_dashboard": '''\
# ==========================================
# PROFESSIONAL DASH DASHBOARD
# ==========================================
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

app = Dash(__name__)

# KPI calculations
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
average_order_value = total_sales / total_orders

# 1. Regional Sales
region_data = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
region_fig = px.bar(region_data, x="Region", y="Sales", title="Sales by Region", text_auto=".2s")
region_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

# 2. Monthly Sales
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
monthly_data = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly_data["Order_Date"] = monthly_data["Order_Date"].astype(str)
monthly_fig = px.line(monthly_data, x="Order_Date", y="Sales", markers=True, title="Monthly Sales Trend")
monthly_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

# 3. Product Category Profit
profit_data = df.groupby("Product_Category", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
profit_fig = px.bar(profit_data, x="Product_Category", y="Profit", title="Profit by Product Category", text_auto=".2s")
profit_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

# 4. Payment Modes
payment_data = df["Payment_Mode"].value_counts().reset_index()
payment_data.columns = ["Payment_Mode", "Orders"]
payment_fig = px.pie(payment_data, names="Payment_Mode", values="Orders", title="Orders by Payment Mode", hole=0.45)
payment_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

# KPI card styling
card_style = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "textAlign": "center",
    "flex": "1",
    "margin": "5px"
}

# Layout
app.layout = html.Div([
    html.Div([
        html.H1("E-Commerce Sales Dashboard", style={"margin": "0", "fontSize": "32px", "fontWeight": "bold"}),
        html.P("Sales, profitability and customer transaction analysis", style={"marginTop": "8px", "fontSize": "15px", "opacity": "0.85"})
    ], style={"backgroundColor": "#1F4E78", "color": "white", "padding": "25px 35px", "borderRadius": "12px", "marginBottom": "20px"}),

    # KPI Section
    html.Div([
        html.Div([html.H4("TOTAL SALES", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}),
                  html.H2(f"{total_sales:,.0f}", style={"margin": "10px 0 0 0", "color": "#1F4E78"})], style=card_style),
        html.Div([html.H4("TOTAL PROFIT", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}),
                  html.H2(f"{total_profit:,.0f}", style={"margin": "10px 0 0 0", "color": "#2E7D32"})], style=card_style),
        html.Div([html.H4("TOTAL ORDERS", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}),
                  html.H2(f"{total_orders:,}", style={"margin": "10px 0 0 0", "color": "#7B1FA2"})], style=card_style),
        html.Div([html.H4("AVERAGE ORDER VALUE", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}),
                  html.H2(f"{average_order_value:,.0f}", style={"margin": "10px 0 0 0", "color": "#C62828"})], style=card_style),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": "20px"}),

    # Charts
    html.Div([
        html.Div(dcc.Graph(figure=region_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "flex": "1", "margin": "5px"}),
        html.Div(dcc.Graph(figure=monthly_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "flex": "1", "margin": "5px"}),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": "10px"}),

    html.Div([
        html.Div(dcc.Graph(figure=profit_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "flex": "1", "margin": "5px"}),
        html.Div(dcc.Graph(figure=payment_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "flex": "1", "margin": "5px"}),
    ], style={"display": "flex", "flexWrap": "wrap"}),

    html.P("Source: E-Commerce Transaction Dataset", style={"textAlign": "center", "color": "#6B7280", "fontSize": "12px", "marginTop": "25px"})
], style={"backgroundColor": "#F3F6F9", "padding": "25px", "fontFamily": "Arial, sans-serif", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=False)
'''
}