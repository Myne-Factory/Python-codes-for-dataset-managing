# Prompt the user for the input file name
input_file = input("Enter the input file name: ")

# Generate the output file name
output_file = input_file.rsplit('.', 1)[0] + " rows removed.txt"

# Read the input file
with open(input_file, 'r') as file:
    tags = file.readlines()

# Remove newline characters and whitespace
tags = [tag.strip() for tag in tags]

# Concatenate tags using commas
output = ', '.join(tags)

# Write the output to a file
with open(output_file, 'w') as file:
    file.write(output)

print("Created a new file file:", output_file)
print("Press Enter to exit")
input()