import os

def count_prompt_in_files(prompt, directory):
    prompt = prompt.lower()
    exact_match = 0
    close_match = {}
    contains_match = {}

    file_count = 0
    longest_word_length = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                file_count += 1

    processed_files = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                processed_files += 1
                processing_percentage = (processed_files / file_count) * 100
                print(f"Processing files: {processed_files}/{file_count} ({processing_percentage:.1f}%)", end='\r')

                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    words = file.read().lower().split(',')

                    for word in words:
                        word = word.strip()
                        if word:
                            if word == prompt:
                                exact_match += 1
                            elif word.startswith(prompt + ' ') or word.endswith(' ' + prompt):
                                close_match[word] = close_match.get(word, 0) + 1
                            elif prompt in word:
                                contains_match[word] = contains_match.get(word, 0) + 1
                                longest_word_length = max(longest_word_length, len(word))

    print(f"\n\nExact match: {'-' * (longest_word_length + 17)}")
    print(f"{prompt.ljust(longest_word_length + 7)}Count: {exact_match:<8} ({(exact_match / file_count * 100):.2f}%)")

    print(f"\nClose match: {'-' * (longest_word_length + 17)}")
    sorted_close_match = sorted(close_match.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_close_match:
        print(f"{word.ljust(longest_word_length + 7)}Count: {count:<8} ({(count / file_count * 100):.2f}%)")

    print(f"\nContains \"{prompt}\": {'-' * (longest_word_length + 17 - len(prompt))}")
    sorted_contains_match = sorted(contains_match.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_contains_match:
        print(f"{word.ljust(longest_word_length + 7)}Count: {count:<8} ({(count / file_count * 100):.2f}%)")

    print(f"\n{'=' * (longest_word_length + 30)}\n")
    input_prompts()

def input_prompts():
    # Prompt the user for input
    prompt = input("Enter a prompt: ")
    directory = input("Enter the directory path: ")
    print("")

    count_prompt_in_files(prompt, directory)

input_prompts()
