#!/usr/bin/env python3
"""
Test script for nids_manager module.
Tests the basic functionality of starting, checking status, and stopping the NIDS.
"""
import sys
import time
from nids_manager import start_nids, stop_nids, get_nids_status

def test_nids_manager():
    """Test the NIDS manager functions."""
    print("Testing NIDS Manager Module")
    print("=" * 50)
    
    # Test 1: Check initial status
    print("\n[Test 1] Checking initial status...")
    status = get_nids_status()
    print(f"Initial status: {status}")
    assert status["running"] == False, "NIDS should not be running initially"
    assert status["status"] == "stopped", "Status should be 'stopped'"
    print("✓ Test 1 passed: Initial status is correct")
    
    # Test 2: Start NIDS (using a mock interface for testing)
    print("\n[Test 2] Testing start_nids function...")
    test_interface = "lo"  # loopback interface for testing
    result = start_nids(test_interface)
    print(f"Start result: {result}")
    assert result["status"] in ["started", "already_running"], "Start should succeed"
    time.sleep(1)  # Give it a moment to start
    print("✓ Test 2 passed: start_nids executed")
    
    # Test 3: Check status after start
    print("\n[Test 3] Checking status after start...")
    status = get_nids_status()
    print(f"Status after start: {status}")
    assert status["running"] == True, "NIDS should be running"
    assert status["interface"] == test_interface, f"Interface should be {test_interface}"
    print("✓ Test 3 passed: Status correctly shows running")
    
    # Test 4: Try to start again (should report already running)
    print("\n[Test 4] Testing double start...")
    result = start_nids(test_interface)
    print(f"Double start result: {result}")
    assert result["status"] == "already_running", "Should report already running"
    print("✓ Test 4 passed: Correctly prevents double start")
    
    # Test 5: Stop NIDS
    print("\n[Test 5] Testing stop_nids function...")
    result = stop_nids()
    print(f"Stop result: {result}")
    assert result["status"] == "stopped", "Stop should succeed"
    time.sleep(1)  # Give it a moment to stop
    print("✓ Test 5 passed: stop_nids executed")
    
    # Test 6: Check status after stop
    print("\n[Test 6] Checking status after stop...")
    status = get_nids_status()
    print(f"Status after stop: {status}")
    assert status["running"] == False, "NIDS should not be running"
    assert status["status"] == "stopped", "Status should be 'stopped'"
    print("✓ Test 6 passed: Status correctly shows stopped")
    
    # Test 7: Try to stop again (should report not running)
    print("\n[Test 7] Testing double stop...")
    result = stop_nids()
    print(f"Double stop result: {result}")
    assert result["status"] == "not_running", "Should report not running"
    print("✓ Test 7 passed: Correctly handles stop when not running")
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    return True

if __name__ == "__main__":
    try:
        test_nids_manager()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
