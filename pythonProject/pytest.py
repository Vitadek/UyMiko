import yfinance as yf
#import pandas as pd
import matplotlib.pyplot as plt
plt.close("all")
#pivot point = previous day (high + low + close) /3
#r1 = (2xpp) - low - resistance
#s1 = (2xpp) - high - support
#r2 = pp+(h-l)
#s2 = pp - (h-l)
#r3 = high + 2(pp-l)
#s3 = low - 2(h-pp)

vuzi = yf.Ticker('vuzi')
vuzi_h = vuzi.info["dayHigh"]
vuzi_l = vuzi.info["dayLow"]
vuzi_c = (vuzi.history().tail(1)['Close'].iloc[0])
print("Pivot Point = {}".format((vuzi_h + vuzi_l + vuzi_c) / 3))
pp = (vuzi_h + vuzi_l + vuzi_c) / 3
# first resistance/support levels
r1 = (2 * pp) - vuzi_l
s1 = (2 * pp) - vuzi_h

# second resistance/support levels
r2 = pp + (vuzi_h - vuzi_l)
s2 = pp - (vuzi_h - vuzi_l)

# third res/sup levels
r3 = vuzi_h + (2 * (pp-vuzi_l))
s3 = vuzi_l - (2 * (vuzi_h - pp))
