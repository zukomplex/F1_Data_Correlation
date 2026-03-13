import fastf1
import pandas as pd
import streamlit as st

# Activate the cache
fastf1.Cache.enable_cache(r'D:\Programmieren\F1_Data_Correlation\F1_Cache') # Set a custom cache directory (optional, adjust the path as needed)

def remove_outliers(df, column):
    """Remove outliers from the specified column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

@st.cache_data
def analyze_correlation(year, gp, target_compound='All'):
    """Load the race data for the specified season and racetrack"""
    
    # Check weekend type if its sprint weekend
    event = fastf1.get_event(year, gp)
    event_format = str(event['EventFormat']).lower()
    if 'sprint' in event_format:
        session_name = 'FP1'  # Use FP1 for sprint weekends
    else:
        session_name = 'FP2'  # Use FP2 for regular weekends

    # Try loading the practice session (fallback to FP1 if FP2 is completely missing)
    try:
        fp_session = fastf1.get_session(year, gp, session_name)
        fp_session.load()
    except ValueError:
        session_name = 'FP1'
        fp_session = fastf1.get_session(year, gp, session_name)
        fp_session.load()

    # Load race results
    race = fastf1.get_session(year, gp, 'R')
    race.load()

    # Get all FP laps
    laps = fp_session.laps

    # Filter out In and Out laps (PitInTime and PitOutTime must be null)
    valid_laps = laps[pd.isnull(laps['PitOutTime']) & pd.isnull(laps['PitInTime'])]
    
    # Filter out laps with red / yellow flags (Track status '1' is green flag)
    valid_laps = valid_laps.pick_track_status('1')

    # Filter for wheel compound used in FP (e.g., SOFT, MEDIUM, HARD)
    if target_compound != 'All':
        valid_laps = valid_laps[valid_laps['Compound'] == target_compound.upper()]

    # Convert LapTime to seconds for easier analysis
    valid_laps = valid_laps.copy()
    valid_laps['LapTime_sec'] = valid_laps['LapTime'].dt.total_seconds()
    valid_laps = valid_laps.dropna(subset=['LapTime_sec'])

    # Remove outliers from the LapTime_sec column for each driver
    clean_laps = valid_laps.groupby('Driver', group_keys=False).apply(
        lambda x: remove_outliers(x, 'LapTime_sec')
    )

    # Calculate average pace of the cleaned laps for each driver
    fp_pace = clean_laps.groupby('Driver')['LapTime_sec'].mean().reset_index()
    fp_pace.columns = ['Driver', 'FP_AVG_Pace']

    # Extract race result
    race_results = race.results[['Abbreviation', 'FullName', 'Position', 'ClassifiedPosition', 'TeamName']]
    race_results.columns = ['Driver', 'FullName', 'Race_Position', 'Classified_Position', 'TeamName']

    # Connect data
    combined_data = pd.merge(fp_pace, race_results, on='Driver')

    # Add DNF status based on Classified_Position (if it's NaN, it's a DNF)
    combined_data['Is_DNF'] = pd.to_numeric(combined_data['Classified_Position'], errors='coerce').isna()

    # Clean data by dropping drivers with missing pace or position data in FP
    combined_data = combined_data.dropna(subset=['FP_AVG_Pace', 'Race_Position'])

    return combined_data, race, session_name