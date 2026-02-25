# AIRisk Analyzer

A sophisticated portfolio risk analysis system powered by AI and LangGraph. This tool analyzes your stock portfolio and generates comprehensive risk reports using real market data and advanced financial metrics.

## 🎯 Features

- **Data Preparation**: Fetches real historical stock price data using Yahoo Finance API
- **Market Risk Analysis**: Calculates Value at Risk (VaR) and runs stress tests based on 3 years of historical data
- **Volatility Metrics**: Computes annualized volatility, Sharpe ratio, and correlation matrix
- **AI-Powered Reports**: Uses GPT-4 to synthesize all risk metrics into actionable insights
- **Parallel Processing**: Leverages LangGraph for efficient concurrent node execution

## 📊 Metrics Calculated

- **Value at Risk (VaR)**: 95% confidence level worst-case loss
- **Volatility**: Annualized standard deviation of returns
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Correlation Matrix**: Asset movement relationships
- **Stress Tests**: Worst-case scenarios from historical data

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (for GPT-4 access)

### Usage

Edit the portfolio in [main.py](main.py):

```python
portfolio = {
        "JPM": 0.05,    # 5% JPMorgan Chase
        "XOM": 0.05,   # 5% ExxonMobil
        "JNJ": 0.1,     # 10% Johnson & Johnson
        "BRK-B": 0.1,     # 10% Gerdau
        "GS": 0.1,     # 10% Goldman Sachs
        "TSLA": 0.1,     # 10% Tesla
        "AMZN": 0.1,     # 10% Amazon
        "MSFT": 0.1,    # 10% Microsoft
        "AAPL": 0.1,    # 10% Apple
        "GOOGL": 0.1    # 10% Alphabet
    }
time_horizon = 90   # 3 months of historical data
```

Run the analyzer:
```bash
python main.py
```

## 📁 Project Structure

```
risk_analyzer/
├── main.py                 # Entry point
├── graph.py               # LangGraph orchestration
├── state.py               # Shared state schema
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── nodes/
│   ├── data_preparation.py    # Fetch historical prices
│   ├── market_risk.py         # VaR & stress testing
│   ├── volatility.py          # Volatility metrics
│   └── report_synthesis.py    # AI report generation
└── tools/
    └── price_simulator.py     # Yahoo Finance integration
```

## 🔄 Architecture

The system uses LangGraph to orchestrate analysis flow:

```
START
  ↓
[Data Preparation] — Fetches historical prices
  ↓
  ├→ [Market Risk] ——→ Calculates VaR & stress tests
  │                        ↓
  └→ [Volatility] ———→ Calculates volatility metrics
                          ↓
                   [Report Synthesis]
                   ↓
                   END
```

## 🔐 Security Considerations

### API Key Management

- **Never commit `.env` file**: The project includes `.env` in `.gitignore`
- **Use `.env.example`**: Copy this template and fill in your own secrets
- **Environment variables**: All sensitive data is loaded via `python-dotenv`

## 📦 Dependencies

- **langgraph**: Graph orchestration framework
- **langchain-openai**: OpenAI integration for LLM
- **langchain-core**: Core LangChain utilities
- **numpy**: Numerical computing
- **python-dotenv**: Environment variable management
- **yfinance**: Real-time stock market data

## 📈 Example Output

```
============================================================
   PORTFOLIO RISK ANALYZER — Starting...
============================================================
[Node A] Fetching historical prices for: ['AAPL', 'GOOGL', 'TSLA']
[Node A] Successfully fetched 90 days of data for 3 assets.
[Node B] Value at Risk (95%): 2.45%
[Node C] Sharpe Ratio: 1.23
[Node C] Volatility scores: {'AAPL': 0.28, 'GOOGL': 0.32, 'TSLA': 0.45}

============================================================
   FINAL RISK REPORT
============================================================
[AI-generated comprehensive risk analysis...]
```

## 🛠️ Customization

### Modify Time Horizon
Change `time_horizon` in [main.py](main.py) to analyze different periods (in days)

### Change Portfolio Weights
Update the `portfolio` dictionary with different ticker symbols and allocations

### Adjust LLM Settings
Modify model and temperature in [report_synthesis.py](nodes/report_synthesis.py):
```python
llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

## 🐛 Troubleshooting

**Issue**: `OPENAI_API_KEY not found`
- Solution: Ensure `.env` file exists with your API key and `.env` is loaded

**Issue**: Invalid ticker symbol errors
- Solution: Use valid Yahoo Finance ticker symbols (e.g., AAPL, GOOGL, TSLA)

**Issue**: Insufficient market data
- Solution: Ensure your time_horizon isn't longer than available historical data

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. It should not be used as the sole basis for investment decisions. Always consult with a financial advisor before making investment decisions.
