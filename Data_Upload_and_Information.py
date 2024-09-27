# Imports

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

# Page Configuration

st.set_page_config(page_title='CAMELS and Market Analysis Dashboard',layout='wide')

# Variables Dataframe Functions

@st.cache_data(ttl=7200)
def loan_loss_provision_market(df):

    df_group = df.groupby(by='Date',sort=False).sum()[['Total Provisions','Total Gross Loans']]
    df_group['Market Loan Loss Rate'] = df_group['Total Provisions']/df_group['Total Gross Loans']
    df_group = df_group.reset_index()

    return df_group

@st.cache_data(ttl=7200)
def df_var(df):

    # Merging Loan Loss Providion market and Input Data
    df_all = pd.merge(df,loan_loss_provision_market(df),how='inner',on='Date')
    df_all = df_all.set_index('Institution Name')
    df_all = df_all.drop(columns=['Total Provisions_y','Total Gross Loans_y'])
    df_all = df_all.rename(columns={'Total Provisions_x':'Total Provisions','Total Gross Loans_x':'Total Gross Loans'})

    # Capital Adequacy
    df_all['Tier 1 Capital Ratio'] = df_all['Tier 1 Capital'] / df_all['RWA']
    df_all['Debt to Equity Ratio'] = df_all['Total Liabilities'] / df_all['Total Equity']

    # Asset Quality
    df_all['NPL to Total Gross Loans Ratio'] = df_all['Stage 3 Exposure'] / df_all['Total Gross Loans']
    df_all['Loan Loss Provision Rate'] = df_all['Total Provisions'] / df_all['Total Gross Loans']
    df_all["Loan Loss Provision Rate Scaled"] = abs(df_all['Loan Loss Provision Rate']-df_all['Market Loan Loss Rate'])

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
    df_final_var = df_all[['Date','Tier 1 Capital Ratio','Debt to Equity Ratio','NPL to Total Gross Loans Ratio','Loan Loss Provision Rate Scaled',
                           'Asset Growth Rate 3Y Average','Efficiency Ratio','Return on Assets (ROA)','Interest Expenses to Interest Income Ratio',
                           'Liquidity Coverage Ratio (LCR)','Cash Ratio','Non Interest Income Share']]

    return df_final_var

