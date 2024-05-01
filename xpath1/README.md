Certainly! I've updated the script to accept command-line arguments and added a help flag. You can now run the script with the following options:


```bash
py main.py --url https://example.com --xpath "//p" --format txt
```

```bash
py main.py --url https://example.com --xpath "//p" --format json
```

```bash
py main.py --url https://example.com --xpath "//div[@class='item']" --format json
```

