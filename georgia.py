import re
import csv
from openai import OpenAI

client = OpenAI()

def get_bill_summary(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Summarize this bill in 2 simple sentences: " + text}
        ]
    )
    return response.choices[0].message.content

def check_hot_button(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Is this bill a hot button political issue that could be relevant for political campaigns? Answer only with 'potential hot button issue' or 'unlikely hot button': " + text}
        ]
    )
    return response.choices[0].message.content

def extract_roll_call_votes(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    
    sections = text.split("On the passage of the bill, a roll call was taken, and the vote was as follows:")
    
    roll_call_results = []
    for i in range(len(sections)-1):
        bill_section = sections[i]
        bill_match = re.search(r'(?:HB|SB)\s+\d+\..*?(?=(?:HB|SB)|$)', bill_section, re.DOTALL)
        if bill_match:
            bill_text = bill_match.group()
        else:
            bill_text = bill_section
            
        votes_section = sections[i+1]
        votes_end = votes_section.find("On the passage of the bill, the yeas were")
        if votes_end != -1:
            votes_text = votes_section[:votes_end]
        else:
            votes_text = votes_section
            
        bill_text = ' '.join(bill_text.split())
        votes_text = ' '.join(votes_text.split())
        
        # Get summary and hot button status
        summary = get_bill_summary(bill_text)
        hot_button = check_hot_button(bill_text)
        
        roll_call_results.append((bill_text, votes_text, summary, hot_button))
    
    return roll_call_results

def save_to_csv(roll_calls, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Roll Call Number", "Summary", "Hot Button Status", "Bill Text", "Votes"])
        
        for i, (bill_text, votes, summary, hot_button) in enumerate(roll_calls, 1):
            csvwriter.writerow([f"Roll Call {i}", summary, hot_button, bill_text, votes])

file_path = 'georgia_senate_journal.txt'
output_file = 'roll_call_votes_with_bills.csv'
try:
    roll_calls = extract_roll_call_votes(file_path)
    save_to_csv(roll_calls, output_file)
    print(f"Successfully extracted {len(roll_calls)} roll call votes to {output_file}")
except Exception as e:
    print(f"Error processing file: {str(e)}")