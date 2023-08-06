# StockHero

## The Ticker module
The Ticker module, will get the financial data from morningstar as a pandas.DataFrame, so you can use it in any way you want

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

### Stay tuned and thanks to my colleagues at Fraunhofer