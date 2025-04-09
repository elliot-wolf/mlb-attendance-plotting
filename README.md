# About

# Repository Organization
mlb-attendance-plotting/ ├── mlbattendanceplotter/ # Main package directory │ ├── data/ # Folder containing input CSV files │ │ ├── bref_2012_2019.csv │ │ ├── weather_2012_2019.csv │ │ ├── census_2012_2019.csv │ │ └── stadium_data.csv │ ├── init.py │ ├── plotting.py # Plotting functions │ └── processing.py # Data loading and preprocessing ├── tests/ # Pytest test cases │ └── test_plotting.py ├── setup.py # Package installation script ├── README.md # Project documentation └── .gitignore

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




