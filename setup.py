from setuptools import setup,find_packages
from typing import List

def get_requirements()-> List[str]:
    """
    this function will return list of requirements
    """
    requirements_list :List[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines() ## read line from the file
            
            for line in lines:  ##process each line
                requirement = line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
             
    except FileNotFoundError:
        print("Requirements.txt file not found")

    return requirements_list

setup(
    name = "Fraud Detection",
    version = "0.0.1",
    author = "Jay Devmurari",
    author_email = "devmurarijay66@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)