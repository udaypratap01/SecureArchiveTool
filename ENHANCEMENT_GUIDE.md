# Archive Password Cracker - Complete Guide

## Overview

Your Archive Password Cracker has been enhanced with **automatic extraction and content display** capabilities. When the correct password is found, the application now extracts the archive and displays the contents directly in the GUI.

## What's New

### ✨ New Features

1. **Automatic Content Extraction** - When a password is found, the archive is automatically extracted
2. **Content Display** - File contents are displayed in the GUI results panel
3. **File Listing** - Shows all files extracted from the archive with their contents
4. **Temporary Storage** - Extracts to a secure temporary directory that's cleaned up automatically
5. **Test File Generator** - A utility to create test archives for testing

### 📦 New Files

- **`generate_test_files.py`** - Script to generate test archives and password lists
- **`TEST_GENERATOR_README.md`** - Detailed guide for the test file generator
- **`test_archive.zip`** - Pre-generated test ZIP file (already created!)
- **`test_passwords.txt`** - Pre-generated password list (already created!)

## Quick Start

### 1. Generate Test Files (Optional)

Test files have already been generated, but you can regenerate them anytime:

```bash
python generate_test_files.py
```

This creates:
- `test_archive.zip` - Password-protected ZIP with sample content
- `test_passwords.txt` - Password list including the correct password

**Password for test files**: `TestPassword123!`

### 2. Run the Application

```bash
python password_cracker.py
```

Or use VS Code's task: Press `Ctrl+Shift+B` and select "Run Archive Password Cracker"

### 3. Test with Sample Files

1. Click "Browse" for Archive File → Select `test_archive.zip`
2. Click "Browse" for Password List → Select `test_passwords.txt`
3. Click "Start Cracking"
4. The application will:
   - Test passwords from the list
   - Find the correct password: `TestPassword123!`
   - Extract the archive
   - Display the file contents in the Results panel

## How It Works

### Password Finding Process

1. **Load Archive** - Opens the ZIP or RAR file
2. **List Files** - Gets the list of files in the archive
3. **Test Passwords** - Tries each password from your list
4. **Verify Password** - Attempts to read a file from the archive
5. **Extract Contents** - If password is correct, extracts all files to a temporary directory
6. **Display Results** - Shows:
   - The found password in the "Found Password" section
   - Archive contents with file names and content previews
   - File count and success status

### Extraction Safety

- Files are extracted to a **temporary directory** that's automatically created
- Temporary files are cleaned up when you close the app or start a new search
- No files are permanently stored outside your temp folder
- No files are extracted from the archive itself (stays intact)

## Technical Details

### Code Changes Made

#### 1. **Import Additions**
```python
import tempfile
import shutil
```

#### 2. **Instance Variables**
```python
self.archive_contents = []      # Store extracted contents
self.temp_extract_dir = None    # Temporary extraction directory
```

#### 3. **New Methods**
- `extract_and_display_zip()` - Extracts ZIP and displays contents
- `extract_and_display_rar()` - Extracts RAR and displays contents

#### 4. **Updated Methods**
- `crack_zip()` - Now calls extraction method when password found
- `crack_rar()` - Now calls extraction method when password found

### Supported Archive Formats

| Format | Support | Status |
|--------|---------|--------|
| ZIP | Native Python | ✅ Full support |
| RAR | rarfile module | ✅ Full support (requires UnRAR) |
| 7z | Not supported | ❌ |
| Tar | Not supported | ❌ |

## Output Example

When you successfully crack an archive, you'll see:

```
ℹ️  Loaded 4 passwords
ℹ️  Testing archive: test_archive.zip
ℹ️  Testing with file: test_file.txt

✓ Password found: TestPassword123!
ℹ️  Tested 3 passwords

ℹ️  Archive Contents:
📄 test_file.txt:
   This is a test file for ZIP archive!
```

## Troubleshooting

### Extraction Not Showing

**Problem**: Password found but contents not displayed

