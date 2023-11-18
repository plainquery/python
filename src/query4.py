import sys
import re

def parse_query(sql_query):
    pattern = re.compile(
        r"^(SELECT|COUNT)\s+(header|codeblock)\s+FROM\s+'([\w\.-]+)'(?:\s+WHERE\s+header='(.*)')?$",
        re.IGNORECASE
    )
    match = pattern.match(sql_query)
    if not match:
        raise ValueError("Invalid query format.")

    command, field, filename, header_filter = match.groups()
    if header_filter:
        header_filter = re.compile(header_filter.replace('*', '.*'), re.IGNORECASE)
    return command, field, filename, header_filter

def execute_query_on_markdown(command, field, markdown_file, header_filter):
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {markdown_file}")

    # Find all headers
    header_pattern = re.compile(r'^(#+)\s+(.*?)\s*$', re.MULTILINE)
    headers = [match.group(2) for match in header_pattern.finditer(content)]

    # Filter headers if WHERE clause is used
    if header_filter:
        headers = [h for h in headers if header_filter.search(h)]

    # Count headers if COUNT command is used
    if command.upper() == 'COUNT' and field.lower() == 'header':
        return len(set(headers))

    # Find all codeblocks
    if field.lower() == 'codeblock':
        codeblock_pattern = re.compile(r'```[\s\S]+?```')
        codeblocks = [match.group(0).strip('`').split('\n', 1)[0] for match in codeblock_pattern.finditer(content)]

        if header_filter:
            # If header filter is applied, we need to associate headers with codeblocks
            header_to_codeblock = {}
            for header in headers:
                header_index = content.find(header)
                for codeblock in codeblocks:
                    codeblock_index = content.find(codeblock)
                    if codeblock_index > header_index:
                        header_to_codeblock[header] = codeblock
                        codeblocks.remove(codeblock)
                        break

            # Return only codeblocks that are under filtered headers
            return [cb for h, cb in header_to_codeblock.items()]

        return codeblocks

    # Default case, return headers
    return headers

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py '<SELECT|COUNT> [header|codeblock] FROM \"filename.md\" [WHERE header=\"*pattern*\"]'")
        sys.exit(1)

    sql_query = sys.argv[1]
    try:
        command, field, filename, header_filter = parse_query(sql_query)
        query_results = execute_query_on_markdown(command, field, filename, header_filter)

        if isinstance(query_results, list):
            for result in query_results:
                print(result)
        else:  # If COUNT command was used
            print(query_results)
    except ValueError as e:
        print(f"Query Error: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
