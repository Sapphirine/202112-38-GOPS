import pandas as pd
import numpy as np

state_codes = ['KY', 'OH', 'PA', 'VA', 'WV']

df = pd.read_csv('heart_disease.csv', low_memory=False)
df = df.loc[df['Topic'] == 'Stroke']
df = df.loc[df['Data_Value_Unit']=="per 100,000"]
df = df.loc[df['LocationAbbr'].isin(state_codes)]

# print(df)
state_to_rates = dict()
for state_code in state_codes:
    state_df = df.loc[df['LocationAbbr'] == state_code].sort_values(by='Year')
    sum_in_state_same_year = 2 * state_df.groupby('Year')['Data_Value'].mean()[12:18] # from 2011-2016
    # print(sum_in_state_same_year)
    state_year_array = sum_in_state_same_year.to_numpy()
    state_to_rates[state_code] = state_year_array


NFLIS = pd.read_csv('MCM_NFLIS_Data.csv')
NFLIS = NFLIS.loc[NFLIS['State'].isin(state_codes)]
NFLIS = NFLIS.loc[NFLIS['YYYY']<=2016]
# print(NFLIS)
drug_names = ['Heroin', 'Hydrocodone', 'Oxycodone', 'Buprenorphine', 'Morphine']

state_res_dict = dict()
for drug_name in drug_names:
    drug_df = NFLIS[NFLIS['SubstanceName'] == drug_name]
    report_sum = drug_df.groupby(['State','YYYY'])[['DrugReports']].sum()
    report_diff = report_sum.groupby(level=0)['DrugReports'].diff()
    drug_increase_dict = dict()
    for code in state_codes:
        drug_increase_dict[code] = report_diff[code].to_numpy()[1:]

    corr_code_dict = dict()
    for code in state_codes:
        state_to_rates_series = pd.Series(state_to_rates[code])
        normalized_state_to_rates_series = (state_to_rates_series-state_to_rates_series.mean())/state_to_rates_series.std()
        # print(normalized_state_to_rates_series)
        drug_increase_series = pd.Series(drug_increase_dict[code])
        # print(drug_increase_series)
        normalized_drug_increase_series = (drug_increase_series-drug_increase_series.mean())/drug_increase_series.std()
        # print(normalized_drug_increase_series)
        corr_code_dict[code] = normalized_state_to_rates_series.corr(normalized_drug_increase_series,method='spearman')
        # corr_code_dict[code] = state_to_rates_series.corr(drug_increase_series,method='pearson')
    
    state_res_dict[drug_name] = corr_code_dict

state_res_df = pd.DataFrame(state_res_dict)
print(state_res_df)
# print(state_res_df.to_numpy().flatten())
np.save('stroke_validation_correlation_spearman', state_res_df.to_numpy().flatten())