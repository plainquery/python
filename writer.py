
import sys
import re

def execute_insert(sql_query, markdown_filename):
    match = re.match(
        r"^(INSERT INTO)\s+'([\w\.]+)'\s+\((.*?)\)\s+VALUES\s+\((.*?)\)(?:\s+WHERE\s+HeaderName='(.+?)')?$",
        sql_query, re.IGNORECASE
    )
    if not match:
        raise ValueError("Invalid SQL-like query format.")

    command, table_name, columns_str, values_str, target_header = match.groups()

    # Parse the values and handle escape characters
    values = re.findall(r"'(.*?)'", values_str)
    header_name, content, codeblock_content, codeblock_type = (v.replace("\\'", "'") for v in values)

    # Build the markdown section
    markdown_section = build_markdown_section(header_name, content, codeblock_content, codeblock_type)

    if target_header:
        # We are going to insert the content under a specific header
        with open(markdown_filename, 'r+', encoding='utf-8') as markdown_file:
            content = markdown_file.read()
            header_regex = re.escape(f"# {target_header}")
            match = re.search(header_regex, content, re.MULTILINE)
            
            if match:
                insertion_point = match.end()
                # Find the end of the section to insert the new content
                next_header_match = re.search(r"^#", content[insertion_point:], re.MULTILINE)
                if next_header_match:
                    insertion_point += next_header_match.start()

                new_content = content[:insertion_point] + '\n\n' + markdown_section + content[insertion_point:]
                markdown_file.seek(0)
                markdown_file.write(new_content)
                markdown_file.truncate()
            else:
                # Append to the end if the header is not found
                markdown_file.write('\n' + markdown_section)
            return f"Section inserted successfully under header '{target_header}' in README.md!"
    else:
        # Insert at the beginning of the file as default
        with open(markdown_filename, 'r+', encoding='utf-8') as markdown_file:
            original_content = markdown_file.read()
            markdown_file.seek(0, 0)
            markdown_file.write(markdown_section + '\n' + original_content)
        return "Section inserted successfully at the beginning of README.md!"

def build_markdown_section(header_name, content, codeblock_content, codeblock_type):
    return f"\n# {header_name}\n{content}\n```{codeblock_type}\n{codeblock_content}\n```\n"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 writer.py \"<INSERT INTO 'README.md' (HeaderName, Content, CodeblockContent, CodeblockType) VALUES (...values...) [WHERE HeaderName='Target Header']\">")
        sys.exit(1)

    sql_query = sys.argv[1]
    markdown_filename = 'README.md'

    try:
        result = execute_insert(sql_query, markdown_filename)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
