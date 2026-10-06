"""
Catalog of all data cleaning, visualization, and dashboard codes
stored as non-executing string templates.
"""

SNIPPETS = {
    # ==============================================================================
# 1. IMPORTS
# ==============================================================================
import PIL
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pywaffle import Waffle
from wordcloud import WordCloud
from dash import Dash, dcc, html

%matplotlib inline
sns.set_theme(style="whitegrid")

# ==============================================================================
# 2. DATA LOADING & INSPECTION
# ==============================================================================
file_path = r"C:\SIM Saintgits\DVB\ecommerce_sales_data_5000_with_missing_values.csv"
df = pd.read_csv(file_path)

print("Dataset Shape:", df.shape)
print("\nFirst 5 Records:")
display(df.head())
print("\nDataFrame Summary:")
df.info()

# ==============================================================================
# 3. DATA CLEANING & PREPROCESSING
# ==============================================================================
# 3.1 Check Missing Values
print("Total missing values:", df.isnull().sum().sum())
print("\nMissing values in each column:")
print(df.isnull().sum())

missing = df.isnull().sum()
print("\nColumns with missing values only:")
print(missing[missing > 0])

# 3.2 Check Duplicate Rows
duplicate_count = df.duplicated().sum()
print("\nNumber of duplicate rows:", duplicate_count)

duplicates = df[df.duplicated(keep=False)]
print("\nDuplicate records:")
display(duplicates)

# 3.3 Impute Numerical Missing Values Using Median
numeric_columns = [
    "Customer_Age", "Quantity", "Unit_Price", "Discount_Percent",
    "Sales", "Profit", "Delivery_Days", "Rating", "Customer_Satisfaction"
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# 3.4 Impute Categorical Missing Values Using Mode
categorical_columns = [
    "Gender", "City", "Region", "Customer_Segment", "Product_Category",
    "Product", "Payment_Mode", "Shipping_Mode", "Order_Status",
    "Marketing_Channel", "Return_Flag"
]
for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

print("\nTotal missing values after correction:", df.isnull().sum().sum())

# 3.5 Deduplication
df = df.drop_duplicates()
print("Duplicate rows after cleaning:", df.duplicated().sum())
print("Final number of rows:", df.shape[0])
print("Final number of columns:", df.shape[1])

# 3.6 Data Type Casting
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Customer_Age"] = df["Customer_Age"].astype(int)
df["Quantity"] = df["Quantity"].astype(int)
df["Discount_Percent"] = df["Discount_Percent"].astype(int)
df["Delivery_Days"] = df["Delivery_Days"].astype(int)

# ==============================================================================
# 4. EXPLORATORY DATA ANALYSIS & AGGREGATIONS
# ==============================================================================
print("\nDescriptive Statistics for Numerical Columns:")
display(df.describe())

print("\nDescriptive Statistics for Sales:")
display(df["Sales"].describe())

region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
category_sales = df.groupby("Product_Category")["Sales"].sum().sort_values(ascending=False)
category_profit = df.groupby("Product_Category")["Profit"].sum().sort_values(ascending=False)
top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)

monthly_sales = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
months = monthly_sales.index.astype(str)

payment_counts = df["Payment_Mode"].value_counts()
segment_counts = df["Customer_Segment"].value_counts()

# ==============================================================================
# 5. MATPLOTLIB VISUALIZATIONS
# ==============================================================================
# 5.1 Monthly Sales Trend (Line Plot)
plt.figure(figsize=(12, 5))
plt.plot(months, monthly_sales.values, marker="s")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=60)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.show()

