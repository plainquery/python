import sys
import re
import os

def execute_insert(sql_query, markdown_filename):
    insert_pattern = re.compile(
        r"^(INSERT INTO)\s+'([\w\.-]+)'\s+\((.*?)\)\s+VALUES\s+\((.*?)\)(?:\s+WHERE\s+HeaderName='(.+?)')?$",
        re.IGNORECASE
    )
    match = insert_pattern.match(sql_query)
    if not match:
        raise ValueError("Invalid SQL-like query format.")

    command, table_name, columns_str, values_str, target_header = match.groups()

    # Handle case where table name does not match markdown filename.
    if table_name != markdown_filename:
        raise ValueError(f"Table name '{table_name}' does not match the markdown filename '{markdown_filename}'.")

    # Parse the values from the SQL-like syntax.
    values = re.findall(r"'(.*?)(?<!\\)'", values_str)
    
    if len(values) != 4:
        raise ValueError("There must be exactly four values for HeaderName, Content, CodeblockContent, and CodeblockType.")

    header_name, content, codeblock_content, codeblock_type = values
    markdown_section = build_markdown_section(header_name, content, codeblock_content, codeblock_type)

    if target_header:  # Insert under a specific header (more complex case, not implemented here).
        raise NotImplementedError("Inserting under a specific header is not supported in this script.")
    else:  # No specific target, insert at the beginning of the file (simple case).
        with open(markdown_filename, 'r+', encoding='utf-8') as markdown_file:
            original_content = markdown_file.read()
            markdown_file.seek(0)
            markdown_file.write(markdown_section + original_content)  # Prepend the new section.
    
    return "Section inserted successfully into README.md!"

def build_markdown_section(header_name, content, codeblock_content, codeblock_type):
    header_str = f"# {header_name}\n\n"
    content_str = f"{content}\n\n"
    codeblock_str = f"```{codeblock_type}\n{codeblock_content}\n```\n\n"
    return header_str + content_str + codeblock_str

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 writer.py \"<INSERT INTO 'README.md' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES ('Header', 'Content', 'Codeblock content', 'codeblock_type') [WHERE HeaderName='Target Header']\"")
        sys.exit(1)

    markdown_filename = 'README.md'  # Define the markdown filename.
    sql_query = sys.argv[1]  # Get the SQL-like query from the command line argument.

    try:
        result = execute_insert(sql_query, markdown_filename)
        print(result)
    except NotImplementedError as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(f"Query Error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Markdown file not found: {markdown_filename}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
