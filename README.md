# Championship Data Visualization

Visualizes sports championship data over time, creating bar charts and compiling them into a video.

## Features

- **Data Processing**: Reads and processes championship data from a CSV file.
- **Visualization**: Generates yearly bar charts of championships won by each team.
- **Video Compilation**: Creates a video from the generated charts.

## Requirements

- Python libraries: `matplotlib`, `pandas`, `seaborn`, `opencv-python`, `Pillow`
- Install with:
  ```bash
  pip install matplotlib pandas seaborn opencv-python pillow
   ```

## Usage

### Prepare Data

- Create a `championship_data_logos.csv` file with columns:
  - `Team`: Team name
  - `Year`: Year won
  - `Logo`: Path to team logo

### Run the Script

- Execute in your Python environment:
  ```bash
  python script_name.py
  ```

  ### Output

- **PNG charts**: Saved in the `charts/` directory.
- **Video file**: `video.avi` generated in the current directory.

## Key Functions

- **`read_and_process_data(file_path)`**: Reads CSV and processes data.
- **`prepare_team_colors(championship_data)`**: Assigns colors to teams.
- **`create_chart_for_year(year, ...)`** and **`create_video()`**: Creates charts and compiles them into a video.

