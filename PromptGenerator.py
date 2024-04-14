import random
import re
import configparser
import os

print("---------------------------------------------------------------------------------------------------\n")
print("This script creates a random prompt based off of a text file created by PromptsToTimesInDataset.py.")
print("Look in the \"PromptGenerator\" folder to modify the outputs.\n")

print("  1. The \"PromptGenerator.ini\" has the file locations and min/max weights.\n")
print("  2. The \"blacklist.txt\" has the tags you want to avoid in random generation. The tags are seperated by a comma.\n")
print("  3. The \"Don't combine.txt\" has the tags you don't want to combine with each other (like sitting and standing).")
print("     The tags are seperated by a comma. Each instruction for a tag starts in their own row with this style:")
print("     standing = lying, sitting, wariza\n")
print("  4. The \"Alwayspick.txt\" has tags you want to always appear. It picks one random tag from each row.")
print("     The tags are seperated by a comma. You can ignore rows by starting them with \"--\".\n")
print("---------------------------------------------------------------------------------------------------\n")

def load_ini_file():
    config = configparser.ConfigParser()

    if not os.path.exists("./PromptGenerator/"): #Most likely the first time running the script, no folder yet.
        os.makedirs("./PromptGenerator/") # Create a PromptGenerator folder
            
        #Create the blacklist.txt file
        with open("./PromptGenerator/blacklist.txt", "w") as file:
            file.write("")
            
        #Create the Don't combine.txt file
        with open("./PromptGenerator/Don't combine.txt", "w") as file:
            file.write("")
            
        #Create the Alwayspick.txt file
        with open("./PromptGenerator/Alwayspick.txt", "w") as file:
            file.write("")

    if not os.path.exists("./PromptGenerator/PromptGenerator.ini"):
        # Create a config file if it doesn't exist
        config["File Locations"] = {
            "PromptList": "",
            "Blacklist": "./PromptGenerator/blacklist.txt",
            "DontCombine": "./PromptGenerator/Don't combine.txt",
            "AlwaysPick": "./PromptGenerator/Alwayspick.txt"
        }
        config["Random weight values"] = {
            "A1111_Min_weight": "0.8",
            "A1111_Max_weight": "1.5",
            "InvokeAI_Min_Weight": "0.8",
            "InvokeAI_Max_Weight": "1.5"
        }        
        with open("./PromptGenerator/PromptGenerator.ini", "w") as configfile:
            config.write(configfile)

    # Read the configuration from the ini file
    config.read("./PromptGenerator/PromptGenerator.ini")
    
    prompt_list_file = config.get("File Locations", "PromptList")
    blacklist_file = config.get("File Locations", "Blacklist")
    dont_combine_file = config.get("File Locations", "DontCombine")
    always_pick_file = config.get("File Locations", "AlwaysPick")
    A1111_Min_weight = int(float(config.get("Random weight values", "A1111_Min_weight"))*10)
    A1111_Max_weight = int(float(config.get("Random weight values", "A1111_Max_weight"))*10)
    InvokeAI_Min_Weight = int(float(config.get("Random weight values", "InvokeAI_Min_Weight"))*10)
    InvokeAI_Max_Weight = int(float(config.get("Random weight values", "InvokeAI_Max_Weight"))*10)
    

    if not os.path.exists(prompt_list_file):
        print("\n    No tag list provided in PromptGenerator.ini.")
        input()
        exit()

    if not os.path.exists(blacklist_file):
        print("Blacklist could not be found. Continuing without it.")

    if not os.path.exists(dont_combine_file):
        print("DontCombine could not be found. Continuing without it.")

    return prompt_list_file, blacklist_file, dont_combine_file, always_pick_file, A1111_Min_weight, A1111_Max_weight, InvokeAI_Min_Weight, InvokeAI_Max_Weight


