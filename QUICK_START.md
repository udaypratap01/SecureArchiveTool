# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Option 1: Test with Pre-Generated Files (Recommended)

1. **Open the application**:
   ```bash
   python password_cracker.py
   ```

2. **In the GUI**:
   - Archive File: Click "Browse" → Select `test_archive.zip`
   - Password List: Click "Browse" → Select `test_passwords.txt`
   - Click "Start Cracking"

3. **Watch the magic happen**:
   - Password found: `TestPassword123!`
   - Contents displayed in Results panel

---

### Option 2: Test with Your Own Archives

1. **Create a password-protected ZIP file**:
   - Open any ZIP tool (Windows Explorer, 7-Zip, WinRAR, etc.)
   - Create a new ZIP file
   - Add some files
   - Set a password (e.g., "MySecret123")
   - Save as `myarchive.zip`

2. **Create a password list** (`passwords.txt`):
   ```
   wrongpassword
   anotherguess
   MySecret123
   onemore
   ```

3. **Run the cracker**:
   ```bash
   python password_cracker.py
   ```
   - Select `myarchive.zip`
   - Select `passwords.txt`
   - Click "Start Cracking"

---

## 📋 What You'll See

### Finding Password
```
ℹ️  Loaded 4 passwords
ℹ️  Testing archive: test_archive.zip
ℹ️  Testing with file: test_file.txt
```

### Success!
```
✓ Password found: TestPassword123!
ℹ️  Tested 3 passwords
```

### Contents Display
```
ℹ️  Archive Contents:
📄 test_file.txt:
   This is a test file for ZIP archive!
```

---

## 🎯 Key Features

| Feature | What It Does |
|---------|-------------|
| **Browse Archive** | Select ZIP or RAR file to crack |
| **Browse Password List** | Select text file with passwords (one per line) |
| **Start Cracking** | Begin testing passwords |
| **Stop** | Halt the process anytime |
| **Found Password** | Displays the correct password (green box) |
| **Results** | Shows all activity and extracted content |

---

## ❓ Common Questions

### Q: Where do I get test files?
**A:** They're already in the project! (`test_archive.zip` and `test_passwords.txt`)

### Q: Can I create my own test files?
**A:** Yes! Run: `python generate_test_files.py`

### Q: Does it really extract files?
**A:** Yes! When password is found, files are extracted and displayed in the Results panel.

### Q: Is my data safe?
**A:** Yes! Files are extracted to a temporary folder that's automatically cleaned up.

### Q: Does it support RAR files?
**A:** Yes, but you need WinRAR or UnRAR installed first.

### Q: How fast is it?
**A:** Typically 10-50 passwords per second depending on archive size.

---

## 🔧 Troubleshooting

### Application won't start
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Then run
python password_cracker.py
```

### No password list available
- Create a `.txt` file with passwords (one per line)
- Or use the provided `test_passwords.txt`

### RAR files not working
- Install WinRAR from https://www.rarlab.com/
- Or UnRAR (Linux/macOS)
- Make sure it's in your system PATH

### Extraction not showing
- Check that you selected a valid password list
- Try with `test_archive.zip` first
- Check disk space in temp folder

---

## 📚 Learn More

For detailed information, see:
- `README.md` - Full documentation
- `ENHANCEMENT_GUIDE.md` - Technical details
- `TEST_GENERATOR_README.md` - Test file generation guide

---

## 🎉 You're Ready!

Your Archive Password Cracker is fully set up. Start by testing with `test_archive.zip` and have fun! 🚀
