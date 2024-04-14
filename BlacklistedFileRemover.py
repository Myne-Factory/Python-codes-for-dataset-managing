import os
import codecs

print("---------------------------------------------------------------------------------------------\n")
print("This is a script for removing blacklisted images from a folder based off of blacklisted tags.\n")
print("---------------------------------------------------------------------------------------------\n")

def remove_text_files_with_blacklisted_phrases(folder_path, blacklist_path, encoding='utf-8'):
    # Read the blacklist file
    with open(blacklist_path, 'r', encoding=encoding) as blacklist_file:
        blacklist_phrases = [phrase.strip() for phrase in blacklist_file.readline().split(',')]

    # Get the total number of files in the folder
    file_count = len([file_name for file_name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_name))])

    # Initialize match counter
    match_count = 0

    # Iterate over the files in the folder
    for i, file_name in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            # Read the content of the text file
            with codecs.open(file_path, 'r', encoding=encoding) as text_file:
                file_content = [phrase.strip() for phrase in text_file.readline().split(', ')]

            # Check if any blacklist phrase is present in the file content
            matches = [phrase.strip() for phrase in blacklist_phrases if phrase.strip() in file_content]

            if matches:
                # Remove the file
                os.remove(file_path)
                reason = ", ".join(matches)
                print(f"Removed {file_path} | Reason: {reason}")

                # Increment match counter
                match_count += 1

        # Calculate progress percentage
        progress = (i + 1) / file_count * 100

        # Print progress and match count on a single line
        print(f"Looking through file {i + 1} / {file_count} ({progress:.1f}% complete) | Matches found: {match_count}", end='\r')

    print("\nRemoval process complete.")
    input("Press any key to exit.")

# Prompt the user to enter the folder path, blacklist file path, and encoding type
folder_path = input("Enter the folder path: ")
blacklist_path = input("Enter the blacklist file path: ")
encoding = input("Enter the encoding type (default: utf-8): ") or 'utf-8'

# Call the function to remove text files
remove_text_files_with_blacklisted_phrases(folder_path, blacklist_path, encoding)
