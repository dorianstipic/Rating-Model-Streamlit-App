import streamlit as st
import pandas as pd
import seaborn as sns

# Set options
st.set_page_config(page_title='CAMELS and Market Analysis Dashboard', layout='wide')

# Gets data from session state
df_final = st.session_state.get('camels_variables')
df_input = st.session_state.get('camels_input')
df_bins = st.session_state.get('expert_bins')

# Data Manipulation Functions
@st.cache_data(ttl=7200) 
def benchmark_dataframe_totals(df, date):
    # Benchmark is the average across all data
    filter_df = df[df['Date'] == date]
    filter_df = pd.DataFrame(filter_df.sum(axis=0, numeric_only=True)).T
    filter_df.index = ['Benchmark values']
    df = filter_df.copy(deep=True)
    
    # Select CAMELS Variables
    df = df[[
        'Total Assets', 'Total Gross Loans',
    ]]
    
    return df

@st.cache_data(ttl=7200) 
def benchmark_dataframe_camels(df, date):
    # Benchmark is the average across all data
    filter_df = df[df['Date'] == date]
    filter_df = pd.DataFrame(filter_df.mean(axis=0, numeric_only=True)).T
    filter_df.index = ['Benchmark values']
    df = filter_df.copy(deep=True)

    # Capital Adequacy
    df['Tier 1 Capital Ratio'] = df['Tier 1 Capital'] / df['RWA']
    df['Debt to Equity Ratio'] = df['Total Liabilities'] / df['Total Equity']
    
    # Asset Quality
    df['NPL to Total Gross Loans Ratio'] = df['Stage 3 Exposure'] / df['Total Gross Loans']
    df['Loan Loss Provision Rate'] = df['Total Provisions'] / df['Total Gross Loans']
    df['Loan Loss Provision Rate Scaled'] = 0 # by definition
    
    # Management Quality
    df['Asset Growth Rate'] = (df['Total Assets'] - df['Total Assets (t-1)']) / df['Total Assets (t-1)']
    df['Asset Growth Rate (t-1)'] = (df['Total Assets (t-1)'] - df['Total Assets (t-2)']) / df['Total Assets (t-2)']
    df['Asset Growth Rate (t-2)'] = (df['Total Assets (t-2)'] - df['Total Assets (t-3)']) / df['Total Assets (t-3)']
    df['Asset Growth Rate 3Y Average'] = df[['Asset Growth Rate', 'Asset Growth Rate (t-1)', 'Asset Growth Rate (t-2)']].mean(axis=1)
    df['Efficiency Ratio'] = df['Expenses'] / df['Net Operating Income']
    
    # Earnings
    df['Return on Assets (ROA)'] = df['Net Income'] / ((df['Total Assets'] + df['Total Assets (t-1)']) / 2)
    df['Interest Expenses to Interest Income Ratio'] = df['Interest Expenses'] / df['Interest Income']
    
    # Liquidity
    df['Cash Ratio'] = df['Liquid Assets'] / df['Current Liabilities']
    
    # Sensitivity
    df['Non Interest Income Share'] = df['Non Interest Income'] / (df['Non Interest Income'] + df['Interest Income'])

    # Select CAMELS Variables
    df = df[[
        'Tier 1 Capital Ratio', 'Debt to Equity Ratio', # C
        'NPL to Total Gross Loans Ratio', 'Loan Loss Provision Rate',# A
        'Asset Growth Rate 3Y Average', 'Efficiency Ratio',# M
        'Return on Assets (ROA)', 'Interest Expenses to Interest Income Ratio',# E
        'Liquidity Coverage Ratio (LCR)', 'Cash Ratio',# L
        'Non Interest Income Share'# S
    ]]

    return df

