## Part 02 - Acquiring and representing data
Notebooks

- 02.1 Pandas DataFrames
- 02.2 Data File Formats
- 02.2.0 File encodings

  - 02.2.1 CSV
  - 02.2.2 JSON
  - 02.2.3 Other

## Part 04-  Data Analysis

- 04.1 [Crosstabs and pivot tables](#crosstabs-and-pivot-tables)
- 04.2 [Descriptive statistics in pandas](#descriptive-statistics-in-pandas)
- 04.3 [Simple visulisations in pandas](#simple-visulisations-in-pandas)
- 04.4 [Activity walkthrough](#activity-walkthrough)
- 04.5 [Split-apply-combine with SQL and pandas](#split-apply-combine-with-sql-and-pandas)
- 04.5 [SalesTeam Exploration](#salesteam-exploration)
- 04.6 [Introducing REGEX](#introducing-regex)
- 04.7 [Reshaping data with pandas](#reshaping-data-with-pandas)


## Part 04 - Data Analysis
### Crosstabs and pivot tables

#### Crosstab - counting occurances
convenient way to count occurances of one column value or index with respect to another.
  
    pd.crosstab(df['column list'],df['row list'], margin=False)

when margin=True we get a new column and row that contains count of all

#### Pivot table - generalising to more than counting
Can be used to aggregate data over a DF over a heirarchy of coulmns in a user controlled manner
    
    df.pivot_table(index=['column'], aggfunc=aFunc)

### Descriptive statistics in pandas

### Simple visulisations in pandas

### Activity walkthrough

### Split apply combine with SQL and pandas

### SalesTeam Exploration

### Introducing REGEX

### Reshaping data with pandas