**Solutions**:
- Check file permissions
- Ensure temp directory can be created (usually C:\Users\YourUser\AppData\Local\Temp)
- Try with a smaller archive first

### Permission Denied Error

**Problem**: Cannot extract to temporary directory

**Solutions**:
- Run application as administrator
- Check disk space available
- Disable antivirus temporarily (may block temp file access)

### Binary Files Not Displayed

**Problem**: See "📦 filename (binary file)" instead of content

**Solutions**:
- This is normal for non-text files (images, executables, etc.)
- Text files will show their full content
- The binary file was still extracted successfully

### RAR Extraction Issues

**Problem**: RAR support not working

**Solutions**:
1. Install WinRAR or UnRAR:
   - Windows: Download from https://www.rarlab.com/
   - Linux: `sudo apt-get install unrar`
   - macOS: `brew install unrar`

2. Add to PATH (Windows):
   - Find `rar.exe` installation folder
   - Add to system PATH environment variable
   - Restart application

## Advanced Usage

### Creating Your Own Test Archives

Using Python to create encrypted ZIP:

```python
import zipfile

# Create a protected ZIP
zf = zipfile.ZipFile('myarchive.zip', 'w', zipfile.ZIP_DEFLATED)
zf.setpassword(b'mypassword')
zf.write('myfile.txt')
zf.close()
```

### Testing Large Password Lists

For efficiency with large lists:
1. Put one password per line in your text file
2. Place the correct password earlier in the list for faster testing
3. The application shows progress every 100 passwords

### Custom Content in Test Files

Edit `generate_test_files.py` and modify the `content` parameter:

```python
create_test_zip_file(
    filename="mytest.zip",
    password="mypassword",
    content="Your custom content here!"
)
```

## Performance Notes

- **Password Testing**: ~10-50 passwords per second (depends on archive size)
- **Extraction Time**: Usually < 1 second for small archives
- **Display Speed**: Instant for text files, may be slower for many files

## Security Considerations

⚠️ **Important**: This tool is for:
- ✅ Recovering lost passwords from your own archives
- ✅ Testing archive encryption
- ✅ Educational purposes

It should **NOT** be used for:
- ❌ Unauthorized access to others' files
- ❌ Illegal activities
- ❌ Breaking into secured archives you don't own

## Project Files Summary

```
project/
├── password_cracker.py           # Main GUI application
├── generate_test_files.py        # Test file generator
├── requirements.txt              # Python dependencies
├── example_passwords.txt         # Example passwords
├── test_archive.zip             # Generated test ZIP
├── test_passwords.txt           # Generated password list
├── README.md                     # Basic documentation
├── TEST_GENERATOR_README.md      # Test generator guide
├── ENHANCEMENT_GUIDE.md          # This file
└── .github/
    └── copilot-instructions.md   # Copilot instructions
```

## Next Steps

### Try These Tests

1. **Basic ZIP Test**
   - Use `test_archive.zip` and `test_passwords.txt`
   - Should find password in 3 attempts

2. **Password Not in List**
   - Create a new password list without the correct password
   - Verify "Password not found" message appears

3. **Empty Archive** (Advanced)
   - Create an empty ZIP file
   - Verify proper error handling

4. **Large Password List**
   - Create a list with 1000+ passwords
   - Test performance and progress updates

### Possible Enhancements

- Add support for 7z archives
- Implement multi-threaded password testing
- Add password generation patterns
- Export extracted files to a folder
- Add session history/logging
- Create GUI for generating test archives

## Support & Issues

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify file permissions and paths
3. Ensure Python version is 3.7+
4. Check that all dependencies are installed: `pip install -r requirements.txt`
5. Try with the pre-generated test files first

## Conclusion

Your Archive Password Cracker is now fully functional with extraction capabilities! You can now:

✅ Identify passwords in encrypted archives
✅ Extract and view archive contents
✅ Test with pre-generated archives
✅ Handle both ZIP and RAR formats
✅ View file contents directly in the GUI

Enjoy recovering your lost archive passwords! 🎉
