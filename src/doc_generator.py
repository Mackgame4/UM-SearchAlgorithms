import os
import subprocess

def generate_docs(src_dir, output_dir):
    """
    Generate HTML documentation for all Python files in the given source directory and its subdirectories.
    :param src_dir: The path to the source directory.
    :param output_dir: The path to save the generated documentation files.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Set the PYTHONPATH to include the src directory
    os.environ["PYTHONPATH"] = src_dir
    # Run pdoc to generate HTML documentation for the src directory and all subdirectories
    try:
        subprocess.run(['pdoc', '--output-dir', output_dir, '--', src_dir], check=True)
        print(f"Documentation successfully generated in {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating documentation: {e}")

if __name__ == "__main__":
    src_directory = os.path.join(os.getcwd(), "src") # Path to the 'src' directory
    output_directory = os.path.join(os.getcwd(), "docs") # Path to save the generated HTML files
    generate_docs(src_directory, output_directory)
