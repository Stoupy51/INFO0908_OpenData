# Imports
import os
import shutil
import subprocess
import sys
from stouputils import clean_path, handle_error
clean_exec: str = clean_path(sys.executable)

def generate_conf_py(source_dir: str) -> None:
    """ Generate conf.py for Sphinx configuration.

    Args:
        source_dir (str): Path to the source directory.
    """
    conf_content = """
# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# Project information
project = '🎓 INFO0908_OpenData'
copyright = '2024'
author = 'INFO0908'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
"""
    conf_path = clean_path(os.path.join(source_dir, "conf.py"))
    with open(conf_path, 'w', encoding="utf-8") as f:
        f.write(conf_content)

def generate_index_rst(readme_path: str, index_path: str) -> None:
    """ Generate index.rst from README.md content.

    Args:
        readme_path (str): Path to the README.md file.
        index_path (str): Path where index.rst should be created.
    """
    with open(readme_path, 'r', encoding="utf-8") as f:
        readme_content: str = f.read()
    
    # Extract sections while preserving emojis
    summary_section: str = readme_content.split('# 🎓 INFO0908_OpenData')[1].split('\n#')[0].strip().replace("<br>", "\n")
    overview_section: str = readme_content.split('# 📚 Utilisation')[1].split('\n#')[0].strip().replace("<br>", "\n")
    file_tree_section: str = readme_content.split('# 📂 Structure du projet')[1].split('\n#')[0].strip()
    file_tree_section = file_tree_section.replace('```bash', '').replace('```', '').strip()
    file_tree_section = "\n".join([f"   {line}" for line in file_tree_section.split('\n')])
    
    # Generate module documentation section
    module_docs: str = ".. toctree::\n   :maxdepth: 10\n   :caption: Contents:\n\n"
    
    # Add modules
    module_docs += "   modules/src\n"
    
    # Generate the RST content with emojis and proper title underlines
    rst_content: str = f"""
🎓 INFO0908_OpenData
====================
{summary_section}

📚 Overview
-----------
{overview_section}

🚀 Project Structure
-------------------
.. code-block:: bash

{file_tree_section}

📖 Module Documentation
----------------------
{module_docs}

⚡ Indices and Tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
    
    # Write the RST file
    with open(index_path, 'w', encoding="utf-8") as f:
        f.write(rst_content)

@handle_error()
def update_documentation() -> None:
    """ Update the Sphinx documentation.
    This script will:
    1. Create necessary directories if they don't exist.
    2. Generate module documentation using sphinx-apidoc.
    3. Build HTML documentation.
    """
    # Get the project root directory
    root_dir: str = clean_path(os.path.dirname(__file__))
    docs_dir: str = clean_path(os.path.join(root_dir, "docs"))
    source_dir: str = clean_path(os.path.join(docs_dir, "source"))
    modules_dir: str = clean_path(os.path.join(source_dir, "modules"))

    # Create directories if they don't exist
    os.makedirs(modules_dir, exist_ok=True)
    os.makedirs(clean_path(os.path.join(source_dir, "_static")), exist_ok=True)
    os.makedirs(clean_path(os.path.join(source_dir, "_templates")), exist_ok=True)

    # Generate conf.py
    generate_conf_py(source_dir)

    # Generate index.rst from README.md
    readme_path: str = clean_path(os.path.join(root_dir, "README.md"))
    index_path: str = clean_path(os.path.join(source_dir, "index.rst"))
    generate_index_rst(readme_path, index_path)

    # Clean up old module documentation
    if os.path.exists(modules_dir):
        shutil.rmtree(modules_dir)
        os.makedirs(modules_dir)

    # Generate module documentation using python -m
    subprocess.run([
        clean_exec,
        "-m", "sphinx.ext.apidoc",
        "-o", modules_dir,      # Output directory
        "-f",                   # Force overwrite
        "-e",                   # Put documentation for each module on its own page
        "-M",                   # Put module documentation before submodule documentation
        "--no-toc",            # Don't create a table of contents file
        "-P",                  # Include private modules
        "--implicit-namespaces", # Handle implicit namespaces
        "--module-first",      # Put module documentation before submodule documentation
        clean_path(os.path.join(root_dir, "src")),  # Source code directory
    ], check=True)

    # Build HTML documentation using python -m
    subprocess.run([
        clean_exec,
        "-m", "sphinx",
        "-b", "html",          # Build HTML
        "-a",                  # Write all files
        source_dir,            # Source directory
        clean_path(os.path.join(docs_dir, "build", "html")),  # Output directory
    ], check=True)

    print("Documentation updated successfully!")
    print(f"You can view the documentation by opening {docs_dir}/build/html/index.html")

if __name__ == "__main__":
    update_documentation()

