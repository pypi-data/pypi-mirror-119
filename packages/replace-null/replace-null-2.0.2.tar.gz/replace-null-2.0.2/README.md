## Contents
This module help you to perform basic machine learning operations. Like replace null values, generate statsmodel summary etc.

###### Replace null value with mean, mode or median of that specific feature.
```sh
  from replace_null import ReplaceNull
  ReplaceNull.replace_by_mean(data_frame)
  ```
###### Note: This is only for numeric features.

###### Generate stats summary.
```sh
  from stats_models import StateModels
  StateModels.generate_summary(data_frame=df, x=['TV', 'Newspaper'], y='Sales')
  ```