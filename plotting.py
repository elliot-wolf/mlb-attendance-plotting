import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from processing import variable_dict, process_yearly, process_daily, group_attendance_by_time


games = pd.read_csv('bref_2012_2019.csv')
census = pd.read_csv('census_2012_2019.csv')
weather = pd.read_csv('weather_2012_2019.csv')



def bar_attendance_by_time(games, weather, by = "month" , team = "BOS", year = None, show_league_avg = False, attendance = "%"):
    """

    by:
        - 'start time'
        - 'weekday'
        - 'month'
        - 'year'
    attendance:
        - 'raw'
        - '%'
    """
    if not isinstance(team, str) and team is not None:
        print("Please enter one team abbreviation as a string. Enter ___ to see a list of team abbrevations.")
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




def bar_by_team(games, weather, census, y, year = None):
    """

    """


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




def scatter_daily(games, weather, x, y, team=None, year=None, lobf = False):
    """
    Works best for evaluating a single team, single year

    """
    df = process_daily(games, weather, team=team, year=year)

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



def scatter_yearly(games, weather, census, x, y, team=None, year=None, lobf = False):
    """


    """
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



def scatter_3d(games, weather, census, x, y, z, team, year, time = "daily"):
    """

    """
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