@st.cache_data(ttl=7200)
def df_bins_and_null(df_final):

    df_ratings = df_final.copy(deep=True)

     # Tier 1 Capital Ratio Bins
    cond_tier1 = [(df_final['Tier 1 Capital Ratio']<=0.06),
                    (df_final['Tier 1 Capital Ratio']>0.06)&(df_final['Tier 1 Capital Ratio']<=0.1),
                    (df_final['Tier 1 Capital Ratio']>0.1)&(df_final['Tier 1 Capital Ratio']<=0.14),
                    (df_final['Tier 1 Capital Ratio']>0.14)&(df_final['Tier 1 Capital Ratio']<=0.2),
                    (df_final['Tier 1 Capital Ratio']>0.2),
                    (df_final['Tier 1 Capital Ratio'].isnull())]
    choice_tier1 =[5,4,3,2,1,5]
    df_ratings['Tier 1 Capital Ratio'] = np.select(cond_tier1,choice_tier1)
    # Debt to Equity Ratio bins
    cond_debt = [(df_final['Debt to Equity Ratio']<=6),
                    (df_final['Debt to Equity Ratio']>6)&(df_final['Debt to Equity Ratio']<=8),
                    (df_final['Debt to Equity Ratio']>8)&(df_final['Debt to Equity Ratio']<=10),
                    (df_final['Debt to Equity Ratio']>10)&(df_final['Debt to Equity Ratio']<=12),
                    (df_final['Debt to Equity Ratio']>12),
                    (df_final['Debt to Equity Ratio'].isnull())]
    choice_debt =[1,2,3,4,5,5]
    df_ratings['Debt to Equity Ratio'] = np.select(cond_debt,choice_debt)
    # NPL to Total Gross Loans Ratio
    cond_npl = [(df_final['NPL to Total Gross Loans Ratio']<=0.04),
                    (df_final['NPL to Total Gross Loans Ratio']>0.04)&(df_final['NPL to Total Gross Loans Ratio']<=0.08),
                    (df_final['NPL to Total Gross Loans Ratio']>0.08)&(df_final['NPL to Total Gross Loans Ratio']<=0.12),
                    (df_final['NPL to Total Gross Loans Ratio']>0.12)&(df_final['NPL to Total Gross Loans Ratio']<=0.16),
                    (df_final['NPL to Total Gross Loans Ratio']>0.16),
                    (df_final['NPL to Total Gross Loans Ratio'].isnull())]
    choice_npl =[1,2,3,4,5,5]
    df_ratings['NPL to Total Gross Loans Ratio'] = np.select(cond_npl,choice_npl)
    # Loan Loss Provision Rate Scaled
    cond_loan_loss = [(df_final['Loan Loss Provision Rate Scaled']<=0.02),
                    (df_final['Loan Loss Provision Rate Scaled']>0.02)&(df_final['Loan Loss Provision Rate Scaled']<=0.04),
                    (df_final['Loan Loss Provision Rate Scaled']>0.04)&(df_final['Loan Loss Provision Rate Scaled']<=0.06),
                    (df_final['Loan Loss Provision Rate Scaled']>0.06)&(df_final['Loan Loss Provision Rate Scaled']<=0.08),
                    (df_final['Loan Loss Provision Rate Scaled']>0.08),
                    (df_final['Loan Loss Provision Rate Scaled'].isnull())]
    choice_loan_loss =[1,2,3,4,5,5]
    df_ratings['Loan Loss Provision Rate Scaled'] = np.select(cond_loan_loss,choice_loan_loss)
    # Asset Growth Rate 3Y Average
    cond_asset = [(df_final['Asset Growth Rate 3Y Average']<=-0.03),
                    (df_final['Asset Growth Rate 3Y Average']>-0.03)&(df_final['Asset Growth Rate 3Y Average']<=0),
                    (df_final['Asset Growth Rate 3Y Average']>0)&(df_final['Asset Growth Rate 3Y Average']<=0.03),
                    (df_final['Asset Growth Rate 3Y Average']>0.03)&(df_final['Asset Growth Rate 3Y Average']<=0.06),
                    (df_final['Asset Growth Rate 3Y Average']>0.06),
                    (df_final['Asset Growth Rate 3Y Average'].isnull())]
    choice_asset =[5,4,3,2,1,5]
    df_ratings['Asset Growth Rate 3Y Average'] = np.select(cond_asset,choice_asset)
    # Efficiency Ratio
    cond_efficiency = [(df_final['Efficiency Ratio']<=0.5),
                    (df_final['Efficiency Ratio']>0.5)&(df_final['Efficiency Ratio']<=0.7),
                    (df_final['Efficiency Ratio']>0.7)&(df_final['Efficiency Ratio']<=0.9),
                    (df_final['Efficiency Ratio']>0.9)&(df_final['Efficiency Ratio']<=1.1),
                    (df_final['Efficiency Ratio']>1.1),
                    (df_final['Efficiency Ratio'].isnull())]
    choice_efficiency =[1,2,3,4,5,5]
    df_ratings['Efficiency Ratio'] = np.select(cond_efficiency,choice_efficiency)
    # Return on Assets (ROA)
    cond_roa = [(df_final['Return on Assets (ROA)']<=-0.002),
                    (df_final['Return on Assets (ROA)']>-0.002)&(df_final['Return on Assets (ROA)']<=0.001),
                    (df_final['Return on Assets (ROA)']>0.001)&(df_final['Return on Assets (ROA)']<=0.005),
                    (df_final['Return on Assets (ROA)']>0.005)&(df_final['Return on Assets (ROA)']<=0.01),
                    (df_final['Return on Assets (ROA)']>0.01),
                    (df_final['Return on Assets (ROA)'].isnull())]
    choice_roa =[5,4,3,2,1,5]
    df_ratings['Return on Assets (ROA)'] = np.select(cond_roa,choice_roa)
    # Interest Expenses to Interest Income Ratio
    cond_interest_ratio = [(df_final['Interest Expenses to Interest Income Ratio']<=0.07),
                    (df_final['Interest Expenses to Interest Income Ratio']>0.07)&(df_final['Interest Expenses to Interest Income Ratio']<=0.14),
                    (df_final['Interest Expenses to Interest Income Ratio']>0.14)&(df_final['Interest Expenses to Interest Income Ratio']<=0.21),
                    (df_final['Interest Expenses to Interest Income Ratio']>0.21)&(df_final['Interest Expenses to Interest Income Ratio']<=0.28),
                    (df_final['Interest Expenses to Interest Income Ratio']>0.28),
                    (df_final['Interest Expenses to Interest Income Ratio'].isnull())]
    choice_interest_ratio =[1,2,3,4,5,5]
    df_ratings['Interest Expenses to Interest Income Ratio'] = np.select(cond_interest_ratio,choice_interest_ratio)
    # Liquidity Coverage Ratio (LCR)
    cond_lcr = [(df_final['Liquidity Coverage Ratio (LCR)']<=1),
                    (df_final['Liquidity Coverage Ratio (LCR)']>1)&(df_final['Liquidity Coverage Ratio (LCR)']<=1.35),
                    (df_final['Liquidity Coverage Ratio (LCR)']>1.35)&(df_final['Liquidity Coverage Ratio (LCR)']<=1.7),
                    (df_final['Liquidity Coverage Ratio (LCR)']>1.7)&(df_final['Liquidity Coverage Ratio (LCR)']<=2),
                    (df_final['Liquidity Coverage Ratio (LCR)']>2),
                    (df_final['Liquidity Coverage Ratio (LCR)'].isnull())]
    choice_lcr =[5,4,3,2,1,5]
    df_ratings['Liquidity Coverage Ratio (LCR)'] = np.select(cond_lcr,choice_lcr)
    # Cash Ratio
    cond_cash = [(df_final['Cash Ratio']<=0.075),
                    (df_final['Cash Ratio']>0.075)&(df_final['Cash Ratio']<=0.15),
                    (df_final['Cash Ratio']>0.15)&(df_final['Cash Ratio']<=0.225),
                    (df_final['Cash Ratio']>0.225)&(df_final['Cash Ratio']<=0.3),
                    (df_final['Cash Ratio']>0.3),
                    (df_final['Cash Ratio'].isnull())]
    choice_cash =[5,4,3,2,1,5]
    df_ratings['Cash Ratio'] = np.select(cond_cash,choice_cash)
    # Non Interest Income Share
    cond_interest_share = [(df_final['Non Interest Income Share']<=0.1),
                    (df_final['Non Interest Income Share']>0.1)&(df_final['Non Interest Income Share']<=0.2),
                    (df_final['Non Interest Income Share']>0.2)&(df_final['Non Interest Income Share']<=0.3),
                    (df_final['Non Interest Income Share']>0.3)&(df_final['Non Interest Income Share']<=0.4),
                    (df_final['Non Interest Income Share']>0.4),
                    (df_final['Non Interest Income Share'].isnull())]
    choice_interest_share =[5,4,3,2,1,5]
    df_ratings['Non Interest Income Share'] = np.select(cond_interest_share,choice_interest_share)

    # Composite Final Rating
    df_ratings['Composite Final Score'] = (df_ratings[[
        'Tier 1 Capital Ratio',
        'Debt to Equity Ratio',
        'NPL to Total Gross Loans Ratio',
        'Loan Loss Provision Rate Scaled',
        'Asset Growth Rate 3Y Average',
        'Efficiency Ratio',
        'Return on Assets (ROA)',
        'Interest Expenses to Interest Income Ratio', 
        'Liquidity Coverage Ratio (LCR)',
        'Cash Ratio',
        'Non Interest Income Share']] * camels_weights.values).sum(axis=1)

    # Final Rating Score 10 categories (+- added)
    cond_final_rating = [
        (df_ratings['Composite Final Score']>=1)&(df_ratings['Composite Final Score']<1.25), # A+
        (df_ratings['Composite Final Score']>=1.25)&(df_ratings['Composite Final Score']<1.5), # A-
            
        (df_ratings['Composite Final Score']>=1.5)&(df_ratings['Composite Final Score']<1.95), # B+
        (df_ratings['Composite Final Score']>=1.95)&(df_ratings['Composite Final Score']<2.4), # B-
            
        (df_ratings['Composite Final Score']>=2.4)&(df_ratings['Composite Final Score']<2.9), # C+
        (df_ratings['Composite Final Score']>=2.9)&(df_ratings['Composite Final Score']<3.4), # C-
            
        (df_ratings['Composite Final Score']>=3.4)&(df_ratings['Composite Final Score']<3.9), # D+
        (df_ratings['Composite Final Score']>=3.9)&(df_ratings['Composite Final Score']<4.5), # D-
            
        (df_ratings['Composite Final Score']>=4.5)&(df_ratings['Composite Final Score']<4.75), # E+
        (df_ratings['Composite Final Score']>=4.75)&(df_ratings['Composite Final Score']<=5), # E-
        (df_ratings['Composite Final Score'].isnull())]
    choice_final_rating =['A+','A-','B+','B-','C+','C-','D+','D-','E+','E-','E-']
    df_ratings['Final Rating'] = np.select(cond_final_rating,choice_final_rating)

    df_ratings_column_order = ['Date','Final Rating','Composite Final Score',
                            'Tier 1 Capital Ratio','Debt to Equity Ratio',
                            'NPL to Total Gross Loans Ratio','Loan Loss Provision Rate Scaled',
                            'Asset Growth Rate 3Y Average','Efficiency Ratio',
                            'Return on Assets (ROA)','Interest Expenses to Interest Income Ratio', 
                            'Liquidity Coverage Ratio (LCR)','Cash Ratio',
                            'Non Interest Income Share']
        
    df_ratings = df_ratings.reindex(columns=df_ratings_column_order)

    return df_ratings

