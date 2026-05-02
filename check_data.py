import pandas as pd
df = pd.read_parquet(r'e:\CUFE\Spring_25\Big Data\Project\outputs\parquet\features')
print('Cols with user:', [c for c in df.columns if 'user' in c.lower()])
print('userRatingCount stats:')
print(df['userRatingCount'].describe())
print(f"\nRows with userRatingCount > 0: {(df['userRatingCount'] > 0).sum()}")
print(f"Total rows: {len(df)}")
