import streamlit as st
import pandas as pd

st.set_page_config(page_title='CAMELS and Market Analysis Dashboard',layout='wide')

# Variables Description and Information Dictionary

variables_description = {
    'Variables':[
        'Tier 1 Capital Ratio','Debt to Equity Ratio',
        'NPL to Total Gross Loans Ratio','Loan Loss Provision Rate','Loan Loss Provision Rate Scaled',
        'Asset Growth Rate','Asset Growth Rate 3Y Average','Efficiency Ratio',
        'Return on Assets (ROA)','Interest Expenses to Interest Income Ratio',
        'Liquidity Coverage Ratio (LCR)','Cash Ratio',
        'Non Interest Income Share'],
    'Formula':[
        'Tier 1 Capital / Risk Weighted Assets','Total Liabilities / Total Shareholders\' Equity',
        'Non-performing Loans / Total Gross Loans','Total Provisions / Total Gross Loans','ABS(Loan Loss Provision Rate - Market Average Loan Loss Provision Rate)',
        '[Total Assets - Total Assets (t-1)] / Total Assets (t-1)','AVERAGE(Asset Growth Rate; Asset Growth Rate (t-1); Asset Growth Rate (t-2))',
        'Expenses / Net Operating Income','Net Income / Average Total Assets',
        'Interest Expenses / Interest Income','High Quality Liquid Assets / Total Net Cash Flow (over 30 day stress period)',
        'Liquid Assets / Current Liabilities','Non Interest Income / (Non Interest Income + Interest Income)'],
    'Description':[
                '''The tier 1 capital ratio is the ratio of tier 1 capital to total risk exposure. 
                Total risk exposure comprises the following: 
                credit risk exposure (including exposures to counterparty credit and dilution risks and free deliveries),
                settlement/delivery risk exposure,
                position, foreign exchange and commodities risk exposure,
                operational risk exposure,
                credit valuation adjustment risk exposure and 
                total risk exposure amount related to large exposures in the trading book. 
                The tier 1 capital ratio must be at least 6% at all times.''',
                '''The debt to equity ratio (D/E ratio) is a financial metric that indicates the proportion of a bank's financing 
                that comes from debt compared to equity. A higher D/E ratio suggests that the bank relies more on debt financing, 
                which can amplify returns but also increases financial risk due to higher interest obligations. In the banking and 
                financial services sector, a relatively high D/E ratio is commonplace. Banks carry higher amounts of debt because 
                they own substantial fixed assets in the form of branch networks.''',
                '''The indicator of the share of non-performing loans in total loans (non-performing loans, NPL) is the ratio of 
                non-performing loans to total loans. Loans are debt instruments that are not securities and that are included in 
                financial assets at amortised cost and financial assets at fair value through other comprehensive income. Non-performing 
                loans are material loans that are more than 90 days past due and loans in relation to which repayment in full is unlikely 
                without realisation of collateral, regardless of the existence of any past due amount or of the number of days past due.''',
                '''The loan loss provision rate is a financial metric used primarily in banking and financial institutions to estimate 
                potential losses from non-performing loans. This rate provides insight into the level of risk management practiced by the 
                institution, as well as its resilience to economic downturns or adverse events affecting loan repayment.''',
                '''A higher loan loss provision rate reflects a conservative approach by financial institutions, as they allocate more 
                funds to cover potential losses from non-performing loans. Conversely, a lower provision rate may indicate a riskier strategy, 
                as fewer resources are set aside for potential losses. However, it's important to note that a higher provision rate could also 
                signify a higher percentage of risky loans or lower collateralization, while a lower rate might suggest the opposite. To address 
                this ambiguity, the loan loss provision rate was scaled to measure absolute deviation from the market average rate, which is 
                considered the benchmark rate.''',
                '''The asset growth rate is a financial metric that measures the percentage change in a bank\'s total assets over a specific period, 
                usually annually. It indicates the rate at which a bank's asset base is expanding or contracting. A higher asset growth rate suggests 
                business expansion or increased investment, while a lower rate may indicate stagnation or conservative financial management.''',
                '''Recognizing the volatility of asset growth rate stemming from diverse economic, industry, and corporate factors, a prudent approach 
                to mitigate this volatility involves averaging the asset growth rate over a three-year period. By smoothing out short-term fluctuations, 
                this method provides a more stable and insightful perspective on the bank's long-term asset growth trajectory. This approach helps gain 
                a clearer understanding of the underlying trends and patterns in asset expansion or contraction, enabling more informed decision-making 
                regarding the bank's financial health and growth prospects.''',
                '''The efficiency ratio is a financial metric used to measure how effectively a bank or company utilizes its resources to generate 
                revenue or profit. A lower efficiency ratio indicates that a bank or company is more efficient in managing its expenses relative to its 
                revenue, which is generally viewed positively. Conversely, a higher efficiency ratio suggests that a bank is less effective in controlling 
                its expenses compared to its revenue, which may raise concerns about operational efficiency and profitability.''',
                '''Return on assets (ROA) is a financial ratio that measures a bank's or company's ability to generate profit from its assets. ROA indicates 
                how efficiently a company uses its assets to generate earnings. ROA is a key indicator of a bank's profitability and efficiency in asset 
                utilization. Since banks are highly leveraged, even a relatively low ROA of 1% to 2% may represent substantial revenues and profit for a bank.''',
                '''The interest expenses to interest income ratio is a financial metric that measures the proportion of a bank's interest expenses to its 
                interest income. A lower ratio indicates that the bank is earning more interest income than it is paying in interest expenses, which is 
                generally favorable. Conversely, a higher ratio suggests that the bank's interest expenses are eroding its interest income, potentially affecting 
                profitability and financial health.''',
                '''The liquidity coverage ratio (LCR) is a financial metric used to assess a financial institution's ability to meet short-term obligations with 
                high-quality liquid assets.The LCR is the ratio of the liquidity buffer (liquid assets) to net liquidity outflow (difference between outflow and 
                inflow). As of 2018, LCR must be at least 100%. However, many banks aim to maintain LCRs well above the regulatory minimum to provide an additional 
                buffer against liquidity risk.''',
                '''The cash ratio is a financial metric used to evaluate a bank's ability to cover its short-term liabilities with its cash and cash equivalents. 
                The cash ratio provides insight into a bank's liquidity position, specifically its ability to pay off its immediate debts without relying on the 
                sale of inventory or the collection of receivables. A higher cash ratio indicates a stronger liquidity position, while a lower cash ratio may 
                suggest that the bank may struggle to meet its short-term obligations solely with its cash reserves.''',
                '''The non-interest income share is a financial metric that assesses the portion of a bank's total income originating from activities not related 
                to interest. A higher non-interest income share indicates a substantial portion of income from sources like fees, commissions, or other activities. 
                These sources often provide stable income streams and are less sensitive to fluctuations in interest rates. Conversely, a lower non-interest income 
                share suggests a significant reliance on income from interest-bearing products, which can be more vulnerable to changes in interest rates.'''],
    'Interpretation':[
        'Higher value indicate better performance.','Lower value indicate better performance.',
        'Lower value indicate better performance.','Higher and lower values can indicate better performance.',
        'Lower value indicate better performance.','Higher value indicate better performance.',
        'Higher value indicate better performance.','Lower value indicate better performance.',
        'Higher value indicate better performance.','Lower value indicate better performance.',
        'Higher value indicate better performance.','Higher value indicate better performance.',
        'Higher value indicate better performance.']
    }

