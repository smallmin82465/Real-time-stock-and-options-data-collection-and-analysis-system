import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error

df = pd.read_csv(r'\testdata.csv')

new_df = df[['Close', 'Black_Scholes_Value', 'Time_to_Expiration_Day']]
results = []

# calculate RMSRE, RMSE, R^2 for each Time_to_Expiration_Day
for day in new_df['Time_to_Expiration_Day'].unique():
    subset = new_df[new_df['Time_to_Expiration_Day'] == day]
    subset = subset.dropna()
    # make sure there are enough data
    if len(subset) > 1:
        # calculate relative residuals
        relative_residuals = (subset['Close'] - subset['Black_Scholes_Value']) / subset['Close']
        
        # calculate RMSRE
        rmsre = np.sqrt(np.mean(relative_residuals**2))
        
        # calculate RMSE
        rmse = np.sqrt(mean_squared_error(subset['Close'], subset['Black_Scholes_Value']))
        
        # calculate R^2
        r2 = r2_score(subset['Close'], subset['Black_Scholes_Value'])
        
        # add results to the list
        results.append({'Time_to_Expiration_Day': day, 'RMSRE': rmsre, 'RMSE': rmse, 'R^2': r2})

# turning results into a DataFrame
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by='Time_to_Expiration_Day')

results_df['Expiration_Category'] = pd.cut(results_df['Time_to_Expiration_Day'],
                                   bins=[0, 1, 7, 30, 90, 180, 365],
                                   labels=['1天內到期', '1-7天到期', '7-30天到期', '30-90天到期', '90-180天到期', '180-365天到期'])

# change RMSRE to percentage
results_df['RMSRE'] = results_df['RMSRE'] * 100

# change R^2 to percentage
results_df['R^2'] = results_df['R^2'] * 100

final_df = results_df.groupby('Expiration_Category').mean()

# delete Time_to_Expiration_Day
final_df = final_df.drop(columns='Time_to_Expiration_Day')

# save result
final_df.to_excel(r'E:\Black_scholes_result_mean.xlsx')