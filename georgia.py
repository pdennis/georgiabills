import re
import csv

def extract_roll_call_votes(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Split on the roll call marker
    sections = text.split("On the passage of the bill, a roll call was taken, and the vote was as follows:")
    
    roll_call_results = []
    for i in range(len(sections)-1):  # Skip the last section
        # Get bill text from current section
        bill_section = sections[i]
        bill_match = re.search(r'(?:HB|SB)\s+\d+\..*?(?=(?:HB|SB)|$)', bill_section, re.DOTALL)
        if bill_match:
            bill_text = bill_match.group()
        else:
            bill_text = bill_section
            
        # Get votes from next section
        votes_section = sections[i+1]
        votes_end = votes_section.find("On the passage of the bill, the yeas were")
        if votes_end != -1:
            votes_text = votes_section[:votes_end]
        else:
            votes_text = votes_section
            
        # Clean text
        bill_text = ' '.join(bill_text.split())
        votes_text = ' '.join(votes_text.split())
        
        roll_call_results.append((bill_text, votes_text))
    
    return roll_call_results

def save_to_csv(roll_calls, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Roll Call Number", "Bill Text", "Votes"])
        
        for i, (bill_text, votes) in enumerate(roll_calls, 1):
            csvwriter.writerow([f"Roll Call {i}", bill_text, votes])

file_path = 'georgia_senate_journal.txt'
output_file = 'roll_call_votes_with_bills.csv'

try:
    roll_calls = extract_roll_call_votes(file_path)
    save_to_csv(roll_calls, output_file)
    print(f"Successfully extracted {len(roll_calls)} roll call votes to {output_file}")
except Exception as e:
    print(f"Error processing file: {str(e)}")