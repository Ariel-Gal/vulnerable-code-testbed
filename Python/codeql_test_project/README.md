# CodeQL Python Test Project

This project is intentionally designed to validate CodeQL behavior with:
- True positives (real vulnerabilities)
- False positives (safe code that can look suspicious)

## Structure

- `true_positive/`
  - `sql_injection_tp.py`
  - `command_injection_tp.py`
  - `path_traversal_tp.py`
- `false_positive/`
  - `sql_parameterized_fp.py`
  - `subprocess_no_shell_fp.py`
  - `safe_file_access_fp.py`

## Expected Results

CodeQL should ideally report findings in `true_positive` files and avoid reporting findings in `false_positive` files.

## Notes

- The code is intentionally insecure in the `true_positive` folder.
- Do not deploy or reuse these examples in production.
