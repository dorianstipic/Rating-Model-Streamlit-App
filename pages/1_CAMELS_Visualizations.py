import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 

# Set options
st.set_page_config(page_title='CAMELS and Market Analysis Dashboard', layout='wide')

# Gets data from session state
df_var = st.session_state.get('camels_variables')
df_ratings = st.session_state.get('ratings')
df_bins = st.session_state.get('expert_bins')

# Ratings Final Score Thresholds
rating_thresholds = {
    '1st': 1.5,
    '2nd': 2.4,
    '3rd': 3.4,
    '4th': 4.5
}

# Plotting Functions
@st.cache_data(ttl=7200)
def auto_adjust_height(ylabel_count, font_size=14, multiplier=2.0, padding=50):
    height = padding + (np.multiply(ylabel_count, font_size) * multiplier)
    return height

@st.cache_resource(ttl=7200)
def ratings_final_plot(df, date, range_score):
    filter_df = df[df['Date'] == date]
    filter_df = filter_df[['Date', 'Composite Final Score', 'Final Rating']].reset_index().sort_values('Composite Final Score', ascending=True)
    fig = px.bar(data_frame=filter_df, x='Composite Final Score', y='Institution Name',
                 color='Final Rating', text='Final Rating', color_discrete_map={'A+': '#175C2C', 'A-': '#2C8646',
                                                                               'B+': '#86DB4F', 'B-': '#C4FC9F',
                                                                               'C+': '#FFECBD', 'C-': '#FFC83D',
                                                                               'D+': '#FFA929', 'D-': '#FD6412',
                                                                               'E+': '#E0301E', 'E-': '#AA2417'},
                 orientation='h')
    fig.update_layout(title='Financial Institutions Final Ratings',
                      height=int(auto_adjust_height(len(df.index.unique()))),
                      xaxis=dict(showgrid=True, title_font=dict(size=16, family='Arial'), tickfont=dict(size=14), tickmode='linear', dtick=0.5),
                      yaxis=dict(showgrid=True, categoryorder="total descending", title_font=dict(size=16, family='Arial'), tickfont=dict(size=14)),
                      legend=dict(title='Final Rating', font=dict(size=14), title_font=dict(size=14), traceorder='normal'),
                      hovermode='closest',
                      font=dict(family='Arial'),
                      title_font=dict(family='Arial', size=18))
    fig.update_traces(textangle=0, textposition="outside")
    fig.add_vline(x=range_score['1st'], line_width=2, line_dash="dot", opacity=0.6)
    fig.add_vline(x=range_score['2nd'], line_width=2, line_dash="dot", opacity=0.6)
    fig.add_vline(x=range_score['3rd'], line_width=2, line_dash="dot", opacity=0.6)
    fig.add_vline(x=range_score['4th'], line_width=2, line_dash="dot", opacity=0.6)
    
    return st.plotly_chart(fig, use_container_width=True)

