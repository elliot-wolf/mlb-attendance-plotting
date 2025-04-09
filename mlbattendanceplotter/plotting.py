import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from .processing import variable_dict, team_abb_dict, process_yearly, process_daily, group_attendance_by_time, load_data



games, weather, census = load_data()


def bar_attendance_by_time(by = "month" , team = "BOS", year = None, show_league_avg = False, attendance = "%"):
    """
    Plots a bar chart of average team attendance grouped by a time measurement of the user's choice.

    This function automatically loads and processes attendance data when called. The generated bar plot is a
        reflection of the user's desired time measure (by), team(s), year(s), and attendance measure. The user can
        also choose to add a 'league average' marker.
    Parameters:
        by (str): Time measurement to group by. Select one of the following:
                - 'start time': Game start time (Day/Night)
                - 'weekday': Day of the week
                - 'month' (default): Month (March/April, September/October are grouped together)
                - 'year': A year between 2012-2019.
        team (str): Team's abbreviation. Print team_abb_dict to see a list of team abbreviations. If no team is
                        selected, 'BOS' is the default.
        year (int): A year between the range 2012-2019. If None, all years are plotted.
        show_league_avg (bool): If True, a red marker indicates league average attendance numbers. Defaults to False.
        attendance (str): Determines whether attendance is measured as a raw number or as a percentage of the team's
                            stadium's capacity. Select one of the following:
                            - 'raw': Total attendance
                            - '%': Attendance as a percentage of stadium capacity (Default)
    Returns a plot with the desired arguments.
    """
    load_data()
    if not isinstance(team, str) and team is not None:
        print("Please enter one team abbreviation as a string. Print team_abb_dict to see a list of team abbrevations.")
        return

    if attendance == "%":
        attendance_measure = "attendance%"
    elif attendance == "raw":
        attendance_measure = "attendance"

    df = process_daily(games, weather, team=team, year=year)
    time_df = group_attendance_by_time(df, by, attendance_measure)

    if show_league_avg:
        league_df = process_daily(games, weather, team=None, year=year)
        league_avg_df = group_attendance_by_time(league_df, by, attendance_measure)


    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=time_df, x='time_measure', y=attendance_measure)

    if show_league_avg:
        x = range(len(league_avg_df))
        y = league_avg_df[attendance_measure].values
        ax.plot(x, y, '-o', color='red', label = 'League Average', zorder = 5, markersize = 10)
        ax.legend()
    if year is None:
        year = "2012-2019"
    x_lab = variable_dict.get(by, by.title())
    if attendance == "%":
        y_lab = variable_dict.get('attendance%', 'Stadium Capacity Filled (%)')
        plt.ylim(0, 100)
    elif attendance == "raw":
        y_lab = variable_dict.get('attendance', 'Attendance (Raw)')
    plt.title(f'Average {y_lab} by {x_lab} ({team}, {year})')
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.show()


def bar_by_team(y, year = None):
    """
    Plots a bar chart for the selected y variable as an average and selected year (or all years),
        where each MLB team is assigned a bar.

    This function processes yearly averages for each team, and can plot variables relating to attendance/game data,
        weather data, and census data. The user can opt to plot a certain year or an average of all years within
        the 2012-2019 range.

    Parameters:
        y (str): The user's desired variable to plot. Select one of the following:
            - attendance (int): Raw Average Attendance (Baseball Reference)
            - attendance% (float): Average Stadium Capacity Filled (%) (Baseball Reference & Seamheads)
            - win_pct (float): Team Win Percentage (%) (Baseball Reference)
            - opp_win_pct (float): Opponent's Team Win Percentage (%) (Baseball Reference)
            - tavg (float): Average Daily Temperature (°F) (Meteostat)
            - prcp (float): Average Daily Precipitation (in) (Meteostat)
            - population (int): City Population (Census)
            - median_age (float): City Median Age (Census)
            - median_household_income (float): Median HouseHold Income (Census)
            - average_household_size (float): Average Household Size (Census)
            - pct_public_transit (float): % of People who Commute to Work via Public Transit (Census)
            - pct_car (float): % of People who Commute to Work via Car (Census)
            - pct_walk (float): % of People who Commute to Work via Walking (Census)
            - poverty_rate (float): Poverty Rate (%) (Census)
            - payroll_est (int): Estimated Team Payroll ($) (Baseball Reference)
        year (int): A year between the range 2012-2019. If None, all years are plotted.
    """
    load_data()

    df = process_yearly(games, weather, census, year=year)

    df = df.groupby('team')[y].mean().reset_index()
    df = df.sort_values(y, ascending=False)
    if year is None:
        year = "2012-2019"

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x='team', y=y)

    y_lab = variable_dict.get(y, y.title())
    plt.title(f'{y_lab} by Team ({year})')
    plt.xlabel("Team")
    plt.ylabel(y_lab)

    plt.xticks(rotation=45)
    plt.show()