#-----------------------------------------------------#
#-----------Ask the user for the settings-------------#
#-----------------------------------------------------#
def ask_for_user_settings():
    
    
    #---------------Ask for specific prompts---------------#
    QuestionSuccess = False
    while QuestionSuccess == False:
        always_include = input("Would you like to always use specific prompts? (y/n): ")
        if always_include == "y" or always_include == "n":
                QuestionSuccess = True
                
    always_include_prompts = []
    if always_include.lower() == 'y':
        always_include_prompts_input = input("Enter the prompts you want to always include (separated by comma): ")
        always_include_prompts = [prompt.strip() for prompt in always_include_prompts_input.split(",")]
           
    #---------------Ask if the user wants to use Alwayspick---------------#
    QuestionSuccess = False
    while QuestionSuccess == False:
        AlwayspickQuestion = input("Would you like to make use of Alwayspick.txt? (y/n): ")
        if AlwayspickQuestion == "y" or AlwayspickQuestion == "n":
                QuestionSuccess = True
        if AlwayspickQuestion.lower() == 'y':
            AlwaysPick = True
        else:
            AlwaysPick = False    
        
    #---------------Ask for tag weights---------------#
    QuestionSuccess = False
    while QuestionSuccess == False:
        tagWeightsQuestion = input("Would you like to add weights to tags? (y/n): ")
        if tagWeightsQuestion == "y" or tagWeightsQuestion == "n":
                QuestionSuccess = True
        if tagWeightsQuestion.lower() == 'y':
            TagWeights = True
        else:
            TagWeights = False

    #---------------Ask the user for the length of the prompt----------#
    QuestionSuccess = False
    while QuestionSuccess == False:
        min_lengthQuestion = input("Enter the minimum length of the prompt: ")
        if min_lengthQuestion.isdigit():
            min_length = int(min_lengthQuestion)
            QuestionSuccess = True
        else: print(f"The answer must be a number.\n")
        
    QuestionSuccess = False
    while QuestionSuccess == False:
        max_lengthQuestion = (input("Enter the maximum length of the prompt: "))
        if max_lengthQuestion.isdigit():
            max_length = int(max_lengthQuestion)
            if(max_length >= min_length):
                QuestionSuccess = True
            else: print(f"The answer must be larger than the minimum length.\n")
        else: print(f"The answer must be a number.\n")

    return min_length, max_length, always_include_prompts, TagWeights, AlwaysPick

def process_prompt_list(prompt_list_file):
    # Read the prompt list file and create a table of prompts with their percentages
    with open(prompt_list_file, 'r') as file:
        data = file.readlines()

    prompt_table = []

    for line in data:
        parts = line.strip().split("Times in dataset:")
        if len(parts) != 2:
            continue
        prompt = parts[0].strip()
        percent_match = re.search(r"(\d+\.\d+)%", parts[1].strip())
        if percent_match:
            percent = float(percent_match.group(1)) / 100.0
            if percent != 0:  # Remove prompts with a value of 0
                prompt_table.append((prompt, percent))

    return prompt_table

#-----------------The alwayspick script----------------#
def always_pick_prompts(always_pick_file, prompt_table):
    if not os.path.exists(always_pick_file):
        return prompt_table

    with open(always_pick_file, 'r') as file:
        always_pick_data = file.readlines()

    always_pick_list = []
    alwaysPickRowNumber = 0
    for row in always_pick_data:
        row = row.strip()
        if row:     #Removes empty rows
            if row.startswith("--") == False:    #Ignores comments
                alwaysPickRowNumber +=1
                tags = [tag.strip() for tag in row.split(",")]
                if len(tags) >= 1:
                    always_pick_list.append(tags)

    always_pick_prompts = []
    for tag_group in always_pick_list:
        if tag_group:
            random_tag = random.choice(tag_group)
            always_pick_prompts.append((random_tag, 99999 + alwaysPickRowNumber))

    prompt_table += always_pick_prompts

    return prompt_table

#-----------------The blacklist script----------------#
def process_blacklist(blacklist_file, prompt_table):
    if not os.path.exists(blacklist_file):
        return prompt_table

    with open(blacklist_file, 'r') as file:
        blacklist_data = file.readlines()

    blacklist = []
    current_tags = []
    for row in blacklist_data:
        row = row.strip()
        if row:
            current_tags.extend([tag.strip() for tag in row.split(",")])
        else:
            blacklist.append(current_tags)
            current_tags = []

    if current_tags:
        blacklist.append(current_tags)

    prompt_table = [(prompt, percent) for prompt, percent in prompt_table if prompt not in flatten(blacklist)]

    return prompt_table

def flatten(lst):
    return [item for sublist in lst for item in sublist]

def add_random(prompt_table):
    updated_prompt_table = []

    # Add some randomness to the prompt percentages
    for prompt, percent in prompt_table:
        updated_percent = percent + random.random()
        updated_prompt_table.append((prompt, updated_percent))

    return updated_prompt_table

def process_dont_combine(dont_combine_file, prompt_table):
    if not os.path.exists(dont_combine_file):
        return prompt_table

    with open(dont_combine_file, 'r') as file:
        dont_combine_data = file.readlines()

    dont_combine_dict = {}
    for row in dont_combine_data:
        row = row.strip()
        if row:
            tags = [tag.strip() for tag in row.split("=")]
            if len(tags) == 2:
                main_tag = tags[0]
                related_tags = [tag.strip() for tag in tags[1].split(",")]
                dont_combine_dict[main_tag] = related_tags

    for main_tag, related_tags in dont_combine_dict.items():
        main_tag_percent = get_tag_percent(main_tag, prompt_table)
        if main_tag_percent is None:
            continue

        max_related_tag_percent = max([get_tag_percent(tag, prompt_table) for tag in related_tags if get_tag_percent(tag, prompt_table) is not None], default=None)
        if max_related_tag_percent is None or main_tag_percent < max_related_tag_percent:
            prompt_table = [(prompt, percent) for prompt, percent in prompt_table if prompt != main_tag]

    return prompt_table