@st.cache_data(ttl=7200) 
def df_var2(df, date):

    df_all = df.copy(deep=True)
    df_all = df_all.set_index('Institution Name')
    df_all = df_all[df_all['Date'] == date]

    # Capital Adequacy
    df_all['Tier 1 Capital Ratio'] = df_all['Tier 1 Capital'] / df_all['RWA']
    df_all['Debt to Equity Ratio'] = df_all['Total Liabilities'] / df_all['Total Equity']

    # Asset Quality
    df_all['NPL to Total Gross Loans Ratio'] = df_all['Stage 3 Exposure'] / df_all['Total Gross Loans']
    df_all['Loan Loss Provision Rate'] = df_all['Total Provisions'] / df_all['Total Gross Loans']
    # Use unscaled version
    # df_all["Loan Loss Provision Rate Scaled"] = abs(df_all['Loan Loss Provision Rate']-df_all['Market Loan Loss Rate'])

    # Management Quality
    df_all['Asset Growth Rate'] = (df_all['Total Assets'] - df_all['Total Assets (t-1)']) / df_all['Total Assets (t-1)']
    df_all['Asset Growth Rate (t-1)'] = (df_all['Total Assets (t-1)'] - df_all['Total Assets (t-2)']) / df_all['Total Assets (t-2)']
    df_all['Asset Growth Rate (t-2)'] = (df_all['Total Assets (t-2)'] - df_all['Total Assets (t-3)']) / df_all['Total Assets (t-3)']
    df_all['Asset Growth Rate 3Y Average'] = df_all[['Asset Growth Rate', 'Asset Growth Rate (t-1)', 'Asset Growth Rate (t-2)']].mean(axis=1)
    df_all['Efficiency Ratio'] = df_all['Expenses'] / df_all['Net Operating Income']

    # Earnings
    df_all['Return on Assets (ROA)'] = df_all['Net Income'] / ((df_all['Total Assets'] + df_all['Total Assets (t-1)']) / 2)
    df_all['Interest Expenses to Interest Income Ratio'] = df_all['Interest Expenses'] / df_all['Interest Income']

    # Liquidity
    df_all['Cash Ratio'] = df_all['Liquid Assets'] / df_all['Current Liabilities']

    # Sensitivity
    df_all['Non Interest Income Share'] = df_all['Non Interest Income'] / (df_all['Non Interest Income'] + df_all['Interest Income'])

    # Select CAMELS Variables
    df_final_var = df_all[[
        'Total Assets', 'Total Gross Loans',
        'Tier 1 Capital Ratio', 'Debt to Equity Ratio',                        # C
        'NPL to Total Gross Loans Ratio', 'Loan Loss Provision Rate',          # A
        'Asset Growth Rate 3Y Average', 'Efficiency Ratio',                    # M
        'Return on Assets (ROA)', 'Interest Expenses to Interest Income Ratio',# E
        'Liquidity Coverage Ratio (LCR)', 'Cash Ratio',                        # L
        'Non Interest Income Share'                                            # S
    ]]

    return df_final_var

@st.cache_data(ttl=7200)
def market_analysis_dataframe(df_tot):
    df_tot_market = df_tot.copy(deep=True)
    df_tot_market['Total Assets Market Share'] = df_tot_market['Total Assets'] / df_tot_market.loc['Benchmark values', 'Total Assets']
    df_tot_market['Total Gross Loans Market Share'] = df_tot_market['Total Gross Loans'] / df_tot_market.loc['Benchmark values', 'Total Gross Loans']

    for c_var in df_tot_market.columns[2:]:
        df_tot_market[c_var + ' Difference'] = ((df_tot_market[c_var] - df_tot_market.loc['Benchmark values', c_var])
                                                / df_tot_market.loc['Benchmark values', c_var])

    df_tot_market = df_tot_market[[
        'Total Assets Market Share', 'Total Gross Loans Market Share',
        'Tier 1 Capital Ratio Difference', 'Debt to Equity Ratio Difference',
        'NPL to Total Gross Loans Ratio Difference', 'Loan Loss Provision Rate Difference',
        'Asset Growth Rate 3Y Average Difference', 'Efficiency Ratio Difference', 
        'Return on Assets (ROA) Difference', 'Interest Expenses to Interest Income Ratio Difference', 
        'Liquidity Coverage Ratio (LCR) Difference', 'Cash Ratio Difference',
        'Non Interest Income Share Difference']].drop(index='Benchmark values')

    return df_tot_market

