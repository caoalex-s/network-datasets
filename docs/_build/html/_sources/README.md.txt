# Network Datasets Documentation

This directory contains the Sphinx documentation for the Network Datasets project.

## Building the Documentation

### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Build Commands

**HTML Documentation:**
```bash
make html
```

**Clean Build:**
```bash
make clean
make html
```

**Windows:**
```cmd
make.bat html
```

### Viewing the Documentation

After building, open `_build/html/index.html` in your web browser to view the documentation.

## Documentation Structure

- `index.rst` - Main documentation page
- `installation.rst` - Installation instructions
- `quickstart.rst` - Quick start guide
- `datasets.rst` - Available datasets
- `ndtools.rst` - ndtools package documentation
- `api.rst` - API reference
- `examples.rst` - Usage examples
- `contributing.rst` - Contribution guidelines

## Configuration

The documentation is configured in `conf.py`. Key settings:

- **Theme**: Read the Docs theme
- **Extensions**: autodoc, napoleon, myst-parser
- **Source**: RST and Markdown files
- **Output**: HTML, PDF, and other formats

## Adding New Documentation

1. Create new `.rst` or `.md` files in this directory
2. Add them to the table of contents in `index.rst`
3. Rebuild the documentation
4. Check for any warnings or errors

## Troubleshooting

**Import Errors:**
- Ensure the parent directory is in the Python path
- Check that all dependencies are installed

**Build Errors:**
- Check for syntax errors in RST/Markdown files
- Verify that all referenced files exist
- Check the Sphinx build log for specific errors

**Missing Modules:**
- Ensure the ndtools package is installed in development mode
- Check that all imports in the code are correct
