import random
import re

def generate_combination(prompts, probabilities, blacklist, always_include_prompts, min_length, max_length):
    filtered_prompts = list(prompts)  # Create a copy of the prompts list
    filtered_probabilities = list(probabilities)  # Create a copy of the probabilities list

    # Add always-included prompts to the blacklist
    blacklist += always_include_prompts

    combination_length = random.randint(min_length, max_length)
    unique_combination = []

    while len(unique_combination) < combination_length:
        prompt = random.choices(filtered_prompts, filtered_probabilities, k=1)[0]
        probability_multiplier = 1

        if prompt in always_include_prompts:
            # Prompt is always included, no need to check blacklist or probabilities
            unique_combination.append(prompt)
            index = filtered_prompts.index(prompt)
            filtered_prompts.pop(index)
            filtered_probabilities.pop(index)
            continue

        if any(word in prompt.split() for word in blacklist):
            # Prompt is in blacklist, skip it
            continue

        unique_combination.append(prompt)
        index = filtered_prompts.index(prompt)
        filtered_prompts.pop(index)
        filtered_probabilities.pop(index)

    # Randomly mix the always_include_prompts within the unique_combination
    random.shuffle(always_include_prompts)
    insertion_points = random.sample(range(len(unique_combination) + 1), len(always_include_prompts))
    for prompt, index in zip(always_include_prompts, insertion_points):
        unique_combination.insert(index, prompt)

    return unique_combination

def modify_prompt(prompt):
    modified_prompt = prompt.replace('(', r'\(').replace(')', r'\)')
    return modified_prompt

def load_blacklist(filename):
    with open(filename, 'r') as file:
        blacklist = [word.strip() for word in file.read().split(",")]
    return blacklist

def ask_for_settings():
    always_include = input("Do you want to always include specific prompt(s)? (y/n): ")
    always_include_prompts = []
    if always_include.lower() == 'y':
        always_include_prompts_input = input("Enter the prompts you want to always include (separated by comma): ")
        always_include_prompts = [prompt.strip() for prompt in always_include_prompts_input.split(",")]

    min_length = int(input("Enter the minimum length of the output: "))
    max_length = int(input("Enter the maximum length of the output: "))
    return min_length, max_length, always_include_prompts

def main():
    filename = input("Enter the input file name or path: ")
    use_blacklist = input("Do you want to use a blacklist? (y/n): ")

    if use_blacklist.lower() == 'y':
        blacklist_filename = input("Enter the blacklist file name or path: ")
        blacklist = load_blacklist(blacklist_filename)
    else:
        blacklist = []

    with open(filename, 'r') as file:
        data = file.readlines()

    prompts = []
    probabilities = []

    for line in data:
        match = re.search(r"(.+?)\s+Times in dataset:\s+(\d+)", line)
        if match:
            prompt = match.group(1)
            probability = float(match.group(2)) / 100  # Convert to a decimal probability
            modified_prompt = modify_prompt(prompt)
            prompts.append(modified_prompt)
            probabilities.append(probability)

    min_length, max_length, always_include_prompts = ask_for_settings()

    combination = generate_combination(prompts, probabilities, blacklist, always_include_prompts, min_length, max_length)

    print("\n" + ", ".join(combination) + "\n")

    while True:
        more = input("Would you like another one? (y/n): ")
        if more.lower() == 'n':
            #Goes back to ask for settings
            min_length, max_length, always_include_prompts = ask_for_settings()

        combination = generate_combination(prompts, probabilities, blacklist, always_include_prompts, min_length, max_length)
        print("\n" + ", ".join(combination) + "\n")

if __name__ == '__main__':
    main()
