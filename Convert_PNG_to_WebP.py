import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import multiprocessing
import time
import psutil

print("-----------------------------------------------------------------------------------------\n")
print("This script converts a folder of .png / .jpg / .jpeg / .bmp image files into .webp files.\n")
print("-----------------------------------------------------------------------------------------\n")

def convert_to_webp(input_files, input_folder, output_folder, progress_bar):
    for input_file in input_files:
        relative_path = os.path.relpath(input_file, input_folder)
        output_file = os.path.join(output_folder, relative_path)
        output_file = os.path.splitext(output_file)[0] + '.webp'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        subprocess.run(['./bin/cwebp.exe', '-q', '100', input_file, '-o', output_file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        progress_bar.update(1)


def get_system_load():
    return psutil.getloadavg()[0]


def adjust_instance_count(instance_count, system_load, target_load, min_instance_count, max_instance_count):
    if system_load > target_load:
        instance_count -= 1
        instance_count = max(instance_count, min_instance_count)
    else:
        instance_count += 1
        instance_count = min(instance_count, max_instance_count)
    return instance_count


def convert_folder_to_webp(input_folder, output_folder):
    input_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg', '.bmp')):
                input_files.append(os.path.join(root, file))

    num_cores = multiprocessing.cpu_count()
    instance_count = num_cores  # Set initial instance count equal to the number of processor cores
    peak_batch_speed = None
    prev_batch_time = None
    batch_size = 200
    target_system_load = 0.8
    min_instance_count = 1
    max_instance_count = num_cores

    total_files = len(input_files)
    with tqdm(total=total_files, desc='Converting Files', unit='files') as progress_bar:
        with ThreadPoolExecutor() as executor:
            for i in range(0, total_files, batch_size):
                batch_files = input_files[i:i + batch_size]
                start_time = time.time()

                executor.map(lambda file: convert_to_webp([file], input_folder, output_folder, progress_bar), batch_files)

                end_time = time.time()
                batch_time = end_time - start_time

                if prev_batch_time is None:
                    prev_batch_time = batch_time
                    peak_batch_speed = batch_time
                elif batch_time < peak_batch_speed:
                    instance_count = num_cores  # Set current instance count as the default
                    peak_batch_speed = batch_time

                system_load = get_system_load()
                instance_count = adjust_instance_count(instance_count, system_load, target_system_load,
                                                       min_instance_count, max_instance_count)

                progress_bar.set_postfix({'Instances': instance_count})
                time.sleep(0.1)  # Add a small delay before the next batch

    return instance_count

while True:
    # Ask the user for the input folder path
    while True:
        input_folder = input('Enter the folder path containing the image files (or type "exit" to quit): ')
        if input_folder.lower() == 'exit':
            print('Exiting the script...')
            exit()
        if os.path.exists(input_folder):
            break
        else:
            print('Input folder does not exist. Please try again.')

    # Ask the user for the output folder path
    output_folder = input('Enter the folder path for the converted WebP files: ')
    os.makedirs(output_folder, exist_ok=True)

    # Activate the virtual environment
    activate_script = os.path.join('venv', 'Scripts', 'activate') if os.name == 'nt' else os.path.join('venv', 'bin', 'activate')
    subprocess.call(activate_script, shell=True)

    # Convert the folder to WebP and optimize the instance count
    optimized_instance_count = convert_folder_to_webp(input_folder, output_folder)

    print('Conversion complete!')
    print(f'Optimized cwebp instance count: {optimized_instance_count}')
