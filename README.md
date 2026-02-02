# CECS Financial Analytics | UTK

Financial analytics platform for the **College of Emerging & Collaborative Studies** at the University of Tennessee, Knoxville. Built with Streamlit.

## Features

- **Executive dashboard** – KPIs, revenue vs expenses, expense distribution
- **Staffing analysis** – Ratios, compensation, headcount and cost breakdowns
- **Financial details** – Revenue/expense breakdown, ratios, full financial statement
- **Advanced analytics** – Enrollment scenarios, break-even, sensitivity, 5-year projections, risk assessment

## Run locally

```bash
# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Calc.py
```

Then open http://localhost:8501 in your browser.

**Demo login:** Username `CECS` | Password `UTK`

## Deploy on Streamlit Community Cloud

1. Push this repo to **GitHub** (e.g. `your-username/CECS-CALC`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, choose your repo and branch.
4. Set:
   - **Main file path:** `Calc.py`
   - **Python version:** 3.11 (or 3.10)
5. Click **Deploy**. Streamlit Cloud will install from `requirements.txt` and run `streamlit run Calc.py`.

Your app will be available at a URL like `https://your-app-name.streamlit.app`.

## Project structure

```
CECS-CALC/
├── Calc.py           # Streamlit app entry point
├── requirements.txt  # Python dependencies
├── README.md
└── LICENSE
```

## License

MIT — see [LICENSE](LICENSE).