def scatter_daily(x, y, team=None, year=None, lobf = False, show_prcp = False):
    """
    Create a scatterplot with daily data for a given team(s) and year(s). For the best interpretation, select a
    single team and a single year, although a list of teams and years are accepted as well.

    This function generates a scatterplot of the user's specified (x,y) using game/attendance and weather data.
    Census data cannot be plotted on the daily level. While the function can take on a list of teams and years, it
    is ideal to input a single team and year. The user can opt to display either a simple line of best fit or add
    color using precipitation, but not both at the same time.

    Parameters:
        x (str): The user's desired x-axis variable to plot.
        y (str): The user's desired y-axis variable to plot.
            x, y variables to select from:
            - win_pct (float): Team Win Percentage (%) (Baseball Reference)
            - attendance (int): Raw Average Attendance (Baseball Reference)
            - attendance% (float): Average Stadium Capacity Filled (%) (Baseball Reference & Seamheads)
            - num_home_game (int): Number Home Game of the Season (81 per year)
            - opp_win_pct (float): Opponent's Team Win Percentage (%) (Baseball Reference)
            - cli (float): Championship Leverage Index (Baseball Reference's measure for a game's 'significance')
            - tavg (float): Average Daily Temperature (°F) (Meteostat)
            - tmin (float): Minimum Daily Temperature (°F) (Meteostat)
            - tmax (float): Maximum Daily Temperature (°F) (Meteostat)
            - prcp (float): Average Daily Precipitation (in) (Meteostat)
        team (str): Team's abbreviation. Print team_abb_dict to see a list of team abbreviations. If no team is
                        selected, all teams are plotted.
        year (int): Year of interest. Defaults to None (selects all years 2012-2019).
        lobf (bool): If True, simple Seaborn line of best fit is generated. By default, no line is plotted.
        show_prcp (bool): If True, color is added to represent precipitation categories. False by default.
        *** Please note that lobf and show_prcp cannot both be True at the same time ***

    """
    load_data()
    df = process_daily(games, weather, team=team, year=year)

    def group_rain(prcp):
        if prcp < 0.1:
            return '0 - 0.1'
        elif prcp < 0.3:
            return '0.1 - 0.3'
        else:
            return '0.3+'

    if show_prcp:
        df["group_rain"] = df['prcp'].apply(group_rain)

    # Plotting setup
    plt.figure(figsize=(8, 5))

    if lobf and show_prcp:
        raise ValueError("Cannot show line of best fit and precipitation at the same time. Either set lobf or show_prcp to True, not both.")

    if lobf:
        sns.regplot(data=df, x=x, y=y, scatter = True, ci = 95, line_kws={'color': 'red'})
    else:
        if show_prcp:
            sns.scatterplot(data=df, x=x, y=y, hue = 'group_rain')
        else:
            sns.scatterplot(data=df, x=x, y=y)

    if show_prcp:
        plt.legend(title = "Precipitation (in.)")

    x_lab = variable_dict.get(x, x.title())
    y_lab = variable_dict.get(y, y)

    plt.title(f' {x_lab} vs. {y_lab}')
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.show()



# - opp_win_pct(float)
# - tavg(float)
# - prcp(float)
# - population(int)
# - median_age(float)
# - median_household_income(float)
# - average_household_size(float)
# - pct_public_transit(float)
# - pct_car(float)
# - pct_walk(float)
# - poverty_rate(float)
# - payroll_est(int)

def scatter_yearly(x, y, team=None, year=None, lobf = False):
    """
    Create a scatterplot with yearly data for a given team(s) and year(s). For the best interpretation, select a
    single team and a single year, although a list of teams and years are accepted as well.

    This function generates a scatterplot of the user's specified (x,y) using game/attendance, weather, and census data.
    The function is best used for exploring broad yearly trends across teams, years, etc. The user can opt to
    insert a simple line of best fit for their chosen x and y variables.

    Parameters:
        x (str): The user's desired x-axis variable to plot.
        y (str): The user's desired y-axis variable to plot.
            x, y variables to select from:
            - attendance (int): Raw Average Attendance (Baseball Reference)
            - attendance% (float): Average Stadium Capacity Filled (%) (Baseball Reference & Seamheads)
            - win_pct (float): Team Win Percentage (%) (Baseball Reference)
            - opp_win_pct (float): Opponent's Team Win Percentage (%) (Baseball Reference)
            - tavg (float): Average Daily Temperature (°F) (Meteostat)
            - prcp (float): Average Daily Precipitation (in) (Meteostat)
            - population (int): City Population (Census)
            - median_age (float): City Median Age (Census)
            - median_household_income (float): Median HouseHold Income (Census)
            - average_household_size (float): Average Household Size (Census)
            - pct_public_transit (float): % of People who Commute to Work via Public Transit (Census)
            - pct_car (float): % of People who Commute to Work via Car (Census)
            - pct_walk (float): % of People who Commute to Work via Walking (Census)
            - poverty_rate (float): Poverty Rate (%) (Census)
            - payroll_est (int): Estimated Team Payroll ($) (Baseball Reference)
        team (str or list): One or more team abbreviations. If None, all teams are plotted.
        year (int or list): One of more years to plot. If None, all years (2012-2019) are plotted.
        lobf (bool): If True, simple Seaborn line of best fit is generated. By default, no line is plotted.
    """
    load_data()
    df = process_yearly(games, weather, census, team=team, year=year)

    # Plotting setup
    plt.figure(figsize=(8, 5))
    if lobf:
        sns.regplot(data=df, x=x, y=y, scatter = True, ci = 95, line_kws={'color': 'red'})
    else:
        sns.scatterplot(data=df, x=x, y=y)

    x_lab = variable_dict.get(x, x.title())
    y_lab = variable_dict.get(y, y)

    plt.title(f' {x_lab} vs. {y_lab}')
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.show()


