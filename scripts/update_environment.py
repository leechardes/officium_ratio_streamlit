import os
import subprocess
import sys
import pkg_resources
from pkg_resources import parse_version
import datetime

def get_latest_version(package_name):
    try:
        latest_version = subprocess.check_output([sys.executable, '-m', 'pip', 'install', f'{package_name}==random'], stderr=subprocess.STDOUT)
        latest_version = latest_version.decode('utf-8')
        latest_version = latest_version.split('(from versions:')[1].split(')')[0].strip().split(',')[-1].strip()
        return latest_version
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        if "Could not find a version that satisfies the requirement" in output:
            versions = output.split('(from versions:')[1].split(')')[0].strip().split(',')
            return versions[-1].strip()
    return None

def update_requirements():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    requirements_path = os.path.join(project_root, 'requirements.txt')
    log_dir = os.path.join(project_root, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f'update_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

    updated_requirements = []
    updates = []

    with open(requirements_path, 'r') as file:
        requirements = file.readlines()

    for req in requirements:
        package_name = req.strip().split('==')[0]
        current_version = req.strip().split('==')[1] if '==' in req else None
        latest_version = get_latest_version(package_name)

        if latest_version and (not current_version or parse_version(latest_version) > parse_version(current_version)):
            updated_requirements.append(f'{package_name}=={latest_version}\n')
            updates.append(f'Updated {package_name}: {current_version or "Not specified"} -> {latest_version}')
        else:
            updated_requirements.append(req)

    with open(requirements_path, 'w') as file:
        file.writelines(updated_requirements)

    with open(log_path, 'w') as log_file:
        log_file.write(f'Update performed on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        if updates:
            log_file.write('\n'.join(updates))
        else:
            log_file.write('No updates were necessary. All packages are up to date.')

    print(f'Requirements updated. Log file created at {log_path}')

if __name__ == '__main__':
    update_requirements()