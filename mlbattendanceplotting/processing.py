import pandas as pd

variable_dict = {
    "date" : "Date",
    "year" : "Year",
    "team" : "Team",
    "win_pct" : "Win %",
    "attendance" : "Attendance",
    "attendance%" : "Stadium Capacity Filled (%)",
    "num_home_game" : "Home Game #",
    "opp" : "Opponent",
    "opp_win_pct" : "Opponent Win %",
    "start_time" : "Start Time (Day/Night)",
    "cli" : "Championship Leverage Index",
    "tavg" : "Average Daily Temperature (°F)",
    "tmin" : "Minimum Daily Temperature (°F)",
    "tmax" : "Maximum Daily Temperature (°F)",
    "prcp" : "Daily Precipitation (inches)",
    "city" : "City/Team",
    "population" : "Population",
    "median_age" : "Median Age",
    "median_household_income" : "Median Household Income",
    "average_household_size" : "Average Household Size",
    "pct_public_transit" : "% Commute to Work via Public Transit",
    "pct_car" : "% Commute to Work via Car",
    "pct_walk" : "% Commute to Work via Walking",
    "poverty_rate" : "Poverty Rate",
    "payroll_est" : "Estimated Team Payroll ($)"
}

team_abb_dict = {
    "ARI" : "Arizona Diamondbacks",
    "ATL" : "Atlanta Braves",
    "BAL" : "Baltimore Orioles",
    "BOS" : "Boston Red Sox",
    "CHC" : "Chicago Cubs",
    "CHW" : "Chicago White Sox",
    "CIN" : "Cincinnati Reds",
    "CLE" : "Cleveland Guardians",
    "COL" : "Colorado Rockies",
    "DET" : "Detroit Tigers",
    "HOU" : "Houston Astros",
    "KCR" : "Kansas City Royals",
    "LAA" : "Los Angeles Angels",
    "LAD" : "Los Angeles Dodgers",
    "MIA" : "Miami Marlins",
    "MIL" : "Milwaukee Brewers",
    "MIN" : "Minnesota Twins",
    "NYM" : "New York Mets",
    "NYY" : "New York Yankees",
    "OAK" : "Oakland Athletics",
    "PHI" : "Philadelphia Phillies",
    "PIT" : "Pittsburg Pirates",
    "SDP" : "San Diego Padres",
    "SEA" : "Seattle Mariners",
    "SFG" : "San Francisco Giants",
    "STL" : "St. Louis Cardinals",
    "TBR" : "Tampa Bay Rays",
    "TEX" : "Texas Rangers",
    "TOR" : "Toronto Blue Jays",
    "WSN" : "Washington Nationals",
}

def load_data():
    """
    Loads and returns necessary data from CSV files.
    Automatically called within the plotting functions. No action is required as long as the required CSV files –
        'bref_2012_2019.csv', 'weather_2012_2019.csv', and 'census_2012_2019.csv' are in the project directory.
    Returns a tuple of three Dataframes: games, weather, and census.
    """
    games = pd.read_csv('bref_2012_2019.csv')
    weather = pd.read_csv('weather_2012_2019.csv')
    census = pd.read_csv('census_2012_2019.csv')
    return games, weather, census