ratings_description = {
    'Rating Category':[' Rating A','Rating B','Rating C','Rating D','Rating E'],
    'Rating Analysis':['Strong','Satisfactory','Fair (watch category)','Marginal (some risk of failure)',
                       'Unsatisfactory (high degree of failure evident)'],
    'Description':[
        '''Indicates strong performance that consistently provides for safe and sound operations. The historical 
        trend and projections for key performance measures are consistently positive. Credit unions in this group 
        are resistant to external economic and financial disturbances and capable of withstanding the unexpected 
        actions of business conditions more ably than credit unions with a lower composite rating. Such institutions 
        give no cause for supervisory concern.''',
        '''Reflects satisfactory performance that consistently provides for safe and sound operations. Both historical 
        and projected key performance measures should generally be positive with any exceptions being those that do 
        not directly affect safe and sound operations. Credit unions in this group are stable and able to withstand 
        business fluctuations quite well; however, areas of weakness can be seen which could develop into conditions 
        of greater concern. The supervisory response is limited to the extent that minor adjustments are resolved in 
        the normal course of business and that operations continue to be satisfactory.''',
        '''Represents performance that is flawed to some degree and is of supervisory concern. Performance is marginal. 
        Both historical and projected key performance measures may generally be flat or negative to the extent that 
        safe and sound operations may be adversely affected. Credit unions in this group are only nominally resistant 
        to the onset of adverse business conditions and could easily deteriorate if concerted action is not effective 
        in correcting certain identifiable areas of weakness. Overall strength and financial capacity is present so as 
        to make failure only a remote probability. Such credit unions require more than normal supervisory attention to 
        address deficiencies.''',
        '''Refers to poor performance that is of serious supervisory concern. Key performance measures are likely to 
        be negative. Such performance, if left unchecked, would be expected to lead to conditions that could threaten 
        the viability of the credit union. A high potential for failure is present but is not yet imminent or pronounced. 
        Credit unions in this group require close supervisory attention.''',
        '''Considered unsatisfactory performance that is critically deficient and in need of immediate remedial attention. 
        Such performance, by itself or in combination with other weaknesses, directly impairs the viability of the credit 
        union. Credit unions in this group have a high probability of failure and will likely require liquidation and the 
        payoff of shareholders, or some other form of emergency assistance, merger, or acquisition.'''
    ]
}

