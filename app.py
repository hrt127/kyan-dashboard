import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="Kyan Trader v1.0")
st.title("🟢 Kyan Trader Dashboard")

# SIDEBAR BOOKMARKS
st.sidebar.title("📑 Quick Links")
st.sidebar.markdown("[Kyan Portfolio](https://alpha.kyan.blue/portfolio)")
st.sidebar.markdown("[Kyan Perps](https://alpha.kyan.blue/perps)")
st.sidebar.markdown("[Kyan Options](https://alpha.kyan.blue/)")
st.sidebar.markdown("[CoinGecko BTC](https://www.coingecko.com/en/coins/bitcoin)")
st.sidebar.markdown("[Elfa AI](https://www.elfa.ai)")
st.sidebar.markdown("---")
st.sidebar.markdown("**Notes:** Update numbers → auto risk calc → Save log → Obsidian")

# PAGES
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Notes & Rationale", "📋 ELFA Logs"])

with tab1:
    # SUMMARY + RISK
    col1, col2 = st.columns([3,2])
    with col1:
        st.header("📋 Session Summary")
        realized = st.number_input("Realized PnL ($)", value=0.0, key="realized")
        unrealized = st.number_input("Unrealized PnL ($)", value=-382.23, key="unrealized")
        delta = st.number_input("Net Delta (BTC)", value=0.67, key="delta")
        imr = st.number_input("IMr (%)", value=1.0, key="imr")

    with col2:
        st.header("⚠️ Risk Engine")
        risk_target = st.slider("Risk Target (1-5)", 1, 5, 4)
        risk_score = 1 + (1 if abs(delta)>2 else 0) + (1 if imr>20 else 0) + (1 if imr>40 else 0)
        st.metric("Risk Score", f"{risk_score}/5", f"Target {risk_target}/5")
        
        if risk_score <= risk_target:
            st.success("✅ Gear up OK")
        else:
            st.error("🔴 De-risk NOW")

    # PORTFOLIO + ORDERS
    col1, col2 = st.columns(2)
    with col1:
        st.header("📊 Portfolio")
        portfolio = pd.DataFrame({
            'Instrument': ['BTC-PERPETUAL', '88k Call', '90k Call', '80k Put', '84k Put'],
            'Size': [75000, -0.6, 0.5, 0.9, 3.1],
            'U.PnL': [718, -1914, 1227, -43, -370],
            'Delta': [0.80, -0.59, 0.46, 0.00, -0.01]
        })
        st.dataframe(portfolio)

    with col2:
        st.header("📋 Open Orders")
        orders = pd.DataFrame({
            'Instrument': ['80k Put', '88k Call(buy)', '88k Call(sell)', '90k Call'],
            'Side': ['Sell', 'Buy', 'Sell', 'Buy'],
            'Size': [2.0, 0.1, 0.1, 0.1],
            'Limit': ['$0.40', '$5050', '$5100', '$3300']
        })
        st.dataframe(orders)

    # PLAN + LOG
    col1, col2 = st.columns(2)
    with col1:
        st.header("🎯 24h Plan")
        st.markdown("""
        **92-94k:** Range scalp perps $25k  
        **>94k:** Bull call spreads  
        **<91.8k:** Cut longs, put spreads
        """)

    with col2:
        st.header("💾 EOD Log")
        note = st.text_area("Notes:", height=100)
        if st.button("🚀 Save Log"):
            log = {
                'Time': datetime.now().strftime('%H:%M SAST'),
                'Realized': realized,
                'Unrealized': unrealized,
                'Delta': delta,
                'IMr': imr,
                'Risk': f"{risk_score}/{risk_target}",
                'Note': note
            }
            if 'logs' not in st.session_state:
                st.session_state.logs = []
            st.session_state.logs.append(log)
            st.success("✅ Saved! Copy table → Obsidian")
        if 'logs' in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state.logs).tail(5))

with tab2:
    st.header("📝 How to Use + Rationale")
    st.markdown("""
    ## **Morning Routine (08:30 SAST - 5 min)**
    1. Open dashboard → Update 4 numbers from Kyan
    2. Screenshot → Paste Obsidian daily note  
    3. Set alerts: 91.8k / 94k / 95k
    4. Execute plan based on risk score

    ## **Risk Framework (4/5 Competition Mode)**
    - **Perps:** $25-50k clips | Max 2-3x equity  
    - **Options:** Spreads only | Max 1 BTC equiv  
    - **IMr:** <40% hard cap  
    - **Daily risk:** 1-1.5% equity OK  
    - **Rules:** No naked shorts. No revenge trades.

    ## **Why This Works**
    - Forces **delta/IMr discipline** every session
    - **Visual risk score** prevents emotional sizing  
    - **One-click logging** = perfect Obsidian integration
    - **24h plan** keeps you tactical, not reactive
    """)

with tab3:
    st.header("📋 ELFA Updates Log")
    elfa_note = st.text_area("Paste latest ELFA BTC summary:", height=200)
    if st.button("💾 Save ELFA Update"):
        elfa_log = {
            'Time': datetime.now().strftime('%H:%M SAST'),
            'Summary': elfa_note[:500]
        }
        if 'elfa_logs' not in st.session_state:
            st.session_state.elfa_logs = []
        st.session_state.elfa_logs.append(elfa_log)
        st.success("✅ ELFA saved!")
    
    if 'elfa_logs' in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state.elfa_logs).tail(10))
    else:
        st.info("Paste your first ELFA update above 👆")
