# Getting Started

Follow the instructions below to get started.

```bash
echo "Hello, world!"
```

# Introduction

This is the intro text.

```python
print("Hello World!")
```


# Welcome to the Project

This project is an example of parsing Markdown with custom Python scripts.

## Installation

To install the application, run the following command:

```bash
pip install -r requirements.txt
```




# Getting Started
Follow the instructions below to get started.
```bash
echo "Hello, world!"
```
## Usage

After installation, you can start the application using:

```python
python app.py
```

Make sure you have the necessary permissions.

# config.yml
database: 'path/to/database.db'
server:
  host: 'localhost'
  port: 8080
```

# This command will print all code blocks without the "```" fences
python3 query.py "SELECT codeblock FROM 'README.md'"

# This command should print all headers in 'README.md'
python3 query.py "SELECT header FROM 'README.md'"

# This command should print the number of headers in 'README.md'
python3 query.py "COUNT header FROM 'README.md'"

# Introduction

This is the intro text.

```python
print("Hello World!")
```


Implementing insertion at a specific location in a Markdown file requires parsing the file, identifying the target header, and adding content in the right place. Below is an implementation that fulfills this requirement without external libraries.

Please note this example is quite basic. It assumes headers are unique and sorts `H1` headers only. For more robust handling, consider using a library dedicated to Markdown parsing and editing.



Now you can call `writer.py` with a `WHERE` clause to insert a new section under a specific header named "Introduction" with the following command:

```bash
python3 writer.py "INSERT INTO 'README.md' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('New Section', 'New section content.', 'Code for the new section', 'bash') WHERE HeaderName='Introduction'"
```

This update will search for the header named "Introduction" in the `README.md` file and insert the new section just beneath it. If the header is not found, it appends the section to the end of the file. If no `WHERE` clause is provided, the section will be inserted at the beginning as per the default behavior.