def get_tag_percent(tag, prompt_table):
    for prompt, percent in prompt_table:
        if prompt == tag:
            return percent
    return None

#--------User defined mandatory prompts-----------#
def add_always_include_prompts(always_include_prompts, prompt_table):
    # Add always include prompts to the prompt table
    for prompt in always_include_prompts:
        prompt_table.append((prompt, 999999))

    return prompt_table

def select_random_prompts(prompt_table, min_length, max_length):

    # Sort the prompt table based on the updated percentages
    prompt_table.sort(key=lambda x: x[1], reverse=True)

    # Select a random number of prompts within the specified length range
    combination_length = random.randint(min_length, max_length)
    selected_prompts = prompt_table[:combination_length]

    return selected_prompts

def print_selected_prompts(selected_prompts, TagWeights, DiffuserType, A1111_Min_weight, A1111_Max_weight, InvokeAI_Min_Weight, InvokeAI_Max_Weight):
    # Print the selected prompts
    formatted_prompts = [modify_prompt(prompt, TagWeights, DiffuserType, A1111_Min_weight, A1111_Max_weight, InvokeAI_Min_Weight, InvokeAI_Max_Weight) for prompt, percent in selected_prompts]
    output = ", ".join(formatted_prompts)
    print(f"\n{output}\n")

def modify_prompt(prompt, TagWeights, DiffuserType, A1111_Min_weight, A1111_Max_weight, InvokeAI_Min_Weight, InvokeAI_Max_Weight):
    # Modify the prompt to escape parentheses
    remove_parenthesis = prompt.replace('(', r'\(').replace(')', r'\)')
    
    if TagWeights == True:
        if DiffuserType == "1":
            modified_prompt = f"({remove_parenthesis}:{random.randrange(A1111_Min_Weight,A1111_Max_Weight)/10})"
        if DiffuserType == "2":
            modified_prompt = f"({remove_parenthesis}){random.randrange(InvokeAI_Min_Weight,InvokeAI_Max_Weight)/10}"
            
    else:
        modified_prompt = remove_parenthesis
        
    return modified_prompt


def main():
    prompt_list_file, blacklist_file, dont_combine_file, always_pick_file, A1111_Min_weight, A1111_Max_weight, InvokeAI_Min_Weight, InvokeAI_Max_Weight = load_ini_file()
    questions_asked = False
    
    #---------Ask the uer for the webui type-----------#
    QuestionSuccess = False
    while QuestionSuccess == False:
        DiffuserType = input("A1111 webui (1) or InvokeAI (2)? (1/2): ")
        if DiffuserType == "1" or DiffuserType == "2":
            QuestionSuccess = True
        else: print(f"The answer must be 1 or 2.\n")        
        
    while True:
        # Process the prompt list and apply filters
        prompt_table = process_prompt_list(prompt_list_file)
        prompt_table = process_blacklist(blacklist_file, prompt_table)
        prompt_table = add_random(prompt_table)
        prompt_table = process_dont_combine(dont_combine_file, prompt_table)

        if questions_asked == False:
            # Ask user for settings only once
            min_length, max_length, always_include_prompts, TagWeights, AlwaysPick = ask_for_user_settings()
            questions_asked = True

        if always_include_prompts:
            # Add always include prompts to the prompt table
            prompt_table = add_always_include_prompts(always_include_prompts, prompt_table)

        if always_pick_file and AlwaysPick == True:
            # Always pick prompts from the specified file
            prompt_table = always_pick_prompts(always_pick_file, prompt_table)

        # Select and print random prompts
        selected_prompts = select_random_prompts(prompt_table, min_length, max_length)
        print_selected_prompts(selected_prompts, TagWeights, DiffuserType, A1111_Min_weight, A1111_Max_weight, InvokeAI_Min_Weight, InvokeAI_Max_Weight)

        QuestionSuccess = False
        while QuestionSuccess == False:
            another_one = input("Would you like another one? (y/n): ")
            if another_one.lower() == 'n':
                questions_asked = False
                QuestionSuccess = True

            if another_one.lower() == 'y':
                QuestionSuccess = True
                continue
                
        


if __name__ == '__main__':
    main()
