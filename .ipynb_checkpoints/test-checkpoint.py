#!/usr/bin/env python3
"""
Test script to verify the PBS job submission pipeline.
"""

import sys
import os
import time

def main():
    print("=" * 50)
    print("PBS Job Submission Test Script")
    print("=" * 50)
    
    print(f"\nPython version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    
    # Test environment
    print("\n--- Environment Variables ---")
    for var in ['PBS_JOBID', 'PBS_JOBNAME', 'PBS_O_WORKDIR', 'CONDA_DEFAULT_ENV']:
        value = os.environ.get(var, 'Not set')
        print(f"{var}: {value}")
    
    # Simple computation test
    print("\n--- Computation Test ---")
    start = time.time()
    result = sum(range(1000000))
    elapsed = time.time() - start
    print(f"Sum of 0-999999: {result}")
    print(f"Computation time: {elapsed:.4f} seconds")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
