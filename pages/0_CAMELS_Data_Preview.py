import streamlit as st

# Set options
st.set_page_config(page_title='CAMELS and Market Analysis Dashboard',layout='wide')

# Gets data from session state
df_final = st.session_state.get('camels_variables')
df_ratings = st.session_state.get('ratings')
mask = st.session_state.get('mask')

# Copy from temporary widget key to permanent key
def keep(key):
    st.session_state[key] = st.session_state[f"_{key}"]

# Copy from permanent key to temporary widget key
def unkeep(key):
    st.session_state[f"_{key}"] = st.session_state[key]

# Checks if Data is Uploaded
if df_final is not None:

    df_ratings.columns = list(df_ratings.columns[:3]) + mask
    df_final.columns = list(df_ratings.columns[:1]) + mask
    # Replace Numerical to Alphabet ratings
    df_ratings = df_ratings.drop(columns='Composite Final Score') # drop numeric rating
    df_ratings.replace([1,2,3,4,5], ['A','B','C','D','E'],inplace=True)

    # Get dates
    dates = sorted(df_ratings['Date'].unique()) 
    
    # Initialize Session State
    if 'date_multiselect' not in st.session_state:
        st.session_state['date_multiselect'] = dates

    # Multiselect dates, handle session_sate with keep/unkeep methods
    unkeep('date_multiselect')
    selected_dates = st.multiselect(r"$\textsf{\normalsize Select Date:}$", 
                                    options=dates, 
                                    default=st.session_state['date_multiselect'],
                                    key='_date_multiselect',
                                    on_change=keep,
                                    args=(('date_multiselect',)))
    
    df_ratings_multiselect = df_ratings[df_ratings['Date'].isin(selected_dates)]
    df_final_multiselect = df_final[df_final['Date'].isin(selected_dates)]

    # df_ratings_multiselect.columns = list(df_ratings_multiselect.columns[:2]) + mask
    # df_final_multiselect.columns = list(df_ratings_multiselect.columns[:1]) + mask
    # Display Dataframes
    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';"
            ">CAMELS Ratings and Subratings</div>", unsafe_allow_html=True)
    st.dataframe(df_ratings_multiselect, use_container_width=True)
    st.markdown('---')
    st.markdown("<div style='text-align: center; font-size: 18px; font-weight: normal; font-family: Arial';" 
            ">CAMELS Variables</div>", unsafe_allow_html=True)
    st.dataframe(
        df_final_multiselect,
        column_config={col: st.column_config.NumberColumn(format='%.4f') for col in df_final_multiselect.columns[1:]},
        use_container_width=True
    ) 

else:
    st.markdown(
        "<div style='text-align: left; font-size: 18px; font-weight: normal; font-family: Arial';" 
        ">No dataframe uploaded. Please upload file in <b><i>Data Upload and Information</i></b> section!</div>", 
        unsafe_allow_html=True
    )
