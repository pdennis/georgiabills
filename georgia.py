import re
import csv

def extract_roll_call_votes(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Regular expression to find roll call vote sections
    roll_call_pattern = re.compile(
        r"On the passage of the bill, a roll call was taken, and the vote was as follows:(.*?)On the passage of the bill, the yeas were \d+, nays \d+\.",
        re.DOTALL
    )
    
    # Find all matches
    roll_calls = roll_call_pattern.findall(text)
    
    # Clean up and format each roll call vote
    roll_call_results = []
    for roll_call in roll_calls:
        # Remove extra spaces and line breaks
        roll_call = re.sub(r'\s+', ' ', roll_call.strip())
        roll_call_results.append(roll_call)
    
    return roll_call_results

def save_to_csv(roll_calls, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Roll Call Number", "Votes"])  # Header row
        
        for i, roll_call in enumerate(roll_calls, 1):
            csvwriter.writerow([f"Roll Call {i}", roll_call])

# Example usage
file_path = 'georgia.txt'  # Update with your file path
output_file = 'roll_call_votes.csv'       # Desired output CSV file name

roll_calls = extract_roll_call_votes(file_path)
save_to_csv(roll_calls, output_file)

print(f"Roll call votes have been exported to {output_file}.")