# 5.2 Regional Sales (Vertical Bar Chart)
plt.figure(figsize=(8, 5))
plt.bar(region_sales.index, region_sales.values)
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# 5.3 Category Sales (Styled Vertical Bar Chart)
plt.figure(figsize=(9, 5))
plt.bar(category_sales.index, category_sales.values, color="red")
plt.title("Total Sales by Product Category", fontsize=16, fontweight="bold")
plt.xlabel("Product Category", fontsize=12, fontweight="bold")
plt.ylabel("Total Sales", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# 5.4 Top 10 Products by Sales (Horizontal Bar Chart)
plt.figure(figsize=(10, 6))
plt.barh(top_products.index, top_products.values)
plt.gca().invert_yaxis()
plt.title("Top 10 Products by Total Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# 5.5 Monthly Sales (Area Plot)
plt.figure(figsize=(12, 5))
plt.fill_between(months, monthly_sales.values, color="red", alpha=0.4)
plt.title("Monthly Sales Area Plot", fontsize=16, fontweight="bold")
plt.xlabel("Month", fontsize=12, fontweight="bold")
plt.ylabel("Total Sales", fontsize=12, fontweight="bold")
plt.xticks(rotation=60, fontsize=10)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.show()

# 5.6 Histograms: Distribution of Sales & Profit
plt.figure(figsize=(8, 5))
plt.hist(df["Sales"], bins=20, edgecolor="black")
plt.title("Distribution of Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(df["Profit"], bins=25, color="red", edgecolor="black", linewidth=1.2, alpha=0.7)
plt.title("Distribution of Profit", fontsize=16, fontweight="bold", fontname="Arial")
plt.xlabel("Profit", fontsize=12, fontweight="bold", fontname="Arial")
plt.ylabel("Frequency", fontsize=12, fontweight="bold", fontname="Arial")
plt.xticks(fontsize=10, fontname="Arial")
plt.yticks(fontsize=10, fontname="Arial")
plt.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.4)
plt.tight_layout()
plt.show()

# 5.7 Payment Mode (Pie & Donut Charts)
plt.figure(figsize=(8, 8))
plt.pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=["red", "skyblue", "gold"],
    explode=[0.05] * len(payment_counts),
    shadow=True,
    textprops={"fontsize": 11, "fontname": "Arial"}
)
plt.title("Payment Mode Distribution", fontsize=16, fontweight="bold", fontname="Arial")
plt.axis("equal")
plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 7))
plt.pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"width": 0.4},
    colors=["red", "skyblue", "gold"],
    explode=[0.03] * len(payment_counts),
    shadow=True
)
plt.title("Payment Mode Distribution", fontsize=16, fontweight="bold", fontname="Arial")
plt.axis("equal")
plt.tight_layout()
plt.show()

# 5.8 Discount Percentage vs Sales (Scatter Plot)
plt.figure(figsize=(10, 6))
plt.scatter(
    df["Discount_Percent"],
    df["Sales"],
    s=45,
    alpha=0.6,
    edgecolors="black",
    linewidths=0.5
)
plt.title("Discount Percentage vs Sales", fontsize=16, fontweight="bold", fontname="Arial")
plt.xlabel("Discount Percentage", fontsize=12, fontweight="bold", fontname="Arial")
plt.ylabel("Sales", fontsize=12, fontweight="bold", fontname="Arial")
plt.xticks(fontsize=10, fontname="Arial")
plt.yticks(fontsize=10, fontname="Arial")
plt.grid(True, linestyle="--", linewidth=0.7, alpha=0.3)
plt.tight_layout()
plt.show()

# ==============================================================================
# 6. SEABORN & SPECIALIZED VISUALIZATIONS
# ==============================================================================
# 6.1 Average Sales by Region
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Region", y="Sales")
plt.title("Average Sales by Region")
plt.xlabel("Region")
plt.ylabel("Average Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6.2 Regression Plot (Discount vs Sales)
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x="Discount_Percent", y="Sales", scatter_kws={"alpha": 0.4})
plt.title("Relationship Between Discount Percentage and Sales")
plt.xlabel("Discount Percentage")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# 6.3 Pair Plot (500-sample subset)
pair_cols = ["Sales", "Profit", "Quantity", "Delivery_Days", "Customer_Satisfaction"]
pair_sample = df[pair_cols].sample(n=500, random_state=42)
sns.pairplot(pair_sample)
plt.show()

