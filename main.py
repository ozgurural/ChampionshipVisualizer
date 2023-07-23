import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import cv2
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

def read_and_process_data(file_path):
    # Read the championship data from the CSV file
    championship_data_df = pd.read_csv(file_path)
    
    # Create a dictionary with teams as keys and years of championship as list of values
    championship_data = {}
    for team in championship_data_df['Team'].unique():
        championship_data[team] = championship_data_df[championship_data_df['Team'] == team]['Year'].tolist()

    # Create a dictionary with teams as keys and logos as values
    team_logos = dict(zip(championship_data_df['Team'], championship_data_df['Logo']))

    return championship_data, team_logos

def prepare_team_colors(championship_data):
    # Create a sorted list of all unique team names
    all_teams = sorted(list(set(championship_data.keys())))

    # Create a list of unique colors
    all_colors = sns.color_palette('hsv', len(all_teams))

    # Assign a unique color to each team
    team_colors = {team: all_colors[i] for i, team in enumerate(all_teams)}
    return team_colors

def create_chart_for_year(year, championship_data, all_teams, team_colors, team_logos):
    # Create a DataFrame for the current year
    data_for_year = {team: len([y for y in years if y <= year]) for team, years in championship_data.items()}

    # Create a DataFrame including all teams
    df = pd.DataFrame([(team, data_for_year.get(team, 0)) for team in all_teams], columns=['Team', 'Championships'])
    df = df.sort_values('Championships', ascending=False)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(16, 9))  # set the figure size to match the 16:9 aspect ratio
    ax.xaxis.tick_top()  # move the x-axis to the top
    ax.set_xlim([0, 30])  # set a fixed x-axis limit, adjusted to make space for the logos

    # Hide the right and bottom spines
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Only show ticks on the left and top spines
    ax.yaxis.tick_left()
    ax.xaxis.tick_top()

    # Remove the labels for the x and y axes
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Increase the size and weight of the y-axis tick labels (team names)
    ax.tick_params(axis='y', labelsize='large')

    # Plot the data with specific colors for some teams
    sns.set_palette(sns.color_palette("hls", len(all_teams)))  # Change the color palette
    sns.barplot(x='Championships', y='Team', data=df, ax=ax)  # Use a single color when plotting

    # Set the color of each bar individually and add the championship counts and logos to the right of each bar
    for index, (bar, team) in enumerate(zip(ax.patches, df['Team'])):
        bar.set_color(team_colors[team])  # Set the color of the bar

        if bar.get_width() > 0:
            ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2, 
                    f' {bar.get_width():.0f}', va='center', color='black', fontsize=13, fontweight='bold')

            if team in team_logos:
                img = Image.open(team_logos[team])
                imagebox = OffsetImage(img, zoom=0.15)
                imagebox.image.axes = ax
                ab = AnnotationBbox(imagebox, (bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2),
                                    boxcoords="data", pad=0, frameon=False)
                ax.add_artist(ab)

    # Add the year at the bottom right
    ax.text(0.95, 0.05, year, transform=ax.transAxes, fontsize=50, fontweight='bold', va='bottom', ha='right')

    # Increase the size of the y-axis tick labels (team names)
    ax.tick_params(axis='y', labelsize='large')

    # Set the weight of the y-axis tick labels (team names) to bold
    for label in ax.get_yticklabels():
        label.set_weight('bold')

    # Adjust the layout
    plt.tight_layout()

    # Save the chart as a png file with higher resolution
    fig.set_size_inches(16, 9)  # Ensure the figure size is proportional to the desired output resolution
    plt.savefig(f'charts/chart_{year}.png', bbox_inches='tight', dpi=380)  # Include all elements of the figure in the saved image

    plt.close(fig)  # close the figure to free up memory

def create_video():
    # Get the list of image files
    images = [img for img in os.listdir('charts') if img.endswith(".png")]
    images.sort()

    # Define the size for resizing the images
    desired_size = (1920, 1080)  # width and height in pixels

    # Create a VideoWriter object
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 1, desired_size)

    # The last image will be added for 20 times
    last_image = images[-1]

    for image in images:
        # Read the image
        img = cv2.imread(os.path.join('charts', image))
        
        # Resize the image to the desired size
        img_resized = cv2.resize(img, desired_size)
        
        video.write(img_resized)

    # Write the last frame 20 times
    for _ in range(20):
        img = cv2.imread(os.path.join('charts', last_image))
        img_resized = cv2.resize(img, desired_size)
        video.write(img_resized)

    video.release()

def main():
    # Create directory for storing the charts
    if not os.path.exists('charts'):
        os.makedirs('charts')

    championship_data, team_logos = read_and_process_data('championship_data_logos.csv')
    team_colors = prepare_team_colors(championship_data)

    # Get all unique team names
    all_teams = sorted(list(set(championship_data.keys())))

    # Get the minimum and maximum years from the championship data
    min_year = min([min(years) for years in championship_data.values()])
    max_year = max([max(years) for years in championship_data.values()])

    # Create a chart for each year from min_year to max_year
    for year in range(min_year, max_year + 1):
        print(f"Processing year {year}")
        create_chart_for_year(year, championship_data, all_teams, team_colors, team_logos)
    
    create_video()


if __name__ == "__main__":
    main()
