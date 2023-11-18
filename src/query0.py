import sys
import re

# Function to simulate executing an SQL-like query on a Markdown file
def execute_query_on_markdown(sql_query):
    # Simplified SQL parsing to extract the filename from the query
    match = re.match(r"SELECT header, codeblock FROM '(.+)'", sql_query, re.IGNORECASE)
    if not match:
        print("Invalid query format. Use: SELECT header, codeblock FROM 'filename.md'")
        return []

    markdown_file = match.group(1)
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"The file {markdown_file} was not found.")
        return []

    # Regex pattern to match headers and following code blocks (non-greedy)
    pattern = re.compile(r'^(#+)\s+(.*?)\s*$\n+(```.*?\n.*?```)', re.MULTILINE | re.DOTALL)

    matches = pattern.findall(content)

    results = []
    for match in matches:
        header, header_text, codeblock = match
        # Extract just the first line of the code block
        first_line_of_code = codeblock.split('\n', 2)[1].strip()
        results.append((header_text.strip(), first_line_of_code))

    return results

# Main script execution with command line arguments
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py 'SELECT header, codeblock FROM filename.md'")
        sys.exit(1)

    sql_query = sys.argv[1]
    extracted_data = execute_query_on_markdown(sql_query)

    for header_text, first_line_of_code in extracted_data:
        print(f"Header: {header_text}")
        print(f"Codeblock first line: {first_line_of_code}\n")
