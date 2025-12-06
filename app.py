import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="Kyan Trader v1.0 - TESTNET DOMINATION")
st.title("🟢 Kyan Trader Dashboard - Stage 2 Competition")
st.markdown("**$301k Equity | +$41.6k Realized (16.7%) | 6/5 TESTNET AGGRO MODE**")

# SIDEBAR - QUICK ACCESS + STATUS
st.sidebar.title("📑 Quick Links")
st.sidebar.markdown("[🏦 Kyan Portfolio](https://alpha.kyan.blue/portfolio)")
st.sidebar.markdown("[📈 Kyan Perps](https://alpha.kyan.blue/perps)")
st.sidebar.markdown("[📋 Kyan Options](https://alpha.kyan.blue/)")
st.sidebar.markdown("[💰 CoinGecko BTC](https://www.coingecko.com/en/coins/bitcoin)")
st.sidebar.markdown("[🧠 Elfa AI](https://www.elfa.ai)")
st.sidebar.markdown("---")
st.sidebar.markdown("**🟢 STATUS: READY**")
st.sidebar.markdown("**IMr Target: 30-50%** | **Daily Risk: 5-8%**")

# PAGES
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 ELFA Logs", "📝 Daily Routine", "💾 Trade Log"])

# TAB 1: MAIN DASHBOARD
with tab1:
    st.header("🔥 6/5 TESTNET DOMINATION DASHBOARD")
    
    # SUMMARY + RISK (col1 = inputs, col2 = risk engine)
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📊 Update from Kyan Portfolio (2 min)")
        realized = st.number_input("Realized PnL ($)", value=41613.0, 
                                  help="From History: Sum ALL 'trade(Close)' + funding to date")
        unrealized = st.number_input("Unrealized PnL ($)", value=-382.23,
                                    help="Current portfolio P&L (open positions)")
        delta = st.number_input("Net Delta (BTC)", value=0.67, 
                               help="Total portfolio delta from Kyan Portfolio page")
        imr_pct = st.number_input("IMr (%)", value=1.0, 
                                 help="Initial Margin Ratio from Portfolio header")
        
        equity = realized + unrealized
        st.metric("Total Equity", f"${equity:,.0f}", f"Starting $250k (+{equity/250000*100-100:.1f}%)")
    
    with col2:
        st.subheader("⚠️ Risk Engine - AUTO CALCULATES")
        risk_target = st.slider("Risk Appetite", 1, 6, 6, help="6/5 = Testnet Domination")
        
        # Risk score calculation
        risk_score = 1
        if abs(delta) > 3: risk_score += 2
        elif abs(delta) > 1.5: risk_score += 1
        if imr_pct > 50: risk_score += 2
        elif imr_pct > 30: risk_score += 1
        if imr_pct > 80: risk_score = 6  # Max risk
        
        st.metric("Risk Score", f"{risk_score}/6", f"Target {risk_target}/6")
        
        if risk_score <= risk_target:
            st.success("✅ **DOMINATE** - Size up aggressively")
            st.info("**Perps:** $100-200k clips | **Options:** 3 BTC spreads")
        else:
            st.warning("🟡 **CAUTION** - Trim positions")
        st.error("🔴 **LIQUIDATION** - IMr >80%")
    
    # POSITIONS + ORDERS
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Current Positions (Update from Kyan)")
        portfolio = pd.DataFrame({
            'Instrument': ['BTC-PERPETUAL', 'BTC-05DEC25-88000-C', 'BTC-05DEC25-90000-C', 
                          'BTC-05DEC25-80000-P', 'BTC-05DEC25-84000-P'],
            'Size': [75000, -0.60, 0.50, 0.90, 3.10],
            'U.PnL': [717.84, -1914.38, 1226.62, -42.52, -369.80],
            'Delta': [0.803, -0.585, 0.459, 0.000, -0.008]
        })
        st.dataframe(portfolio.style.format({'U.PnL': '${:,.0f}'}))
    
    with col2:
        st.subheader("📋 Open Orders (Update from Kyan)")
        orders = pd.DataFrame({
            'Instrument': ['BTC-05DEC25-80000-P', 'BTC-05DEC25-88000-C(buy)', 
                          'BTC-05DEC25-88000-C(sell)', 'BTC-05DEC25-90000-C'],
            'Side': ['Sell', 'Buy', 'Sell', 'Buy'],
            'Size': [2.0, 0.10, 0.10, 0.10],
            'Limit': ['$0.40', '$5050', '$5100', '$3300'],
            'Filled': [1.1, 0.0, 0.0, 0.0]
        })
        st.dataframe(orders)
    
    # PLAN + QUICK ACTION
    col1, col2 = st.columns(2)
   with col1:
    st.subheader("🎯 Today's BTC Plan - EDITABLE")
    btc_plan = st.text_area("",
        value="""**Range 88-90k** → Perp scalps $100-150k
**Breakout >90.3k** → Add 12Dec 90/95C spreads (2x size)
**Breakdown <88k** → Cut 50% delta → Add put spreads""",
        height=140, key="btc_plan")


    
    with col2:
        st.subheader("⚡ Quick Actions")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📱 Set Alerts (91.8k/94.5k)", type="secondary"):
                st.balloons()
                st.info("✅ Set phone alerts: 91.8k ↓, 94.5k ↑")
        with col_b:
            if st.button("📸 Screenshot for Obsidian", type="secondary"):
                st.balloons()
                st.success("✅ Screenshot → Paste daily note!")

