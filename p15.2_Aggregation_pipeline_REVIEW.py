# set up the pipeline to match 30+ accidents
# group by speed limit and accident severity
pipeline = [{'$match': {'Speed_limit': {'$gte': 30}}},
            {'$group': {'_id': {'Speed_limit': '$Speed_limit', 'Accident_Severity': '$Accident_Severity'},
                        'num_accidents': {'$sum': 1}}}]
results = list(accidents.aggregate(pipeline))

# convert the results into a dict
results_long_df = pd.DataFrame([
    {'Accident_Severity': r['_id']['Accident_Severity'], 'Speed_limit': r['_id']['Speed_limit'], 'num_accidents': r['num_accidents']}
    for r in results
])

# reshape and relabel the dataframe
results_df = pd.pivot(index=results_long_df['Speed_limit'],
                      columns=results_long_df['Accident_Severity'],
                      values=results_long_df['num_accidents'])

# relabel the columns
results_df.columns = [label_of['Accident_Severity', c] for c in results_df.columns]
results_df


# Helper function
def results_to_table(results, index_name, column_name, results_name,
                     fillna=None,
                     relabel_index=False, relabel_columns=False,
                     index_label=None, column_label=None):

    # move items in dicts-of-dicts to the top level
    def flatten(d):
        new_d = {}
        for k in d:
            if isinstance(d[k], dict):
                new_d.update(flatten(d[k]))
            else:
                new_d[k] = d[k]
        return new_d

    df = pd.DataFrame([flatten[r] for r in results])
    df = df.pivot(index=index_name, columns=column_name, values=results_name)

    # optionally change the names and labels for presentation
    if not fillna is None:
        df.fillna(fillna, inplace=True)
    if relabel_columns:
        df.columns = [label_of[column_name, c] for c in df.columns]
    if relabel_index:
        df.index = [label_of[index_name, r] for r in df.index]
    if column_label:
        df.columns.name = column_label
    else:
        df.columns.name = column_name
    if index_label:
        df.index.name = index_label
    else:
        df.index.name = index_name

    return df
