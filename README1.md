
# Welcome to the Project

This project is an example of parsing Markdown with custom Python scripts.

## Installation

To install the application, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

After installation, you can start the application using:

```python
python app.py
```

Make sure you have the necessary permissions.

### Configuration

Set up your application with the configuration below:

```yaml
# config.yml
database: 'path/to/database.db'
server:
  host: 'localhost'
  port: 8080
```

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.



## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

Save this content into a file named `README.md` in the same folder as your `query.py` script.

Now you can run your script with the command:


```shell
python3 query.py "SELECT header, codeblock FROM 'README.md'"
```


## Upgraded

Now the script can handle the following use cases:

1. `SELECT header FROM 'README.md' WHERE header='*Configuration*'`: This will print headers that include the word "Configuration".
2. `COUNT header FROM 'README.md'`: This will print the count of unique headers.
3. `SELECT codeblock FROM 'README.md' WHERE header='*Configuration*'`: This will print the first line from all codeblocks under headers that include the word "Configuration".

Run the script with the desired SQL-like query:

```shell
python3 query.py "SELECT codeblock FROM 'README.md' WHERE header='*Configuration*'"
```

Note that the WHERE clause uses asterisks (`*`) as wildcards for pattern matching and it is applied case-insensitively. The COUNT command only supports counting headers and assumes that headers are unique per Markdown file (no repeated headers with the same text).

The patterns used for regex matching and the overall script structure are simplified to demonstrate the concept. In a production environment, you would need to implement more robust error handling and potentially a more sophisticated parsing system to handle complex SQL-like queries and Markdown structures.




## Test


You can test this script by running the following commands:

```shell
# This command will print all code blocks without the "```" fences
python3 query.py "SELECT codeblock FROM 'README.md'"

# This command should print all headers in 'README.md'
python3 query.py "SELECT header FROM 'README.md'"

# This command should print the number of headers in 'README.md'
python3 query.py "COUNT header FROM 'README.md'"

# This command should print code blocks under headers with "Configuration" in the title
python3 query.py "SELECT codeblock FROM 'README.md' WHERE header='*Configuration*'"
```

