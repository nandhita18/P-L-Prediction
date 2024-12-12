import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from preprocessing import df


business_revenue = df.groupby('BUSINESS GROUP')['C_Revenue'].sum().reset_index()
#sort by revenue in descending order and select top 15 businesses
top_15_businesses = business_revenue.sort_values(by='C_Revenue', ascending=False).head(15)

# Group by BUSINESS GROUP and calculate total revenue
business_revenue = df.groupby('BUSINESS GROUP')['C_Revenue'].sum().reset_index()
business_revenue = business_revenue.sort_values(by='C_Revenue', ascending=False)

# Calculate cumulative revenue and percentage
business_revenue['Cumulative_Revenue'] = business_revenue['C_Revenue'].cumsum()
business_revenue['Cumulative_Percentage'] = business_revenue['Cumulative_Revenue'] / business_revenue['C_Revenue'].sum() * 100

# Filter businesses contributing to 80% of revenue
top_contributors = business_revenue[business_revenue['Cumulative_Percentage'] <= 80]

#Top 15 business with least revenue 
least_15_businesses = business_revenue.sort_values(by='C_Revenue', ascending=False).tail(15)


# Create Month-Year column in the desired format
df['Month-Year'] = pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str))
df['Month-Year'] = df['Month-Year'].dt.strftime('%Y-%m')
df['Month-Year'] = pd.to_datetime(df['Month-Year'], errors='coerce')
# Group by Month-Year for combined depreciation trends
df['Quarter'] = df['Month-Year'].dt.to_period('Q')  
df[' DEPRECIATION INVENTORY '] = df[' DEPRECIATION INVENTORY '].clip(lower=0)
# Recalculate grouped data
depreciation_trend_quarter = df.groupby('Quarter')[[' DEPRECIATION INVENTORY ', ' DEPRECIATION ON ASSET ']].sum().reset_index()
# Convert the 'Quarter' back to string for better labeling in the chart
depreciation_trend_quarter['Quarter'] = depreciation_trend_quarter['Quarter'].astype(str)


#Top 15 businesses with highest PAT amount
business_pat = df.groupby('BUSINESS GROUP')[" PROFIT AFTER TAX "].sum().reset_index()
#sort by revenue in descending order and select top 15 businesses
top_15_pat = business_pat.sort_values(by=' PROFIT AFTER TAX ', ascending=False).head(15)


#Revenue distribution over the years
top_15_revenue_data = df[df['BUSINESS GROUP'].isin(top_15_businesses)]
#Group by year
yearly_revenue = df.groupby(['DATE', 'BUSINESS GROUP'])['C_Revenue'].sum().unstack()


#yearly pat distribution of the top 15 contributors
yearly_pat = df.groupby(['YEAR', 'BUSINESS GROUP'])['C_PAT'].sum().unstack(fill_value=0)
#the revenue distribution of the companies over the years
new = df.groupby(['BUSINESS GROUP',"YEAR"])['C_Revenue'].sum().reset_index()
years_required = list(range(2019, df['YEAR'].max() + 1))
consistent_biz = (
    df[df['YEAR'].isin(years_required)]
    .groupby('BUSINESS GROUP')['YEAR']
    .nunique()
)
consistent_biz = consistent_biz[consistent_biz == len(years_required)].index
#Filter the data for these consistent businesses
consistent_data = df[df['BUSINESS GROUP'].isin(consistent_biz)]
#aggregate revenue and groupby
aggregated_data = consistent_data.groupby(['BUSINESS GROUP', 'YEAR'], as_index=False)['C_Revenue'].sum()
#Identify inconsistent businesses
consistent_biz = (
    df[df['YEAR'].isin(years_required)]
    .groupby('BUSINESS GROUP')['YEAR']
    .nunique()
)
inconsistent_biz = consistent_biz[consistent_biz < len(years_required)].index
#Filter the data for these inconsistent businesses
inconsistent_data = df[df['BUSINESS GROUP'].isin(inconsistent_biz)]
#aggregate revenue and groupby
aggregated_inconsistent_data = inconsistent_data.groupby(['BUSINESS GROUP', 'YEAR'], as_index=False)['C_Revenue'].sum()
#Gross margin contribution of businesses and sub businesses 
sunburst_data = df.groupby(['BUSINESS GROUP', 'MATERIAL GROUP']).agg({'C_Gross_Margin': 'sum'}).reset_index()
#Filter out rows with negative values
sunburst_data = sunburst_data[sunburst_data['C_Gross_Margin'] > 0]


# forcast display

