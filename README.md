# Flask Demo Repository

## Table of Contents

1. [Introduction](#introduction)
2. [Repository Structure](#repository-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Projects](#projects)
6. [Contributing](#contributing)
7. [Licence](#licence)
8. [Contact](#contact)

## Introduction
* Welcome to the FLask Demo Repository! This repository contains various subprojects demonstrating how to implement common features and functionalities using Flask
* Whether you are a beginner on an experienced developer, you'll find experience snippets to help you understan and utilize Flask in your own projects

## Repository Structure
* This repository is organized into subdirectories, each representing a specific feature or functionality demonstrated with Flask
* Each subdirectory contains its own README.md explaining the specific project, setup instructions, and usage details
* Here is the structure:

flask/
├── basic-authentication/
| |-----README.md
| |-----app.py
| |-----templates
| |-----static/
|       |____css/
\________________________

## Installation
* To get started with this repository, follow these steps

1. **Clone the Repository**: clone the repository to your local machine
    '''sh
        git fork https://github.com/Emogy-reunion/flask.git
        cd flask
    '''

2. **Create a Virtual Environment**: Ensure you have python and virtualenv installed. Create and activate a virtual environment
    '''sh
        python3 -m venv venv
        source venv/bin/activate
    '''

3. **Install Dependencies**: Install the required dependencies from `requirements.txt`.
    '''sh
         pip install -r requirements.txt
    '''

## Usage
* Each directory is a standalone python project: let's say you want to use basic authentication

1. **Navigate to the Project directory**:
    '''sh
        cd basic-authentication
    '''
2. **Run the Application**:
    '''sh
        python app.py
    '''
* The application should now be running, and you can access it in your browser at `http://127.0.0.1:5000`.

## Projects
* Here's a list of the projects included in this repository:

1: basic-authentication: 
* It demonstrates user registration, login, and authentication mechanisms
* Password hashing and email verification is not handled

## License
* This project is licence under the MIT License

## Contact
* If you have any questions, feel free to reach out

   -**Mark Victor Mugendi**
   -**Email:** mv7786986@gmail.com