@st.cache_resource(ttl=7200)
def variables_final_plot(df_r, df_v, date, range_score, var):
    df_r_filter = df_r[df_r['Date'] == date][['Date', var]]
    df_v_filter = df_v[df_v['Date'] == date][['Date', var]]
    filter_df = pd.merge(df_r_filter, df_v_filter, how='inner', left_index=True, right_index=True).reset_index()
    filter_df = filter_df.sort_values(filter_df.columns[2], ascending=True)
    filter_df[var + ' Rating Adjusted'] = filter_df[var + '_x'].replace([1, 2, 3, 4, 5], ['A', 'B', 'C', 'D', 'E'])
    category_order = 'total ascending' if range_score.loc[var, 'Reverse'] else 'total descending'
    
    fig = px.bar(data_frame=filter_df, x=var + '_y', y='Institution Name',
                 color=var + ' Rating Adjusted', text=var + ' Rating Adjusted', color_discrete_map={'A': '#175C2C',
                                                                                                'B': '#86DB4F',
                                                                                                'C': '#FFECBD',
                                                                                                'D': '#FFA929',
                                                                                                'E': '#E0301E'},
                 orientation='h')
    fig.update_layout(title=var + ' Ratings',
                      height=int(auto_adjust_height(len(df_r.index.unique()))),
                      xaxis_title=var,
                      xaxis=dict(showgrid=True, title_font=dict(size=16, family='Arial'), tickfont=dict(size=14)),
                      yaxis=dict(showgrid=True, categoryorder=category_order, title_font=dict(size=16, family='Arial'), tickfont=dict(size=14)),
                      legend_title_text=var + ' Rating',
                      legend=dict(font=dict(size=14), title_font=dict(size=14), traceorder='normal', orientation='h',
                                  yanchor='bottom', yref='container', xanchor='right', xref='paper'),
                      hovermode='closest',
                      font=dict(family='Arial'),
                      title_font=dict(family='Arial', size=18))
    fig.update_traces(textangle=0, textposition="outside")
    fig.add_vline(x=range_score.loc[var, '1st_Threshold'], line_width=2, line_dash="dot", opacity=0.6)
    fig.add_vline(x=range_score.loc[var, '2nd_Threshold'], line_width=2, line_dash="dot", opacity=0.6)
    fig.add_vline(x=range_score.loc[var, '3rd_Threshold'], line_width=2, line_dash="dot", opacity=0.6)
    fig.add_vline(x=range_score.loc[var, '4th_Threshold'], line_width=2, line_dash="dot", opacity=0.6)
    
    return st.plotly_chart(fig, use_container_width=True)

# Callback function to update session state
def update_selected_date():
    st.session_state.save_date = sorted(df_ratings['Date'].unique()).index(st.session_state.selected_date)

# Checks if Data is Uploaded 
if df_var is not None:
    
    # Initialize Session State
    if 'save_date' not in st.session_state:
        st.session_state.save_date = len(sorted(df_ratings['Date'].unique())) - 1

    # Create Date Selectbox with callback
    st.selectbox(r"$\textsf{\normalsize Select Date:}$", sorted(df_ratings['Date'].unique()), 
                 index=st.session_state.save_date, key='selected_date', on_change=update_selected_date)

    # Create Tabs
    ratings_final, capital_adequacy, asset_quality, management, earnings, liquidity, sensitivity = st.tabs(
        ['Ratings Final', '(C) Capital Adequacy', '(A) Asset Quality', '(M) Management', '(E) Earnings', '(L) Liquidity', '(S) Sensitivity']
    )

    # Ratings Final Tab
    with ratings_final:       
        ratings_final_plot(df_ratings, st.session_state.selected_date, rating_thresholds)

    # Capital Adequacy Tab
    with capital_adequacy:
        tier_1_capital, debt_to_equity = st.columns(2)
        with tier_1_capital:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Tier 1 Capital Ratio')
        with debt_to_equity:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Debt to Equity Ratio')

    # Asset Quality Tab
    with asset_quality:
        npl_to_gross_loans, loan_loss_provision = st.columns(2)
        with npl_to_gross_loans:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'NPL to Total Gross Loans Ratio')
        with loan_loss_provision:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Loan Loss Provision Rate Scaled')

    # Management Tab
    with management:
        asset_growth, efficiency = st.columns(2)
        with asset_growth:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Asset Growth Rate 3Y Average')
        with efficiency:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Efficiency Ratio')

    # Earnings Tab
    with earnings:
        return_on_assets, interest_expenses_to_income = st.columns(2)
        with return_on_assets:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Return on Assets (ROA)')
        with interest_expenses_to_income:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Interest Expenses to Interest Income Ratio')

    # Liquidity Tab
    with liquidity:
        liquidity_coverage, cash = st.columns(2)
        with liquidity_coverage:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Liquidity Coverage Ratio (LCR)')
        with cash:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Cash Ratio')

    # Sensitivity Tab
    with sensitivity:
        non_interest_income, _placeholder = st.columns(2)
        with non_interest_income:
            variables_final_plot(df_ratings, df_var, st.session_state.selected_date, df_bins, 'Non Interest Income Share')
        with _placeholder:
            st.write('')

# Display Text when Data Input is Missing
else:
    st.markdown("<div style='text-align: left; font-size: 18px; font-weight: normal; font-family: Arial';" 
                ">No dataframe uploaded. Please upload file in <b><i>Data Upload and Information</i></b> section!</div>", unsafe_allow_html=True)
