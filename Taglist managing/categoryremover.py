def delete_lines_not_in_file(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines_file1 = set(f1.read().splitlines())
        lines_file2 = set(f2.read().splitlines())

    lines_file1 = lines_file1.difference(lines_file2)

    new_file = f"{file1} - modified"
    with open(new_file, 'w') as modified_file:
        modified_file.write('\n'.join(lines_file1))

    print(f"Modified file '{new_file}' created.")


if __name__ == "__main__":
    file1 = input("Enter the path to file you need cleaned up: ")
    file2 = input("Enter the tag list file: ")

    delete_lines_not_in_file(file1, file2)
