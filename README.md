# Infi Scripting Language & Compiler Environment (v1.0.0)
## Official Developer Manual & Repository Documentation

---

## 1. Introduction & Architectural Overview
Infi is a low-overhead, system-automation scripting language designed for batch filesystem manipulation, internal pattern auditing, and lightweight file cryptography. 

The framework features a multi-stage compilation pipeline that translates high-level `.infi` source code into native, procedural C code via the built-in Infi Engine. This generated intermediate script is dynamically compiled into a standalone binary executable via an integrated, portable GCC toolchain. 

By default, the execution path context maps directly to the parent directory housing the target `.infi` script file rather than the application workspace, allowing decentralized deployment across any local directory structure.

---

## 2. Key Performance Features
* **Dual-Layer Runtime Environment:** Supports direct filesystem execution alongside a sandbox simulation subsystem (`safe_run`) for dry-run validation.
* **Decentralized Scripting Scope:** Automatons run natively inside the directory where the script file lives, with support for absolute global paths.
* **Zero-Dependency Portability:** Distributed as a self-contained environment via the desktop IDE layout (`InfiCodeEditor`).

---

## 3. Core Technical Architecture & File Layout
The development workspace and compiler distribution are organized into an isolated, clean directory structure:

```text
InfiProject/
│
├── gcc/                           # Bundled portable C toolchain
│   └── bin/gcc.exe                # Standard GNU compiler back-end
│
├── src/                           # Core source codebase
│   ├── compiler/
│   │   ├── infi.py                # Main compiler translator engine
│   │   └── infi_lib.h             # Standard operational runtime headers
│   │
│   └── editor_app.py              # Tkinter-powered desktop GUI IDE
│
├── demo/                          # Local automated testing directory
│   └── demo1.inf                  # Pre-configured syntax validation file
│
├── LICENSE                        # GNU General Public License v3.0
├── .gitignore                     # Git filter control configurations
└── README.md                      # Language manual and reference guide

```

---

## 4. Language Reference Guide

### Level 1: Core Filesystem Operations

#### `print`

Outputs a literal string message sequence to the execution console pipeline.

* **Syntax:** `print "message"`
* **Code Example:**
```text
print "Initializing system verification sequence..."

```


* **Expected Output:**
```text
Initializing system verification sequence...

```



#### `make_folder`

Creates a directory inside the current target path. Also accepts absolute paths to target any drive sector location.

* **Syntax:** `make_folder "folder_name"`
* **Code Example:**
```text
make_folder "Production_Build"

```


* **Expected Output:**
*(A new folder named `Production_Build` is created on disk)*

#### `write`

Generates or completely replaces a specified target file, injecting the provided text buffer directly into the stream payload.

* **Syntax:** `write "file_name" "file_content"`
* **Code Example:**
```text
write "build_report.log" "Status: Active"

```


* **Expected Output:**
*(A file named `build_report.log` is generated containing the text `Status: Active`)*

#### `copy`

Executes a raw binary stream duplicate of a file from source to target bounds.

* **Syntax:** `copy "source_path" to "destination_path"`
* **Code Example:**
```text
copy "build_report.log" to "Backup/report_copy.log"

```


* **Expected Output:**
*(The file is duplicated to the specified location)*

#### `move`

Re-maps file indexes or migrates a resource to a completely separate path location.

* **Syntax:** `move "source_path" to "destination_path"`
* **Code Example:**
```text
move "build_report.log" to "Production_Build/final.log"

```


* **Expected Output:**
*(The source file is relocated to the destination path)*

#### `delete`

Permanently unlinks and purges a single file record from the storage sector.

* **Syntax:** `delete "file_name"`
* **Code Example:**
```text
delete "temporary_cache.tmp"

```


* **Expected Output:**
*(The file is deleted from the filesystem)*

---

### Level 2: Batch Directory Automation

Batch operations automatically loop through, filter, and modify regular files found inside the script's working folder, skipping system pointers like `.` or `..`.

#### `add_prefix`

Prepends a specific text flag string directly to the beginning of all filenames in the workspace.

* **Syntax:** `add_prefix "prefix_string"`
* **Code Example:**
```text
add_prefix "verified_"

```


* **Expected Output:**
```text
[Infi Engine] Renamed: log.txt -> verified_log.txt
[Infi Engine] Renamed: data.csv -> verified_data.csv

```



#### `add_suffix`

Appends a specific text string directly to the file name while preserving its original file extension format.

* **Syntax:** `add_suffix "suffix_string"`
* **Code Example:**
```text
add_suffix "_stable"

```


* **Expected Output:**
```text
[Infi Engine] Renamed: script.py -> script_stable.py
[Infi Engine] Renamed: notes.md -> notes_stable.md

```



#### `delete_if_contains`

Scans all files within the directory workspace, purging any file matching the name pattern.

