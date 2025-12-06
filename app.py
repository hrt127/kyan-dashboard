import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="Kyan Trader v1.1 - ELFA Flow")

# ---------- SIDEBAR ----------
st.sidebar.title("📑 Quick Links")
st.sidebar.markdown("[🏦 Kyan Portfolio](https://alpha.kyan.blue/portfolio)")
st.sidebar.markdown("[📈 Kyan Perps](https://alpha.kyan.blue/perps)")
st.sidebar.markdown("[📋 Kyan Options](https://alpha.kyan.blue/)")
st.sidebar.markdown("[💰 CoinGecko BTC](https://www.coingecko.com/en/coins/bitcoin)")
st.sidebar.markdown("[🧠 Elfa AI](https://www.elfa.ai)")
st.sidebar.markdown("---")

# Simple status context you update manually
market_regime = st.sidebar.selectbox("Market regime", ["Ranging", "Trending up", "Trending down", "Choppy"], index=0)
bias = st.sidebar.selectbox("Bias", ["Neutral", "Bullish", "Bearish"], index=2)
st.sidebar.markdown(f"**🟢 STATUS: READY**")
st.sidebar.markdown("**IMr Target:** 30–50%  \n**Daily Risk:** 5–8%")
st.sidebar.markdown(f"**Regime:** {market_regime}  \n**Bias:** {bias}")

# ---------- HEADER ----------
st.title("🟢 Kyan Trader Dashboard – Stage 2")
st.markdown("**Target: Top 5 leaderboard | 6/5 testnet aggro | Structure over vibes**")

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 ELFA → Plan",
    "📊 Book from Kyan",
    "🎯 Execute + EOD",
    "🤖 Co‑Pilot (manual)"
])


# ---------- TAB 1: ELFA → PLAN ----------
with tab1:
    st.header("🧠 Step 1 – ELFA First")

    colL, colR = st.columns([3, 2])

    with colL:
        st.subheader("1️⃣ Paste full ELFA report")
        elfa_raw = st.text_area(
            "From ELFA (TL;DR + body):",
            height=350,
            placeholder="Paste full BTC report from ELFA here…"
        )

        if st.button("🤖 Parse ELFA → Trading Plan"):
            text = elfa_raw.lower()

            plan_lines = []

            # Detect short‑scalp setup like your example
            if "short scalp" in text or "short-term short" in text or "$90,250" in text:
                plan_lines.append("**SHORT BIAS** → Short ~$90.2k → TP $87.5k → SL $91.4k")
                plan_lines.append("**Perps:** $100–150k short clips")

            # Key levels
            if "87,000" in text or "$87,000" in text or "87k" in text:
                plan_lines.append("**Support $87k–87.7k** → Watch for bounce / reversal candle")
            if "90,000" in text or "91,000" in text or "90k" in text:
                plan_lines.append("**Resistance $90–91k** → Sell rallies into this zone")
            if "82,000" in text or "85,000" in text or "82k" in text or "85k" in text:
                plan_lines.append("**Breakdown <87k** → Targets $85k → $82k")

            # Fallback if nothing matched
            if not plan_lines and "range" in text:
                plan_lines.append("**Range bias** → Small size scalps inside described range")
            if not plan_lines:
                plan_lines.append("No clear edge → Wait for breakout or reversal signal.")

            btc_plan = "\n".join(plan_lines)

            # Save to session so Tab 2/3 can show it
            st.session_state["btc_plan"] = btc_plan
            st.success("✅ Plan generated & saved. It will appear on other tabs.")
            st.text_area("Generated BTC Plan (readable):", value=btc_plan, height=160)

            # Log ELFA snapshot
            elfa_entry = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Summary": elfa_raw[:140].replace("\n", " ") + ("..." if len(elfa_raw) > 140 else ""),
                "Plan": btc_plan
            }
            st.session_state.setdefault("elfa_logs", []).append(elfa_entry)

    with colR:
        st.subheader("2️⃣ Checklist from plan (mental)")
        st.markdown("""
- [ ] Bias matches my own TA/voodoo/raindancing  
- [ ] Levels clear (entry / invalidation / targets)  
- [ ] No stupid size vs IMr limits  
- [ ] Happy to execute this even if wrong
        """)
        st.markdown("Once this feels right → go to **Tab 2 – Book from Kyan**.")


    st.subheader("📋 ELFA History (last 10)")
    if "elfa_logs" in st.session_state:
        df_elfa = pd.DataFrame(st.session_state["elfa_logs"]).tail(10)
        st.dataframe(df_elfa, use_container_width=True)
    else:
        st.info("No ELFA logs yet – paste a report and generate a plan to start.")


