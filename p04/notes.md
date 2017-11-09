
# Part 4 -

# 04.1 - Crosstabs and pivot tables
## Crosstab - counting occurances
convenient way to count occurances of one column value or index with respect to another.
`pd.crosstab(df['column list'],df['row list'], margin=False)`

when margin=True we get a new column and row that contains count of all

## Pivot table - generalising to more than counting
Can be used to aggregate data over a DF over a heirarchy of coulmns in a user controlled manner
`df.pivot_table(index=['column'], aggfunc=aFunc)`

##