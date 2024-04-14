def process_line(line):
    colon_index = line.find(':')
    if colon_index != -1 and line[colon_index - 1].isdigit():
        content = line[colon_index + 1 :].split("  ")[0]
        return content.strip()
    return ""

input_file_path = "N++ search.txt"
output_file_path = input_file_path.replace('.txt', '_trimmed.txt')

with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    lines = input_file.readlines()
    trimmed_lines = [process_line(line) for line in lines]
    trimmed_lines = [line for line in trimmed_lines if line != ""]
    
    output_file.write(', '.join(trimmed_lines))

print(f"Trimmed lines saved to {output_file_path}")
input()