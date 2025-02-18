import instructor
from pydantic import BaseModel, Field
from enum import Enum
from typing import List
import ollama
import json
import os
import csv

class TicketCategory(str, Enum):
    ORDER_ISSUE = "order_issue"
    ACCOUNT_ACCESS = "account_access"
    PRODUCT_INQUIRY = "product_inquiry"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING = "billing"
    OTHER = "other"

class CustomerSentiment(str, Enum):
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"
    SATISFIED = "satisfied"

class TicketUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketClassification(BaseModel):
    category: TicketCategory
    urgency: TicketUrgency
    sentiment: CustomerSentiment
    confidence: float = Field(ge=0, le=1)
    key_information: List[str]
    suggested_action: str

SYSTEM_PROMPT = """
You are an AI assistant for a large e-commerce platform's customer support team. 
Your role is to analyze incoming customer support tickets and provide structured information to help our team respond quickly and effectively.
Business Context:
- We handle thousands of tickets daily across various categories (orders, accounts, products, technical issues, billing).
- Quick and accurate classification is crucial for customer satisfaction and operational efficiency.
- We prioritize based on urgency and customer sentiment.
Your tasks:
1. Categorize the ticket into the most appropriate category from ['order_issue','account_access','product_inquiry','technical_support','billing','other'].
2. Assess the urgency of the issue from ['low','medium','high','critical'].
3. Determine the customer's sentiment from ['angry','frustrated','neutral','satisfied'].
4. Extract key information that would be helpful for our support team.
5. Suggest an initial action for handling the ticket.
6. Provide a confidence score (0.0 to 1.0).
Ensure the output JSON contains these exact field names: 'category', 'urgency', 'sentiment', 'key_information', 'suggested_action', and 'confidence'.
Respond ONLY with a valid JSON object that adheres to this structure, without any additional text. Make sure that the response is in a valid json format. 
"""

def classify_ticket(ticket_text: str) -> TicketClassification:
    response = ollama.chat(
        model='llama2',
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": ticket_text}
        ]
    )
    json_response = response['message']['content'].strip()
    try:
        json_data = json.loads(json_response)
        return TicketClassification.model_validate(json_data)
    except (json.JSONDecodeError, ValueError) as e:
        print("Error: Invalid JSON response.")
        print("Raw response:", json_response)
        raise e


def process_tickets_from_directory(directory: str, output_csv: str):
    with open(output_csv, mode='w', newline='') as csvfile:
        fieldnames = ['ticket_number', 'client_name', 'ticket_text', 'category', 'urgency', 'sentiment', 'confidence', 'key_information', 'suggested_action']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename), 'r') as file:
                    tickets = json.load(file)
                    for ticket in tickets:
                        try:
                            result = classify_ticket(ticket['ticket_text'])
                            writer.writerow({
                                'ticket_number': ticket['ticket_number'],
                                'client_name': ticket['client_name'],
                                'ticket_text': ticket['ticket_text'],
                                'category': result.category,
                                'urgency': result.urgency,
                                'sentiment': result.sentiment,
                                'confidence': result.confidence,
                                'key_information': '; '.join(result.key_information),
                                'suggested_action': result.suggested_action
                            })
                        except Exception as e:
                            print(f"Failed to classify ticket {ticket['ticket_number']}: {e}")

if __name__ == "__main__":
    input_directory = "tickets"
    output_csv_file = "classified_tickets.csv"
    process_tickets_from_directory(input_directory, output_csv_file)
    print("Tickets processed and saved to CSV.")
