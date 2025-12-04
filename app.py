"""
Kyan Trader Dashboard - Stage 2 Competition
Real-time portfolio tracking, risk management, and trade logging
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="Kyan Trader v1.0")
st.title("🟢 Kyan Trader Dashboard")
st.markdown("**Stage 2 Competition | Risk Framework 4/5**")

# 1. Summary + Risk
col1, col2 = st.columns([3,2])

with col1:
    st.header("📋 Portfolio Summary")
    realized = st.number_input("Realized PnL ($)", value=0.0, help="From Kyan History")
    unrealized = st.number_input("Unrealized PnL ($)", value=-382.23, help="Portfolio total")
    delta = st.number_input("Net Delta (BTC)", value=0.67, help="Total portfolio delta")
    imr = st.number_input("IMr (%)", value=1.0, help="Initial Margin Ratio")

with col2:
    st.header("⚠️ Risk Management")
    risk_target = st.slider("Risk Appetite (1-5)", 1, 5, 4, help="4/5 = Competition mode")
    
    # Risk calculation
    risk_score = 1
    if abs(delta) > 2: risk_score += 1
    if imr > 20: risk_score += 1  
    if imr > 40: risk_score += 2
    
    st.metric("Risk Score", f"{risk_score}/5", f"Target {risk_target}/5")
    
    if risk_score <= risk_target:
        st.success("✅ Gear Up: Add perps/spreads")
        st.info("Max: 2-3x equity perps | 1 BTC options spreads")
    else:
        st.error("🔴 De-Risk: Trim 25-50% positions")

# 2. Portfolio + Orders  
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Current Positions")
    portfolio = pd.DataFrame({
        'Instrument': ['BTC-PERPETUAL', '88k-C', '90k-C', '80k-P', '84k-P'],
        'Size': [75000, -0.6, 0.5, 0.9, 3.1],
        'U.PnL': [718, -1914, 1227, -43, -370],
        'Delta': [0.80, -0.59, 0.46, 0.00, -0.01]
    })
    total_pnl = portfolio['U.PnL'].sum()
    st.metric("Net Position PnL", f"${total_pnl:,.0f}")
    st.dataframe(portfolio)

with col2:
    st.header("📋 Open Orders")
    orders = pd.DataFrame({
        'Instrument': ['80k-P', '88k-C(buy)', '88k-C(sell)', '90k-C'],
        'Side': ['Sell', 'Buy', 'Sell', 'Buy'],
        'Size': [2.0, 0.1, 0.1, 0.1],
        'Limit': ['$0.40', '$5050', '$5100', '$3300']
    })
    st.dataframe(orders)

# 3. Trading Plan + Logs
col1, col2 = st.columns(2)

with col1:
    st.header("🎯 24h Trading Plan")
    st.markdown("""
    **Range 92-94k**  
    → Perp scalps $25-50k clips
    
    **Breakout >94k**  
    → 12Dec bull call spreads (92/97k)
    
    **Breakdown <91.8k**  
    → Cut 50% longs + put spreads
    """)

with col2:
    st.header("💾 Trade Log")
    note = st.text_area("Session notes", height=120, 
                       placeholder="BTC action? Risk decisions? Lessons?")
    
    if st.button("🚀 Save EOD Log", type="primary"):
        log_entry = {
            'DateTime': datetime.now().strftime('%Y-%m-%d %H:%M SAST'),
            'Realized': realized,
            'Unrealized': unrealized,
            'Delta': delta,
            'IMr': f"{imr}%",
            'Risk': f"{risk_score}/{risk_target}",
            'Notes': note[:200]
        }
        
        # Store logs
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        st.session_state.logs.append(log_entry)
        
        st.success("✅ Log saved!")
        st.dataframe(pd.DataFrame(st.session_state.logs).tail(5))

st.markdown("---")
st.caption("👆 Update → Auto-calculates | Logs persist | Copy to Obsidian Daily Notes")
