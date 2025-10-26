import os
import re
import sys

def validate_markdown_links(root_dir):
    """
    Validates internal markdown links within a given root directory.
    Reports any broken links found.
    """
    print(f"Starting markdown link validation in: {root_dir}")
    broken_links_found = False
    
    # Regex to find markdown links: [text](path)
    # Group 1: link text, Group 2: link path
    link_pattern = re.compile(r'\[[^\]]+\]\((?!https?://)(?!#)([^)]+\.md)\)')

    # Collect all markdown files
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))

    for md_file_path in markdown_files:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all internal markdown links in the file
        for match in link_pattern.finditer(content):
            linked_path_raw = match.group(1)
            
            # Resolve the absolute path of the linked file
            # os.path.dirname(md_file_path) gives the directory of the current markdown file
            resolved_linked_path = os.path.abspath(os.path.join(os.path.dirname(md_file_path), linked_path_raw))
            
            # Check if the resolved file exists
            if not os.path.exists(resolved_linked_path):
                print(f"  Broken link found in: {os.path.relpath(md_file_path, root_dir)}")
                print(f"    Link: '{linked_path_raw}' -> Resolved: '{os.path.relpath(resolved_linked_path, root_dir)}'")
                broken_links_found = True

    if not broken_links_found:
        print("All internal markdown links are valid!")
    else:
        print("Validation complete with broken links. Please review the output above.")
        sys.exit(1) # Exit with error code if broken links are found

if __name__ == "__main__":
    # Assuming the script is run from the root of the repository
    # or that the root_dir is passed as an argument
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up two levels from script location
    
    validate_markdown_links(repo_root)
