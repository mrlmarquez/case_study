def load_text(filepath):
    with open(filepath, "r", encoding="UTF-8") as file:
        return file.read()


def copy_lines(source_file, target_file, start_line, end_line):
    """
    Copies a range of lines from a source file to a target file.

    Args:
        source_file (str): The path to the source file.
        target_file (str): The path to the target file.
        start_line (int): The starting line number (1-based index).
        end_line (int): The ending line number (inclusive).
    """
    try:
        with (
            open(source_file, "r", encoding="UTF-8") as infile,
            open(target_file, "w") as outfile,
        ):
            for i, line in enumerate(infile, 1):
                if start_line <= i <= end_line:
                    outfile.write(line)
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