@st.cache_resource(ttl=7200)
def styler_rel(df_tot_market, exp_bins):

    cm_green = sns.light_palette("#175C2C", as_cmap=True)
    cm_blend_reverse = sns.blend_palette(colors=['#AA2417', '#FFECBD', '#175C2C'], as_cmap=True)
    cm_blend = sns.blend_palette(colors=['#175C2C', '#FFECBD', '#AA2417'], as_cmap=True)

    styled_market_df_table = df_tot_market.style.format('{:.2%}')    
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_green, subset=['Total Assets Market Share'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_green, subset=['Total Gross Loans Market Share'])

    for c_var in styled_market_df_table.columns[2:]:
        c_var_pom = " ".join(c_var.split(" ")[0:-1])  # everything but last word
        if c_var_pom == 'Loan Loss Provision Rate':
            styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=[c_var])
        else:
            if exp_bins.loc[c_var_pom, "Reverse"]:
                styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend_reverse, subset=[c_var])
            else:
                styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=[c_var])
        
    return styled_market_df_table


@st.cache_resource(ttl=7200)
def styler_abs(df_tot_market, exp_bins):
    
    styled_market_df_table = df_tot_market.style.format('{:.2%}').format('{:,.2f}', subset=['Total Assets', 'Total Gross Loans'])
    
    cm_green = sns.light_palette("#175C2C", as_cmap=True)
    cm_blend_reverse = sns.blend_palette(colors=['#AA2417', '#FFECBD', '#175C2C'], as_cmap=True)
    cm_blend = sns.blend_palette(colors=['#175C2C', '#FFECBD', '#AA2417'], as_cmap=True)

    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_green, subset=['Total Assets'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_green, subset=['Total Gross Loans'])

    for c_var in styled_market_df_table.columns[2:]:
        if c_var == 'Loan Loss Provision Rate':
            styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=[c_var])
        else:
            if exp_bins.loc[c_var, "Reverse"]:
                styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend_reverse, subset=[c_var])
            else:
                styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=[c_var])
    
    return styled_market_df_table

# Callback function to update session state, date index
def update_benchmark_date():
    st.session_state['selected_bench_date_index'] = sorted(df_input['Date'].unique()).index(st.session_state['selected_bench_date'])

# Checks if Data is Uploaded 
if df_input is not None:

    # Initialize Session State
    if 'selected_bench_date_index' not in st.session_state:
        st.session_state['selected_bench_date_index'] = len(sorted(df_input['Date'].unique())) - 1

    # Create Date Selectbox with callback
    st.selectbox(r"$\textsf{\normalsize Select Date:}$", 
                 options=sorted(df_input['Date'].unique()), 
                 index=st.session_state['selected_bench_date_index'], 
                 key='selected_bench_date',
                 on_change=update_benchmark_date)

    # Get CAMELS data and calculate Benchmark
    df_bench_camels = benchmark_dataframe_camels(df_input, st.session_state['selected_bench_date'])
    df_bench_totals = benchmark_dataframe_totals(df_input, st.session_state['selected_bench_date'])
    df_bench = pd.concat([df_bench_totals, df_bench_camels], axis=1)
    df_out = df_var2(df_input, st.session_state['selected_bench_date'])
    df_tot_sum = pd.concat([df_bench, df_out], axis=0)
    df_tot_sum.index.name = "Institution Name"
    df_tot_market = market_analysis_dataframe(df_tot_sum)
    
    # Market Analysis Dataframe
    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';"
            ">CAMELS Variables Relative Differences Compared to Benchmark</div>", unsafe_allow_html=True)
    st.dataframe(styler_rel(df_tot_market, df_bins), use_container_width=True)
    
    # with st.expander('Click to show underlying data'):
    st.markdown('---')
    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';"
            ">CAMELS Variables - Benchmark</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(df_tot_sum.loc["Benchmark values", :]).T.style.format('{:.2%}').format('{:,.2f}', subset=['Total Assets', 'Total Gross Loans']))
    
    st.markdown('---')
    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';"
            ">CAMELS Variables</div>", unsafe_allow_html=True)
    st.dataframe(styler_abs(df_tot_sum.drop(index="Benchmark values"), df_bins))

# Display Text when Data Input is Missing
else:
    st.markdown(
        "<div style='text-align: left; font-size: 18px; font-weight: normal; font-family: Arial';" 
        ">No dataframe uploaded. Please upload file in <b><i>Data Upload and Information</i></b> section!</div>", 
        unsafe_allow_html=True
    )
