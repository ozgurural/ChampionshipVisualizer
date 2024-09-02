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
