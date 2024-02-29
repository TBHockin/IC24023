import pandas as pd

d1 = {'A': [1, 1, 1, 2], 'B': [2, 2, 2, 3], 'C': [3, 3, 4, 5]}
source_df = pd.DataFrame(d1)

print('Source DataFrame:\n', source_df)

result_df = source_df.drop_duplicates(subset=['A','B'])
print('Result DataFrame:\n', result_df)