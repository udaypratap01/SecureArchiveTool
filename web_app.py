"""
Archive Password Cracker - Web UI
Flask-based web application for cracking archive passwords
"""

from flask import Flask, render_template, request, jsonify, send_file
import zipfile
import threading
import os
import tempfile
import shutil
import json
from datetime import datetime

# Try to import rarfile for RAR support
try:
    import rarfile
    RARFILE_AVAILABLE = True
except ImportError:
    RARFILE_AVAILABLE = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Error handlers to return JSON instead of HTML
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed. Please use GET or POST.'}), 405

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error: ' + str(error)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'Error: ' + str(e)}), 500

# Global state for tracking cracking process
cracking_state = {
    'is_cracking': False,
    'progress': 0,
    'status': 'Ready',
    'found_password': None,
    'messages': [],
    'archive_contents': [],
    'temp_dir': None
}

def add_message(message, msg_type='info'):
    """Add message to the messages list"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    cracking_state['messages'].append({
        'time': timestamp,
        'type': msg_type,
        'text': message
    })

def clean_temp_dir():
    """Clean up temporary extraction directory"""
    if cracking_state['temp_dir'] and os.path.exists(cracking_state['temp_dir']):
        try:
            shutil.rmtree(cracking_state['temp_dir'])
        except Exception as e:
            print(f"Error cleaning temp directory: {e}")

def extract_and_display_zip(archive_path, password):
    """Extract ZIP file and get its contents"""
    try:
        clean_temp_dir()
        cracking_state['temp_dir'] = tempfile.mkdtemp(prefix="zip_extract_")
        
        with zipfile.ZipFile(archive_path) as zf:
            zf.setpassword(password.encode('utf-8'))
            zf.extractall(cracking_state['temp_dir'])
        
        # Get file contents
        contents = []
        for root, dirs, files in os.walk(cracking_state['temp_dir']):
            for filename in files:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, cracking_state['temp_dir'])
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[:500]  # Limit to 500 chars
                    contents.append({
                        'name': rel_path,
                        'type': 'text',
                        'content': content
                    })
                except:
                    contents.append({
                        'name': rel_path,
                        'type': 'binary'
                    })
        
        cracking_state['archive_contents'] = contents
        add_message(f"✓ Successfully extracted {len(contents)} file(s)", 'success')
        
    except Exception as e:
        add_message(f"✗ Error extracting ZIP: {e}", 'error')

def extract_and_display_rar(archive_path, password):
    """Extract RAR file and get its contents"""
    try:
        clean_temp_dir()
        cracking_state['temp_dir'] = tempfile.mkdtemp(prefix="rar_extract_")
        
        rf = rarfile.RarFile(archive_path)
        rf.setpassword(password)
        rf.extractall(cracking_state['temp_dir'])
        
        # Get file contents
        contents = []
        for root, dirs, files in os.walk(cracking_state['temp_dir']):
            for filename in files:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, cracking_state['temp_dir'])
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[:500]  # Limit to 500 chars
                    contents.append({
                        'name': rel_path,
                        'type': 'text',
                        'content': content
                    })
                except:
                    contents.append({
                        'name': rel_path,
                        'type': 'binary'
                    })
        
        cracking_state['archive_contents'] = contents
        add_message(f"✓ Successfully extracted {len(contents)} file(s)", 'success')
        
    except Exception as e:
        add_message(f"✗ Error extracting RAR: {e}", 'error')

def crack_archive_thread(archive_path, passwords, file_type):
    """Background thread for cracking"""
    try:
        add_message(f"Starting password cracking for {file_type.upper()} file...", 'info')
        add_message(f"Testing {len(passwords)} passwords...", 'info')
        
        if file_type == 'zip':
            crack_zip_internal(archive_path, passwords)
        elif file_type == 'rar':
            crack_rar_internal(archive_path, passwords)
        
    except Exception as e:
        add_message(f"✗ Error: {e}", 'error')
    finally:
        cracking_state['is_cracking'] = False

def crack_zip_internal(archive_path, passwords):
    """Internal ZIP cracking logic"""
    try:
        zf = zipfile.ZipFile(archive_path)
        if not zf.namelist():
            add_message("✗ ZIP file is empty", 'error')
            return
        
        test_file = zf.namelist()[0]
        
        for i, password in enumerate(passwords):
            if not cracking_state['is_cracking']:
                break
            
            try:
                zf.setpassword(password.encode('utf-8'))
                zf.testzip()
                
                # Password found!
                cracking_state['found_password'] = password
                add_message(f"✓ Password found: {password}", 'success')
                add_message(f"Tested {i + 1}/{len(passwords)} passwords", 'info')
                
                # Extract contents
                extract_and_display_zip(archive_path, password)
                return
                
            except RuntimeError:
                if (i + 1) % 100 == 0 or i + 1 == len(passwords):
                    cracking_state['progress'] = int((i + 1) / len(passwords) * 100)
                    add_message(f"Tested {i + 1}/{len(passwords)} passwords...", 'info')
            except Exception as e:
                add_message(f"✗ Error: {e}", 'error')
                break
        
        if not cracking_state['found_password']:
            add_message("✗ Password not found in the list", 'error')
    
    except Exception as e:
        add_message(f"✗ Error opening ZIP: {e}", 'error')

def crack_rar_internal(archive_path, passwords):
    """Internal RAR cracking logic"""
    if not RARFILE_AVAILABLE:
        add_message("✗ rarfile module not installed: pip install rarfile", 'error')
        return
    
    try:
        rf = rarfile.RarFile(archive_path)
        file_list = rf.infolist()
        
        if not file_list:
            add_message("✗ RAR file is empty", 'error')
            return
        
        test_file = None
        for file_info in file_list:
            if not file_info.is_dir():
                test_file = file_info.filename
                break
        
        if test_file is None:
            add_message("✗ No extractable files in RAR", 'error')
            return
        
        for i, password in enumerate(passwords):
            if not cracking_state['is_cracking']:
                break
            
            try:
                rf = rarfile.RarFile(archive_path)
                rf.setpassword(password)
                
                try:
                    data = rf.read(test_file)
                    
                    # Password found!
                    cracking_state['found_password'] = password
                    add_message(f"✓ Password found: {password}", 'success')
                    add_message(f"Tested {i + 1}/{len(passwords)} passwords", 'info')
                    
                    # Extract contents
                    extract_and_display_rar(archive_path, password)
                    return
                
                except (rarfile.BadRarFile, RuntimeError, OSError):
                    if (i + 1) % 100 == 0 or i + 1 == len(passwords):
                        cracking_state['progress'] = int((i + 1) / len(passwords) * 100)
                        add_message(f"Tested {i + 1}/{len(passwords)} passwords...", 'info')
                
            except Exception as e:
                add_message(f"✗ Error: {e}", 'error')
                break
        
        if not cracking_state['found_password']:
            add_message("✗ Password not found in the list", 'error')
    
    except Exception as e:
        add_message(f"✗ Error opening RAR: {e}", 'error')

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/crack', methods=['POST'])
def crack():
    """Start cracking process"""
    if cracking_state['is_cracking']:
        return jsonify({'error': 'Already cracking. Please wait.'}), 400
    
    if 'archive' not in request.files or 'passwords' not in request.files:
        return jsonify({'error': 'Missing archive or password file'}), 400
    
    archive_file = request.files['archive']
    password_file = request.files['passwords']
    
    if archive_file.filename == '' or password_file.filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    try:
        # Get file extension
        file_ext = os.path.splitext(archive_file.filename)[1].lower()
        if file_ext not in ['.zip', '.rar']:
            return jsonify({'error': 'Only ZIP and RAR files are supported'}), 400
        
        # Save files temporarily
        archive_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_archive' + file_ext)
        password_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_passwords.txt')
        
        archive_file.save(archive_path)
        password_file.save(password_path)
        
        # Read passwords
        with open(password_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        if not passwords:
            return jsonify({'error': 'Password list is empty'}), 400
        
        # Reset state
        cracking_state['is_cracking'] = True
        cracking_state['progress'] = 0
        cracking_state['found_password'] = None
        cracking_state['messages'] = []
        cracking_state['archive_contents'] = []
        
        # Start cracking in background thread
        thread = threading.Thread(
            target=crack_archive_thread,
            args=(archive_path, passwords, file_ext[1:])
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'Cracking started'})
    
    except Exception as e:
        cracking_state['is_cracking'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET', 'POST'])
def get_status():
    """Get current status"""
    return jsonify({
        'is_cracking': cracking_state['is_cracking'],
        'progress': cracking_state['progress'],
        'found_password': cracking_state['found_password'],
        'messages': cracking_state['messages'],
        'archive_contents': cracking_state['archive_contents']
    })

@app.route('/api/stop', methods=['POST'])
def stop_cracking():
    """Stop cracking"""
    cracking_state['is_cracking'] = False
    clean_temp_dir()
    add_message("Cracking stopped by user", 'info')
    return jsonify({'status': 'Stopped'})

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download extracted file"""
    if cracking_state['temp_dir'] and os.path.exists(cracking_state['temp_dir']):
        file_path = os.path.join(cracking_state['temp_dir'], filename)
        if os.path.exists(file_path) and file_path.startswith(cracking_state['temp_dir']):
            return send_file(file_path, as_attachment=True)
    
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("Starting Archive Password Cracker Web UI...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=False, host='127.0.0.1', port=5000)