# ---------- TAB 2: BOOK FROM KYAN ----------
with tab2:
    st.header("📊 Step 2 – Build Book from Kyan (no code edits)")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("1️⃣ Top‑level numbers (from Kyan Portfolio)")
        realized = st.number_input("Realized PnL ($)", value=41613.0)
        unrealized = st.number_input("Unrealized PnL ($)", value=-382.24)
        net_delta = st.number_input("Net Delta (BTC)", value=0.67)
        imr_pct = st.number_input("IMr (%)", value=1.0)

        equity = 250000 + realized + unrealized
        ret_pct = (equity / 250000 - 1) * 100
        st.metric("Total Equity", f"${equity:,.0f}", f"{ret_pct:+.1f}% vs $250k start")

        st.session_state["topline"] = dict(
            realized=realized, unrealized=unrealized,
            net_delta=net_delta, imr_pct=imr_pct, equity=equity
        )

    with colB:
        st.subheader("2️⃣ Risk appetite")
        risk_target = st.slider("Risk appetite (1–6)", 1, 6, 6)
        risk_score = 1
        if abs(net_delta) > 3:
            risk_score += 2
        elif abs(net_delta) > 1.5:
            risk_score += 1
        if imr_pct > 50:
            risk_score += 2
        elif imr_pct > 30:
            risk_score += 1
        if imr_pct > 80:
            risk_score = 6

        st.metric("Risk Score", f"{risk_score}/6", f"Target {risk_target}/6")
        if risk_score <= risk_target:
            st.success("✅ DOMINATE – sizing OK for testnet.")
        else:
            st.warning("⚠️ High risk – trim or hedge before adding more.")

    st.markdown("---")
    colP, colO = st.columns(2)

    with colP:
        st.subheader("3️⃣ Current positions (paste from Kyan)")
        pos_text = st.text_area(
            "Paste simple rows: instrument,size,upnl,delta (one per line)",
            height=140,
            placeholder="BTC-PERPETUAL,75000,718,0.803\nBTC-05DEC25-88000-C,-0.6,-1914,-0.585"
        )
        positions = []
        for line in pos_text.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                inst, size, upnl, delta = parts[:4]
                positions.append(
                    dict(Instrument=inst, Size=size, U_PnL=upnl, Delta=delta)
                )
        if positions:
            df_pos = pd.DataFrame(positions)
            st.dataframe(df_pos, use_container_width=True)
        st.session_state["positions"] = positions

    with colO:
        st.subheader("4️⃣ Open orders (paste from Kyan)")
        ord_text = st.text_area(
            "instrument,side,size,limit (one per line)",
            height=140,
            placeholder="BTC-05DEC25-80000-P,Sell,2,0.40\nBTC-05DEC25-88000-C(buy),Buy,0.1,5050"
        )
        orders = []
        for line in ord_text.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                inst, side, size, limit = parts[:4]
                orders.append(
                    dict(Instrument=inst, Side=side, Size=size, Limit=limit)
                )
        if orders:
            df_ord = pd.DataFrame(orders)
            st.dataframe(df_ord, use_container_width=True)
        st.session_state["orders"] = orders

    st.markdown("---")
    st.subheader("5️⃣ Orderbook notes (manual)")
    ob_notes = st.text_area(
        "Perps & options orderbook notes",
        height=120,
        placeholder="Perps: asks stacked 90–91k, bids 87–88k.\nOptions: 90–92k calls rich, downside puts bid."
    )
    st.session_state["orderbook_notes"] = ob_notes


