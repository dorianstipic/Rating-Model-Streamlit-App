import streamlit as st

# Set options
st.set_page_config(page_title='CAMELS and Market Analysis Dashboard',layout='wide')

# Gets data from sesstion state

df_final = st.session_state.get('camels_variables')
df_ratings = st.session_state.get('ratings')

# Callback Function for Date Selection
def update_selected_dates():
    st.session_state.selected_dates = st.session_state.date_multiselect

# Checks if Data is Uploaded
if df_final is not None:

    # Replace Numerical to Alphabet ratings
    df_ratings = df_ratings.drop(columns='Composite Final Score')
    df_ratings.replace([1,2,3,4,5],['A','B','C','D','E'],inplace=True)

    # Initialize Session State
    if 'selected_dates' not in st.session_state:
        st.session_state.selected_dates = sorted(df_ratings['Date'].unique())

    # Date variable
    dates = sorted(df_ratings['Date'].unique()) 

    # Select Multiselect Options for Dates
    selected_dates = st.multiselect(r"$\textsf{\normalsize Select Date:}$", 
                                    dates, 
                                    default=st.session_state.selected_dates,
                                    key='date_multiselect',
                                    on_change=update_selected_dates)
    df_ratings_multiselect = df_ratings[df_ratings['Date'].isin(selected_dates)]
    df_final_multiselect = df_final[df_final['Date'].isin(selected_dates)]

    # Display Dataframes
    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';" 
            ">CAMELS Ratings and Subratings</div>", unsafe_allow_html=True)
    st.dataframe(df_ratings_multiselect,use_container_width=True)
    
    st.markdown('---')

    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';" 
            ">CAMELS Variables</div>", unsafe_allow_html=True)
    st.dataframe(df_final_multiselect,column_config={'Tier 1 Capital Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'Debt to Equity Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'NPL to Total Gross Loans Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'Loan Loss Provision Rate Scaled':st.column_config.NumberColumn(format='%.4f'),
                                                     'Asset Growth Rate 3Y Average':st.column_config.NumberColumn(format='%.4f'),
                                                     'Efficiency Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'Return on Assets (ROA)':st.column_config.NumberColumn(format='%.4f'),
                                                     'Interest Expenses to Interest Income Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'Liquidity Coverage (LCR) Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'Cash Ratio':st.column_config.NumberColumn(format='%.4f'),
                                                     'Non Interest Income Share':st.column_config.NumberColumn(format='%.4f')},
                                                     use_container_width=True) 

else:
    st.markdown("<div style='text-align: left; font-size: 18px; font-weight: normal; font-family: Arial';" 
            ">No dataframe uploaded. Please upload file in <b><i>Data Upload and Information</i></b> section!</div>", unsafe_allow_html=True)
