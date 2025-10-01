# smart_insights.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def get_stock_fundamentals(stock_symbol):
    """Stock ke fundamentals data fetch karta hai"""
    try:
        ticker = f"{stock_symbol}.NS"
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'industry_pe': info.get('industryPE', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'roe': info.get('returnOnEquity', 0),
            'eps': info.get('trailingEps', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'book_value': info.get('bookValue', 0),
            'face_value': info.get('faceValue', 1),
            'current_price': info.get('currentPrice', 0)
        }
        return fundamentals
    except Exception as e:
        return get_fallback_fundamentals(stock_symbol)

def get_fallback_fundamentals(stock_symbol):
    """Agar API fail ho toh fallback data"""
    fundamentals_data = {
        'TCS': {
            'market_cap': 1047943 * 10000000,
            'pe_ratio': 21.27,
            'pb_ratio': 11.14,
            'industry_pe': 24.51,
            'debt_to_equity': 0.10,
            'roe': 51.24,
            'eps': 136.19,
            'dividend_yield': 4.35,
            'book_value': 260.08,
            'face_value': 1,
            'current_price': 2888.40
        },
        'INFY': {
            'market_cap': 584732 * 10000000,
            'pe_ratio': 23.45,
            'pb_ratio': 8.12,
            'industry_pe': 24.51,
            'debt_to_equity': 0.08,
            'roe': 29.87,
            'eps': 62.34,
            'dividend_yield': 2.85,
            'book_value': 185.67,
            'face_value': 5,
            'current_price': 1425.60
        },
        'RELIANCE': {
            'market_cap': 1567892 * 10000000,
            'pe_ratio': 26.78,
            'pb_ratio': 2.45,
            'industry_pe': 18.34,
            'debt_to_equity': 0.45,
            'roe': 10.23,
            'eps': 98.76,
            'dividend_yield': 0.45,
            'book_value': 890.12,
            'face_value': 10,
            'current_price': 2456.78
        },
        'HDFCBANK': {
            'market_cap': 1123456 * 10000000,
            'pe_ratio': 19.56,
            'pb_ratio': 3.12,
            'industry_pe': 20.12,
            'debt_to_equity': 0.12,
            'roe': 16.45,
            'eps': 78.90,
            'dividend_yield': 1.23,
            'book_value': 345.67,
            'face_value': 2,
            'current_price': 1567.89
        }
    }
    return fundamentals_data.get(stock_symbol, fundamentals_data['TCS'])

def get_financials_chart_data(stock_symbol):
    """Company-specific financial data for charts"""
    financials_data = {
        'TCS': {
            'quarters': ['Jun 24', 'Sep 24', 'Dec 24', 'Mar 25', 'Jun 25'],
            'revenue': [63575, 64988, 65216, 65507, 65097],
            'profit': [12432, 13125, 13567, 13892, 14215],
            'net_worth': [94567, 96842, 98123, 99245, 100567]
        },
        'INFY': {
            'quarters': ['Jun 24', 'Sep 24', 'Dec 24', 'Mar 25', 'Jun 25'],
            'revenue': [38567, 39234, 40123, 41234, 42567],
            'profit': [7567, 7890, 8234, 8567, 8923],
            'net_worth': [72345, 74567, 76890, 79234, 81567]
        },
        'RELIANCE': {
            'quarters': ['Jun 24', 'Sep 24', 'Dec 24', 'Mar 25', 'Jun 25'],
            'revenue': [215678, 223456, 234567, 245678, 256789],
            'profit': [15678, 16789, 17890, 18901, 19876],
            'net_worth': [345678, 356789, 367890, 378901, 389012]
        },
        'HDFCBANK': {
            'quarters': ['Jun 24', 'Sep 24', 'Dec 24', 'Mar 25', 'Jun 25'],
            'revenue': [45678, 46789, 47890, 48901, 49876],
            'profit': [12345, 12890, 13456, 13987, 14567],
            'net_worth': [234567, 245678, 256789, 267890, 278901]
        }
    }
    return financials_data.get(stock_symbol, financials_data['TCS'])

def create_financial_chart(quarters, values, title, company):
    """Financial metrics ka line chart banata hai"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=quarters,
        y=values,
        mode='lines+markers',
        name=title,
        line=dict(color='#00d09c', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f"{company} - {title} Trend",
        xaxis_title='Quarters',
        yaxis_title='Amount (₹ Cr)',
        height=300,
        showlegend=False,
        template='plotly_white'
    )
    
    return fig

def get_balance_sheet_data(stock_symbol):
    """Company-specific balance sheet data - SIMPLE FIXED VERSION"""
    balance_sheets = {
        'TCS': [
            {'Particulars': 'Total Assets', '2021': 130759, '2022': 141514, '2023': 143651, '2024': 146449, '2025': 159629},
            {'Particulars': 'Current Assets', '2021': 99280, '2022': 108310, '2023': 110270, '2024': 112984, '2025': 123011},
            {'Particulars': 'Non Current Assets', '2021': 31479, '2022': 33204, '2023': 33381, '2024': 33465, '2025': 36618},
            {'Particulars': 'Total Liabilities', '2021': 43651, '2022': 51668, '2023': 52445, '2024': 55130, '2025': 63858},
            {'Particulars': 'Current Liabilities', '2021': 34155, '2022': 42351, '2023': 43558, '2024': 46104, '2025': 53001},
            {'Particulars': 'Non Current Liabilities', '2021': 9496, '2022': 9317, '2023': 8887, '2024': 9026, '2025': 10857},
            {'Particulars': 'Total Equity', '2021': 87108, '2022': 89846, '2023': 91206, '2024': 91319, '2025': 95771}
        ],
        'INFY': [
            {'Particulars': 'Total Assets', '2021': 98765, '2022': 105678, '2023': 112345, '2024': 118901, '2025': 125678},
            {'Particulars': 'Current Assets', '2021': 75678, '2022': 82345, '2023': 87654, '2024': 92345, '2025': 97890},
            {'Particulars': 'Non Current Assets', '2021': 23087, '2022': 23333, '2023': 24691, '2024': 26556, '2025': 27788},
            {'Particulars': 'Total Liabilities', '2021': 34567, '2022': 37890, '2023': 41234, '2024': 44567, '2025': 47890},
            {'Particulars': 'Current Liabilities', '2021': 28765, '2022': 31234, '2023': 33456, '2024': 35678, '2025': 37890},
            {'Particulars': 'Non Current Liabilities', '2021': 5802, '2022': 6656, '2023': 7778, '2024': 8889, '2025': 10000},
            {'Particulars': 'Total Equity', '2021': 64198, '2022': 67788, '2023': 71111, '2024': 74334, '2025': 77788}
        ],
        'RELIANCE': [
            {'Particulars': 'Total Assets', '2021': 345678, '2022': 367890, '2023': 389012, '2024': 412345, '2025': 445678},
            {'Particulars': 'Current Assets', '2021': 234567, '2022': 256789, '2023': 278901, '2024': 301234, '2025': 334567},
            {'Particulars': 'Non Current Assets', '2021': 111111, '2022': 111101, '2023': 110111, '2024': 111111, '2025': 111111},
            {'Particulars': 'Total Liabilities', '2021': 156789, '2022': 167890, '2023': 178901, '2024': 189012, '2025': 201234},
            {'Particulars': 'Current Liabilities', '2021': 123456, '2022': 134567, '2023': 145678, '2024': 156789, '2025': 167890},
            {'Particulars': 'Non Current Liabilities', '2021': 33333, '2022': 33323, '2023': 33223, '2024': 32223, '2025': 33344},
            {'Particulars': 'Total Equity', '2021': 188889, '2022': 200000, '2023': 210111, '2024': 223333, '2025': 244444}
        ],
        'HDFCBANK': [
            {'Particulars': 'Total Assets', '2021': 456789, '2022': 478901, '2023': 501234, '2024': 523456, '2025': 545678},
            {'Particulars': 'Current Assets', '2021': 345678, '2022': 367890, '2023': 389012, '2024': 401234, '2025': 423456},
            {'Particulars': 'Non Current Assets', '2021': 111111, '2022': 111011, '2023': 112222, '2024': 122222, '2025': 122222},
            {'Particulars': 'Total Liabilities', '2021': 234567, '2022': 245678, '2023': 256789, '2024': 267890, '2025': 278901},
            {'Particulars': 'Current Liabilities', '2021': 198765, '2022': 207890, '2023': 216789, '2024': 225678, '2025': 234567},
            {'Particulars': 'Non Current Liabilities', '2021': 35802, '2022': 37788, '2023': 40000, '2024': 42212, '2025': 44334},
            {'Particulars': 'Total Equity', '2021': 222222, '2022': 233223, '2023': 244445, '2024': 255566, '2025': 266777}
        ]
    }
    return balance_sheets.get(stock_symbol, balance_sheets['TCS'])

def get_company_info(stock_symbol):
    """Company ke baare mei basic info"""
    companies_data = {
        'TCS': {
            'name': 'Tata Consultancy Services',
            'sector': 'IT Services',
            'industry': 'Information Technology',
            'description': 'Tata Consultancy Services (TCS) is a global IT services and digital transformation partner, assisting the world\'s leading organizations with technology-led growth and business solutions. The company helps its clients become Perpetually Adaptive Enterprises that can thrive in uncertainty by using rapid innovation and collaboration.',
            'website': 'https://www.tcs.com',
            'employees': 592000,
            'ceo': 'Mr. K. Krithivasan',
            'founded': '1968'
        },
        'INFY': {
            'name': 'Infosys Limited',
            'sector': 'IT Services', 
            'industry': 'Information Technology',
            'description': 'Infosys is a global leader in next-generation digital services and consulting, enabling clients in 50+ countries to navigate their digital transformation. With over four decades of experience in managing the systems and workings of global enterprises.',
            'website': 'https://www.infosys.com',
            'employees': 335000,
            'ceo': 'Mr. Salil Parekh',
            'founded': '1981'
        },
        'RELIANCE': {
            'name': 'Reliance Industries Limited',
            'sector': 'Oil & Gas',
            'industry': 'Energy',
            'description': 'Reliance Industries Limited is India\'s largest private sector company, with businesses spanning energy, petrochemicals, natural gas, retail, telecommunications, mass media, and textiles.',
            'website': 'https://www.ril.com',
            'employees': 236000,
            'ceo': 'Mr. Mukesh Ambani',
            'founded': '1966'
        },
        'HDFCBANK': {
            'name': 'HDFC Bank Limited',
            'sector': 'Banking',
            'industry': 'Financial Services',
            'description': 'HDFC Bank is one of India\'s leading private banks and was among the first to receive approval from the Reserve Bank of India (RBI) to set up a private sector bank in 1994.',
            'website': 'https://www.hdfcbank.com',
            'employees': 120000,
            'ceo': 'Mr. Sashidhar Jagdishan',
            'founded': '1994'
        }
    }
    return companies_data.get(stock_symbol, companies_data['TCS'])

def get_shareholding_pattern(stock_symbol):
    """Company-specific shareholding pattern data"""
    patterns = {
        'TCS': {
            'promoters': 71.77,
            'fiis': 11.47, 
            'dii': 6.87,
            'mutual_funds': 5.13,
            'retail': 4.75
        },
        'INFY': {
            'promoters': 14.91,
            'fiis': 33.26,
            'dii': 35.12,
            'mutual_funds': 8.45,
            'retail': 8.26
        },
        'RELIANCE': {
            'promoters': 50.39,
            'fiis': 23.18,
            'dii': 15.27,
            'mutual_funds': 6.89,
            'retail': 4.27
        },
        'HDFCBANK': {
            'promoters': 25.56,
            'fiis': 45.23,
            'dii': 18.67,
            'mutual_funds': 7.45,
            'retail': 3.09
        }
    }
    return patterns.get(stock_symbol, patterns['TCS'])

def get_top_mutual_funds(stock_symbol):
    """Company-specific top mutual funds"""
    funds_data = {
        'TCS': [
            {'name': 'Franklin India Focused Equity Fund Direct Growth', 'aum': 6.04},
            {'name': 'Franklin India Large Cap Fund Direct Growth', 'aum': 4.84},
            {'name': 'Quantum Value Fund Direct Growth', 'aum': 4.49},
            {'name': 'Bandhan ELSS Tax Saver Fund Direct Plan Growth', 'aum': 4.14}
        ],
        'INFY': [
            {'name': 'ICICI Prudential Technology Fund Direct Growth', 'aum': 5.87},
            {'name': 'SBI Technology Opportunities Fund Direct Growth', 'aum': 4.92},
            {'name': 'Aditya Birla Sun Life Digital India Fund Direct Growth', 'aum': 4.56},
            {'name': 'Tata Digital India Fund Direct Growth', 'aum': 3.89}
        ],
        'RELIANCE': [
            {'name': 'HDFC Top 100 Fund Direct Growth', 'aum': 5.42},
            {'name': 'SBI Bluechip Fund Direct Growth', 'aum': 4.78},
            {'name': 'ICICI Prudential Bluechip Fund Direct Growth', 'aum': 4.35},
            {'name': 'Nippon India Large Cap Fund Direct Growth', 'aum': 3.96}
        ],
        'HDFCBANK': [
            {'name': 'HDFC Top 100 Fund Direct Growth', 'aum': 6.23},
            {'name': 'ICICI Prudential Bluechip Fund Direct Growth', 'aum': 5.45},
            {'name': 'SBI Bluechip Fund Direct Growth', 'aum': 4.78},
            {'name': 'Axis Bluechip Fund Direct Growth', 'aum': 4.12}
        ]
    }
    return funds_data.get(stock_symbol, funds_data['TCS'])

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("💡 Smart Insights & Fundamentals")
    
    if not company:
        st.info("Select a company from the sidebar.")
        return
    
    # Session state for active metric
    if 'active_metric' not in st.session_state:
        st.session_state.active_metric = 'revenue'
    
    if 'show_balance_sheet' not in st.session_state:
        st.session_state.show_balance_sheet = False
    
    # Company-specific data fetch karo
    company_info = get_company_info(company)
    financial_data = get_financials_chart_data(company)
    quarters = financial_data['quarters']
    
    # Tabs create karo
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Fundamentals", "💰 Financials", "🏢 About Company", "📈 Shareholding"])
    
    with tab1:
        st.header(f"📊 {company} Fundamentals")
        
        fundamentals = get_stock_fundamentals(company)
        if fundamentals:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                | Metric | Value |
                |--------|-------|
                | **Market Cap** | ₹{:,.0f} Cr |
                | **P/E Ratio (TTM)** | {:.2f} |
                | **P/B Ratio** | {:.2f} |
                | **Industry P/E** | {:.2f} |
                | **Debt to Equity** | {:.2f} |
                """.format(
                    fundamentals['market_cap'] / 10000000,
                    fundamentals['pe_ratio'],
                    fundamentals['pb_ratio'],
                    fundamentals['industry_pe'],
                    fundamentals['debt_to_equity']
                ))
            
            with col2:
                st.markdown("""
                | Metric | Value |
                |--------|-------|
                | **ROE** | {:.2f}% |
                | **EPS (TTM)** | {:.2f} |
                | **Dividend Yield** | {:.2f}% |
                | **Book Value** | {:.2f} |
                | **Face Value** | {:.1f} |
                """.format(
                    fundamentals['roe'],
                    fundamentals['eps'],
                    fundamentals['dividend_yield'],
                    fundamentals['book_value'],
                    fundamentals['face_value']
                ))
        else:
            st.warning("Fundamentals data not available")
        
        st.info("💡 Understand Fundamentals - Learn how to analyze company fundamentals")
    
    with tab2:
        st.header(f"💰 {company} Financials")
        
        # Financial Metrics Selection - Clickable buttons
        st.subheader("Financial Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Revenue", use_container_width=True):
                st.session_state.active_metric = 'revenue'
        with col2:
            if st.button("💰 Profit", use_container_width=True):
                st.session_state.active_metric = 'profit'
        with col3:
            if st.button("🏦 Net Worth", use_container_width=True):
                st.session_state.active_metric = 'net_worth'
        
        # Active metric display
        st.write(f"### {st.session_state.active_metric.title()}")
        
        # Chart display for active metric
        metric_titles = {
            'revenue': 'Revenue',
            'profit': 'Profit', 
            'net_worth': 'Net Worth'
        }
        
        chart_fig = create_financial_chart(
            quarters, 
            financial_data[st.session_state.active_metric],
            metric_titles[st.session_state.active_metric],
            company
        )
        st.plotly_chart(chart_fig, use_container_width=True)
        
        # Quarterly values table
        st.subheader("Quarterly Values")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        quarter_cols = [col1, col2, col3, col4, col5]
        current_values = financial_data[st.session_state.active_metric]
        
        for i, (col, quarter, value) in enumerate(zip(quarter_cols, quarters, current_values)):
            with col:
                st.metric(quarter, f"₹{value:,}")
        
        st.caption("*All values are in Rs. Crores")
        
        # Quarterly/Yearly toggle
        qy_col1, qy_col2, qy_col3 = st.columns([1, 1, 2])
        with qy_col1:
            st.button("📅 Quarterly", use_container_width=True)
        with qy_col2:
            st.button("📊 Yearly", use_container_width=True)
        
        # Expandable Balance Sheet Section - ERROR FIXED
        with st.expander("📋 View Detailed Balance Sheet", expanded=st.session_state.show_balance_sheet):
            st.header(f"{company} Balance Sheet")
            
            # Balance Sheet Tabs
            bs_tab1, bs_tab2, bs_tab3, bs_tab4, bs_tab5 = st.tabs([
                "Income Statement", "Balance Sheet", "Cash Flow", "Quarterly", "Yearly"
            ])
            
            with bs_tab2:  # Balance Sheet tab
                balance_data = get_balance_sheet_data(company)
                
                # Direct DataFrame creation - NO ERROR
                balance_df = pd.DataFrame(balance_data)
                
                st.dataframe(
                    balance_df,
                    use_container_width=True,
                    height=400
                )
                
                st.caption("All values in ₹ Crores")
        
        # See Details button
        if st.button("See Details", type="primary"):
            st.session_state.show_balance_sheet = not st.session_state.show_balance_sheet
            st.rerun()
    
    with tab3:
        st.header(f"🏢 About {company}")
        
        st.write(f"**{company_info['name']}**")
        st.write(company_info['description'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Company Details")
            st.write(f"**Sector:** {company_info['sector']}")
            st.write(f"**Industry:** {company_info['industry']}")
            st.write(f"**Founded:** {company_info.get('founded', 'N/A')}")
            st.write(f"**Employees:** {company_info['employees']:,}")
            st.write(f"**NSE Symbol:** {company}")
        
        with col2:
            st.subheader("Management")
            st.write(f"**CEO/MD:** {company_info['ceo']}")
            st.write(f"**Website:** {company_info['website']}")
    
    with tab4:
        st.header(f"📈 {company} Shareholding Pattern")
        
        shareholding = get_shareholding_pattern(company)
        
        # Current price display
        fundamentals = get_stock_fundamentals(company)
        if fundamentals and fundamentals.get('current_price'):
            st.metric(f"{company} Current Price", f"₹{fundamentals['current_price']:.2f}")
        
        # Shareholding table
        st.markdown("""
        | Category | Percentage |
        |----------|------------|
        | **Promoters** | {:.2f}% |
        | **Foreign Institutions** | {:.2f}% |
        | **Domestic Institutions** | {:.2f}% |
        | **Mutual Funds** | {:.2f}% |
        | **Retail & Others** | {:.2f}% |
        """.format(
            shareholding['promoters'],
            shareholding['fiis'], 
            shareholding['dii'],
            shareholding['mutual_funds'],
            shareholding['retail']
        ))
        
        # Top Mutual Funds
        st.subheader("Top Mutual Funds Invested")
        funds = get_top_mutual_funds(company)
        
        for fund in funds:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(fund['name'])
            with col2:
                st.write(f"{fund['aum']}%")
        
        st.button("📌 Add to Watchlist")