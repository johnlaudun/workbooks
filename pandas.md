# PANDAS

## Filters

`males = df[(df[Gender] == 'Male' & (df[Year] == 2014))]`

View a column: `df['name']` or, possibly: df.name

View 2 columns: `df[['name', 'reports']]` passing a list

View first 2 rows: `df[:2]`

View all rows where value > 50: `df[df['value'] > 50 ]`

View a row: `df.ix`['Maricopa']

View a column: `df.ix[:, 'column']`

View a cell based on row and column: `df.ix['rowid', 'column']
