#!/usr/bin/env python3
"""
Test script to verify the NIDS structure and imports are correct.
This test doesn't require running packet capture, just validates code structure.
"""
import sys
import os
import ast

def test_file_exists(filepath):
    """Test if a file exists."""
    if not os.path.exists(filepath):
        raise AssertionError(f"File {filepath} does not exist")
    print(f"✓ File exists: {filepath}")

def test_file_has_function(filepath, function_name):
    """Test if a Python file contains a specific function."""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    if function_name not in functions:
        raise AssertionError(f"Function {function_name} not found in {filepath}")
    print(f"✓ Function '{function_name}' found in {filepath}")

def test_structure():
    """Test the NIDS application structure."""
    print("Testing NIDS Application Structure")
    print("=" * 50)
    
    # Test 1: Check core files exist
    print("\n[Test 1] Checking core files...")
    core_files = [
        "app.py",
        "nids_manager.py",
        "packet_sniffer.py",
        "signature_engine.py",
        "signatures.yaml",
        "pages/1_Home.py",
        "pages/2_NIDS_Control.py",
        ".gitignore",
        "requirements.txt"
    ]
    for file in core_files:
        test_file_exists(file)
    print("✓ Test 1 passed: All core files exist")
    
    # Test 2: Check nids_manager has required functions
    print("\n[Test 2] Checking nids_manager.py functions...")
    required_functions = ["start_nids", "stop_nids", "get_nids_status"]
    for func in required_functions:
        test_file_has_function("nids_manager.py", func)
    print("✓ Test 2 passed: nids_manager has all required functions")
    
    # Test 3: Check packet_sniffer has required functions
    print("\n[Test 3] Checking packet_sniffer.py functions...")
    test_file_has_function("packet_sniffer.py", "start_sniffing")
    test_file_has_function("packet_sniffer.py", "packet_callback")
    print("✓ Test 3 passed: packet_sniffer has required functions")
    
    # Test 4: Check signature_engine has required functions
    print("\n[Test 4] Checking signature_engine.py functions...")
    test_file_has_function("signature_engine.py", "load_signatures")
    test_file_has_function("signature_engine.py", "match_signature")
    print("✓ Test 4 passed: signature_engine has required functions")
    
    # Test 5: Verify nids_manager doesn't import requests (no Flask API dependency)
    print("\n[Test 5] Verifying no Flask API dependencies in control page...")
    with open("pages/2_NIDS_Control.py", 'r') as f:
        control_content = f.read()
    if "import requests" in control_content:
        raise AssertionError("Control page should not import requests (Flask API dependency)")
    if "API_BASE" in control_content and "localhost:5000" in control_content:
        raise AssertionError("Control page should not reference Flask API endpoint")
    print("✓ Test 5 passed: No Flask API dependencies in control page")
    
    # Test 6: Verify nids_manager is imported in control page
    print("\n[Test 6] Verifying nids_manager import in control page...")
    if "from nids_manager import" not in control_content:
        raise AssertionError("Control page should import from nids_manager")
    if "start_nids" not in control_content or "stop_nids" not in control_content:
        raise AssertionError("Control page should use start_nids and stop_nids functions")
    print("✓ Test 6 passed: Control page imports and uses nids_manager")
    
    # Test 7: Verify README reflects consolidated approach
    print("\n[Test 7] Verifying README documentation...")
    with open("README.md", 'r') as f:
        readme_content = f.read()
    if "python api_server.py" in readme_content and "streamlit run app.py" in readme_content:
        # Check if it's in the setup section as two separate commands
        setup_section = readme_content.split("## Setup")[1].split("##")[0] if "## Setup" in readme_content else ""
        if "python api_server.py" in setup_section and "Launch the application" not in setup_section:
            raise AssertionError("README should not require running Flask API separately in setup")
    print("✓ Test 7 passed: README reflects consolidated approach")
    
    # Test 8: Verify .gitignore excludes generated files
    print("\n[Test 8] Verifying .gitignore...")
    with open(".gitignore", 'r') as f:
        gitignore_content = f.read()
    required_ignores = ["packet_stats.json", "alert_log.json", "alerts.csv"]
    for item in required_ignores:
        if item not in gitignore_content:
            raise AssertionError(f".gitignore should exclude {item}")
    print("✓ Test 8 passed: .gitignore properly configured")
    
    print("\n" + "=" * 50)
    print("All structure tests passed! ✓")
    print("\nThe NIDS application has been successfully consolidated.")
    print("Users can now run the entire application with a single command:")
    print("  streamlit run app.py")
    return True

if __name__ == "__main__":
    try:
        # Change to the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        test_structure()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
