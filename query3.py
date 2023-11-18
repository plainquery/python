import sys
import re

# Custom exception for invalid queries
class InvalidQueryException(Exception):
    pass

# Parses the query and returns components
def parse_query(sql_query):
    pattern = re.compile(r"^(SELECT|COUNT)\s+(\S+?)\s+FROM\s+'([\w\.-]+)'\s*(WHERE\s+header\s*=\s*'(.+?)')?$", re.IGNORECASE)
    match = pattern.match(sql_query)
    if not match:
        raise InvalidQueryException("Invalid query format.")
    command, field, filename, where_clause, header_pattern = match.groups()
    # Modify header pattern to convert '*' wildcard to regex '.*'
    if header_pattern:
        header_pattern = re.compile(header_pattern.replace('*', '.*'), re.IGNORECASE)
    return command, field, filename, header_pattern

# Executes the parsed query on the Markdown file
def execute_query_on_markdown(command, field, markdown_file, header_pattern):
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {markdown_file} was not found.")

    # Patterns to find headers and code blocks
    header_pattern_regex = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)
    codeblock_pattern_regex = re.compile(r'```[\s\S]+?```')

    headers = [(match.group(1), match.group(2).strip()) for match in header_pattern_regex.finditer(content)]
    codeblocks = codeblock_pattern_regex.findall(content)

    # Associate headers with codeblocks
    header_to_codeblock = {}
    for (level, header), codeblock in zip(headers, codeblocks):
        header_to_codeblock[header] = codeblock.strip('```')

    results = []
    if command.upper() == 'SELECT':
        for header, code in header_to_codeblock.items():
            if not header_pattern or header_pattern.search(header):
                if 'header' in field.lower():
                    results.append(header)
                if 'codeblock' in field.lower():
                    first_line = code.split('\n', 1)[0]
                    results.append(first_line)

    elif command.upper() == 'COUNT':
        if 'header' in field.lower():
            if header_pattern:
                results = sum(1 for header in header_to_codeblock if header_pattern.search(header))
            else:
                results = len(header_to_codeblock)
        else:
            raise InvalidQueryException("COUNT operation is only supported for headers.")

    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py '<SELECT|COUNT> [header[,codeblock]] FROM \"filename.md\" [WHERE header=\"pattern\"]'")
        sys.exit(1)
    
    sql_query = sys.argv[1]
    try:
        command, field, filename, header_pattern = parse_query(sql_query)
        query_result = execute_query_on_markdown(command, field, filename, header_pattern)
        
        if isinstance(query_result, list):
            for result in query_result:
                print(result)
        else:
            print(query_result)
    except InvalidQueryException as e:
        print(f"Query Error: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