monthly_combined_results = pd.read_csv("monthly_combined_results.csv")
monthly_combined_results_r = pd.read_csv("monthly_combined_results_r.csv")
monthly_combined_results_e = pd.read_csv("monthly_combined_results_e.csv")
monthly_combined_results_eb = pd.read_csv("monthly_combined_results_eb.csv")
monthly_combined_results_p = pd.read_csv("monthly_combined_results_p.csv")
monthly_combined_results_pa = pd.read_csv("monthly_combined_results_pa.csv")
monthly_combined_results_man = pd.read_csv("monthly_combined_results_manpower.csv")
monthly_combined_results_biz = pd.read_csv("monthly_combined_results_biztrade.csv")
monthly_combined_results_pro = pd.read_csv("monthly_combined_results_pro.csv")


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Example figures (these should be replaced with your actual data)
fig1 = px.pie(top_15_businesses, values='C_Revenue', names='BUSINESS GROUP',title= 'Top 15 Revenue contributors', hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
fig2 = px.pie(top_contributors, values='C_Revenue', names='BUSINESS GROUP',title = '80% of Revenue contributors', color_discrete_sequence=px.colors.sequential.RdBu)
fig3 = px.bar(depreciation_trend_quarter, x='Quarter', y=[' DEPRECIATION INVENTORY ', ' DEPRECIATION ON ASSET '], barmode='group',title='Depreciation Trends', color_discrete_sequence=px.colors.sequential.RdBu)
fig4 = px.bar(top_15_pat, x=' PROFIT AFTER TAX ', y='BUSINESS GROUP', orientation='h', title = 'Top 15 PAT contributors',color_discrete_sequence=px.colors.sequential.RdBu)
fig5 = go.Figure([go.Scatter(x=yearly_revenue.index, y=yearly_revenue[business], mode='lines+markers', name=business, visible='legendonly' if i >= 5 else True) for i, business in enumerate(yearly_revenue.columns)])
fig6 = go.Figure([go.Bar(x=yearly_pat.index, y=yearly_pat[business], name=business) for business in yearly_pat.columns])

# Define app layout
app.layout = html.Div([
    dbc.Row([
        # Side Navigation Bar
        dbc.Col(
            dbc.Nav([
                dbc.NavLink("EDA", href="/eda", active="exact", style={'margin': '10px'}),
                dbc.NavLink("Factors Forcast", href="/forecasting", active="exact", style={'margin': '10px'}),
                dbc.NavLink("Profitability Forcast", href="/Profitability", active="exact", style={'margin': '10px'}),
            ], vertical=True, pills=True),
            width=2, style={'backgroundColor': '#f0f0f0', 'height': '100vh', 'position': 'fixed', 'zIndex': 1000}
        ),
            
        # Main content area
        dbc.Col(
            html.Div([
                dcc.Location(id='url', refresh=False),  # Location for page routing
                html.Div(id='page-content')  # This will dynamically load the content based on the page
            ], style={'marginLeft': '250px', 'paddingTop': '40px'})  # Adjusted margin for content area
        )
    ])
])

# EDA Page Layout
eda_layout = html.Div([
    html.H1('Exploratory Data Analysis (EDA)', style={'textAlign': 'center'}),
    dbc.Row([  
        dbc.Col(dcc.Graph(figure=fig1), width=6),  
        dbc.Col(dcc.Graph(figure=fig2), width=6),  
    ]),
    dbc.Row([  
        dbc.Col(dcc.Graph(figure=fig3), width=6),  
        dbc.Col(dcc.Graph(figure=fig4), width=6), 
    ]),
    
    html.H3('  Monthly Revenue Distribution for Top 15 Businesses'),
    dcc.Graph(figure=fig5),
    
    html.H3('  PAT Distribution for Top 15 Businesses'),
    dcc.Graph(figure=fig6),
])

# Forecasting Page Layout
forecasting_layout = html.Div([
    html.H1('  Forecast  ', style={'textAlign': 'center'}),
    html.Div([
        html.H3('  Actual and Predicted Gross Margin'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results['Date'], y=monthly_combined_results['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results['Date'], y=monthly_combined_results['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='Gross Margin')),

        html.H3('  Actual and Predicted Revenue'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_r['Date'], y=monthly_combined_results_r['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_r['Date'], y=monthly_combined_results_r['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='Revenue')),

        html.H3('  Actual and Predicted EBITDA'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_e['Date'], y=monthly_combined_results_e['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_e['Date'], y=monthly_combined_results_e['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='EBITDA')),
      
        html.H3('  Actual and Predicted EBIT'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_eb['Date'], y=monthly_combined_results_eb['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_eb['Date'], y=monthly_combined_results_eb['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='EBIT')),

        html.H3('  Actual and Predicted PBT'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_p['Date'], y=monthly_combined_results_p['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_p['Date'], y=monthly_combined_results_p['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='PBT')),

        html.H3('  Actual and Predicted PAT'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_pa['Date'], y=monthly_combined_results_pa['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_pa['Date'], y=monthly_combined_results_pa['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='PAT')),
        
        html.H3('  Actual and Predicted ManPower Cost'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_man['Date'], y=monthly_combined_results_man['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_man['Date'], y=monthly_combined_results_man['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='PBT')),
        
        html.H3('  Actual and Predicted Biz Trading Cost'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_biz['Date'], y=monthly_combined_results_biz['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_biz['Date'], y=monthly_combined_results_biz['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='PBT')),
    ])
])

Profitability_layout = html.Div([
    html.H1('  Profitability  ', style={'textAlign': 'center'}),
        html.H3('  Actual and Predicted Profitability'),
        dcc.Graph(figure=go.Figure([
            go.Scatter(x=monthly_combined_results_pro['Date'], y=monthly_combined_results_pro['Actual'], mode='lines+markers', name='Actual Values', line=dict(color='blue')),
            go.Scatter(x=monthly_combined_results_pro['Date'], y=monthly_combined_results_pro['Predicted'], mode='lines+markers', name='Predicted Values', line=dict(color='red', dash='dash'))
        ]).update_layout(xaxis_title='Date', yaxis_title='Profidabilty')),
])

# Callback to update the page content based on URL
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/eda':
        return eda_layout
    elif pathname == '/forecasting':
        return forecasting_layout
    elif pathname == '/Profitability':
        return Profitability_layout
    else:
        return eda_layout  
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




