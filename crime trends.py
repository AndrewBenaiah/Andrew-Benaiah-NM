import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure output directory exists
os.makedirs('plots', exist_ok=True)

# Load dataset
url = "https://raw.githubusercontent.com/navneet-nmk/Indian-Crime-Data/master/crime_data.csv"
df = pd.read_csv(url)

# Get actual available years (ideally 2001–2012)
available_years = sorted(df['Year'].unique())[-3:]
if len(available_years) < 3:
    print(f"Warning: Only {len(available_years)} year(s) of data found: {available_years}")
else:
    print(f"Analyzing data for years: {available_years}")

# Filter for last 3 available years
df = df[df['Year'].isin(available_years)]

# 1. Yearly Murder Trend
plt.figure(figsize=(12, 7))
ax = sns.lineplot(data=df, x='Year', y='Murder', estimator='sum',
                  marker='o', linewidth=3, markersize=10, color='#e74c3c')

# Add data labels
for year, value in zip(df['Year'].unique(), df.groupby('Year')['Murder'].sum()):
    ax.text(year, value + 100, f'{value:,}', ha='center', va='bottom',
            fontsize=12, fontweight='bold', color='#2c3e50')

# Formatting
years = sorted(df['Year'].unique())
ax.set_xticks(years)
ax.set_xticklabels([str(int(year)) for year in years], rotation=45)
plt.title(f'Murder Trend Analysis ({min(years)}-{max(years)})',
          fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Year', fontsize=12, labelpad=15)
plt.ylabel('Total Murders Reported', fontsize=12, labelpad=15)
plt.grid(True, linestyle='--', alpha=0.7)

# Add contextual annotation
plt.annotate(f"Data Source: National Crime Records Bureau\nPeriod: {min(years)}-{max(years)}",
             xy=(0.5, -0.25),
             xycoords='axes fraction',
             ha='center', va='center',
             fontsize=10, color='#7f8c8d')

plt.tight_layout()
plt.savefig('plots/trend.png', bbox_inches='tight')
plt.close()

# 2. Top States by Murders
state_murder = df.groupby('States/UTs')['Murder'].sum().nlargest(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=state_murder.values, y=state_murder.index, palette='Reds_r')
plt.title(f'Top 10 States by Murders ({min(available_years)}-{max(available_years)})')
plt.xlabel('Total Murders')
plt.ylabel('States/UTs')
plt.tight_layout()
plt.savefig('plots/top_states.png')
plt.close()

# 3. Crime Type Distribution
crime_types = df[['Murder', 'Rape', 'Kidnapping & Abduction', 'Robbery']].sum()
plt.figure(figsize=(10, 10))
plt.pie(crime_types, labels=crime_types.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
plt.title('Crime Type Distribution')
plt.tight_layout()
plt.savefig('plots/crime_types.png')
plt.close()

# 4. Crime Heatmap
heatmap_data = df.pivot_table(
    index='States/UTs',
    columns='Year',
    values='Murder',
    aggfunc='sum',
    fill_value=0
)
plt.figure(figsize=(15, 10))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='d')
plt.title(f'Murder Heatmap ({min(available_years)}-{max(available_years)})')
plt.tight_layout()
plt.savefig('plots/heatmap.png')
plt.close()

# 5. Crime Type Trends
crime_trends = df.groupby('Year')[['Murder', 'Rape', 'Kidnapping & Abduction', 'Robbery']].sum()
plt.figure(figsize=(12, 6))
sns.lineplot(data=crime_trends, markers=True)
plt.title('Crime Type Trends Over Years')
plt.xlabel('Year')
plt.ylabel('Reported Cases')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('plots/crime_trends.png')
plt.close()

# Generate HTML report
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Crime Data Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; text-align: center; }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            gap: 20px; 
            max-width: 1200px; 
            margin: 0 auto;
        }
        .card { 
            background: #f9f9f9; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        img { width: 100%; height: auto; }
    </style>
</head>
<body>
    <h1>Indian Crime Analysis ({start_year}-{end_year})</h1>
    <div class="grid">
        <div class="card">
            <h2>Murder Trend</h2>
            <img src="plots/trend.png">
        </div>
        <div class="card">
            <h2>Top States by Murders</h2>
            <img src="plots/top_states.png">
        </div>
        <div class="card">
            <h2>Crime Type Distribution</h2>
            <img src="plots/crime_types.png">
        </div>
        <div class="card">
            <h2>Murder Heatmap</h2>
            <img src="plots/heatmap.png">
        </div>
        <div class="card">
            <h2>Crime Type Trends</h2>
            <img src="plots/crime_trends.png">
        </div>
    </div>
</body>
</html>
'''.replace("{start_year}", str(min(available_years))).replace("{end_year}", str(max(available_years)))

with open('crime_report.html', 'w') as f:
    f.write(html_content)

print("Analysis complete! Open crime_report.html to view results")