import streamlit as st
import fastf1.plotting
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import io
from analysis import analyze_correlation

# Configure plotting style
fastf1.plotting.setup_mpl(misc_mpl_mods=False)  # Activates FastF1-Design

# --- STREAMLIT UI ---
st.set_page_config(page_title="F1 Data Correlation", layout="wide")
st.title("🏎️ F1 Data Correlation Menu 🏁")
st.write("Choose a year and a race track to analyze the correlation between FP2 pace and race results. *(FP1 pace will be used for sprint weekends)*")

# Dropdowns and inputs for user selection 
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Dropdown for year selection
    year_input = st.selectbox("Select a year:", list(range(2026, 2017, -1)))

with col2:
    # Text input for GP name
    gp_input = st.text_input("Enter race track or country (e.g., Melbourne / Australia):", value="").title()

with col3:
    # Dropdown for wheel compound selection
    compound_input = st.selectbox("Select wheel compound:", ['All', 'Soft', 'Medium', 'Hard'])

with col4:
    # Dropdown to select whether to exclude DNFs from correlation calculation
    exclude_dnfs_option = st.selectbox("Correlation Dataset:", ["Finishers only", "Include DNFs"])
    exclude_dnfs = (exclude_dnfs_option == "Finishers only")

# Button to start analysis
if st.button("Analyze 🚀"):
    with st.spinner(f"Loading and analyzing data for {gp_input} {year_input}..."):
        try:
            # --- DATA ANALYSIS ---
            df, race, session_name = analyze_correlation(year_input, gp_input, compound_input)
            
            if df.empty:
                st.warning("No valid data found for the selected options. Please try different inputs.")
            else:
                if session_name == 'FP1':
                    st.info(f"ℹ️ Note: {gp_input} {year_input} is a sprint weekend, so FP1 data is being analyzed instead of FP2.")
                # Split the data into DNF and non-DNF for separate visualization
                df_finishers = df[~df['Is_DNF']]
                df_dnfs = df[df['Is_DNF']]

                # Decide which dataset to use for the trend line based on the checkbox selection
                df_for_trend = df_finishers if exclude_dnfs else df

                # --- VISUALIZATION ---
                plt.style.use('dark_background') 
                fig, ax = plt.subplots(figsize=(25, 9))

                # Plot trend line (Seaborn)
                if not df_for_trend.empty:
                    sns.regplot(data=df_for_trend, x='FP_AVG_Pace', y='Race_Position', 
                                scatter=False, 
                                line_kws={'color': "#ffcc00", 'lw': 2, 'linestyle': '--'},
                                ax=ax)

                # Plot drivers
                for i, row in df.iterrows():
                    try:
                        color = fastf1.plotting.get_team_color(row['TeamName'], race)
                    except:
                        color = '#ffffff'
                    
                    # DNF drivers will be marked with an 'X' and have a different color and size
                    is_dnf = row['Is_DNF']
                    marker_style = 'X' if is_dnf else 'o'
                    alpha_val = 0.6 if is_dnf else 1.0
                    size = 200 if is_dnf else 150
                    
                    # Draw the dot/cross
                    ax.scatter(row['FP_AVG_Pace'], row['Race_Position'], 
                            color=color, marker=marker_style, s=size, 
                            edgecolors='white', linewidth=1, alpha=alpha_val, zorder=10)
                    
                    # Add labels
                    label_text = f"{row['Driver']}"
                    
                    if is_dnf != True:
                        ax.text(row['FP_AVG_Pace'] + 0.2, 
                                row['Race_Position'] - 0.4, 
                                label_text, 
                                fontsize=11, weight='bold', color='white', alpha=alpha_val, zorder=11)
                    else:
                        ax.text(row['FP_AVG_Pace'] + 0.2,
                                row['Race_Position'] - 0.4,
                                label_text,
                                fontsize=11, weight='bold', color='red', alpha=alpha_val, zorder=11)
                    

                # Formatting x-axis to M:SS:MS
                ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x // 60)}:{int(x % 60):02d}:{int((x % 1) * 1000):03d}'))


                # Title and Labels
                compound_title = "" if compound_input == "All" else f" ({compound_input} Tires)"
                ax.set_title(f'F1 Analysis: FP Pace vs. Race Result - {gp_input} {year_input}{compound_title}', fontsize=18, pad=55)
                ax.set_xlabel('Average FP Lap Time (Clean Air & Outliers Removed)', fontsize=13, labelpad=15)
                ax.set_ylabel('Final Race Position', fontsize=13, labelpad=15)

                # Set y-axis limits and ticks based on the number of drivers in the selected year (22 since 2026, 20 before)
                max_drivers = 22 if year_input >= 2026 else 20

                # Limit y-axis to the number of drivers and add grid
                ax.set_ylim(max_drivers + 0.5, 0.5)
                ax.set_yticks(range(1, max_drivers + 1))
                ax.grid(True, linestyle=':', alpha=0.4)

                # --- CORRELATION-BOX ---
                # Calculate correlation based on checkbox selection
                if len(df_for_trend) > 1:
                    correlation = df_for_trend['FP_AVG_Pace'].corr(df_for_trend['Race_Position'])
                    
                   
                    box_text = "Finishers only" if exclude_dnfs else "Incl. DNFs"
                    
                    ax.text(0.5, 1.04, f'Correlation (R) - {box_text}: {correlation:.2f}', 
                            transform=ax.transAxes, fontsize=14, weight='bold', color='black',
                            ha='center', va='bottom',
                            bbox=dict(boxstyle="round,pad=0.6", fc="#ffcc00", ec="black", alpha=0.9))

                # --- LEGEND AND INFO BOX ---
                legend_elements = []
                unique_teams = sorted(df['TeamName'].dropna().unique())
                
                # Create legend entries for each team and their drivers
                for team in unique_teams:
                    team_data = df[df['TeamName'] == team].sort_values(by='Driver')
                    
                    try:
                        t_color = fastf1.plotting.get_team_color(team, race)
                    except:
                        t_color = '#ffffff'
                    
                    # 1st entry: Team name with a colored marker
                    legend_elements.append(mlines.Line2D([0], [0], marker='o', color='w', label=team,
                                            markerfacecolor=t_color, markersize=10, linestyle='None'))
                    
                    # 2nd entry: Drivers of the team, indented under the team name (without marker, just text)
                    for _, row in team_data.iterrows():
                        driver_str = f"      {row['FullName']} ({row['Driver']})"
                        legend_elements.append(mlines.Line2D([0], [0], marker='', color='w', label=driver_str,
                                                linestyle='None'))

                # Create the legend for teams and drivers
                team_legend = ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1.0), borderaxespad=0,
                                        title="Teams & Drivers", fontsize=11, title_fontsize=13,
                                        frameon=True, facecolor='#111111', edgecolor='#555555', labelcolor='white')
                plt.setp(team_legend.get_title(), color='white', weight='bold')
                
                # Add a second box for correlation guide and DNF marker explanation
                info_text = (
                    "--- Correlation (R) Guide ---\n"
                    "R ≥ 0.7  : Strong\n"
                    "R ≥ 0.3  : Moderate\n"
                    "R < 0.3  : Weak\n\n"
                    "--- Marker Guide ---\n"
                    "● : Regular Finisher\n"
                    "✖ : DNF (Did Not Finish)"
                )
                
                ax.text(1.23, 0.985, info_text, transform=ax.transAxes, fontsize=11, color='white',
                        ha='left', verticalalignment='top', linespacing=1.6,
                        bbox=dict(boxstyle="round,pad=0.8", fc="#111111", ec="#555555", alpha=0.9))

                plt.subplots_adjust(right=0.7) # Adjust right margin to make space for the legend and info box

                # --- SVG EXPORT ---
                buf = io.BytesIO()
                fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.3)
                buf.seek(0)
                
                svg_code = buf.getvalue().decode("utf-8")
                st.markdown(f'<div style="display: flex; justify-content: center;">{svg_code}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error during analysis. Details: {e}")