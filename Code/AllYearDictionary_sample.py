import pandas as pd

#this code provides a sample of how 'Allyeardic' looks like
base_path = "C:/"
base_filename = "OPopweighted_{}_ReadytoUse.txt"
years = range(2005, 2019)  # From2005to2018

flow_dfs = {}
flow_dicts = {}
Allyeardict = {}

for year in years:
    # Read the CSV files
    flow_dfs[year] = pd.read_csv(base_path + base_filename.format(year), sep='\s+')
    # Convert dataframe to a dictionary
    temp_dict = dict(zip(zip(flow_dfs[year]['O'], flow_dfs[year]['D']), flow_dfs[year]['Flow']))
    # Remove 'L' character and parse back to a dictionary
    temp_str = str(temp_dict).replace('L', '')
    temp_dict_cleaned = eval(temp_str)
    # Update dictionary for the specific year with the new structure
    flow_dicts[year] = {(k[0], k[1], year): [v] for k, v in temp_dict_cleaned.items()}
    # Update the cumulative dictionary across all years
    Allyeardict.update(flow_dicts[year])

# Change Dictionary to DataFrame
df = pd.DataFrame.from_dict(Allyeardict, orient='index', columns=['Flow'])
df.reset_index(inplace=True)
df[['O', 'D', 'Year']] = pd.DataFrame(df['index'].tolist(), index=df.index)
df.drop('index', axis=1, inplace=True)

# Export as .csv file
df.to_csv('yourpath/Allyeardict.csv', index=False)



import pandas as pd

# 读取CSV文件
df = pd.read_csv('Allyeardict.csv')

# 将DataFrame转换回字典
# 假设原始字典的键是由'O', 'D', 'Year'组成的元组，值是'Flow'
Allyeardict_reconstructed = {(row['O'], row['D'], row['Year']): row['Flow'] for index, row in df.iterrows()}
