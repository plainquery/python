
import sys
import re

def execute_delete(sql_query, markdown_filename):
    match = re.match(
        r"DELETE FROM '([\w\.]+)' WHERE HeaderName='(.+)'$",
        sql_query, re.IGNORECASE
    )
    if not match:
        raise ValueError("Invalid SQL-like DELETE statement.")

    file_to_modify, header_search_pattern = match.groups()
    header_search_pattern = header_search_pattern.replace("*", ".*")
    header_search_regex = re.compile(rf"^(#{header_search_pattern})$", re.MULTILINE)

    if file_to_modify != markdown_filename:
        raise ValueError(f"File to modify '{file_to_modify}' does not match markdown filename '{markdown_filename}'.")

    try:
        with open(markdown_filename, 'r+', encoding='utf-8') as file:
            content = file.readlines()

        deleted = False
        with open(markdown_filename, 'w', encoding='utf-8') as file:
            inside_section = False
            for line in content:
                if inside_section:
                    # If we encounter another header of the same level, it means the section is over
                    if line.startswith("# "):
                        inside_section = False
                elif header_search_regex.search(line):
                    inside_section = True  # Flag to start skipping lines
                    deleted = True
                    continue  # Skip this line since it's a starting point for deletion
                
                if not inside_section:
                    file.write(line)

        if not deleted:
            return f"No section with header matching pattern '{header_search_pattern}' was found."

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{markdown_filename}' not found.")

    return f"Section with header matching pattern '{header_search_pattern}' deleted successfully."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 deleter.py \"DELETE FROM 'README.md' WHERE HeaderName='*pattern*'\"")
        sys.exit(1)

    sql_query = sys.argv[1]
    
    try:
        result = execute_delete(sql_query, 'README.md')
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