#scatter_3d(x = "win_pct", y = "payroll_est", z = "attendance%", team = None, year = None, time = "yearly")
def scatter_3d(x='win_pct', y='payroll_est', z='attendance%', team=None, year=None, time = "daily"):
    """
    Create a 3D scatterplot using daily or yearly data.

    This function generates a 3D scatterplot of a user's choice of x, y, and z. Available data depends on the user's
    choice of the 'time' argument. Census data can only be plotted when time is on a yearly basis, not daily.

    Parameters:
        x (str): The user's desired x-axis variable to plot (Default x = 'win_pct').
        y (str): The user's desired y-axis variable to plot. (Default y = 'payroll_est').
        z (str): The user's desired z-axis variable to plot. (Default z = 'attendance%').
            See 'time' parameter for a list of variables that are able to be plotted for each 'time' argument.
        team (str or list): One or more team abbreviations. If None, all teams are plotted.
        year (int or list): One of more years to plot. If None, all years (2012-2019) are plotted.
        time (str): Two options: 'daily' and 'yearly' (Default time = 'daily').
            If time = 'daily', select x,y,z from the following:
                - win_pct (float): Team Win Percentage (%) (Baseball Reference)
                - attendance (int): Raw Average Attendance (Baseball Reference)
                - attendance% (float): Average Stadium Capacity Filled (%) (Baseball Reference & Seamheads)
                - num_home_game (int): Number Home Game of the Season (81 per year)
                - opp_win_pct (float): Opponent's Team Win Percentage (%) (Baseball Reference)
                - cli (float): Championship Leverage Index (Baseball Reference's measure for a game's 'significance')
                - tavg (float): Average Daily Temperature (°F) (Meteostat)
                - tmin (float): Minimum Daily Temperature (°F) (Meteostat)
                - tmax (float): Maximum Daily Temperature (°F) (Meteostat)
                - prcp (float): Average Daily Precipitation (in) (Meteostat)
            If time = 'yearly', select x,y,z from the following:
                - attendance (int): Raw Average Attendance (Baseball Reference)
                - attendance% (float): Average Stadium Capacity Filled (%) (Baseball Reference & Seamheads)
                - win_pct (float): Team Win Percentage (%) (Baseball Reference)
                - opp_win_pct (float): Opponent's Team Win Percentage (%) (Baseball Reference)
                - tavg (float): Average Daily Temperature (°F) (Meteostat)
                - prcp (float): Average Daily Precipitation (in) (Meteostat)
                - population (int): City Population (Census)
                - median_age (float): City Median Age (Census)
                - median_household_income (float): Median HouseHold Income (Census)
                - average_household_size (float): Average Household Size (Census)
                - pct_public_transit (float): % of People who Commute to Work via Public Transit (Census)
                - pct_car (float): % of People who Commute to Work via Car (Census)
                - pct_walk (float): % of People who Commute to Work via Walking (Census)
                - poverty_rate (float): Poverty Rate (%) (Census)
                - payroll_est (int): Estimated Team Payroll ($) (Baseball Reference)
    """
    load_data()
    if time == "daily":
        df = process_daily(games, weather, team, year)
    elif time == "yearly":
        df = process_yearly(games, weather, census, team, year)
    else:
        raise ValueError("Please select time as daily or yearly.")

    if not all(col in df.columns for col in [x, y, z]):
        raise ValueError(f"One of: ({x}, {y}, {z}) cannot be obtained. Recall that census data can only be used on a yearly basis.")

    if team is None:
        team = "All Teams"
    if year is None:
        year = "2012-2019"

    x_lab = variable_dict.get(x, x)
    y_lab = variable_dict.get(y, y)
    z_lab = variable_dict.get(z, z)

    fig = px.scatter_3d(df, x=x, y=y, z=z,
                        title = f"3D Scatterplot: {team}, {year}, {time.title()}",
                        width = 700,
                        height = 700,
                        opacity = 0.7,
                        labels={
                            x: variable_dict.get(x, x.title()),
                            y: variable_dict.get(y, y.title()),
                            z: variable_dict.get(z, z.title())
                        })
    fig.update_traces(marker = dict(size=4))
    fig.update_layout(
        margin=dict(l=20, r=20, b=120, t=80),

        scene=dict(camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)))
    )

    fig.show()



