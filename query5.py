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

    command, field, filename, header_filter_pattern = match.groups()
    return command, field, filename, header_filter_pattern

def execute_query_on_markdown(command, field, markdown_file, header_filter_pattern):
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {markdown_file} was not found.")

    # Compile regex patterns for Markdown headers and code blocks
    header_pattern = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)
    codeblock_pattern = re.compile(r'```.*\n([\s\S]*?)\n```', re.MULTILINE)

    headers = [(m.group(2), m.start()) for m in header_pattern.finditer(content)]
    codeblocks = [(m.group(1), m.start()) for m in codeblock_pattern.finditer(content)]

    # If a header filter pattern was provided, compile it to a regex object
    if header_filter_pattern:
        header_filter_regex = re.compile(header_filter_pattern.replace('*', '.*'), re.IGNORECASE)

    results = []
    if command.upper() == 'SELECT' and field.lower() == 'header':
        # Extract headers, apply filter if needed
        headers = [header for header, _ in headers]
        if header_filter_pattern:
            headers = [h for h in headers if header_filter_regex.search(h)]
        return headers

    if command.upper() == 'SELECT' and field.lower() == 'codeblock':
        for header, header_start in headers:
            codeblock = next(((cb, cb_start) for cb, cb_start in codeblocks if cb_start > header_start), ("", 0))
            if header_filter_pattern:
                if not header_filter_regex.search(header):
                    continue
            results.append(codeblock[0])

    elif command.upper() == 'COUNT' and field.lower() == 'header':
        filtered_headers = [header for header, _ in headers]
        if header_filter_pattern:
            filtered_headers = [h for h in filtered_headers if header_filter_regex.search(h)]
        return len(set(filtered_headers))

    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py '<SELECT|COUNT> [header|codeblock] FROM \"filename.md\" [WHERE header=\"*pattern*\"]'")
        sys.exit(1)

    sql_query = sys.argv[1]
    try:
        command, field, filename, header_filter_pattern = parse_query(sql_query)
        query_results = execute_query_on_markdown(command, field, filename, header_filter_pattern)

        if isinstance(query_results, int):  # Result from COUNT
            print(query_results)
        else:  # Results from SELECT
            for result in query_results:
                print(result)
    except ValueError as e:
        print(f"Query Error: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