def process_yearly(games, weather, census, team=None, year=None):
    """
    Process and merge data from the three data sources: games, weather, and census.
    This function converts data from games and weather into yearly averages to be merged with census data which is
    collected on a yearly basis. No user action is required – this function is called within the plotting functions.
    Please note that the Toronto Blue Jays do not have census data available.
    Parameters:
        games (pd.DataFrame): Dataframe containing Baseball Reference attendance data (Attendance, Date, W-L, ...)
        weather (pd.DataFrame): Dataframe containing daily weather data for each team's city (Average Temperature,
                                    Daily Precipitation, ...)
        census (pd.DataFrame): Dataframe containing census data on a yearly basis (Population, Median Age, Methods of
                                    Commuting to Work, ...)
        team (str, list): A str of the user's team of interest. If None, data is collected for all teams.
        year (int, list): An integer of the user's year of interest. If None, data is collected for all years (2012-19).
    Returns a pd.DataFrame where each observation is a Team/Year combination with the following columns:
        - year (int)
        - team (str)
        - attendance (int)
        - attendance% (float)
        - win_pct (float)
        - opp_win_pct (float)
        - tavg (float)
        - prcp (float)
        - population (int)
        - median_age (float)
        - median_household_income (float)
        - average_household_size (float)
        - pct_public_transit (float)
        - pct_car (float)
        - pct_walk (float)
        - poverty_rate (float)
        - payroll_est (int)
    """
    # Convert daily Baseball Reference game data into group of team/year averages
    games_yearly_avg = (
        games.sort_values('date') # Should already be ordered, but sort so the last game's win_pct can be extracted easily
        .groupby(['team', 'year']) # Each observation is a team/year combo
        .agg({
            'win_pct': 'last', # Last recorded value of the season is a team's yearly win_pct
            'attendance': 'mean', # Average yearly attendance for a given team/year
            'attendance%': 'mean', # Average yearly capacity full for a given team/year
            'opp_win_pct' : 'mean' # Average opponent win % at time of game
        })
        .reset_index())

    # Convert daily Meteostat weather data into a group of team/year averages
    weather_yearly_avg = (
        weather.groupby(['team', 'year'])[['tavg', 'prcp']].mean()
        .reset_index())

    # Combine game and weather data on a team/year basis
    yearly_df = games_yearly_avg.merge(weather_yearly_avg, on=['team', 'year'], how='left')

    # Merge census data with already-merged data. Census data is already on a yearly basis
    yearly_df = yearly_df.merge(census, on=['team', 'year'], how='left')

    yearly_df = yearly_df[[
        'year', 'team', 'attendance', 'attendance%', 'win_pct', 'opp_win_pct', 'tavg', 'prcp',
        'population', 'median_age', 'median_household_income', 'average_household_size',
        'pct_public_transit', 'pct_car', 'pct_walk', 'poverty_rate', 'payroll_est'
    ]]

    # yearly_df now contains all team/year combos. If user specified team(s) or year(s), filter below:
    if team is not None: # If user specified a team or list of teams
        if isinstance(team, str): # If a single team is inputted (as a string)
            team = [team] # Put it in list format to be consistent with multiple teams being inputted
        yearly_df = yearly_df[yearly_df['team'].isin(team)] # Select user's specified list of teams

    # Repeat the same process for years
    if year is not None:
        if isinstance(year, int):
            year = [year]
        yearly_df = yearly_df[yearly_df['year'].isin(year)]

    # Round: attendance (whole number), attendance%, tavg, prcp to 1 decimal
    yearly_df['attendance'] = yearly_df['attendance'].round(0)
    yearly_df['attendance%'] = yearly_df['attendance%'].round(1)
    yearly_df['tavg'] = yearly_df['tavg'].round(1)
    yearly_df['prcp'] = yearly_df['prcp'].round(2)

    return yearly_df

