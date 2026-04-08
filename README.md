# Archive Password Cracker

A simple GUI-based tool to identify passwords in RAR and ZIP files using a password list.

## Features

- 🎨 User-friendly Tkinter GUI
- 📦 Support for both RAR and ZIP archives
- 🔐 Test passwords from a text file
- 📊 Real-time progress and status updates
- ⏸️ Stop the cracking process at any time
- ✓ Display the correct password when found
- � **Automatically extract and display archive contents**
- 🚫 Secure temporary extraction (files cleaned up automatically)

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- rarfile (optional, for RAR support)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python password_cracker.py
   ```

2. Select an archive file (RAR or ZIP)
3. Select a text file containing a list of passwords (one password per line)
4. Click "Start Cracking" to begin testing passwords
5. The tool will:
   - Find the correct password if it exists in your list
   - Automatically extract the archive contents
   - Display extracted files and their contents in the Results panel

## Quick Test with Provided Files

Pre-generated test files are included:

1. Run the application: `python password_cracker.py`
2. Select archive: `test_archive.zip`
3. Select passwords: `test_passwords.txt`
4. Click "Start Cracking"
5. The correct password (`TestPassword123!`) will be found and contents displayed

## Generate Your Own Test Files

To create new test archives:

```bash
python generate_test_files.py
```

This creates:
- `test_archive.zip` - Password-protected ZIP file
- `test_passwords.txt` - Password list for testing

For more details, see `TEST_GENERATOR_README.md` and `ENHANCEMENT_GUIDE.md`

## Password File Format

The password file should be a plain text file with one password per line:

```
password123
letmein
admin
password123
test
```

An example file `example_passwords.txt` is included.

## Supported File Formats

- **ZIP files**: Supported natively via Python's `zipfile` module
- **RAR files**: Supported via the `rarfile` module (requires WinRAR or UnRAR to be installed)

### RAR Support Setup

For RAR file support, you need to have WinRAR or UnRAR installed:

- **Windows**: Install WinRAR (free trial available at https://www.rarlab.com/)
- **Linux**: Install unrar package (`sudo apt-get install unrar`)
- **macOS**: Install via Homebrew (`brew install unrar`)

## Notes

- The tool only identifies passwords; it does not extract files
- Processing time depends on the password list size and archive complexity
- For large password lists, the process may take some time
- All passwords are tested exactly as they appear in the file (case-sensitive)

## Troubleshooting

### "rarfile module not installed" error
Install the module:
```bash
pip install rarfile
```

### RAR files not working even after installing rarfile
Ensure WinRAR or UnRAR is installed on your system and added to the PATH.

### ZIP files showing errors
Ensure the ZIP file is not corrupted and is a valid archive.

## License

This project is provided as-is for educational purposes.