@st.cache_resource(ttl=7200)
def df_info_display(df):

    df = df.copy(deep=True)
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
    df = df.set_index('Date').style.format(precision=2,thousands=',',decimal='.')

    return df

# Hard-coded bins for variables

bins_dict = {'Tier 1 Capital Ratio':         ['expert', True, 0.06, 0.1, 0.14, 0.2], 
          'Debt to Equity Ratio':            ['expert', False, 6, 8, 10, 12],
          'NPL to Total Gross Loans Ratio':  ['expert', False, 0.04, 0.08, 0.12, 0.16],
          'Loan Loss Provision Rate Scaled': ['expert', False, 0.02, 0.04, 0.06, 0.08],
          'Asset Growth Rate 3Y Average':    ['expert', True, -0.03, 0, 0.03, 0.06],
          'Efficiency Ratio':                ['expert', False, 0.5, 0.7, 0.9, 1.1],
          'Return on Assets (ROA)':          ['expert', True, -0.002, 0.001, 0.005, 0.01],
          'Interest Expenses to Interest Income Ratio': ['expert', False,  0.07, 0.14, 0.21, 0.28],
          'Liquidity Coverage Ratio (LCR)':  ['expert', True,  1, 1.35, 1.7, 2],
          'Cash Ratio':                      ['expert', True,  0.075, 0.15, 0.225, 0.3],
          'Non Interest Income Share':       ['expert', True,  0.1, 0.2, 0.3, 0.4]}

