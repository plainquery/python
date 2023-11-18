
To prevent Bash from treating the `!` as the start of a history expansion, you can either escape it with a backslash in the double-quoted SQL-like string or use single quotes around the SQL-like string and double quotes inside the values, like so:

```bash
python3 writer.py 'INSERT INTO '\''README.md'\'' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('\''Introduction'\'', '\''This is the intro text.'\'', '\''print("Hello World!")'\'', '\''python'\'')'
```


1. Create a file with the SQL-like statement, let's name it `query.txt`:

```txt
INSERT INTO 'README.md' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('Introduction', 'This is the intro text.', 'print("Hello World!")', 'python')
```

2. Use the `$(<filename)` Bash syntax to pass the content of `query.txt` to `writer.py`:

```bash
python3 writer.py "$(cat test.sql)"
```




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
python3 query.py "SELECT codeblock FROM 'README.md'"

# This command should print all headers in 'README.md'
python3 query.py "SELECT header FROM 'README.md'"

# This command should print the number of headers in 'README.md'
python3 query.py "COUNT header FROM 'README.md'"

# This command should print code blocks under headers with "Configuration" in the title
python3 query.py "SELECT codeblock FROM 'README.md' WHERE header='*Configuration*'"
```

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


Section inserted successfully into README.md!
```bash
python3 writer.py 'INSERT INTO '\''README.md'\'' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('\''Introduction'\'', '\''This is the intro text.'\'', '\''print("Hello World!")'\'', '\''python'\'') WHERE HeaderName="Introduction"' 
Query Error: Invalid SQL-like query format.
```

```bash
python3 writer.py 'INSERT INTO '\''README.md'\'' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('\''Introduction'\'', '\''This is the intro text.'\'', '\''print("Hello World!")'\'', '\''python'\'') WHERE HeaderName='\''Introduction'\'' ' 
Query Error: Invalid SQL-like query format.
```

```bash
python3 writer.py 'INSERT INTO '\''README.md'\'' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('\''Introduction'\'', '\''This is the intro text.'\'', '\''print("Hello World!")'\'', '\''python'\'') WHERE HeaderName='\''Introduction'\'' ' 
Query Error: Invalid SQL-like query format.
```

```bash
python3 writer.py "INSERT INTO 'README.md' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('New Section Header', 'Section content goes here.', 'print(\"Hello World\")', 'python') WHERE HeaderName='Introduction'"
Inserting under a specific header is not supported in this script.
```

```bash
nano test.sql
```

```bash
python3 writer.py "$(cat test.sql)"
Inserting under a specific header is not supported in this script.
```

```bash
python3 writer.py "$(cat test.sql)"
Section inserted successfully into README.md!
```

```bash
python3 writer.py "$(cat test.sql)"
Inserting under a specific header is not supported in this script.
```

```bash
python3 writer.py "$(cat test.sql)"
Section inserted successfully under header 'Installation' in README.md!
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Introduction'"
Section with header 'Introduction' deleted successfully from 'README.md'.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Installation'"
Section with header 'Installation' deleted successfully from 'README.md'.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Configuration'"
Section with header 'Configuration' deleted successfully from 'README.md'.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Configuration'"
No section with header 'Configuration' was found in 'README.md'.
```


```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Upgraded'"
No section with header 'Upgraded' was found in 'README.md'.
```


```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Test'"
No section with header 'Test' was found in 'README.md'.
```


```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Test*'"
No section with header '*Test*' was found in 'README.md'.
```


```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Test*'"
Section matching header pattern '.*Test.*' deleted successfully from 'README.md'.
```


```bash
cat README.md
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Test*'"
No headers found with pattern '*Test*'. Nothing was deleted.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Test*'"
Header(s) with the pattern '*Test*' deleted successfully.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Test*'"
Section with header matching pattern '.*Test.*' deleted successfully.
```


```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Contr*'"
Section with header matching pattern '.*Contr.*' deleted successfully.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Conf*'"
No section with header matching pattern 'Conf.*' was found.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='Conf*'"
No section with header matching pattern 'Conf.*' was found.
```

```bash
python3 deleter.py "DELETE FROM 'README.md' WHERE HeaderName='*Conf*'"
Section with header matching pattern '.*Conf.*' deleted successfully.
```
