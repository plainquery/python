import sys
import re

# Function to execute an INSERT INTO operation and write to a markdown file.
def execute_insert(sql_query, markdown_filename):
    pattern = re.compile(
        r"^(INSERT INTO)\s+'([\w\.-]+)'\s+\((.*?)\)\s+VALUES\s+\((.*?)\)$",
        re.IGNORECASE
    )
    match = pattern.match(sql_query)
    if not match:
        raise ValueError("Invalid SQL-like query format.")

    command, table_name, columns_str, values_str = match.groups()

    # We expect 'README.md' as the table name (markdown filename) for this script.
    if table_name != markdown_filename:
        raise ValueError(f"Table name '{table_name}' does not match the markdown filename '{markdown_filename}'.")

    # Parse the values from the SQL-like syntax.
    values = re.findall(r"\'(.*?)\'", values_str)
    
    if len(values) != 4:
        raise ValueError("There must be exactly four values for HeaderName, Content, CodeblockContent, and CodeblockType.")

    header_name, content, codeblock_content, codeblock_type = values
    markdown_section = build_markdown_section(header_name, content, codeblock_content, codeblock_type)
    
    # Append the constructed markdown to the file.
    with open(markdown_filename, 'a', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_section)
    
    return "Section inserted successfully into README.md!"

# Helper function to construct markdown section.
def build_markdown_section(header_name, content, codeblock_content, codeblock_type):
    header_str = f"# {header_name}\n\n"
    content_str = f"{content}\n\n"
    codeblock_str = f"```{codeblock_type}\n{codeblock_content}\n```\n\n"
    return header_str + content_str + codeblock_str

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 writer.py \"<INSERT INTO 'README.md' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('Example Header', 'Content goes here.', 'Code block content', 'python')>\"")
        sys.exit(1)

    markdown_filename = 'README.md'  # Define the markdown filename.
    sql_query = sys.argv[1]  # Get the SQL-like query from the command line argument.

    try:
        result = execute_insert(sql_query, markdown_filename)
        print(result)
    except ValueError as e:
        print(f"Query Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
