import os
import random

print("-------------------------------------------------\n")
print("This script reads a random .txt file in a folder.\n")
print("-------------------------------------------------\n")

def load_blacklist(blacklist_file_path):
    # Load the blacklist tags from the file
    with open(blacklist_file_path, 'r') as blacklist_file:
        # Split the file content into lines and flatten the list
        blacklist_tags = [tag.strip() for line in blacklist_file for tag in line.split(',')]

    return set(blacklist_tags)

def get_random_file_content(folder_path, use_blacklist, blacklist_tags):
    # Get a list of text files in the specified folder and its subfolders
    text_files = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files if file.endswith('.txt')]

    if not text_files:
        print("No text files found in the specified folder.")
        return

    while True:
        # Choose a random text file
        random_file = random.choice(text_files)

        # Read the content of the random file
        with open(random_file, 'r') as file:
            content = file.read()

        if use_blacklist == "y":
            # Check if any tag in the content is in the blacklist
            file_tags = [tag.strip() for tag in content.split(',')]
            if not any(tag in blacklist_tags for tag in file_tags):
                # Print the content and break out of the loop
                print(f"\nContent of {random_file}:\n\n{content}")
                break
        else:
            print(f"\nContent of {random_file}:\n\n{content}")
            break

if __name__ == "__main__":
    while True:
        # Get user input for the folder path
        folder_path = input("Enter the folder path: ")
        # Check if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            break
        print("\nInvalid folder path. \n")

    # Get user input for the blacklist file path
    blacklist_file_path = r"F:\Python codes for dataset managing\PromptGenerator\blacklist.txt"
    # Check if the blacklist file exists
    if not os.path.exists(blacklist_file_path) or not os.path.isfile(blacklist_file_path):
        print("Invalid blacklist file path. Exiting.")
        exit()

    while True:
        # Get user input for using the blacklist
        while True:
            use_blacklist = input("Use blacklist? (y/n): ")
            if use_blacklist == "y" or use_blacklist == "n":
                break

        while True:
            # Load the blacklist tags
            blacklist_tags = load_blacklist(blacklist_file_path)

            # Call the function to get random file content, considering the blacklist
            get_random_file_content(folder_path, use_blacklist, blacklist_tags)

            # Ask the user if they want another random file
            another_file = input("\nPress Enter for another one. Type \"n\" to change settings: ")
            if another_file == "n":
                # Prompt the user for a new folder path
                while True:
                    folder_path = input("Enter the folder path: ")
                    if os.path.exists(folder_path) and os.path.isdir(folder_path):
                        break
                    print("\nInvalid folder path. \n")
                    
                # Ask the user if they want to use a blacklist
                while True:
                    use_blacklist = input("Use blacklist? (y/n): ")
                    if use_blacklist == "y" or use_blacklist == "n":
                        break
            elif another_file != "":
                break