# Help Formulas

@st.cache_data(ttl=7200)
def var_description_table(var_description_dict):

    df = pd.DataFrame(var_description_dict).set_index('Variables')

    return df

@st.cache_data(ttl=7200)
def rating_description_table(rating_description_dict):

    df = pd.DataFrame(rating_description_dict)
    df.index = df.index + 1

    return df

# Creating Help Tabs

dashboard_help, camels_variables_info, rating_description = st.tabs([
    'Dashboard Help', 'CAMELS Variables Information', 'Rating Description'
])

# Dashboard Help Tab
with dashboard_help:

    # Dashboard User Manual
    st.markdown("<div style='text-align: left; font-size: 22px; font-weight: bold; font-family: Arial;'>Dashboard User Manual</div>", unsafe_allow_html=True)
    st.text('')
    st.write('Welcome to the CAMELS Dashboard! This guide will help you navigate and utilize the features effectively.')

    # Dashboard Pages and Tabs Section
    st.markdown('#### Dashboard Pages and Tabs')
    st.write('''
    Dashboard Pages: Displayed on the left side of the panel are various dashboard pages:
    - Data Upload and Information
    - CAMELS Data Preview
    - CAMELS Visualizations
    - Market Analysis
    - Help
             
    Pages section can be collapsed clicking on the X icon in the top right corner.
    ''')

    # Data Upload and Information Section
    st.markdown('#### Data Upload and Information')
    st.write('''
    In the 'Drag and drop file here' section, user can input a file with necessary data for the CAMELS rating calculation. Only .xlsx file type is accepted, 
             and only one file at a time can be uploaded. In case the user tries to load a file that is not in the correct format or containing wrong data types 
             (for example, string type in float section), the dashboard will display an error. User should double-check the file and correct the errors, then try 
             uploading again.

    After the file is uploaded successfully, the message is displayed: 'File uploaded successfully and is stored in memory!'

    Below the displayed message, two dataframes are displayed:
    - "CAMELS Input Dataframe Preview" which shows the currently uploaded .xlsx file
    - "CAMELS Input Dataframe Information" which shows basic dataframe information alongside descriptive statistics of the numerical data.
    ''')

    # CAMELS Data Preview Section
    st.markdown('#### CAMELS Data Preview')
    st.write('''
    This section shows two dataframes:
    - "CAMELS Rating and Subratings" which shows the final rating of financial institutions along with subratings of selected variables.
    - "CAMELS Variables dataframe" which: shows CAMELS selected variables values.

    Both tables can be filtered by year (default value setting is to show all available years). When leaving the page, the page saves the Filter setting 
             (selected year).

    It's crucial to note that if there is missing data in the input table, the model cannot calculate the appropriate rating. In such cases, 
             the worst rating category (Rating E) is assigned instead.
    ''')

    # CAMELS Visualizations Section
    st.markdown('#### CAMELS Visualizations')
    st.write('''
    This section shows graphical representations of the CAMELS model results. It has 7 tabs:
    - Rating Final: Shows the bar chart of all Financial Institutions by their respective Final Rating.
    - (C) Capital Adequacy: Shows 2 bar charts side by side, showing subratings of the 2 selected Capital Adequacy components (Tier 1 Capital Ratio and Debt to Equity Ratio).
    - (A) Asset Quality: Shows 2 bar charts side by side, showing subratings of the 2 selected Asset Quality components (NPL to Total Gross Loans Ratio and Loan Loss Provision Rate Scaled).
    - (M) Management: Shows 2 bar charts side by side, showing subratings of the 2 selected Management components (Asset Growth Rate 3Y Average and Efficiency Ratio).
    - (E) Earnings: Shows 2 bar charts side by side, showing subratings of the 2 selected Earnings components (Return on Assets (ROA) and Interest Expenses to Interest Income Ratio).
    - (L) Liquidity: Shows 2 bar charts side by side, showing subratings of the 2 selected Liquidity components (Liquidity Coverage Ratio (LCR) Ratings and Cash Ratio).
    - (S) Capital Adequacy: Shows a bar chart showing subratings of the selected Sensitivity component (Non-Interest Income Share).

    CAMELS Visualizations page also allows displaying results based on the selected year. It should be noted that missing values will show as 'None' in the bar plots without any rating category assigned.
    ''')

    # Market Analysis Section
    st.markdown('#### Market Analysis')
    st.write('''
    This section compares all financial institutions with the market (benchmark values). It includes:
    - Total Assets Market Share and Total Gross Loans Market Share: Show financial institution share in the whole market in terms of the asset and gross loan size.
    - Relative Difference: Shows relative differences from the benchmark values for each selected CAMELS variable. On relative differences, conditional formatting is applied where **:green[green color]** 
    signals better results compared to the benchmark while **:red[red color]** signals worst result compared to the benchmark. It should be noted that both positive and negative values can indicate better results in 
    comparison to the benchmark (this depends on the variable).
    - Missing Data Handling: In order to have correct market analysis representation, data from all financial institutions should be filled in .xlsx file. If there is missing data, the cell is left blank and colored in black color.
    ''')
    st.markdown("<div style='text-align: left; font-size: 14px; font-weight: bold; font-style: italic; font-family: Arial';" 
        ">Note:</div>", unsafe_allow_html=True)
    st.write('''Benchmark values of Total Assets and Total Gross Loans are calculated as the sum, while the rest of the CAMELS variables are calculated as the
             average of the inputted Data.''')

# CAMELS Variables Tab
with camels_variables_info:
    st.table(var_description_table(variables_description))

# Rating Description Tab
with rating_description:
    st.table(rating_description_table(ratings_description))
    st.markdown("<div style='text-align: left; font-size: 14px; font-weight: bold; font-style: italic; font-family: Arial';" 
            ">Note:</div>", unsafe_allow_html=True)
    st.write('''The Final Rating categories are further divided into plus (+) and minus (-) subcategories for finer 
             differentiation. Each of the five main rating categories is split into two subcategories: a plus (+) sign 
             indicates the upper half of the threshold range, and a minus (-) sign indicates the lower half.''')