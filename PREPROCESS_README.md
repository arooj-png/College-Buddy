# File Preprocessing Script

This script (`preprocess_files.py`) converts various file formats to clean `.txt` files for ingestion into the College Buddy RAG system.

## Supported File Formats

- **`.doc`** - Microsoft Word 97-2003 documents (converted to .docx first)
- **`.docx`** - Microsoft Word 2007+ documents
- **`.html`** - HTML files (cleaned of scripts and styles)

## Features

- **BOM Removal**: Automatically removes UTF-8 BOM (`ï»¿`) and other Unicode artifacts
- **Text Cleaning**: Normalizes whitespace, removes excessive line breaks
- **HTML Sanitization**: Removes scripts, styles, and HTML tags while preserving content
- **Safe Conversion**: Original files are kept intact, only `.txt` files are created
- **Error Handling**: Graceful handling of corrupted or unsupported files

## Installation

Install the required dependencies:

```bash
pip install python-docx beautifulsoup4 pywin32
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Usage

1. **Place your files** in the `backend/data/` directory:
   ```
   backend/data/
   ├── document1.doc
   ├── document2.docx
   ├── webpage.html
   └── existing.txt
   ```

2. **Run the preprocessing script**:
   ```bash
   cd backend
   python preprocess_files.py
   ```

3. **Build the vector database**:
   ```bash
   python ingest.py
   ```

## Example Output

```
Found 3 files to process:
  - document1.doc
  - document2.docx
  - webpage.html

Processing: document1.doc
Converted: document1.doc → document1.docx
Cleaned up temporary file: document1.docx
Created: document1.txt

Processing: document2.docx
Created: document2.txt

Processing: webpage.html
Created: webpage.txt

Processing complete!
Successfully converted: 3/3 files

You can now run 'python ingest.py' to build the vector database.
```

## Text Cleaning Features

The script performs extensive text cleaning:

- **BOM Removal**: `ï»¿`, `\ufeff`, zero-width spaces
- **Whitespace Normalization**: Converts tabs to spaces, removes excessive whitespace
- **Line Break Normalization**: Converts Windows/Mac line endings to Unix
- **HTML Entity Decoding**: `&nbsp;`, `&amp;`, `&lt;`, etc.
- **Artifact Removal**: Removes scripts, styles, and formatting artifacts

## Requirements

- **python-docx**: For reading .docx files
- **beautifulsoup4**: For parsing HTML files
- **pywin32**: For converting .doc to .docx (Windows only)

## Notes

- **Windows Only**: `.doc` file conversion requires Windows and Microsoft Word
- **Temporary Files**: .doc files are temporarily converted to .docx, then cleaned up
- **Encoding**: All output files use UTF-8 encoding
- **Error Handling**: Failed conversions are logged but don't stop the process

## Troubleshooting

### "python-docx not installed"
```bash
pip install python-docx
```

### "beautifulsoup4 not installed"
```bash
pip install beautifulsoup4
```

### "pywin32 not installed" (Windows only)
```bash
pip install pywin32
```

### "No files found"
- Ensure files are in `backend/data/` directory
- Check file extensions are `.doc`, `.docx`, or `.html`
- Files are case-insensitive (`.DOC`, `.DOCX`, `.HTML` also work)

### "Error converting .doc file"
- Ensure Microsoft Word is installed
- Check file is not corrupted
- Verify file is not password-protected
