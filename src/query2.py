import sys
import re

# Function to parse the SQL-like query and return the appropriate components
def parse_query(sql_query):
    query_components = re.match(r"^(SELECT|COUNT) (.+?) FROM '(.+?)'(\s*WHERE header='(.+?)')?$", sql_query, re.IGNORECASE)
    if not query_components:
        print("Invalid query format. Please use: SELECT header[, codeblock] FROM 'filename.md'[ WHERE header='pattern']")
        return None, None, None, None

    command, fields, filename, _, header_filter = query_components.groups()
    if header_filter:
        header_filter = header_filter.replace('*', '.*')  # Replace * with regex wildcard
    return command, fields, filename, header_filter

# Function to execute the parsed query on the Markdown file
def execute_query_on_markdown(command, fields, markdown_file, header_filter):
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"The file {markdown_file} was not found.")
        return []

    # Compile regex patterns for headers and code blocks
    headers_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
    codeblock_pattern = re.compile(r'```[\s\S]+?```')

    # Find all headers and code blocks
    headers = headers_pattern.findall(content)
    codeblocks = codeblock_pattern.findall(content)

    # Extract headers with their corresponding code blocks
    header_to_codeblock = {}
    current_header = None
    for index, line in enumerate(content.splitlines()):
        header_match = headers_pattern.match(line)
        if header_match:
            current_header = header_match.group(1).strip()
            continue
        if current_header and codeblock_pattern.match(line):
            codeblock_content = codeblocks.pop(0)
            header_to_codeblock[current_header] = codeblock_content

    results = []
    if command.upper() == 'SELECT':
        for header, codeblock in header_to_codeblock.items():
            if (not header_filter) or re.search(header_filter, header, re.IGNORECASE):
                if 'header' in fields.lower():
                    results.append(header)
                if 'codeblock' in fields.lower():
                    results.append(codeblock.split('\n', 1)[0])  # First line of code block
    elif command.upper() == 'COUNT':
        return len(headers)

    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py '<COMMAND> [header[, codeblock]] FROM \"filename.md\"[ WHERE header=\"pattern\"]'")
        sys.exit(1)

    sql_query = sys.argv[1]
    command, fields, filename, header_filter = parse_query(sql_query)
    if not command or not fields or not filename:
        print("Invalid query. Please ensure the query format is correct.")
        sys.exit(1)

    query_result = execute_query_on_markdown(command, fields, filename, header_filter)

    if isinstance(query_result, int):
        print(f"Count: {query_result}")
    else:
        for result in query_result:
            print(result)
