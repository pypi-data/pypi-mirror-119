# PovertyScale

Poverty scale, updated approximately on an annual basis, to use for calculating
income eligibility in the United States.

See example and demo in demo_poverty_scale.yml

This package contains a JSON file, poverty.json, which can be referenced directly,
as well as a module poverty.py which exports `poverty_scale_income_qualifies`

```python
def poverty_scale_income_qualifies(total_monthly_income:float, household_size:int=1, multiplier:int=1)->Union[bool,None]:
  """
  Given monthly income, household size, and an optional multiplier, return whether an individual
  is at or below the federal poverty level.
  
  Returns None if the poverty level data JSON could not be loaded.
  """
  
def poverty_scale_get_income_limit(household_size:int=1, multiplier:int=1)->Union[int, None]:
  """
  Return the income limit matching the given household size.
  """
  
```