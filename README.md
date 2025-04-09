# About

This project was designed with the goal of allowing the user to easily plot attendance trends across the MLB from 2012 to 2019. Three data sources are considered when examining trends: game data (taken from Baseball Reference), weather data (Meteostat), and census data (US Census). There are a wide range of explanations as to why attendance might fluctuate around the league, or why a specific team might see year-to-year changes in attendance. This package aims to explain attendance trends through multiple lenses, and the user is encouraged to see how various factors may be influencing attendance numbers behind the scenes. 

# Repository Organization

>
    .
    ├── mlbattendanceplotter
    │   ├── __init__.py                    # Initialization
    │   ├── plotting.py         
    │   └── processing.py  
    │   └── data 
    │           ├── bref_2012_2019.csv          
    │           ├── census_2012_2019.csv 
    │           ├── weather_2012_2019.csv 
    │           └── stadium_data.csv               
    ├── tests                             # Test files 
    │   ├── test_plotting.py          
    │   ├── test_processing.py         
    │   └── unit                
    ├── processing-notebooks              # Used for data cleaning. Not necessary for the user
    │   ├── clean_census_data.ipynb       
    │   ├── clean_gamedata.ipynb         
    │   └── clean_weather_data.ipynb                
    └── README.md
    └── setup.py
>


# Package Requirements
This package relies on the following packages:
- pandas
- matplotlib
- seaborn
- plotly

These packages are automatically installed if the installation instructions are followed properly.


# Package Installation
1. Clone the repo
   ```sh
   git clone https://github.com/elliot-wolf/mlb-attendance-plotting.git
   cd mlb-attendance-plotting
   ```

2. Install the package and dependencies
   ```sh
   pip install .
   ``` 

3. Import necessary functions
   ```sh
   from mlbattendanceplotter.processing import *
   from mlbattendanceplotter.plotting import *
   ``` 





# Example Use

## bar_attendance_by_time()
```sh
from mlbattendanceplotter.plotting import bar_attendance_by_time

bar_attendance_by_time(by = "month", team = "BOS", year = 2018, show_league_avg=True, attendance="raw")
```

```sh
from mlbattendanceplotter.plotting import bar_attendance_by_time

bar_attendance_by_time(by = "weekday", team = "ATL", year = 2018, show_league_avg=True, attendance="%")
```


## bar_by_team()
```sh
from mlbattendanceplotter.plotting import bar_by_team

bar_by_team(y = "attendance%", year = 2013)
```

## scatter_daily()
```sh
from mlbattendanceplotter.plotting import scatter_daily

scatter_daily(x = "tavg", y = "attendance", team = "NYY", year = 2018, lobf = True)
```

## scatter_yearly()
```sh
from mlbattendanceplotter.plotting import scatter_yearly

scatter_yearly(x="payroll_est", y = "win_pct", team = None, year = None, lobf=True)
```

```sh
from mlbattendanceplotter.plotting import scatter_yearly

scatter_yearly(x="pct_walk", y = "attendance%", team = None, year = 2018, lobf=True)
```

## scatter_3d()
```sh
from mlbattendanceplotter.plotting import scatter_3d

scatter_3d(x = "win_pct", y = "payroll_est", z = "attendance%", team = None, year = None, time = "yearly")
```




# Credits/Citations
