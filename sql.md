
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
