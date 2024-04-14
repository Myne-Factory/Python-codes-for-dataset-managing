def read_tags(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        tags = [line.strip().split(', ') for line in lines]
    return tags

def filter_tags(input_tags, source_tags):
    filtered_tags = []
    for tags in input_tags:
        filtered_tags.append([tag for tag in tags if tag in source_tags])
    return filtered_tags

def write_tags(filtered_tags, output_file_path):
    with open(output_file_path, 'w') as file:
        for tags in filtered_tags:
            line = ', '.join(tags)
            file.write(line + '\n')

input_file_path = input("Enter the path to the input file: ")
source_file_path = input("Enter the path to the source file: ")
output_file_path = input_file_path.replace('.txt', '_filtered.txt')

input_tags = read_tags(input_file_path)
source_tags = set(tag for tags in read_tags(source_file_path) for tag in tags)
filtered_tags = filter_tags(input_tags, source_tags)
write_tags(filtered_tags, output_file_path)

print(f"Filtered tags saved to {output_file_path}")