# Variables Weights

camels_weights = pd.DataFrame({'Tier 1 Capital Ratio': 0.09,
              'Debt to Equity Ratio': 0.10,
              'NPL to Total Gross Loans Ratio': 0.15,
              'Loan Loss Provision Rate Scaled': 0.11,
              'Asset Growth Rate 3Y Average': 0.09,
              'Efficiency Ratio': 0.1,
              'Return on Assets (ROA)': 0.1,
              'Interest Expenses to Interest Income Ratio': 0.06, 
              'Liquidity Coverage Ratio (LCR)': 0.01,
              'Cash Ratio': 0.07,
              'Non Interest Income Share': 0.12}, index = ["Weight"])

# Initialize session state for data upload file

if 'upload' not in st.session_state:
    st.session_state.upload = None

# File uploader widget
st.markdown("<div style='text-align: center; font-size: 20px; font-family: Arial';" 
            ">Upload CAMELS Input Data:</div>", unsafe_allow_html=True)
upload_file = st.file_uploader('Upload File', label_visibility='collapsed', type="xlsx")

# If a file is uploaded, save it to session state and reset relevant variables

if upload_file:
    try:
        df = pd.read_excel(upload_file, sheet_name='Institution_Data')
        st.session_state.upload = df
        # Reset other session state variables when a new file is uploaded
        st.session_state.camels_input = None
        st.session_state.camels_variables = None
        st.session_state.expert_bins = None
        st.session_state.weights = None
        st.session_state.ratings = None
        # Clear cache on new data upload
        st.cache_resource.clear() # fixes plot resizing issue
    except:
        st.error('Error loading file. Please be sure to upload an XLSX file format.')

