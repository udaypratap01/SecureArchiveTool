<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Archive Password Cracker - Custom Instructions

This is a Python GUI application built with Tkinter for identifying passwords in RAR and ZIP archive files.

## Project Structure

- `password_cracker.py` - Main application file with the Tkinter GUI
- `requirements.txt` - Python package dependencies
- `example_passwords.txt` - Example password list for testing
- `README.md` - Comprehensive documentation

## Key Technologies

- **Framework**: Tkinter (Python GUI toolkit)
- **Archive Support**: 
  - zipfile (built-in Python module)
  - rarfile (external module for RAR support)
- **Threading**: Used for non-blocking password testing

## Architecture

The application uses a single main class `PasswordCrackerGUI` that:
1. Manages the user interface
2. Handles file selection
3. Implements password cracking logic in a separate thread
4. Provides real-time progress updates

## Development Guidelines

- Keep the GUI responsive using threading for long-running operations
- Update the results text widget thread-safely
- Provide clear user feedback for all operations
- Handle both encrypted and non-encrypted archives gracefully

## Testing

To test the application:
1. Create a test archive (ZIP or RAR) with a password
2. Create a password list containing the correct password
3. Run the application and test with the created files

## Future Enhancements

Possible improvements for future versions:
- Multi-threading for faster password testing
- Support for additional archive formats (7z, etc.)
- Password generation patterns
- Saving session history
- Batch processing multiple archives