# 6.4 Correlation Heatmap
corr_cols = [
    "Sales", "Profit", "Quantity", "Discount_Percent",
    "Delivery_Days", "Rating", "Customer_Satisfaction"
]
plt.figure(figsize=(10, 7))
sns.heatmap(df[corr_cols].corr(), annot=True, fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of E-Commerce Variables")
plt.tight_layout()
plt.show()

# 6.5 Violin Plot (Sales Distribution by Customer Segment)
plt.figure(figsize=(10, 5))
sns.violinplot(data=df, x="Customer_Segment", y="Sales")
plt.title("Sales Distribution by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6.6 Waffle Chart (Customer Segment Proportions)
plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=segment_counts.to_dict(),
    title={"label": "Customer Segment Distribution"}
)
plt.show()

# 6.7 Product Word Cloud
product_text = " ".join(df["Product"].dropna().astype(str))
wc = WordCloud(width=1000, height=500, background_color="white").generate(product_text)
plt.figure(figsize=(12, 6))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Product Word Cloud")
plt.show()

# ==============================================================================
# 7. INTERACTIVE VISUALIZATIONS (PLOTLY)
# ==============================================================================
# 7.1 Plotly Express: Grouped Category Bar
category_summary = df.groupby("Product_Category", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
fig_px_cat = px.bar(
    category_summary,
    x="Product_Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Product Category"
)
fig_px_cat.show()

# 7.2 Plotly Express: Scatter Plot with Hover Metadata
fig_px_scatter = px.scatter(
    df,
    x="Discount_Percent",
    y="Sales",
    color="Product_Category",
    hover_data=["Product", "Region", "Profit"],
    title="Discount Percentage vs Sales"
)
fig_px_scatter.show()

# 7.3 Plotly Graph Objects: Multi-Trace Bar
fig_go = go.Figure()
fig_go.add_trace(go.Bar(x=category_summary["Product_Category"], y=category_summary["Sales"], name="Sales"))
fig_go.add_trace(go.Bar(x=category_summary["Product_Category"], y=category_summary["Profit"], name="Profit"))
fig_go.update_layout(
    title="Sales and Profit by Product Category",
    xaxis_title="Product Category",
    yaxis_title="Amount",
    barmode="group"
)
fig_go.show()

# ==============================================================================
# 8. PRODUCTION DASHBOARD (DASH APPLICATION)
# ==============================================================================
app = Dash(__name__)

# Key Performance Indicators (KPIs)
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
average_order_value = total_sales / total_orders if total_orders > 0 else 0

# Dashboard Figures
region_data = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
dash_region_fig = px.bar(region_data, x="Region", y="Sales", title="Sales by Region", text_auto=".2s")
dash_region_fig.update_traces(hovertemplate="<b>%{x}</b><br>Sales: %{y:,.0f}<extra></extra>")
dash_region_fig.update_layout(
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Arial", size=12),
    title=dict(font=dict(size=18, color="#1F2937")), xaxis_title="Region", yaxis_title="Sales",
    margin=dict(l=50, r=30, t=60, b=50)
)

monthly_data = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly_data["Order_Date"] = monthly_data["Order_Date"].astype(str)
dash_monthly_fig = px.line(monthly_data, x="Order_Date", y="Sales", markers=True, title="Monthly Sales Trend")
dash_monthly_fig.update_traces(line=dict(width=3), marker=dict(size=8), hovertemplate="<b>%{x}</b><br>Sales: %{y:,.0f}<extra></extra>")
dash_monthly_fig.update_layout(
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Arial", size=12),
    title=dict(font=dict(size=18, color="#1F2937")), xaxis_title="Month", yaxis_title="Sales",
    margin=dict(l=50, r=30, t=60, b=50)
)

profit_data = df.groupby("Product_Category", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
dash_profit_fig = px.bar(profit_data, x="Product_Category", y="Profit", title="Profit by Product Category", text_auto=".2s")
dash_profit_fig.update_traces(hovertemplate="<b>%{x}</b><br>Profit: %{y:,.0f}<extra></extra>")
dash_profit_fig.update_layout(
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Arial", size=12),
    title=dict(font=dict(size=18, color="#1F2937")), xaxis_title="Product Category", yaxis_title="Profit",
    margin=dict(l=50, r=30, t=60, b=50)
)

payment_data = df["Payment_Mode"].value_counts().reset_index()
payment_data.columns = ["Payment_Mode", "Orders"]
dash_payment_fig = px.pie(payment_data, names="Payment_Mode", values="Orders", title="Orders by Payment Mode", hole=0.45)
dash_payment_fig.update_traces(textposition="inside", textinfo="percent+label", hovertemplate="<b>%{label}</b><br>Orders: %{value}<extra></extra>")
dash_payment_fig.update_layout(
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Arial", size=12),
    title=dict(font=dict(size=18, color="#1F2937")), margin=dict(l=30, r=30, t=60, b=30)
)

card_style = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "textAlign": "center",
    "flex": "1",
    "margin": "5px"
}

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("E-Commerce Sales Dashboard", style={"margin": "0", "fontSize": "32px", "fontWeight": "bold"}),
                html.P("Sales, profitability and customer transaction analysis", style={"marginTop": "8px", "fontSize": "15px", "opacity": "0.85"})
            ],
            style={"backgroundColor": "#1F4E78", "color": "white", "padding": "25px 35px", "borderRadius": "12px", "marginBottom": "20px"}
        ),
        html.Div(
            [
                html.Div([html.H4("TOTAL SALES", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}), html.H2(f"{total_sales:,.0f}", style={"margin": "10px 0 0 0", "color": "#1F4E78"})], style=card_style),
                html.Div([html.H4("TOTAL PROFIT", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}), html.H2(f"{total_profit:,.0f}", style={"margin": "10px 0 0 0", "color": "#2E7D32"})], style=card_style),
                html.Div([html.H4("TOTAL ORDERS", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}), html.H2(f"{total_orders:,}", style={"margin": "10px 0 0 0", "color": "#7B1FA2"})], style=card_style),
                html.Div([html.H4("AVERAGE ORDER VALUE", style={"margin": "0", "color": "#6B7280", "fontSize": "13px"}), html.H2(f"{average_order_value:,.0f}", style={"margin": "10px 0 0 0", "color": "#C62828"})], style=card_style),
            ],
            style={"display": "flex", "flexWrap": "wrap", "marginBottom": "20px"}
        ),
        html.Div(
            [
                html.Div(dcc.Graph(figure=dash_region_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)", "flex": "1", "margin": "5px"}),
                html.Div(dcc.Graph(figure=dash_monthly_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)", "flex": "1", "margin": "5px"}),
            ],
            style={"display": "flex", "flexWrap": "wrap", "marginBottom": "10px"}
        ),
        html.Div(
            [
                html.Div(dcc.Graph(figure=dash_profit_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)", "flex": "1", "margin": "5px"}),
                html.Div(dcc.Graph(figure=dash_payment_fig, responsive=True), style={"backgroundColor": "white", "borderRadius": "12px", "padding": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)", "flex": "1", "margin": "5px"}),
            ],
            style={"display": "flex", "flexWrap": "wrap"}
        ),
        html.P(
            "Source: E-Commerce Transaction Dataset | Dashboard developed using Python and Dash",
            style={"textAlign": "center", "color": "#6B7280", "fontSize": "12px", "marginTop": "25px", "paddingBottom": "15px"}
        )
    ],
    style={"backgroundColor": "#F3F6F9", "padding": "25px", "fontFamily": "Arial, sans-serif", "minHeight": "100vh"}
)

if __name__ == "__main__":
    app.run(debug=False, jupyter_mode="external")
# ==============================================================================
# 9. SIDHARTH EDITION
# ==============================================================================
# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv(r"C:\Users\SIDHARTH\Downloads\ecommerce_sales_data_5000_with_missing_values.csv")

# Fill missing values: median for numeric, mode for categorical
data = data.fillna(data.median(numeric_only=True))
data = data.fillna(data.mode().iloc[0])

# Verify missing values count
print("Missing values per column:\n", data.isnull().sum())
print("Total missing values:", data.isnull().sum().sum())

# Drop duplicates
data = data.drop_duplicates()

# Verify duplicate count
print("Duplicate rows:", data.duplicated().sum())

# Line plot
data.groupby('Product_Category')['Sales'].sum().plot(kind='line')
plt.show()

# Bar plot
data.groupby('Product_Category')['Sales'].sum().plot(kind='bar')
plt.show()

# Histogram
data.groupby('Product_Category')['Sales'].sum().plot(kind='hist')
plt.show()

# Pie plot
data.groupby('Product_Category')['Sales'].sum().plot(kind='pie')
plt.show()

# Donut plot
data.groupby('Product_Category')['Sales'].sum().plot(kind='pie')
plt.gca().add_artist(plt.Circle((0,0),0.7,fc='white'))
plt.show()

# Scatter plot
plt.scatter(
    data.groupby('Product_Category')['Sales'].sum().index,
    data.groupby('Product_Category')['Sales'].sum().values
)
plt.show()
'''
}