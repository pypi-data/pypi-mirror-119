# StockHero

[![Downloads](https://pepy.tech/badge/stockhero)](https://pepy.tech/project/stockhero)

## The Ticker module
The Ticker module, gets the financial data from morningstar.com as a pandas.DataFrame, so you can use it in any way you want

```python
import StockHero as stock
t = stock.Ticker('NVDA') # e.g. NVIDIA Corp

t.financials            # Financials
t.marginofsales         # Key Ratios - Profitability - Margins % of Sales
t.profitability         # Key Ratios - Profitability - Profitability
t.growth_rev            # Key Ratios - Growth - Revenue %
t.growth_op_inc         # Key Ratios - Growth - Operating Income %
t.growth_net_inc        # Key Ratios - Growth - Net Income %
t.growth_eps            # Key Ratios - Growth - EPS %
t.cf_ratios             # Key Ratios - Cash Flow - Cash Flow Ratios
t.bs                    # Key Ratios - Financial Health - Balance Sheet Items (in %)
t.li_fin                # Key Ratios - Financial Health - Liquidity/Financial Health
t.efficiency            # Key Ratios - Efficiency Ratios - Efficiency
```

### Installing
https://pypi.org/project/StockHero/

### Legal Stuff

StockHero is distributed under the Apache Software License


### Stay tuned and thanks to my colleagues at Fraunhofer

Any feedback, let me know

Robert Wenzel
<br>
<br>
<br>
### Versions
0.0.2 Bug fixes / Changed License <br>
0.0.1 First Release

