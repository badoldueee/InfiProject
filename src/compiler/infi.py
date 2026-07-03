import os
import sys
import re
import subprocess

def compile_infi(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    # Normalize the target script's location path
    abs_script_path = os.path.abspath(filename)
    script_directory = os.path.dirname(abs_script_path)

    with open(abs_script_path, "r") as f:
        lines = f.readlines()

    variables = {}
    
    # Escape backward slashes for C language compatibility string literals on Windows
    escaped_dir = script_directory.replace('\\', '\\\\')

    # Injected standard system context mapping adjustments to bind the runtime process
    # directly to the folder housing the .infi script.
    c_code = [
        '#include "infi_lib.h"',
        '#include <stdio.h>',
        '#ifdef _WIN32',
        '#include <direct.h>',  # Required for _chdir on Windows
        '#define chdir _chdir',
        '#else',
        '#include <unistd.h>',  # Required for chdir on Unix/Linux systems
        '#endif',
        'int main() {',
        f'    chdir("{escaped_dir}"); // Switch system context context directly to script source path',
        '    // Infi Runtime Engine Initialized'
    ]
    
    has_errors = False
    nested_scopes = []  # Tracks open blocks ('safe_run' or 'repeat')
    print("Infi Compiler v2.0.0")

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        
        if not line or line.startswith("#"): 
            continue

        if line.startswith("set "):
            var_match = re.match(r'set\s+(\w+)\s*=\s*"(.*?)"', line)
            if var_match:
                variables[var_match.group(1)] = var_match.group(2)
            else:
                print(f"[Syntax Error] Line {line_num}: Invalid variable definition.")
                has_errors = True
            continue

        for var, val in variables.items():
            line = re.sub(r'\b' + re.escape(var) + r'\b', f'"{val}"', line)

        args = re.findall(r'"(.*?)"', line)

        if line.startswith("print"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing text to print.")
                has_errors = True
            else:
                c_code.append(f'    printf("%s\\n", "{args[0]}");')

        elif line.startswith("make_folder"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing folder name.")
                has_errors = True
            else:
                c_code.append(f'    create_folder("{args[0]}");')

        elif line.startswith("write"):
            if len(args) < 2:
                print(f"[Syntax Error] Line {line_num}: 'write' requires a file name and content.")
                has_errors = True
            else:
                c_code.append(f'    write_file("{args[0]}", "{args[1]}");')

        elif line.startswith("copy ") or line.startswith("move "):
            cmd = "copy" if line.startswith("copy") else "move"
            c_func = "copy_file" if cmd == "copy" else "move_file"
            match = re.search(r'(?:copy|move)\s+"(.*?)"\s+to\s+"(.*?)"', line)
            if match:
                c_code.append(f'    {c_func}("{match.group(1)}", "{match.group(2)}");')
            else:
                print(f"[Syntax Error] Line {line_num}: Invalid syntax for '{cmd}'.")
                has_errors = True

        elif line.startswith("delete "):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing target filename.")
                has_errors = True
            else:
                c_code.append(f'    delete_single("{args[0]}");')

        elif line.startswith("add_prefix"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing prefix value.")
                has_errors = True
            else:
                c_code.append(f'    bulk_prefix("{args[0]}");')

        elif line.startswith("add_suffix"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing suffix value.")
                has_errors = True
            else:
                c_code.append(f'    bulk_suffix("{args[0]}");')

        elif line.startswith("delete_if_contains"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing search match parameter.")
                has_errors = True
            else:
                c_code.append(f'    delete_if_match("{args[0]}");')

        elif line.startswith("archive_except"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing safety file bypass rule.")
                has_errors = True
            else:
                c_code.append(f'    archive_others("{args[0]}");')

        elif line.startswith("encrypt"):
            match = re.search(r'encrypt\s+"(.*?)"\s+with\s+"(.*?)"', line)
            if match:
                c_code.append(f'    encrypt_file("{match.group(1)}", "{match.group(2)}");')
            else:
                print(f"[Syntax Error] Line {line_num}: Cryptography statement structured incorrectly.")
                has_errors = True

        elif line.startswith("scan_inside"):
            match = re.search(r'scan_inside\s+"(.*?)"\s+for\s+"(.*?)"', line)
            if match:
                c_code.append(f'    scan_content_for_phrase("{match.group(1)}", "{match.group(2)}");')
            else:
                print(f"[Syntax Error] Line {line_num}: File scanning expression structured incorrectly.")
                has_errors = True

        elif line.startswith("get_hash"):
            if len(args) < 1:
                print(f"[Syntax Error] Line {line_num}: Missing file path context target.")
                has_errors = True
            else:
                c_code.append(f'    printf("[Infi Hash] File \\"%s\\" Checksum: %lu\\n", "{args[0]}", calculate_file_hash("{args[0]}"));')

        elif line.startswith("safe_run {"):
            nested_scopes.append("safe_run")
            c_code.append("    infi_enable_simulation();")

        elif line.startswith("repeat"):
            count_match = re.search(r'\((\d+)\)', line)
            if count_match:
                nested_scopes.append("repeat")
                count = count_match.group(1)
                c_code.append(f'    for(int i=0; i<{count}; i++) {{')
            else:
                print(f"[Syntax Error] Line {line_num}: Broken iteration format parameters.")
                has_errors = True

        elif line == "}":
            if nested_scopes:
                scope_type = nested_scopes.pop()
                if scope_type == "safe_run":
                    c_code.append("    infi_disable_simulation();")
                elif scope_type == "repeat":
                    c_code.append("    }")
            else:
                print(f"[Syntax Error] Line {line_num}: Extraneous closing brace '}}' found without matching expression.")
                has_errors = True

        else:
            print(f"[Semantic Error] Line {line_num}: Unknown command error: '{line.split()[0] if line.split() else line}'")
            has_errors = True

    if has_errors or len(nested_scopes) > 0:
        if len(nested_scopes) > 0:
            print(f"\nBuild aborted: Unclosed scoping blocks remaining: {nested_scopes}")
        else:
            print("\nBuild aborted: Please resolve the structural errors indicated above.")
        return

    c_code.append("    return 0;\n}")

    # Explicitly compile inside the folder where the script engine lives
    compiler_dir = os.path.dirname(os.path.abspath(__file__))
    temp_c_path = os.path.join(compiler_dir, "temp_out.c")
    output_bin_name = "InfiApp.exe" if os.name == 'nt' else "InfiApp"
    output_bin_path = os.path.join(compiler_dir, output_bin_name)

    with open(temp_c_path, "w") as f:
        f.write("\n".join(c_code))

    print(f"Building system pipeline binary via GCC compiler for {filename}...")
    
    # Locate the embedded gcc/bin directory structure accurately
    gcc_bin_path = os.path.abspath(os.path.join(compiler_dir, "..", "..", "gcc", "bin", "gcc.exe"))
    
    compile_cmd = [gcc_bin_path, f"-I{compiler_dir}", temp_c_path, "-o", output_bin_path]
    
    try:
        # Added silent execution flag constraints for GUI background environments
        compile_process = subprocess.run(
            compile_cmd, 
            capture_output=True, 
            text=True,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        if compile_process.returncode == 0:
            print("Success! Booting standalone binary build runtime application...\n" + "="*50)
            
            # Run the compiled binary safely via subprocess with execution flags protected
            run_process = subprocess.run(
                [output_bin_path], 
                capture_output=True, 
                text=True,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            print(run_process.stdout)
            if run_process.stderr:
                print(run_process.stderr)
                
            # Cleanup compilation footprints
            if os.path.exists(temp_c_path):
                os.remove(temp_c_path)
            if os.path.exists(output_bin_path):
                os.remove(output_bin_path)
        else:
            print("Build failed: Fatal compilation error.")
            print(compile_process.stderr)
            
    except Exception as e:
        print(f"Build failed: System pipeline compilation exception:\n{str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python infi.py <file.infi>")
    else:
        compile_infi(sys.argv[1])