# If data uploaded in session state perform all functions

if st.session_state.upload is not None:

    # Data Manipulation and Preparation
    df_input = st.session_state.upload.copy(deep=True)

    try:
        df_final = df_var(st.session_state.upload)
    except:
        st.error('Error in data type!')

    exp_bins = pd.DataFrame(bins_dict, index=['Binning Method', 'Reverse', '1st_Threshold', '2nd_Threshold', '3rd_Threshold', '4th_Threshold']).T

    try:
        df_ratings = df_bins_and_null(df_final)
    except:
        st.error('Please check the following in the .xlsx file:\n'
         '1. The \'Date\' column is of datetime format\n'
         '2. The \'Institution Name\' column is of string/object type\n'
         '3. The rest of the columns are numerical (integer or float type)')
        st.stop()

    # Dataframe information
    st.markdown("<div style='text-align: center; font-size: 20px; font-family: Arial';" 
                ">File uploaded successfully and is stored in memory!</div>", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown("<div style='text-align: center; font-size: 20px; font-family: Arial';" 
                ">CAMELS Input Dataframe Preview:</div>", unsafe_allow_html=True)
    st.dataframe(df_info_display(df_input), use_container_width=True)
    st.markdown('---')
    st.markdown("<div style='text-align: center; font-size: 20px; font-family: Arial';" 
                ">CAMELS Input Dataframe Information:</div>", unsafe_allow_html=True)
    df_info_type = pd.DataFrame(st.session_state.upload.dtypes).astype(str)  # as type 'str' removes Serialization warning
    df_info_type.rename(columns={0: 'Data Types'}, inplace=True)
    df_nulls = pd.DataFrame(st.session_state.upload.isnull().sum())
    df_nulls.rename(columns={0: 'Null Values Sum'}, inplace=True)

    df_describe = st.session_state.upload.describe().drop(columns='Date').T
    df_describe.columns = ['Count', 'Mean', 'Min', 'First Quartile', 'Median', 'Third Quartile', 'Max', 'Standard Deviation']

    concatenated_df = pd.concat([df_info_type, df_nulls, df_describe], axis=1)
    concatenated_df = concatenated_df.style.format(precision=2,thousands=',',decimal='.')
    st.dataframe(concatenated_df, use_container_width=True)

    # Formatting Dates
    df_ratings['Date'] = df_ratings['Date'].dt.strftime('%d-%m-%Y')
    df_final['Date'] = df_final['Date'].dt.strftime('%d-%m-%Y')
    df_input['Date'] = df_input['Date'].dt.strftime('%d-%m-%Y')

    # Saving Final Dataframes to Session State
    st.session_state.camels_input = df_input
    st.session_state.camels_variables = df_final
    st.session_state.expert_bins = exp_bins
    st.session_state.weights = camels_weights
    st.session_state.ratings = df_ratings