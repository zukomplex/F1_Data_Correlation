from urllib.request import urlopen
import fastf1
import fastf1.plotting
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# TO DO 
# Data cleaning: Handle missing values, outliers, and ensure data consistency.
# Use FP1 and FP3 data to analyze consistency across sessions.
# Add Main Menu for user to select different analyses (Remove CLI input and use buttons or dropdowns)
# Show what correlation is good and what is bad (e.g., R > 0.7 is strong, R < 0.3 is weak)
# Show DNF drivers in a different color or with a special marker to indicate they did not finish the race or did not compete in FP2.

# Configure plotting style
fastf1.plotting.setup_mpl(misc_mpl_mods=False)  # Activates FastF1-Design

# Activate the cache
fastf1.Cache.enable_cache(r'D:\Programmieren\F1_Datenanalyse-Projekt\F1_Cache')


def race_user_input():
    """Get user input for the season and racetrack"""
    try:
        year = int(input("Enter the season (e.g., 2023): "))
        gp = input("Enter the racetrack (e.g., Silverstone): ").title()  # Capitalize first letter of each word
        return year, gp
    except ValueError:
        print("Invalid input. Please enter a valid season and racetrack.")
        return None, None

def analyze_correlation(year, gp):
    """Load the race data for the specified season and racetrack"""
    
    # Compare FP2 and Race results
    fp2 = fastf1.get_session(year, gp, 'FP2')
    fp2.load()
    race = fastf1.get_session(year, gp, 'R')
    race.load()

    # Extract free practice 2 lap times and average pace
    fp2_laps = fp2.laps.pick_quicklaps()
    fp2_pace = fp2_laps.groupby('Driver')['LapTime'].mean().dt.total_seconds().reset_index()
    fp2_pace.columns = ['Driver', 'FP2_AVG_Pace']

    # Extract race result
    race_results = race.results[['Abbreviation', 'ClassifiedPosition', 'TeamName']]
    race_results.columns = ['Driver', 'Race_Position', 'TeamName']

    # Connect data
    combined_data = pd.merge(fp2_pace, race_results, on='Driver')

    # Clean data
    combined_data['Race_Position'] = pd.to_numeric(combined_data['Race_Position'], errors='coerce')
    combined_data = combined_data.dropna(subset=['FP2_AVG_Pace', 'Race_Position'])

    return combined_data, race

# --- MAIN PROGRAM ---
year_input, gp_input = race_user_input()
print(f"Analyzing correlation for {gp_input} {year_input}...")

if year_input is not None and gp_input is not None:
    # Analyze the correlation between FP2 average pace and race results
    df, race = analyze_correlation(year_input, gp_input)

    # --- VISUALIZATION ---
    plt.style.use('dark_background') 
    fig, ax = plt.subplots(figsize=(14, 9))

    # Plot trend line (Seaborn)
    sns.regplot(data=df, x='FP2_AVG_Pace', y='Race_Position', 
                scatter=False, 
                line_kws={'color': "#ffcc00", 'lw': 2, 'linestyle': '--'},
                ax=ax)

    # Plot drivers with explicit color handling
    for i, row in df.iterrows():
        try:
            # Use FastF1 official team color logic
            color = fastf1.plotting.get_team_color(row['TeamName'], race)
        except:
            color = '#ffffff' # Fallback to white
        
        # Draw the dot
        ax.scatter(row['FP2_AVG_Pace'], row['Race_Position'], 
                   color=color, s=150, edgecolors='white', linewidth=1, zorder=10)
        
        # Add labels with a small "shadow" (path_effects) for better visibility
        ax.text(row['FP2_AVG_Pace'] + 0.04, 
                row['Race_Position'] - 0.2, 
                row['Driver'], 
                fontsize=11, weight='bold', color='white', zorder=11)

    # Formatting x-axis to M:SS:MS
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x // 60)}:{int(x % 60):02d}:{int((x % 1) * 1000):03d}'))

    # Title and Labels
    ax.set_title(f'F1 Analysis: FP2 Pace vs. Race Result ({gp_input} {year_input})', fontsize=18, pad=30)
    ax.set_xlabel('Average FP2 Lap Time', fontsize=13, labelpad=15)
    ax.set_ylabel('Final Race Position', fontsize=13, labelpad=15)

    ax.invert_yaxis()
    ax.set_yticks(range(1, 21))
    ax.grid(True, linestyle=':', alpha=0.4)

    # Correlation message box
    correlation = df['FP2_AVG_Pace'].corr(df['Race_Position'])
    # Place text in the figure coordinates to prevent overlapping with data
    plt.text(0.03, 0.05, f'Correlation (R): {correlation:.2f}', 
             transform=ax.transAxes, fontsize=13, weight='bold', color='black',
             bbox=dict(boxstyle="round,pad=0.6", fc="#ffcc00", ec="black", alpha=0.9))

    plt.tight_layout()
    plt.show()