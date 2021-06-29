import glob
import pandas, seaborn

results = glob.glob("result_network_ring_*.csv")

df_list = []
for result in results:
    df_list.append(pandas.read_csv(result))

df = pandas.concat(df_list)
seaborn.relplot(data=df, kind="line", x="t/ms", y="U/mV",hue="Cell",ci=None).savefig('network_ring_result.png')