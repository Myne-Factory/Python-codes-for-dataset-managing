import os
import subprocess


def create_virtual_environment():
    # Create a virtual environment named "venv"
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)


def activate_virtual_environment():
    # Activate the virtual environment
    activate_script = os.path.join('venv', 'Scripts', 'activate') if os.name == 'nt' else os.path.join('venv', 'bin', 'activate')
    subprocess.run(activate_script, shell=True, check=True)


def install_libraries():
    # Install the required libraries
    subprocess.run(['pip', 'install', 'Pillow'], check=True)
    subprocess.run(['pip', 'install', 'tqdm'], check=True)


def main():
    # Create virtual environment
    create_virtual_environment()

    # Activate virtual environment
    activate_virtual_environment()

    # Install libraries
    install_libraries()

    print('Setup completed successfully.')


if __name__ == '__main__':
    main()
