def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

input_file_path = input("Enter file: ")
output_file_path = input_file_path.replace('.txt', '_noduplicates.txt')

with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    lines = input_file.read().split(', ')
    deduplicated_lines = remove_duplicates(lines)
    
    output_file.write(', '.join(deduplicated_lines))

print(f"Duplicate tags removed! New file saved as {output_file_path}.")
input()
