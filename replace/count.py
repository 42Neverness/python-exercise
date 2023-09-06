import re

# Function to count and replace "terrible" occurrences
def replace_terrible(text):
    count = 0

    def replace(match):
        nonlocal count
        count += 1
        if count % 2 == 0:
            return "pathetic"
        else:
            return "marvellous"

    # Use regular expressions to find and replace "terrible"
    modified_content = re.sub(r'\bterrible\b', replace, text, flags=re.IGNORECASE)

    return modified_content, count

# Input and output file names
input_filename = "file_to_read.txt"
output_filename = "result.txt"

try:
    # Step 1: Read the content of the input file
    with open(input_filename, "r") as file:
        content = file.read()

    # Step 2: Count and replace "terrible" occurrences
    modified_content, total_terrible_count = replace_terrible(content)

    # Step 3: Write the modified content to a new file
    with open(output_filename, "w") as output_file:
        output_file.write(modified_content)

    print(f"Total occurrences of 'terrible': {total_terrible_count}")

except FileNotFoundError:
    print(f"The file '{input_filename}' does not exist.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
