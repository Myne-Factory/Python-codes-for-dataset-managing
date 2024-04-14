import os

print("---------------------------------------------------------------------\n")
print("This script creates a prompts list text file in the following format:\n")

print("   tag1                              Times in dataset: 200 (71.2%)")
print("   tag2                              Times in dataset: 184 (65.6%)")
print("   tag3                              Times in dataset: 177 (63.0%)\n")
print("---------------------------------------------------------------------\n")

input_folder_path = input(f"Enter the directory of the prompts: ")  # Replace with the actual path to your input folder
folder_name = os.path.basename(input_folder_path)
output_file_path = f'{folder_name} prompt list.txt'  # Replace with the desired path for your output file

def custom_split(text):
    # Split the text using both comma and asterisk as delimiters
    return [word.strip() for word in text.replace("*", "* ").split(',')]

def count_words_in_files(input_folder_path, output_file):
    word_counts = {}

    file_count = 0
    files = sorted(os.listdir(input_folder_path))
    print(f"Looking for .txt files in \"{input_folder_path}\"")
    for filename in files:
        if filename.endswith(".txt"):
            file_count += 1
            print(f"Found files: {file_count}", end='\r')
            
    print(f"Found files: {file_count}")

    processed_files = 0

    # Iterate over each file in the input folder
    for filename in files:
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder_path, filename)
            with open(filepath, 'r') as file:
                # Use custom split function
                words = custom_split(file.read())

                # Count the occurrences of each word
                for word in words:
                    if word:
                        word_counts[word] = word_counts.get(word, 0) + 1

            processed_files += 1
            percent_complete = round((processed_files / file_count) * 100)
            print(f"Processing files: {processed_files}/{file_count} ({percent_complete}%)", end='\r')
    print(f"Processing files: {processed_files}/{file_count} ({percent_complete}%)")

    # Sort the word counts in descending order
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Write the sorted word counts to the output file with folder name
    with open(output_file, 'w') as file:
        for word, count in sorted_counts:
            percent_of_dataset = round((count/file_count) * 100, 1)
            file.write(f"{word.ljust(35)}Times in dataset: {count} ({percent_of_dataset}%)\n")

    print(f"\nCreated prompt list \"{output_file_path}\"")
    input("\nPress Enter to exit.")

count_words_in_files(input_folder_path, output_file_path)
