import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

def setup_mock_repository(target_dir, file_count=1500, max_depth=5):
    """Programmatically builds a deeply nested codebase to stress-test your shell script."""
    print(f"[✓] Pre-allocating mock codebase in '{target_dir}' with {file_count} files...")
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    for i in range(file_count):
        depth = i % max_depth
        sub_dirs = [f"nested_dir_{d}" for d in range(depth)]
        current_depth_path = target_path.joinpath(*sub_dirs)
        current_depth_path.mkdir(parents=True, exist_ok=True)
        
        # Balance file extensions to ensure all internal logic chains fire
        if i % 3 == 0:
            filename = f"module_{i}.py"
            content = "import os\nimport sys\nfrom collections import defaultdict\n"
        elif i % 3 == 1:
            filename = f"service_{i}.cpp"
            content = "#include <iostream>\n#include <vector>\n"
        else:
            filename = f"README_{i}.md"
            content = "# Performance Log\nTesting wrapper boundaries."
            
        file_path = current_depth_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

def execute_wrapper_benchmark():
    sandbox_dir = "tests/perf_test_sandbox"
    total_files = 2500  # Scaled count to truly profile system I/O velocity
    
    try:
        # 1. Build out the temporary sandbox tree
        setup_mock_repository(sandbox_dir, file_count=total_files)
        
        print(f"\n[✓] Launching tool environment execution...")
        
        # 2. Match the shell script syntax: ./reposcan <path> <mode>
        # Used an argument list to avoid shell=True and improve safety.
        command = ["./reposcan", sandbox_dir]

        # High-resolution monotonic clock start
        start_time = time.perf_counter()

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        # 3. Print clean performance telemetry
        print("\n==================================================")
        print("           repoScanner Benchmark Suite            ")
        print("==================================================")
        print(f"  Target Workspace        : {sandbox_dir}")
        print(f"  Total Files Processed   : {total_files}")
        print(f"  Execution Time          : {elapsed_time:.5f} seconds")
        print(f"  I/O Processing Velocity : {total_files / elapsed_time:.2f} files/sec")
        print("==================================================")
        
    except Exception as e:
        print(f"[✗] Benchmark execution failed: {e}")
        print("[!] Ensure the execution permissions on 'reposcan' are set (`chmod +x reposcan`).")
        
    finally:
        # 4. Strict sandbox teardown
        if os.path.exists(sandbox_dir):
            shutil.rmtree(sandbox_dir)
            print("[✓] Flushed test sandbox environment directories cleanly.")

if __name__ == "__main__":
    execute_wrapper_benchmark()
