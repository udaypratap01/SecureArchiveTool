"""
Utility script to generate test RAR and ZIP files with passwords for testing
"""

import zipfile
import os
import tempfile


def create_test_zip_file(filename="test_archive.zip", password="TestPassword123!", content="This is a test file for ZIP archive!"):
    """
    Create a password-protected ZIP file for testing.
    
    Args:
        filename: Name of the ZIP file to create
        password: Password to protect the file
        content: Content of the test file inside the archive
    """
    try:
        # Create a temporary file with content
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_filename = temp_file.name
        
        try:
            # Create ZIP file with password
            with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.setpassword(password.encode('utf-8'))
                zf.write(temp_filename, arcname='test_file.txt')
            
            print(f"✓ Created test ZIP file: {filename}")
            print(f"  Password: {password}")
            print(f"  Content: {content}")
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
    except Exception as e:
        print(f"✗ Error creating ZIP file: {e}")


def create_test_rar_file(filename="test_archive.rar", password="TestPassword123!", content="This is a test file for RAR archive!"):
    """
    Create a password-protected RAR file for testing.
    Note: This requires WinRAR or UnRAR to be installed.
    
    Args:
        filename: Name of the RAR file to create
        password: Password to protect the file
        content: Content of the test file inside the archive
    """
    try:
        import subprocess
        import tempfile
        
        # Create a temporary file with content
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_filename = temp_file.name
        
        try:
            # Try to create RAR file using WinRAR command line (Windows)
            # RAR.exe needs to be in PATH or we use its full path
            rar_commands = [
                ['rar', 'a', '-hp' + password, '-ep1', filename, temp_filename],
                ['rar.exe', 'a', '-hp' + password, '-ep1', filename, temp_filename],
            ]
            
            success = False
            for cmd in rar_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, timeout=10)
                    if result.returncode == 0:
                        print(f"✓ Created test RAR file: {filename}")
                        print(f"  Password: {password}")
                        print(f"  Content: {content}")
                        success = True
                        break
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue
            
            if not success:
                print("⚠ Could not create RAR file - WinRAR/UnRAR not found in PATH")
                print("  Please install WinRAR or add it to your PATH environment variable")
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
    except Exception as e:
        print(f"✗ Error creating RAR file: {e}")


def create_test_password_list(filename="test_passwords.txt"):
    """
    Create a test password list file.
    """
    passwords = [
        "wrongpassword1",
        "anotherpassword",
        "TestPassword123!",  # Correct password
        "incorrectpassword",
    ]
    
    try:
        with open(filename, 'w') as f:
            f.write('\n'.join(passwords))
        
        print(f"✓ Created test password list: {filename}")
        print(f"  Correct password is: TestPassword123!")
        
    except Exception as e:
        print(f"✗ Error creating password list: {e}")


if __name__ == "__main__":
    print("Archive Password Cracker - Test File Generator\n")
    
    # Create test files in the current directory
    create_test_zip_file("test_archive.zip", "TestPassword123!", "This is a test file for ZIP archive!")
    print()
    create_test_rar_file("test_archive.rar", "TestPassword123!", "This is a test file for RAR archive!")
    print()
    create_test_password_list("test_passwords.txt")
    
    print("\nTest files created successfully!")
    print("You can now use these files to test the Archive Password Cracker application.")
