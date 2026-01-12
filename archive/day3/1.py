import pandas as pd
import numpy as np
import statsmodels.api as sm

np.random.seed(42)
n_samples = 1000

data = pd.DataFrame({
    'education_years' : np.random.choice([12,16],n_samples,p=[0.3,0.7]),
    'experience_years' : np.random.randint(0,40,n_samples),
})

data['hire_year'] = 2024 - data['experience_years']

def is_ice_age(year):
    if 1994 <= year <= 2003:
      return 1
    else:
      return 0

data['ice_age_dummy'] = data['hire_year'].apply(is_ice_age)

data['wage'] = (
    200
    + 15 * data['education_years']
    + 5 * data['experience_years']
    - 0.05 * (data['experience_years']** 2)
    - 30 * data['ice_age_dummy']
    + np.random.normal(0,50,n_samples)
)

X = [['education_years','experience_years','ice_age_dummy']]
X['experienced_squared'] = X['experienced_years'] ** 2
X = sm.add_constant(X)

y = data['wage']

model = sm.OLS(y,X).fit()

print(model.summary)