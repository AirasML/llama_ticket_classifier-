# AI-Powered Customer Support Ticket Classifier

## Overview

This project is an AI-powered customer support ticket classifier that processes customer queries and extracts structured information using a locally hosted LLM (Llama 2 via Ollama). The system reads support tickets from JSON files, classifies them into predefined categories, assesses urgency and sentiment, and extracts key information. The results are saved in a CSV file for easy analysis and further processing.

## Features

- **Automated Ticket Classification**: Categorizes support tickets into predefined categories (Order Issues, Account Access, Billing, etc.).
- **Urgency and Sentiment Analysis**: Determines how critical the issue is and the customer's sentiment.
- **Key Information Extraction**: Extracts essential details from the ticket for customer support teams.
- **Resilient Processing**: Implements retry logic and fallback mechanisms to ensure all tickets are classified and stored.
- **Batch Processing**: Reads multiple JSON files from a directory and processes them efficiently.

## Project Structure

```
├── tickets/                      # Directory containing JSON files with customer tickets
├── classified_tickets.csv        # Output file containing classified tickets
├── main.py                       # Main script to process tickets
├── README.md                     # Project documentation
```

## Installation

### Prerequisites

- Python 3.8+
- Ollama installed and configured with `llama2`
- Required Python libraries (listed below)

### Install Dependencies

Run the following command to install the required Python packages:

```sh
pip install pydantic instructor ollama
```

## Usage

### Running the Script

1. Ensure your JSON files containing customer tickets are stored in the `tickets/` directory.
2. Run the script:
   ```sh
   python main.py
   ```
3. Once executed, the processed results will be available in `classified_tickets.csv`.

### Input JSON Format

Each JSON file should contain an array of tickets in the following format:

```json
[
    {
        "ticket_number": 1,
        "client_name": "Alice Johnson",
        "ticket_text": "I received a damaged phone in my last order. I need a replacement."
    },
    {
        "ticket_number": 2,
        "client_name": "Bob Smith",
        "ticket_text": "I'm unable to access my account even after resetting my password. Please help!"
    }
]
```

### Output CSV Format

The output file `classified_tickets.csv` will contain:

- `ticket_number`
- `client_name`
- `ticket_text`
- `category`
- `urgency`
- `sentiment`
- `confidence`
- `key_information`
- `suggested_action`

Example row in CSV:

```
1,Alice Johnson,"I received a damaged phone...",order_issue,high,frustrated,0.95,"damaged phone, replacement","Initiate return process"
```

## Error Handling & Resilience

- **Retry Logic**: If the LLM fails to return a valid response, the script retries up to **3 times**.
- **Fallback Defaults**: If the LLM still fails, the ticket is assigned a default category, and a manual review is suggested.
- **Logging**: Errors are logged, and ticket processing continues without interruptions.

## Future Enhancements

- Integrate a web-based UI using **Streamlit**.
- Store classified tickets in a **database** instead of CSV.
- Extend support for **multi-language ticket classification**.

### Author

Developed by Syeda Airas Burhan