def process_daily(games, weather, team=None, year=None):
    """
    Process and merge data from two data sources: games and weather.
    This function merges data from games and weather and maintains observations at the daily level. No user action
    is required – this function is called within the plotting functions.
    Parameters:
        games (pd.DataFrame): Dataframe containing Baseball Reference attendance data (Attendance, Date, W-L, ...)
        weather (pd.DataFrame): Dataframe containing daily weather data for each team's city (Average Temperature,
                                    Daily Precipitation, ...)
        team (str, list): A str of the user's team of interest. If None, data is collected for all teams.
        year (int, list): An integer of the user's year of interest. If None, data is collected for all years (2012-19).
    Returns a pd.DataFrame where each observation is a Team/Year combination with the following columns:
        - date (pd.Datetime)
        - year (int)
        - team (str)
        - win_pct (float)
        - attendance (int)
        - attendance% (float)
        - num_home_game (int)
        - opp (str)
        - opp_win_pct (float)
        - 'start_time' (str)
        - cli (float)
        - tavg (float)
        - tmin (float)
        - tmax (float)
        - prcp (float)
    """
    # Combine game and weather data on a team/year basis
    daily_df = games.merge(weather, on=['team', 'date'], how='left')

    daily_df['year'] = pd.to_datetime(daily_df['date']).dt.year

    daily_df = daily_df[['date', 'year', 'team', 'win_pct', 'attendance', 'attendance%', 'num_home_game', 'opp',
                         'opp_win_pct', 'start_time', 'cli', 'tavg', 'tmin', 'tmax', 'prcp']]

    if team is not None: # If user specified a team or list of teams
        if isinstance(team, str): # If a single team is inputted (as a string)
            team = [team] # Put it in list format to be consistent with multiple teams being inputted
        daily_df = daily_df[daily_df['team'].isin(team)] # Select user's specified list of teams

    # Repeat the same process for years
    if year is not None:
        if isinstance(year, int):
            year = [year]
        daily_df = daily_df[daily_df['year'].isin(year)]

    # Round: attendance%, tavg, tmin, tmax, prcp to 1 decimal
    daily_df['attendance%'] = daily_df['attendance%'].round(1)
    daily_df['tavg'] = daily_df['tavg'].round(1)
    daily_df['tmin'] = daily_df['tmin'].round(1)
    daily_df['tmax'] = daily_df['tmax'].round(1)
    daily_df['prcp'] = daily_df['prcp'].round(2)

    return daily_df

def group_attendance_by_time(df, by, attendance = 'attendance%'):
    """
    This function is called within plotting functions and groups attendance by a certain time unit (game start time,
        weekday, month, year), and then returns measurement averages based on the selected time measurement.
    Parameters:
        df (pd.DataFrame): Dataframe that has already been processed.
        by (str): Time measurement: 'start time', 'weekday', 'month', 'year'.
        attendance (str): Either raw attendance count ('attendance') or as
                            a percentage of stadium capacity ('attendance%')
    Returns a Dataframe containing measurements that were grouped and averaged by the selected 'by' method.
    """
    by = by.lower()

    if by == "start time":
        df['time_measure'] = df['start_time']
        time_df = df.groupby('time_measure')[attendance].mean().reset_index()
        return time_df

    elif by == "weekday":
        df['date'] = pd.to_datetime(df['date'])
        df['weekday_int'] = df['date'].dt.weekday
        weekday_dict = {
            0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
            4: 'Friday', 5: 'Saturday', 6: 'Sunday'
        }
        df['time_measure'] = df['weekday_int'].map(weekday_dict)
        time_df = df.groupby(['weekday_int', 'time_measure'])[attendance].mean().reset_index()
        return time_df.sort_values('weekday_int')

    elif by == "month":
        df['date'] = pd.to_datetime(df['date'])
        df['month_int'] = df['date'].dt.month

        # Group March/April, September/October together. Not many regular season games played in March, October
        def group_months(i):
            if i in [3, 4]:
                return 'March/April'
            elif i == 5:
                return 'May'
            elif i == 6:
                return 'June'
            elif i == 7:
                return 'July'
            elif i == 8:
                return 'August'
            elif i in [9, 10]:
                return 'September/October'
            elif i == 11:
                return 'November'

        df['time_measure'] = df['month_int'].map(group_months)

        monthly_order = ['March/April', 'May', 'June', 'July', 'August', 'September/October']

        time_df = (df[df['time_measure'].isin(monthly_order)]
            .groupby('time_measure')[attendance].mean()
                   .reindex(monthly_order)
                   .reset_index())
        return time_df

    elif by == "year":
        df['time_measure'] = df['year']
        return df.groupby('time_measure')[attendance].mean().reset_index()

    else:
        raise ValueError("Invalid argument for 'by'. Valid arguments are 'start time', 'weekly', 'monthly', 'yearly'.")


