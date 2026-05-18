from typing import List, Literal
from pydantic import BaseModel, Field


class FilterCondition(BaseModel):
    """ Schema for the LLM/Agent's response describing filters to be used in the analysis plan"""
    column: str = Field(description="The dataset column to filter")
    operator: Literal["equals", "not_equals", "in"] = Field(description="The comparison operator for the filter")
    value: str | int | float | list[str] = Field(
        description="The values to filter the column by"
    )

class AnalysisPlan(BaseModel): 
    """ Schema for the LLM/Agent's response describing the analysis plan """

    dataset: str = Field(description="The data set / data source table that should be used for analysis")
    analysis_type: Literal["average_by_group", "distribution_by_group", "correlation"] = Field(
        description="The type of analysis to perform"
    )
    x_variable: str = Field(
        description="The independent variable, predictor variable, or explanatory variable (usually plotted on the horizontal axis).",
        default=None)
    y_variable: str = Field(
        description="The dependent variable, outcome variable, or response variable (usually plotted on the vertical axis).",
        default=None)
    metric_column: str = Field(description="The numerical value to be aggregated e.g. exam scores")
    aggregation: Literal["mean", "sum", "min", "max", "count"] = Field(
        description="The aggregation to apply to the metric column when doing average by group")
    group_by: List[str] = Field(
        default_factory=list,
        description="The columns used to split the result into groups such as gender, program name, study mode")
    filters: List[FilterCondition] = Field(
        default_factory=list,
        description="Conditions to filter/restrict rows before calculting the result")
    clarification_required: bool = Field(
        default=False,
        description="Whether the user query is too ambigious to create a valid plan")
    clarification_question: str = Field(
        default=None,
        description="Question to ask user if clarification needed is true, otherwise null")    


class ChartSpec(BaseModel):
    """ Chart specification  """

    chart_type: Literal["metric", "bar", "line", "scatter", "table"] = Field(
        description="The type of chart to display")
    title: str = Field(description="The tite of the chart")

    x: str | None = None
    y: str | None = None

    x_label: str | None = None
    y_label: str | None = None