# TAB 2: ELFA LOGS
with tab2:
    st.header("📋 ELFA Parser - Auto-generates BTC Plan")
    
    elfa_raw = st.text_area("Paste full ELFA report:", height=400)
    
    if st.button("🤖 PARSE ELFA → BTC PLAN", type="primary"):
        lines = elfa_raw.lower()
        
        ranges = []
        if any(word in lines for word in ['range', '88k', '90k']):
            ranges.append("**Range 88-90k** → Perp scalps $100k")
        if '90k' in lines or 'breakout' in lines:
            ranges.append("**Breakout >90.3k** → 12Dec bull spreads")
        if '88k' in lines or 'breakdown' in lines:
            ranges.append("**Breakdown <88k** → Cut delta + puts")
        
        auto_plan = "\n".join(ranges)
        st.text_area("✅ COPY THIS → Tab 1 BTC Plan:", 
                    value=auto_plan or "Range-bound → Small scalps only", 
                    height=140, key="auto_plan")
        st.success("✅ Copy above → Paste Tab 1!")

# TAB 3: DAILY ROUTINE
with tab3:
    st.header("🕐 Your Daily Routine - Copy to Obsidian")
    st.markdown("""
    ## **08:30 SAST - MORNING PREP (5 min)**
    1. ✅ Open Dashboard → Update 4 numbers (Realized/Unrealized/Delta/IMr)
    2. ✅ ELFA.ai → Copy BTC summary → Tab 2 → Save  
    3. ✅ Risk green? → Execute plan (Tab 1)
    4. ✅ Screenshot dashboard → Paste Obsidian daily note
    5. ✅ Phone alerts: Key levels from ELFA

    ## **13:00 SAST - MID-DAY CHECK (2 min)**
    1. ✅ BTC hit levels? → Update dashboard  
    2. ✅ Risk still green? → Add to winners
    3. ✅ Quick Obsidian note: "13:00 - BTC 93.2k, added perp"

    ## **20:00 SAST - US CLOSE / EOD (3 min)**
    1. ✅ Final dashboard update  
    2. ✅ Tab 4 → "Save EOD Log" → Copy table → Obsidian  
    3. ✅ Screenshot PnL → Archive
    
    ## 📸 EOD SCREENSHOTS (30 sec)
    1. **Tab 1** (Dashboard) → Ctrl+Shift+P → "Full page screenshot"  
    2. **Tab 2** (ELFA) → Full page screenshot  
    3. **Tab 3** (Routine) → Screenshot  
    4. **Tab 4** → "Generate EOD Report" → Copy → Obsidian

    **Browser Extensions (1-click):**  
    **GoFullPage** (Chrome) → Full PNG  
    **Fireshot** → PDF  
    **Awesome Screenshot** → Annotated

    **TOTAL TIME: 10 min/day. REST = Execute.**
    """)