* **Syntax:** `delete_if_contains "match_phrase"`
* **Code Example:**
```text
delete_if_contains "temp_cache"

```


* **Expected Output:**
```text
[Infi Engine] Purged: temp_cache_01.tmp
[Infi Engine] Purged: old_temp_cache.log

```



#### `archive_except`

Renames and archives all local files in the active workspace by applying an `OLD_YYYY-MM-DD_` pattern string timestamp, completely bypassing the specified protected file.

* **Syntax:** `archive_except "safe_file"`
* **Code Example:**
```text
archive_except "verify.infi"

```


* **Expected Output:**
```text
[Infi Engine] Archiving: system_test.txt -> OLD_2026-07-03_system_test.txt
[Infi Engine] Bypassed protected file: verify.infi

```



---

### Level 3: Cryptography & Deep Content Auditing

#### `encrypt`

Applies an un-indexed symmetric bitwise XOR key stream mutation across the target binary payload. Passing the same key string a second time reverses the cipher.

* **Syntax:** `encrypt "file_name" with "cipher_key"`
* **Code Example:**
```text
encrypt "production_report.log" "secret_key_123"

```


* **Expected Output:**
```text
[Infi Crypto] Applied symmetric mutation to production_report.log

```



#### `get_hash`

Runs a modified non-cryptographic djb2 hashing string loop to calculate and return a signature checksum of the file's raw layout properties.

* **Syntax:** `get_hash "file_name"`
* **Code Example:**
```text
get_hash "production_report.log"

```


* **Expected Output:**
```text
[Infi Audit] File: production_report.log | Checksum Hash: 5381398231

```



#### `scan_inside`

Performs deep pattern inspection across all files matching the target string pattern. Outputs the file name, line index, and content line string upon a match.

* **Syntax:** `scan_inside "file_pattern" for "search_phrase"`
* **Code Example:**
```text
scan_inside ".log" for "FATAL_ERROR"

```


* **Expected Output:**
```text
[Infi Scanner] Match found in production_report.log [Line 14]: [CRITICAL] FATAL_ERROR detected.

```



---

## 5. Control Structures & Scope Layouts

### Iteration Blocks

The `repeat` statement loops all enclosed procedural lines for a defined literal count.

* **Syntax:**
```text
repeat(count) {
    # Loop Body
}

```


* **Code Example:**
```text
repeat(3) {
    print "Looping process instance..."
}

```


* **Expected Output:**
```text
Looping process instance...

```



### Safe_Run Simulation Block

The `safe_run` statement enables a dry-run environment wrapper. It runs syntactic validation, tracks path variables, and prints structural execution logs without altering the physical disk layout.

* **Syntax:**
```text
safe_run {
    # Non-destructive simulation commands
}

```


* **Code Example:**
```text
safe_run {
    make_folder "Test_Sim"
    delete "production_file.db"
}

```


* **Expected Output:**
```text
[SIMULATION WARNING] dry_run context active. No physical changes will be written to disk.
[SIMULATION] make_folder: Test_Sim (Passed)
[SIMULATION] delete: production_file.db (Passed)

```



---

## 6. End-to-End Automation Case Study

The following comprehensive script leverages multiple layers of the language. Save this code sample as `verify.infi` and load it into your `InfiCodeEditor` application to execute:

```text
# --- Infi Automated System Verification Script ---
print "--- Initiating System Feature Verification Pipeline ---"

safe_run {
    print "[Infi System] Testing critical scripts inside dry-run context..."
    make_folder "Infi_Verification_Vault"
    write "sandbox_test.txt" "Simulated automated context storage layer raw asset payload."
    write "production_report.log" "Operational status: system framework active."
    get_hash "production_report.log"
    encrypt "production_report.log" "VaultKey2026"
    scan_inside "production" for "status"
}

print "Simulation concluded successfully. No structural filesystem changes applied."

```

### Complete Runtime Output

```text
--- Initiating System Feature Verification Pipeline ---
[SIMULATION WARNING] dry_run context active. No physical changes will be written to disk.
[Infi System] Testing critical scripts inside dry-run context...
[SIMULATION] make_folder: Infi_Verification_Vault (Passed)
[SIMULATION] write: sandbox_test.txt (Passed)
[SIMULATION] write: production_report.log (Passed)
[Infi Audit] File: production_report.log | Checksum Hash: 238491024
[SIMULATION] encrypt: production_report.log with key VaultKey2026 (Passed)
[Infi Scanner] Match found in production_report.log [Line 1]: Operational status: system framework active.
Simulation concluded successfully. No structural filesystem changes applied.

```

---

## 7. License

This project is open-source software licensed under the terms of the **GNU General Public License v3.0 (GPL-3.0)**. See the accompanying `LICENSE` file for full permission details.

```

```
