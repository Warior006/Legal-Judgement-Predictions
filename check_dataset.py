import pandas as pd

df = pd.read_excel('D:\\case_files_total.csv.xlsx', nrows=500)
print('Columns:', df.columns.tolist())
print('DataFrame shape:', df.shape)

df_valid = df.dropna(subset=['label'])
print(f'Rows with labels: {len(df_valid)} out of {len(df)}')

if len(df_valid) > 0:
    print('\nUnique labels:')
    print(df_valid['label'].value_counts())
