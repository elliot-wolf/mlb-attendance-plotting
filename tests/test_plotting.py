import pytest
from mlbattendanceplotter.plotting import bar_attendance_by_time, bar_by_team, scatter_daily, scatter_yearly, scatter_3d

### bar_attendance_by_time() tests ###
def test_bar_attendance_by_time_invalid_arguments():
    with pytest.raises(ValueError):
        bar_attendance_by_time(team="Red Sox") # Invalid 'team' argument
    with pytest.raises(ValueError):
        bar_attendance_by_time(by="century") # Invalid 'by' argument
    with pytest.raises(ValueError):
        bar_attendance_by_time(attendance="capacity") # Invalid 'attendance' argument
    with pytest.raises(ValueError):
        bar_attendance_by_time(year="2018") # Invalid 'year' argument
    with pytest.raises(ValueError):
        bar_attendance_by_time(year=2020) # Invalid 'year' argument

### bar_by_team() tests ###
def test_bar_by_team_invalid_arguments():
    with pytest.raises(ValueError):
        bar_by_team(y = "not a column") # Invalid y argument
    with pytest.raises(ValueError):
        bar_by_team(y="win_pct", year = 2020) # Invalid year

### scatter_daily() tests ###
def test_scatter_daily_invalid_arguments():
    with pytest.raises(ValueError):
        scatter_daily(x = "win_pct", y = "attendance", team="Red Sox") # Invalid team
    with pytest.raises(ValueError):
        scatter_daily(x = "lose_pct", y = "attendance", team="BOS") # Invalid x
    with pytest.raises(ValueError):
        scatter_daily(x = "win_pct", y = "attend", team = "BOS") # Invalid y
    with pytest.raises(ValueError):
        # Cannot have lobf and show_prcp both True
        scatter_daily(x = "win_pct", y = "attendance", team = "BOS", lobf=True, show_prcp=True)

### scatter_yearly() tests ###
def test_scatter_yearly_invalid_arguments():
    with pytest.raises(ValueError):
        scatter_yearly(x = "win", y = "attendance", team = "BOS") # Invalid x
    with pytest.raises(ValueError):
        scatter_yearly(x = "win_pct", y = "attend", team = "BOS") # Invalid y
    with pytest.raises(ValueError):
        scatter_yearly(x = "win_pct", y = "attendance", team = "Red Sox")

### scatter_3D() tests ###
def test_scatter_3d_invalid_arguments():
    with pytest.raises(ValueError):
        scatter_3d(x = "win", y = "attendance", z = "payroll_est", team = "BOS") # Invalid x
    with pytest.raises(ValueError):
        scatter_3d(x = "win_pct", y = "payroll_est", z = "attendance%", time = "not a time") # Invalid time
    with pytest.raises(ValueError):
        scatter_3d(x="win_pct", y="payroll_est", z="attendance%", year = 2020, time="yearly") # Invalid year
    with pytest.raises(ValueError):
        scatter_3d(x="win_pct", y="payroll_est", z="attendance%", time="yearly", team="Red Sox") # Invalid team
