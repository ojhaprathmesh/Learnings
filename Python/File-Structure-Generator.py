import os
import fnmatch


def read_gitignore(root_directory):
    """Reads the .gitignore file and returns a list of patterns to ignore."""
    gitignore_path = os.path.join(root_directory, '.gitignore')
    ignore_patterns = []

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    return ignore_patterns


def should_ignore(path, ignore_patterns):
    """Checks if the given path should be ignored based on the ignore patterns."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False


def generate_structure(root_directory):
    output = []
    ignore_patterns = read_gitignore(root_directory)

    # Add .git to ignore patterns
    ignore_patterns.append('.git')

    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Skip if the current directory is .git or any of its subdirectories
        if '.git' in dirpath.split(os.sep):
            continue

        # Ignore directories that match the ignore patterns
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d), ignore_patterns)]

        # Determine level of the current directory
        level = dirpath.replace(root_directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output.append(f"{indent}├── {os.path.basename(dirpath)}/")

        subindent = ' ' * 4 * (level + 1)
        for filename in filenames:
            # Ignore files that match the ignore patterns
            if not should_ignore(os.path.join(dirpath, filename), ignore_patterns):
                output.append(f"{subindent}├── {filename}")

    # Get the main directory name dynamically
    main_directory_name = os.path.basename(root_directory)

    # Save the output to a text file with UTF-8 encoding
    with open(f"File-Structure-{main_directory_name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    # Detect the current working directory as the root directory
    root_directory = os.getcwd()
    generate_structure(root_directory)
