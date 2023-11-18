import sys
import re

# Function to parse the SQL-like query and determine what to extract
def extract_from_query(query):
    query_lower = query.lower()
    if "codeblock" in query_lower:
        return "header_codeblock"
    elif "header" in query_lower:
        return "header"
    return None

# Function to simulate executing an SQL-like query on a Markdown file
def execute_query_on_markdown(sql_query, query_type):
    match = re.match(r"SELECT .+ FROM '(.+)'", sql_query, re.IGNORECASE)
    if not match:
        print("Invalid query format. Use: SELECT [header[, codeblock]] FROM 'filename.md'")
        return []

    markdown_file = match.group(1)
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"The file {markdown_file} was not found.")
        return []

    results = []
    if query_type == "header_codeblock":
        # Regex pattern to match headers and following code blocks (non-greedy)
        pattern = re.compile(r'^(#+)\s+(.*?)\s*$\n+(```.*?\n.*?```)', re.MULTILINE | re.DOTALL)
        matches = pattern.findall(content)

        for header, header_text, codeblock in matches:
            # Extract just the first line of the code block
            first_line_of_code = codeblock.split('\n', 2)[1].strip()
            results.append((header_text.strip(), first_line_of_code))
    else:
        # Regex pattern to match headers only
        pattern = re.compile(r'^(#+)\s+(.*?)\s*$', re.MULTILINE)
        matches = pattern.findall(content)

        for header, header_text in matches:
            results.append(header_text.strip())

    return results

# Main script execution with command line arguments
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 query.py 'SELECT [header[, codeblock]] FROM filename.md'")
        sys.exit(1)

    sql_query = sys.argv[1]
    query_type = extract_from_query(sql_query)
    if not query_type:
        print("Invalid query. Specify what to select: header and/or codeblock.")
        sys.exit(1)

    extracted_data = execute_query_on_markdown(sql_query, query_type)

    for item in extracted_data:
        if query_type == "header_codeblock":
            header_text, first_line_of_code = item
            print(f"Header: {header_text}")
            print(f"Codeblock first line: {first_line_of_code}\n")
        else:
            header_text = item
            print(f"Header: {header_text}\n")
