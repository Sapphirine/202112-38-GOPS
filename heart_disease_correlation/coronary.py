import pandas as pd

from statistics import mean

state_codes = ['KY', 'OH', 'PA', 'VA', 'WV']

df = pd.read_csv('heart_disease.csv', low_memory=False)
df = df.loc[df['Topic'] == 'Coronary Heart Disease']
df = df.loc[df['Data_Value_Unit']=="per 100,000"]
df = df.loc[df['LocationAbbr'].isin(state_codes)]

# print(df)
state_to_rates = dict()
for state_code in state_codes:
    state_df = df.loc[df['LocationAbbr'] == state_code].sort_values(by='Year')
    sum_in_state_same_year = 2 * state_df.groupby('Year')['Data_Value'].mean()[12:19] # from 2011- 2017
    state_year_array = sum_in_state_same_year.to_numpy()
    state_to_rates[state_code] = state_year_array

# print(state_to_rates)

fips_list = df['LocationID'].unique()
fips_to_rates = dict()
for location_id in fips_list:
    county_df = df.loc[df['LocationID'] == location_id].sort_values(by='Year')
    sum_in_same_year = county_df.groupby('Year')['Data_Value'].sum()[12:19] # from 2011- 2017
    year_array = sum_in_same_year.to_numpy()
    fips_to_rates[location_id] = year_array


NFLIS = pd.read_csv('MCM_NFLIS_Data.csv')
NFLIS = NFLIS.loc[NFLIS['State'].isin(state_codes)]
# drug_names = ['Heroin', 'Hydrocodone', 'Fentanyl', 'Oxycodone', 'Buprenorphine', 'Morphine', 'Hydromorphone', 'Oxymorphone', 'Tramadol', 'Methadone']
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
        drug_increase_series = pd.Series(drug_increase_dict[code])
        normalized_drug_increase_series = (drug_increase_series-drug_increase_series.mean())/drug_increase_series.std()
        corr_code_dict[code] = normalized_state_to_rates_series.corr(normalized_drug_increase_series,method='pearson')
    
    state_res_dict[drug_name] = corr_code_dict

state_res_df = pd.DataFrame(state_res_dict)
# print(state_res_df)
state_res_df.to_csv('coronary_state_combined.csv')

res_dict = dict()
for drug_name in drug_names:
    drug_df = NFLIS[NFLIS['SubstanceName'] == drug_name]
    fips_dict = dict()
    for fips in fips_list:
        drug_fips_df = drug_df[drug_df['FIPS_Combined'] == fips]
        increase = drug_fips_df['DrugReports'].diff().to_numpy()
        if(len(increase) < 8): #drop unvailable data
            continue
        increase = increase[1:] # get rid of NaN
        disease_rate = fips_to_rates[fips]
        drug_increase_series = pd.Series(increase)
        normalized_drug_increase_series = (drug_increase_series-drug_increase_series.mean())/drug_increase_series.std()
        disease_rate_series = pd.Series(disease_rate)
        normalized_disease_rate_series = (disease_rate_series-disease_rate_series.mean())/disease_rate_series.std()
        corr = normalized_drug_increase_series.corr(normalized_disease_rate_series, method='pearson')
        # print(corr)
        fips_dict[fips] = corr
    res_dict[drug_name] = fips_dict

result_df = pd.DataFrame(res_dict)

state_mean_dict = dict()
fips_state_dict= {21:'KY', 39:'OH', 42:'PA',51:'VA', 54:'WV'}

for drug_name in drug_names:
    state_dict = dict()
    fips_dict = res_dict[drug_name]
    fips = fips_dict.keys()
    ky_fips = [key for key in fips_dict.keys() if 20999 <key and key < 22000 ]
    oh_fips = [key for key in fips_dict.keys() if 38999 <key and key < 40000 ]
    pa_fips = [key for key in fips_dict.keys() if 41999 <key and key < 43000 ]
    va_fips = [key for key in fips_dict.keys() if 50999 <key and key < 52000 ]
    wv_fips = [key for key in fips_dict.keys() if 53999 <key and key < 55000 ]

    if ky_fips:
        state_dict['KY'] = mean([fips_dict[key] for key in ky_fips])
    if oh_fips:
        state_dict['OH'] = mean([fips_dict[key] for key in oh_fips])
    if pa_fips:
        state_dict['PA'] = mean([fips_dict[key] for key in pa_fips])
    if va_fips:
        state_dict['VA'] = mean([fips_dict[key] for key in va_fips])
    if wv_fips:
        state_dict['WV'] = mean([fips_dict[key] for key in wv_fips])

    state_mean_dict[drug_name] = state_dict

state_mean_df = pd.DataFrame(state_mean_dict)
# print(state_mean_df)
state_mean_df.to_csv('coronary_state_mean.csv')