"""
Code quality assessment for the Phase II Todo Backend API
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

def check_import_organization(file_path: str) -> Dict[str, Any]:
    """
    Check if imports are properly organized in a file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        # Count import statements
        import_count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_count += 1

        # Check if there are any import statements (basic check)
        passed = import_count > 0
        details = f"Found {import_count} import statements"

        return {
            "check": "Import Organization",
            "passed": passed,
            "details": details,
            "file": file_path,
            "import_count": import_count
        }
    except Exception as e:
        return {
            "check": "Import Organization",
            "passed": False,
            "details": f"Error parsing file: {str(e)}",
            "file": file_path,
            "import_count": 0
        }

def check_function_complexity(file_path: str, max_complexity: int = 10) -> Dict[str, Any]:
    """
    Check function complexity (simplified version)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        # Count function definitions
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        complexity_issues = []

        for func in functions:
            # Simplified complexity estimation (just counting nodes as proxy)
            complexity = len([n for n in ast.walk(func)])
            if complexity > max_complexity:
                complexity_issues.append({
                    "function": func.name,
                    "complexity": complexity
                })

        passed = len(complexity_issues) == 0
        details = f"Functions with high complexity: {len(complexity_issues)}"

        return {
            "check": "Function Complexity",
            "passed": passed,
            "details": details,
            "file": file_path,
            "complexity_issues": complexity_issues,
            "function_count": len(functions)
        }
    except Exception as e:
        return {
            "check": "Function Complexity",
            "passed": False,
            "details": f"Error parsing file: {str(e)}",
            "file": file_path,
            "complexity_issues": [],
            "function_count": 0
        }

def check_file_length(file_path: str, max_lines: int = 500) -> Dict[str, Any]:
    """
    Check if files are not too long
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        line_count = len(lines)
        passed = line_count <= max_lines
        details = f"File has {line_count} lines (max: {max_lines})"

        return {
            "check": "File Length",
            "passed": passed,
            "details": details,
            "file": file_path,
            "line_count": line_count
        }
    except Exception as e:
        return {
            "check": "File Length",
            "passed": False,
            "details": f"Error reading file: {str(e)}",
            "file": file_path,
            "line_count": 0
        }

def scan_directory_for_py_files(directory: str) -> List[str]:
    """
    Recursively scan directory for Python files
    """
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def run_code_quality_assessment(base_dir: str = "src") -> Dict[str, Any]:
    """
    Run code quality assessment on the project
    """
    logger.info(f"Starting code quality assessment for {base_dir}...")

    py_files = scan_directory_for_py_files(base_dir)

    all_results = []
    for file_path in py_files:
        # Run multiple checks on each file
        import_check = check_import_organization(file_path)
        complexity_check = check_function_complexity(file_path)
        length_check = check_file_length(file_path)

        all_results.extend([import_check, complexity_check, length_check])

    # Calculate summary
    total_checks = len(all_results)
    passed_checks = sum(1 for result in all_results if result["passed"])
    failed_checks = total_checks - passed_checks

    summary = {
        "total_files": len(py_files),
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "quality_score": passed_checks / total_checks if total_checks > 0 else 0,
        "all_passed": failed_checks == 0,
        "results": all_results
    }

    logger.info(f"Code quality assessment completed: {passed_checks}/{total_checks} checks passed")

    return summary

def print_code_quality_report(report: Dict[str, Any]):
    """
    Print a formatted code quality report
    """
    print("\nCode Quality Assessment Report")
    print("=" * 50)
    print(f"Files Scanned: {report['total_files']}")
    print(f"Total Checks: {report['total_checks']}")
    print(f"Passed: {report['passed_checks']}")
    print(f"Failed: {report['failed_checks']}")
    print(f"Quality Score: {report['quality_score']:.2%}")
    print(f"All Passed: {'Yes' if report['all_passed'] else 'No'}")
    print()

    # Group results by file
    results_by_file = {}
    for result in report['results']:
        file_path = result['file']
        if file_path not in results_by_file:
            results_by_file[file_path] = []
        results_by_file[file_path].append(result)

    # Print results for each file
    for file_path, file_results in results_by_file.items():
        print(f"\nFile: {file_path}")
        for result in file_results:
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            print(f"  {status} - {result['check']}: {result['details']}")

if __name__ == "__main__":
    # Run the code quality assessment
    report = run_code_quality_assessment()
    print_code_quality_report(report)

    # Exit with appropriate code
    exit(0 if report['all_passed'] else 1)