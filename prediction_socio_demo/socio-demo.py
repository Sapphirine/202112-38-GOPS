import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# print(ann)
df = pd.read_csv("ACS_15_5YR_DP02.csv")
ann = pd.read_csv("ACS_15_5YR_DP02_ann.csv")
filter_col = [col for col in df if col.startswith('Percent Margin of Error')]
ann_filter_col = [col for col in ann if ann[col][0].startswith('Percent Margin of Error')]

ann_filtered = ann[ann_filter_col]
# print(filter_col)
data = df[filter_col]
data.columns = ann_filtered.columns.values
# print(data)
corr = data.corr()
# print(corr)

non_related = [c for c in corr.columns if any(corr[c] < 0.2)]
# print(non_related)
# print(non_related)
data = data[non_related]
ann_non_related = ann_filtered[non_related]
# print(ann_non_related)
# print(data)

# # data.columns = data.columns.str.lstrip('Percent Margin of Error; ')
# # print(data)
corr_matix = data.corr()
# print(corr_matix)
mask = np.triu(np.ones_like(corr_matix, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr_matix, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

# plt.show()

plt.savefig('corr.png')

v = ann_non_related.iloc[0].values.tolist()
with open('ann.txt','w') as f:
    for i in range(len(non_related)):
        f.write(non_related[i] +': ' + v[i] + '\n')