# ---------- TAB 3: EXECUTE + EOD ----------
with tab3:
    st.header("🎯 Step 3 – Execute, Track, Close the Day")

    colL, colR = st.columns(2)

    with colL:
        st.subheader("1️⃣ Today’s BTC Plan (from ELFA)")
        plan = st.session_state.get("btc_plan", "No plan parsed yet. Go to Tab 1 first.")
        st.markdown(plan)

        st.subheader("2️⃣ Execution checklist")
        c1 = st.checkbox("Perp positions sized according to plan")
        c2 = st.checkbox("Options structure matches bias (no naked shorts)")
        c3 = st.checkbox("Alerts set at key levels")
        c4 = st.checkbox("IMr and daily risk within limits")

        st.session_state["exec_checks"] = dict(
            perps=c1, options=c2, alerts=c3, risk_ok=c4
        )

    with colR:
        st.subheader("3️⃣ Quick notes during session")
        intraday_note = st.text_area(
            "Running notes (tape reads, feelings, mistakes to avoid):",
            height=160
        )
        st.session_state["intraday_note"] = intraday_note

    st.markdown("---")
    st.subheader("4️⃣ End‑of‑Day Report Generator")

        if st.button("📸 Generate EOD report (copy to Obsidian)"):
        topline = st.session_state.get("topline", {})
        exec_checks = st.session_state.get("exec_checks", {})
        positions = st.session_state.get("positions", [])
        orders = st.session_state.get("orders", [])
        plan = st.session_state.get("btc_plan", "No plan saved.")
        ob_notes = st.session_state.get("orderbook_notes", "")
        intraday = st.session_state.get("intraday_note", "")

        equity = topline.get("equity", 0)
        realized = topline.get("realized", 0)
        unrealized = topline.get("unrealized", 0)
        net_delta = topline.get("net_delta", 0)
        imr_pct = topline.get("imr_pct", 0)

        report = f"""# Kyan Stage 2 – EOD Report ({datetime.now().strftime('%Y-%m-%d %H:%M SAST')})

## 📊 Dashboard Snapshot
- Equity: ${equity:,.0f}
- Realized: ${realized:,.0f}
- Unrealized: ${unrealized:,.0f}
- Net Delta: {net_delta:.2f} BTC
- IMr: {imr_pct}%

## 🧠 ELFA Plan
{plan}

## ✅ Execution Checklist
- Perps sized per plan: {exec_checks.get('perps', False)}
- Options match bias (no naked shorts): {exec_checks.get('options', False)}
- Alerts set at key levels: {exec_checks.get('alerts', False)}
- Risk within limits: {exec_checks.get('risk_ok', False)}

## 📋 Positions (summary)
Positions count: {len(positions)}
Orders count: {len(orders)}

## 🧾 Orderbook Notes
{ob_notes}

## 📝 Intraday Notes
{intraday}
"""
        st.code(report, language="markdown")
        st.success("✅ EOD report ready – copy into Obsidian.")

# ---------- TAB 4: CO‑PILOT (MANUAL) ----------
with tab4:
    st.header("🤖 Step 4 – Manual Co‑Pilot")

    st.markdown("""
This is a scratchpad to work with an external LLM (ChatGPT, Claude, etc.).

**How to use:**
1. Copy your ELFA plan + positions summary from Tabs 1–2  
2. Paste into the box below  
3. Paste the LLM's reply into the second box  
4. Use it to refine tomorrow's plan
    """)

    context = st.text_area("Context sent to LLM (plan + book):", height=200)
    reply = st.text_area("LLM reply (paste here):", height=200)

    st.markdown("Use this as a review tool, not a signal generator.")
