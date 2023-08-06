# TickerAnalysis
TickerAnalysis is on open source library that calculates technical indicators for any ticker available on yahoo finance.

## Installation
    pip install ticker-analysis
    
## Example Usage
    from TickerAnalysis import TickerAnalysis
    
    ticker = TickerAnalysis("SU", "5m", "1mo")

    current_price = ticker.get_price()

    bollinger_bands = ticker.get_bollinger_bands()
    lower_bollinger_band = bollinger_bands["bolDown"]

    if lower_bollinger_band < current_price:
        print("SU is oversold")