# TAB 4: TRADE LOG
with tab4:
    st.header("💾 EOD Trade Log - Copy to Obsidian")
    note = st.text_area("What happened today? (BTC action / sizing / lessons)", 
                       height=150, placeholder="BTC tested 94k → Added 12Dec spreads. Risk stayed green.")
    
    if st.button("🚀 Save EOD Log", type="primary"):
        log_entry = {
            'DateTime': datetime.now().strftime('%Y-%m-%d %H:%M SAST'),
            'Equity': f"${realized + unrealized:,.0f}",
            'Realized': f"${realized:,.0f}",
            'Unrealized': f"${unrealized:,.0f}",
            'Delta': f"{delta:.2f} BTC",
            'IMr': f"{imr_pct}%",
            'Risk': f"{risk_score}/{risk_target}",
            'Notes': note[:300]
        }
        if 'trade_logs' not in st.session_state:
            st.session_state.trade_logs = []
        st.session_state.trade_logs.append(log_entry)
        st.success("✅ **EOD LOG SAVED** - Copy table → Obsidian Daily Note!")
    
    if 'trade_logs' in st.session_state:
        st.subheader("Recent Logs (Copy All)")
        recent_logs = pd.DataFrame(st.session_state.trade_logs).tail(7)
        st.dataframe(recent_logs)
    else:
        st.info("👆 Save your first log")

# EOD REPORT GENERATOR
st.markdown("---")
st.subheader("📸 EOD Report Generator")

if st.button("🎯 GENERATE FULL EOD REPORT", type="primary"):
    report = f"""
# Kyan Stage 2 - EOD Report ({datetime.now().strftime('%Y-%m-%d %H:%M SAST')})

## 📊 DASHBOARD SNAPSHOT
**Equity:** ${realized + unrealized + 250000:,.0f} | **Realized:** ${realized:,.0f} | **Risk:** {risk_score}/{risk_target}

**IMr:** {imr_pct}% | **Delta:** {delta:.2f} BTC

## 🎯 TODAY'S ACTIONS
- Updated from Kyan: {realized + unrealized:,.0f} equity
- Risk: {risk_score}/{risk_target} → {'DOMINATE' if risk_score <= risk_target else 'CAUTION'}
"""
    
    if 'elfa_logs' in st.session_state:
        report += "\n## 📋 ELFA LOGS (Last 3):\n"
        for log in st.session_state.elfa_logs[-3:]:
            report += f"- {log['Time']}: {log['Summary'][:100]}...\n"
    
    if 'trade_logs' in st.session_state:
        report += "\n## 💾 TRADE LOGS (Last 3):\n"
        for log in st.session_state.trade_logs[-3:]:
            report += f"- {log['DateTime']}: {log['Notes'][:100]}...\n"
    
    st.markdown("### 📄 **Copy this → Obsidian Daily Note**")
    st.code(report, language="markdown")
    st.success("✅ **EOD REPORT READY** - One-click copy!")
    st.balloons()

st.markdown("---")
st.markdown("""
**🎯 QUICK START:** Update 4 numbers → Check risk → Execute plan → Log EOD → Obsidian  
**📱 MOBILE:** Bookmark this page | Works on phone  
**🔄 REFRESH:** Data persists in browser session  
**💾 BACKUP:** Copy tables → Obsidian daily notes daily
""")
