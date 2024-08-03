# TikTok Scraper

A Python script for scraping TikTok post data using the TikTok API. The script fetches detailed information about TikTok posts, including user details, post statistics, and more, and writes this data to a CSV file.

## Features

- Generates necessary headers (X-Gorgon and X-Khronos) to make authenticated requests to the TikTok API.
- Fetches post data including author information, statistics, and music details.
- Handles requests with random API endpoints for reliability.
- Supports input of multiple URLs and outputs data to a specified CSV file.

## Requirements

- Python 3.x
- The following Python packages:
  - `requests`
  - `protobuf`

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:
    ```sh
    pip install requests protobuf
    ```

## Usage

To run the script, you need to provide two command-line arguments: the input file containing URLs and the output CSV file name.

### Input File

The input file should contain lines formatted as `music_id;post_url`. For example:

1234567890;https://www.tiktok.com/@username/video/1234567890
0987654321;https://www.tiktok.com/@username/video/0987654321


### Command Line

Run the script with the following command:

```sh
python tiktok_scrapper.py input_file.txt output_file.csv
```

### Example

python tiktok_scrapper.py urls.txt tiktok_data.csv

