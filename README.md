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

