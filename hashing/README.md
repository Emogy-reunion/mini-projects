# Hashing passwords using flask_bcrypt
* Hashing a password is a process of transforming the password into a fixed-size string of characters, which is typically a sequence of numbers and letters.
* This transformation is done using a cryptographic hashing algorithm.
* The resulting hashed value, or hash, is unique to each input and is designed to be irreversible, meaning it cannot be converted back into the original password.
* Hashing passwords is an important security matter since it ensures that during a data breach your passwords are safe

## Installation
* To get started with this directory
1. clone the repository
```sh
     git fork https://github.com/Emogy-reunion/flask.git
     cd flask
```

2. Navigate to the directory
```sh
    cd hash
```

3. Create and activate a virtual environment
```sh
    python3 -m venv myenv
    source myenv/bin/activate
```

4. Install dependencies in the requirements.txt using pip
```
    pip install -r requirements.txt
```

5. Run the python application
```sh
    python app.py
```
* The application should now be running, and you can access it in your browser at http://127.0.0.1:5000.
