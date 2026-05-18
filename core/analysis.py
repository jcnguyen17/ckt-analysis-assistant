# analysis functions of the data
# data will be from excel
# convert to pandas dataframe
# get json from main.py
# run analysis on dataframe

import pandas as pd
from core.config import DATA_DIR
from typing import Dict, List







def apply_filters(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """ Applies the filter to the dataframe"""

    # create a mask from a series that selects all rows
    mask = pd.Series(True, index=df.index)

    # Loop through the filters, convert the column, operator, and value into a condition and combined with the mask
    for f in filters:
        column = f["column"]
        operator = f["operator"]
        value = f["value"]

        if operator == "equals":
            condition = df[column] == value
        elif operator == "not_equals":
            condition = df[column] != value
        elif operator == "in":
            condition = df[column].isin(value)
        else:
            raise ValueError(f"Unsupported Operator {operator}")
        
        mask = mask & condition
    
    return df[mask]


def apply_aggregation(filtered_df: pd.DataFrame, metric_column: str, aggregation: str, group_by: List[str]) -> pd.DataFrame:
    """Applies the aggregation to the filtered dataframe
    
    """
    if group_by:
        return filtered_df.groupby(group_by, dropna=False).agg(avg_score=(metric_column, aggregation)).reset_index()
    # if no group by, its just a single metric, but still return it as a dataframe
    else: 
        result = filtered_df[metric_column].agg(aggregation)
        return pd.DataFrame[{
            "metric": [metric_column],
            "aggregation": [aggregation],
            "result": [result]
        }]
    


#TODO: choose dataset, currently fixed to
def execute_analysis(analysis_plan: Dict) -> pd.DataFrame:
    ''' Applies the analysis plan (filtering, group by, and aggregation) to the dataframe
    '''
    
    DATA_FILE = f"{DATA_DIR}\\ {analysis_plan["dataset"]}.csv"
    DATA_FILE = DATA_DIR / f"{analysis_plan["dataset"]}.csv"

    df = pd.read_csv(DATA_FILE)

    filtered_df = apply_filters(df, analysis_plan["filters"])

    return apply_aggregation(filtered_df, analysis_plan["metric_column"], analysis_plan["aggregation"], analysis_plan["group_by"])


def select_x_y_correlation(analysis_plan: Dict) -> pd.DataFrame:
    '''Selects the X Variable (independent variable) and Y variable (dependent variable) for correlation analysis'''
    