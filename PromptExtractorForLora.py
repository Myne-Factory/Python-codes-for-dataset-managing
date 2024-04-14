import os
import shutil

print("--------------------------------------------------------------------------------\n")
print("This script copies images and their prompt files that have a matching input tag.\n")
print("--------------------------------------------------------------------------------\n")

def check_folder_exists(folder_path):
    return os.path.exists(folder_path) and os.path.isdir(folder_path)

def check_file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)

def get_image_files(folder_path):
    image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".bmp"]  # Add more extensions if needed
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files

def split_into_tables(text):
    tables = []
    lines = text.strip().split(";")
    for line in lines:
        table_row = line.strip().split(", ")
        tables.append(table_row)
    return tables

def copy_files_with_tag(input_folder, output_folder, desired_tag, specific_subtag, keep_all_primary_tags, keep_subtags, create_subfolders):
    num_copied_images = 0
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".txt"):
                text_file_path = os.path.join(root, file)
                image_file_path = os.path.splitext(text_file_path)[0] + ".webp"

                if not check_file_exists(image_file_path):
                    continue

                with open(text_file_path, "r") as f:
                    contents = f.read()

                tags = split_into_tables(contents)

                filtered_tags = []
                primary_tag = None

                for tag_set in tags:
                    if desired_tag in tag_set:
                        primary_tag = tag_set[0]
                        if specific_subtag:
                            if specific_subtag in tag_set:
                                filtered_tags = tag_set
                        else:
                            filtered_tags = tag_set

                if filtered_tags:
                    output_text = "\n".join(filtered_tags)

                    if not keep_subtags:
                        if primary_tag:
                            output_text = primary_tag + "\n"

                    if create_subfolders:
                        output_folder_path = os.path.join(output_folder, os.path.relpath(root, input_folder))
                    else:
                        output_folder_path = output_folder

                    os.makedirs(output_folder_path, exist_ok=True)

                    output_text_file = os.path.join(output_folder_path, file)
                    output_image_file = os.path.join(output_folder_path, os.path.basename(image_file_path))

                    with open(output_text_file, "w") as f:
                        f.write(output_text)

                    shutil.copy(image_file_path, output_image_file)
                    num_copied_images += 1

    return num_copied_images

def main():
    input_folder = ""
    output_folder = ""
    desired_tag = ""
    specific_subtag = None
    keep_all_primary_tags = False
    keep_subtags = False
    create_subfolders = False

    while not check_folder_exists(input_folder):
        input_folder = input("Enter the input folder path: ")

    while not check_folder_exists(output_folder):
        output_folder = input("Enter the output folder path: ")
        os.makedirs(output_folder, exist_ok=True)

    desired_tag = input("Enter the desired tag: ")

    specific_subtag_input = input("Are you looking for a specific subtag? (y/n): ")
    if specific_subtag_input.lower() == "y":
        specific_subtag = input("Enter the specific subtag: ")

    keep_all_primary_tags_input = input("Do you want to keep all primary tags? (y/n): ")
    if keep_all_primary_tags_input.lower() == "y":
        keep_all_primary_tags = True

    keep_subtags_input = input("Do you want to keep the subtags? (y/n): ")
    if keep_subtags_input.lower() == "y":
        keep_subtags = True

    create_subfolders_input = input("Do you want to create subfolders in the output folder? (y/n): ")
    if create_subfolders_input.lower() == "y":
        create_subfolders = True

    num_copied_images = copy_files_with_tag(
        input_folder, output_folder, desired_tag, specific_subtag,
        keep_all_primary_tags, keep_subtags, create_subfolders
    )

    print(f"{num_copied_images} images copied successfully.")
    input("Press Enter to exit.")

if __name__ == "__main__":
    main()
