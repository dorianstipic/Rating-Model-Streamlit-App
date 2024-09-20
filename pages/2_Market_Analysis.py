import streamlit as st
import pandas as pd
import seaborn as sns

# Set options
st.set_page_config(page_title='CAMELS and Market Analysis Dashboard', layout='wide')

# Gets data from session state
df_var = st.session_state.get('camels_variables')
df_input = st.session_state.get('camels_input')
df_bins = st.session_state.get('expert_bins')

# Data Manipulation Functions

@st.cache_data(ttl=7200) 
def benchmark_dataframe(df, date):
    filter_df = df[df['Date'] == date]
    filter_df = pd.DataFrame(filter_df.sum(axis=0, numeric_only=True)).T
    filter_df.index = ['Benchmark values']
    df = filter_df.copy(deep=True)

    df['Tier 1 Capital Ratio'] = df['Tier 1 Capital'] / df['RWA']
    df['Debt to Equity Ratio'] = df['Total Liabilities'] / df['Total Equity']
    df['NPL to Total Gross Loans Ratio'] = df['Stage 3 Exposure'] / df['Total Gross Loans']
    df['Loan Loss Provision Rate'] = df['Total Provisions'] / df['Total Gross Loans']
    df['Efficiency Ratio'] = df['Expenses'] / df['Net Operating Income']
    df['Return on Assets (ROA)'] = df['Net Income'] / ((df['Total Assets'] + df['Total Assets (t-1)']) / 2)
    df['Interest Expenses to Interest Income Ratio'] = df['Interest Expenses'] / df['Interest Income']
    df['Cash Ratio'] = df['Liquid Assets'] / df['Current Liabilities']
    df['Non Interest Income Share'] = df['Non Interest Income'] / (df['Non Interest Income'] + df['Interest Income'])

    df = df[['Total Assets', 'Total Gross Loans',
             'Tier 1 Capital Ratio', 'Debt to Equity Ratio',
             'NPL to Total Gross Loans Ratio', 'Loan Loss Provision Rate', 'Efficiency Ratio',
             'Return on Assets (ROA)', 'Interest Expenses to Interest Income Ratio',
             'Cash Ratio', 'Non Interest Income Share']]

    return df.T

@st.cache_data(ttl=7200)
def variables_dataframe(df_inputs, df_variables, date):
    df_inputs = df_inputs[df_inputs['Date'] == date]
    df_inputs = df_inputs.copy(deep=True)  # removes SettingWithCopyWarning
    df_inputs['Loan Loss Provision Rate'] = df_inputs['Total Provisions'] / df_inputs['Total Gross Loans']
    df_inputs = df_inputs[['Total Assets', 'Total Gross Loans', 'Loan Loss Provision Rate']]

    df_variables = df_variables[df_variables['Date'] == date]
    df_variables = df_variables.drop(columns=['Date', 'Loan Loss Provision Rate Scaled', 'Asset Growth Rate 3Y Average', 'Liquidity Coverage Ratio (LCR)'])

    df_all_vars = pd.merge(df_inputs, df_variables, how='inner', left_index=True, right_index=True)

    return df_all_vars.T

