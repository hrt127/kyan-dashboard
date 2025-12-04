# Kyan Trader Dashboard

**Real-time trading dashboard for the Kyan Stage 2 competition**

---

## Overview

This is a minimal yet functional Streamlit app designed to help traders track their Kyan derivatives portfolio and make defined-risk trading decisions during the Stage 2 competition.

- Shows portfolio unrealized + realized PnL, net delta, and margin ratio (IMr).  
- Computes a simple risk score and suggests whether to scale up or de-risk.  
- Displays current positions and open orders in tabular form.  
- Summarizes the tactical 24h BTC trading plan for quick reference.  
- Enables easy end-of-day logging for manual copying into personal journals (e.g., Obsidian).

---

## What it is

- A **streamlined, user-driven dashboard**: all inputs are manual number fields — no API connectivity yet.  
- A **risk framework tool** tuned for a 4/5 risk appetite, matching defined-risk spreads and measured perp exposure.  
- A **competition-centric tool** to cultivate disciplined habits and structured decision-making.  
- A **logging utility** captures daily snapshots to assist post-mortem and journaling.

---

## What it isn’t

- Not connected to any exchange API (yet).  
- Not a full trading platform / execution system.  
- No automatic alerts or trade automation.  
- Not designed for general-purpose crypto portfolio tracking.  
- No guarantees or investment advice; use at your own risk.

---

## How to use

1. 1. Open [your actual Streamlit URL](https://kyan-dashboard-hrt127.streamlit.app)
2. Enter your portfolio data from the Kyan UI: realized/unrealized PnL, net delta (BTC), IMr %.  
3. Review the dashboard’s risk score and follow suggested actions (gear up or de-risk).  
4. Review the positions and open orders to confirm your current exposure.  
5. Read the 24h BTC trading plan for context on market behavior and your plays.  
6. Use the “End-of-Day Log” section to save notes; copy the generated log table into your journal tool (e.g., Obsidian) daily.  

---

## Repository contents

- `app.py`: The full Streamlit dashboard source code.  
- `.gitignore`: Python standard ignores.  
- `README.md`: This file.

---

## Future work (planned, but not implemented)

- API integration to fetch portfolio data automatically from Kyan.  
- Interactive order book and options chain views.  
- Push notifications / alert systems.  
- Trade execution capabilities.  

---

## Requirements

- Python 3.8+  
- Streamlit 1.20+  
- Pandas  

---

## Setup (local dev)
```
git clone https://github.com/hrt127/kyan-dashboard.git
cd kyan-dashboard
pip install -r requirements.txt # (add your own requirements.txt if needed)
streamlit run app.py
```

---

## License

MIT License © 2025 [hrt127]

---

## Disclaimer

This tool is provided "as is" without warranty. Trading derivatives is risky. Use at your own discretion.

---

*Last updated: December 2025*
