# Data analysis and prediction of weather data

The analysis is based on the **weather status** of Athens back in 2017. Based on the analysis and the real data, it is possible to extract the weather characteristics of that year (i.g., temperature, rain status, wind speed etc) and also to **predict** the temperature for specific date the next year.

# Installation & run project
These are the packages used in the analysis:
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

```bash
git clone https://github.com/askandali/weather-data-analysis.git
cd weather-data-analysis
```

```python
pip install numpy pandas matplotlib
python weather_analysis.py
```

> To see all generated plots, set `with_plots=True` in the `main()` function

# Data

The file **weather_data.csv** consists of 364 observations, representing the days of the whole year. The columns of the data frame give us information about:

-  The average, low and high temperature of a day.
-  The rain status.
- The wind speed and its direction.
- The date, time and month of the current day.

## Methods

- For the analysis it was created a function that executes **cubic interpolation** in order to fill some of the NA values.
```
def cubic_interpolate(dataframe, colname):
    for i, value in dataframe[colname].items():
        if np.isnan(value):
            dataframe[colname][i] = dataframe[colname][(i - 3):(i + 4)].interpolate(method='cubic')[i]
```
- Also except for the descriptive statistics, a function that checks the **rain status** of year was featured.
```
def rain_status(sum_rain):
    if sum_rain < 400:
        print('Lack of rain')
    elif 400 <= sum_rain < 600:
        print('Satisfactory amount of rain')
    else:
        print('Excessive rainfall')
```

- Furthermore, a **linear regression model** was used to predict the temperature of the following year.

> To visualize some of the results of the study, **pie chart**, **histogram** and **line charts** were used.


## Results & Visualization

```
> The median of average temperature is: 16.8

> The std of average temperature is: 7.41542197484

> The 4 of the highest temperature are:
HIGH
37.4    16:20
40.1    13:40
41.7    16:30
42.1    16:40

> Most times the wind was: North    103 times

> Max wind speed caused: 64.4mph

> The avg temperature predicted is: 9.56919357 celcius

> Rain status: Excessive rainfall

```

![Average rain monthly plot](https://github.com/askandali/weather-data-analysis/blob/main/plots/avg_rain_monthly.png)

![Pie wind direction plot](https://github.com/askandali/weather-data-analysis/blob/main/plots/pie_wind_direction.png)

![Temperature per season plot](https://github.com/askandali/weather-data-analysis/blob/main/plots/temp_per_season.png)