@st.cache_resource(ttl=7200)
def market_analysis_dataframe(bench_df, var_df):
    market_df = pd.merge(var_df, bench_df, how='inner', left_index=True, right_index=True).T

    market_df['Total Assets Market Share'] = market_df['Total Assets'] / market_df.loc['Benchmark values']['Total Assets']
    market_df['Total Gross Loans Market Share'] = market_df['Total Gross Loans'] / market_df.loc['Benchmark values']['Total Gross Loans']
    market_df['Tier 1 Capital Ratio Difference'] = (
        market_df['Tier 1 Capital Ratio'] - market_df.loc['Benchmark values']['Tier 1 Capital Ratio']
    ) / market_df.loc['Benchmark values']['Tier 1 Capital Ratio']
    market_df['Debt to Equity Ratio Difference'] = (
        market_df['Debt to Equity Ratio'] - market_df.loc['Benchmark values']['Debt to Equity Ratio']
    ) / market_df.loc['Benchmark values']['Debt to Equity Ratio']
    market_df['NPL to Total Gross Loans Ratio Difference'] = (
        market_df['NPL to Total Gross Loans Ratio'] - market_df.loc['Benchmark values']['NPL to Total Gross Loans Ratio']
    ) / market_df.loc['Benchmark values']['NPL to Total Gross Loans Ratio']
    market_df['Loan Loss Provision Rate Difference'] = abs((
        market_df['Loan Loss Provision Rate'] - market_df.loc['Benchmark values']['Loan Loss Provision Rate']
    ) / market_df.loc['Benchmark values']['Loan Loss Provision Rate'])
    market_df['Efficiency Ratio Difference'] = (
        market_df['Efficiency Ratio'] - market_df.loc['Benchmark values']['Efficiency Ratio']
    ) / market_df.loc['Benchmark values']['Efficiency Ratio']
    market_df['Return on Assets (ROA) Difference'] = (
        market_df['Return on Assets (ROA)'] - market_df.loc['Benchmark values']['Return on Assets (ROA)']
    ) / market_df.loc['Benchmark values']['Return on Assets (ROA)']
    market_df['Interest Expenses to Interest Income Ratio Difference'] = (
        market_df['Interest Expenses to Interest Income Ratio'] - market_df.loc['Benchmark values']['Interest Expenses to Interest Income Ratio']
    ) / market_df.loc['Benchmark values']['Interest Expenses to Interest Income Ratio']
    market_df['Cash Ratio Difference'] = (
        market_df['Cash Ratio'] - market_df.loc['Benchmark values']['Cash Ratio']
    ) / market_df.loc['Benchmark values']['Cash Ratio']
    market_df['Non Interest Income Share Difference'] = (
        market_df['Non Interest Income Share'] - market_df.loc['Benchmark values']['Non Interest Income Share']
    ) / market_df.loc['Benchmark values']['Non Interest Income Share']

    market_df_table = market_df[['Total Assets Market Share', 'Total Gross Loans Market Share',
                                 'Tier 1 Capital Ratio Difference', 'Debt to Equity Ratio Difference',
                                 'NPL to Total Gross Loans Ratio Difference', 'Loan Loss Provision Rate Difference',
                                 'Efficiency Ratio Difference', 'Return on Assets (ROA) Difference',
                                 'Interest Expenses to Interest Income Ratio Difference', 'Cash Ratio Difference',
                                 'Non Interest Income Share Difference']].drop(index='Benchmark values')

    cm_green = sns.light_palette("#175C2C", as_cmap=True)
    cm_blend_reverse = sns.blend_palette(colors=['#AA2417', '#FFECBD', '#175C2C'], as_cmap=True)
    cm_blend = sns.blend_palette(colors=['#175C2C', '#FFECBD', '#AA2417'], as_cmap=True)
    styled_market_df_table = market_df_table.style.format('{:.2%}')
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_green, subset=['Total Assets Market Share'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_green, subset=['Total Gross Loans Market Share'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend_reverse, subset=['Tier 1 Capital Ratio Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=['Debt to Equity Ratio Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=['NPL to Total Gross Loans Ratio Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=['Loan Loss Provision Rate Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=['Efficiency Ratio Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend_reverse, subset=['Return on Assets (ROA) Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend, subset=['Interest Expenses to Interest Income Ratio Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend_reverse, subset=['Cash Ratio Difference'])
    styled_market_df_table = styled_market_df_table.background_gradient(cmap=cm_blend_reverse, subset=['Non Interest Income Share Difference'])

    return styled_market_df_table, market_df

# Callback function to update session state
def update_benchmark_date():
    st.session_state.benchmark_date = sorted(df_input['Date'].unique()).index(st.session_state.selected_benchmark_date)

# Checks if Data is Uploaded 
if df_input is not None:
    df_input = df_input.set_index('Institution Name')

    # Initialize Session State
    if 'benchmark_date' not in st.session_state:
        st.session_state.benchmark_date = len(sorted(df_input['Date'].unique())) - 1

    # Create Date Selectbox with callback
    st.selectbox(r"$\textsf{\normalsize Select Date:}$", sorted(df_input['Date'].unique()), 
                 index=st.session_state.benchmark_date, key='selected_benchmark_date', on_change=update_benchmark_date)

    # Market Analysis Dataframe
    st.dataframe(market_analysis_dataframe(benchmark_dataframe(df_input, st.session_state.selected_benchmark_date),
                                           variables_dataframe(df_input, df_var, st.session_state.selected_benchmark_date))[0],
                                           use_container_width=True)

# Display Text when Data Input is Missing
else:
    st.markdown("<div style='text-align: left; font-size: 18px; font-weight: normal; font-family: Arial';" 
            ">No dataframe uploaded. Please upload file in <b><i>Data Upload and Information</i></b> section!</div>", unsafe_allow_html=True)
