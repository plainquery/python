import sys
import re

def parse_query(sql_query):
    mat = re.match(r"^(SELECT|COUNT)\s+(header|codeblock)\s+FROM\s+'(.+?)'(?:\s+WHERE\s+header='(.+?)')?$", sql_query, re.IGNORECASE)
    if not mat:
        raise ValueError("Invalid query format.")
    return mat.groups()

def find_headers_codeblocks(markdown_content):
    in_code_block = False
    headers = []
    code_blocks = []
    current_code_block = []
    current_header = None

    for line in markdown_content.splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block  # Toggle the boolean flag for codeblock state.
            if not in_code_block:  # We are closing a code block.
                if current_header is not None:  # We have a valid header.
                    code_block_str = "\n".join(current_code_block).strip()
                    code_blocks.append((current_header, code_block_str))
                current_code_block = []  # Reset the current code block for the next one.
        elif in_code_block:
            current_code_block.append(line)
        else:
            # Check if the line starts with a header pattern and capture the header text.
            header_match = re.match(r"^\s*(#{1,6})\s+(.*)$", line)
            if header_match:
                current_header = header_match.group(2).strip()
                headers.append(current_header)
    return headers, dict(code_blocks)

def execute_query_on_markdown(command, fields, markdown_file, header_filter_pattern):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Find headers and their corresponding code blocks.
    headers, code_blocks = find_headers_codeblocks(markdown_content)

    # Filter headers and code blocks if necessary.
    if header_filter_pattern:
        header_filter_regex = re.compile(header_filter_pattern.replace("*", ".*"), re.IGNORECASE)
        if fields.lower() == 'header':
            headers = filter(header_filter_regex.search, headers)
        else:
            code_blocks = {h: cb for h, cb in code_blocks.items() if header_filter_regex.search(h)}
    
    if command.upper() == 'SELECT':
        if fields.lower() == 'header':
            return headers
        elif fields.lower() == 'codeblock':
            return code_blocks.values()
    elif command.upper() == 'COUNT' and fields.lower() == 'header':
        return len(headers)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py '<SELECT|COUNT> header|codeblock FROM \"filename.md\" [WHERE header=\"*pattern*\"]'")
        sys.exit(1)

    try:
        command, fields, filename, header_filter_pattern = parse_query(sys.argv[1])
        results = execute_query_on_markdown(command, fields, filename, header_filter_pattern)
        if isinstance(results, int):  # COUNT result
            print(results)
        else:  # SELECT result
            for res in results:
                print(res)
    except ValueError as e:
        print(f"Error parsing query: {e}")
    except FileNotFoundError as e:
        print(f"Markdown file not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
