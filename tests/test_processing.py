import pytest
from mlbattendanceplotter.processing import load_data, process_yearly, process_daily, group_attendance_by_time

### load_data() test ###
def test_load_data():
    games, weather, census = load_data()
    # Make sure csv's are correctly read
    assert games is not None
    assert weather is not None
    assert census is not None

### process_yearly() test ###
def test_process_yearly():
    games, weather, census = load_data()
    yearly_df = process_yearly(games, weather, census)

    # If test_cols are present, data was correctly loaded from all datasources
    test_cols = ['team', 'year', 'win_pct', 'tavg', 'median_age']
    missing_cols = [each for each in test_cols if each not in yearly_df.columns]
    assert not missing_cols # AssertionError if test_cols aren't in yearly_df.columns

def test_process_daily():
    games, weather, census = load_data()
    daily_df = process_daily(games, weather)

    # If test_cols are present, data was correctly loaded from all datasources
    test_cols = ['team', 'year', 'win_pct', 'tavg']
    missing_cols = [each for each in test_cols if each not in daily_df.columns]
    assert not missing_cols  # AssertionError if test_cols aren't in daily_df.columns
