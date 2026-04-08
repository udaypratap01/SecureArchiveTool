# Archive Password Cracker - Test File Generator

This script generates test archives (ZIP and RAR files) with known passwords for testing the Archive Password Cracker application.

## What It Creates

The `generate_test_files.py` script creates three files:

1. **test_archive.zip** - A password-protected ZIP file
   - Password: `TestPassword123!`
   - Contains: A text file with sample content

2. **test_archive.rar** - A password-protected RAR file
   - Password: `TestPassword123!`
   - Contains: A text file with sample content
   - ⚠️ Requires WinRAR or UnRAR to be installed

3. **test_passwords.txt** - A password list for testing
   - Contains several passwords including the correct one
   - Use this when testing the Archive Password Cracker

## How to Use

### Step 1: Generate Test Files

Run the test file generator:

```bash
python generate_test_files.py
```

This will create the test files in your project directory.

### Step 2: Test the Archive Password Cracker

1. Open the Archive Password Cracker GUI:
   ```bash
   python password_cracker.py
   ```

2. Select a test archive:
   - Click "Browse" under "Select Archive File"
   - Choose `test_archive.zip` or `test_archive.rar`

3. Select the password list:
   - Click "Browse" under "Select Password List"
   - Choose `test_passwords.txt`

4. Click "Start Cracking"

5. The application will:
   - Find the correct password: `TestPassword123!`
   - Extract the archive contents
   - Display the extracted files and their contents in the Results panel

## Requirements for RAR Support

To generate and work with RAR files, you need to have **WinRAR** or **UnRAR** installed:

- **Windows**: Download WinRAR from https://www.rarlab.com/ (free trial available)
- **Linux**: Install unrar: `sudo apt-get install unrar`
- **macOS**: Install via Homebrew: `brew install unrar`

After installation, ensure the RAR executable is in your system PATH.

## Test Results Expected

When you run the password cracker with the generated test files, you should see:

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

### RAR file not created
- Ensure WinRAR or UnRAR is installed
- On Windows, check that `rar.exe` is in your PATH
- Try running: `rar` or `rar.exe` in command line to verify installation

### ZIP file creation failed
- Check that you have write permissions in the project directory
- Ensure the `test_archive.zip` file is not currently in use by another program

### Password list not found
- Make sure `test_passwords.txt` exists in the project directory
- Check file permissions
