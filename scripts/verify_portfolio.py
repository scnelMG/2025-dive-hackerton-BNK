#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
# How to run: python scripts/verify_portfolio.py
from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
MAX_TRACKED_FILE_BYTES: Final = 50 * 1024 * 1024
NOTEBOOK_OUTPUT_LIMIT: Final = 500
PORTFOLIO_GUIDE_HEADING: Final = "# 포트폴리오 검토 안내"
FORBIDDEN_TRACKED_SUFFIXES: Final = (
    ".csv",
    ".parquet",
    ".xls",
    ".xlsx",
    ".jsonl",
    ".zip",
)
ALLOWED_DATA_DOCUMENTS: Final = (
    "data/README.md",
    "data/input-contract.md",
)
REQUIRED_PATHS: Final = (
    "README.md",
    "requirements.txt",
    "data/README.md",
    "data/input-contract.md",
    "docs/analysis-method.md",
    "docs/interest-analysis-walkthrough.md",
    "docs/model-validation.md",
    "docs/execution-measurement.md",
    "docs/presentation-assets.md",
    "docs/public-safety.md",
    "docs/reproducibility.md",
    "docs/results.md",
    "docs/usage.md",
    "docs/verification-report.md",
    "assets/presentation/two-track-framework.png",
    "assets/presentation/noninterest-growth-roadmap.png",
    "assets/presentation/loan-targeting-strategy.png",
    "assets/analysis/noninterest-elbow-k4.png",
)
README_SECTIONS: Final = (
    "## 문제 정의: 고객 분류가 아니라 수익 구조를 푸는 일",
    "## 접근 방향: 수익 목표에 따라 분석 축을 분리",
    "## 데이터: 왜 전처리가 분석의 출발점이었나",
    "## 핵심 결과",
    "## 내 역할: 데이터 전처리 및 모델링",
)
NOTEBOOKS: Final = (
    "notebooks/1.전처리_및_군집화.ipynb",
    "notebooks/2.비이자이익_분석.ipynb",
    "notebooks/3.이자이익_분석.ipynb",
)
MARKDOWN_LINK_PATTERN: Final = re.compile(r"\]\(([^)]+)\)")
FORBIDDEN_NOTEBOOK_EXECUTION_PATTERNS: Final = (
    "pip install",
    "urlretrieve",
    "koreanize_matplotlib",
    "Path.home()",
)


@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True, slots=True)
class TrackedFileListing:
    paths: tuple[Path, ...]
    error: str | None


def check_required_paths() -> CheckResult:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).is_file()]
    if missing:
        return CheckResult("required paths", False, ", ".join(missing))
    return CheckResult("required paths", True, "all required files exist")


def check_readme_structure() -> CheckResult:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    positions = [readme.find(section) for section in README_SECTIONS]
    missing = [section for section, position in zip(README_SECTIONS, positions) if position < 0]
    if missing:
        return CheckResult("README structure", False, "missing: " + " | ".join(missing))
    if positions != sorted(positions):
        return CheckResult("README structure", False, "problem-to-contribution order changed")
    return CheckResult("README structure", True, "problem-first narrative is intact")


def check_markdown_links() -> CheckResult:
    missing: list[str] = []
    documents = (
        ROOT / "README.md",
        *ROOT.glob("data/*.md"),
        *ROOT.glob("docs/*.md"),
        *ROOT.glob("notebooks/*.md"),
    )
    for document in documents:
        text = document.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            destination = document.parent / target.split("#", maxsplit=1)[0]
            if not destination.exists():
                missing.append(f"{document.relative_to(ROOT)} -> {target}")
    if missing:
        return CheckResult("Markdown links", False, "; ".join(missing))
    return CheckResult("Markdown links", True, "all local links resolve")


def check_presentation_assets() -> CheckResult:
    invalid: list[str] = []
    for path in REQUIRED_PATHS:
        if not path.startswith(("assets/presentation/", "assets/analysis/")):
            continue
        with (ROOT / path).open("rb") as file:
            if file.read(8) != b"\x89PNG\r\n\x1a\n":
                invalid.append(path)
    if invalid:
        return CheckResult("visual assets", False, ", ".join(invalid))
    return CheckResult("visual assets", True, "README assets are valid PNG files")


def join_notebook_text(value: str | list[str] | None) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "".join(value)
    return value


def is_likely_tabular_text(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    aligned_lines = sum(bool(re.search(r"\S\s{2,}\S", line)) for line in lines)
    return len(lines) >= 4 and aligned_lines >= 3


def check_notebooks() -> CheckResult:
    issues: list[str] = []
    for relative_path in NOTEBOOKS:
        path = ROOT / relative_path
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            issues.append(f"{relative_path}: invalid JSON")
            continue
        cells = notebook.get("cells", [])
        guide = join_notebook_text(cells[0].get("source") if cells else None)
        if not cells or cells[0].get("cell_type") != "markdown" or PORTFOLIO_GUIDE_HEADING not in guide:
            issues.append(f"{relative_path}: missing portfolio guide")
        for cell in cells:
            source = join_notebook_text(cell.get("source"))
            forbidden_pattern = next(
                (pattern for pattern in FORBIDDEN_NOTEBOOK_EXECUTION_PATTERNS if pattern in source),
                None,
            )
            if forbidden_pattern is not None:
                issues.append(f"{relative_path}: forbidden execution pattern {forbidden_pattern}")
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    issues.append(f"{relative_path}: stored error output")
                    break
                data = output.get("data", {})
                html = join_notebook_text(data.get("text/html"))
                if "<table" in html:
                    issues.append(f"{relative_path}: raw HTML table output")
                    break
                plain_text = join_notebook_text(data.get("text/plain"))
                if is_likely_tabular_text(plain_text):
                    issues.append(f"{relative_path}: aligned text table output")
                    break
                stream = join_notebook_text(output.get("text"))
                if output.get("output_type") == "stream" and len(stream) > NOTEBOOK_OUTPUT_LIMIT:
                    issues.append(f"{relative_path}: long stream output")
                    break
                if output.get("output_type") == "execute_result" and len(plain_text) > NOTEBOOK_OUTPUT_LIMIT:
                    issues.append(f"{relative_path}: long text output")
                    break
    if issues:
        return CheckResult("notebook publication", False, "; ".join(issues))
    return CheckResult("notebook publication", True, "no stored errors or raw table traces")


def listed_tracked_files() -> TrackedFileListing:
    try:
        completed = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return TrackedFileListing((), "git executable was not found")
    except subprocess.CalledProcessError as error:
        return TrackedFileListing((), f"git ls-files failed with exit code {error.returncode}")
    return TrackedFileListing(tuple(ROOT / line for line in completed.stdout.splitlines() if line), None)


def check_required_paths_tracked() -> CheckResult:
    listing = listed_tracked_files()
    if listing.error:
        return CheckResult("required paths tracked", False, listing.error)
    tracked = {path.relative_to(ROOT).as_posix() for path in listing.paths}
    missing = [path for path in REQUIRED_PATHS if path not in tracked]
    if missing:
        return CheckResult("required paths tracked", False, ", ".join(missing))
    return CheckResult("required paths tracked", True, "all required public files are tracked")


def check_sensitive_tracked_paths() -> CheckResult:
    listing = listed_tracked_files()
    if listing.error:
        return CheckResult("sensitive tracked paths", False, listing.error)
    forbidden = [
        path.relative_to(ROOT).as_posix()
        for path in listing.paths
        if path.suffix.lower() in FORBIDDEN_TRACKED_SUFFIXES
        or path.relative_to(ROOT).as_posix().startswith("data/")
        and path.relative_to(ROOT).as_posix() not in ALLOWED_DATA_DOCUMENTS
    ]
    if forbidden:
        return CheckResult("sensitive tracked paths", False, ", ".join(forbidden))
    return CheckResult("sensitive tracked paths", True, "no raw-data file type is tracked")


def check_tracked_file_sizes() -> CheckResult:
    listing = listed_tracked_files()
    if listing.error:
        return CheckResult("tracked file size", False, listing.error)
    oversized = [
        path.relative_to(ROOT).as_posix()
        for path in listing.paths
        if path.exists() and path.stat().st_size > MAX_TRACKED_FILE_BYTES
    ]
    if oversized:
        return CheckResult("tracked file size", False, ", ".join(oversized))
    return CheckResult("tracked file size", True, "no tracked file exceeds 50MB")


def main() -> int:
    results = (
        check_required_paths(),
        check_required_paths_tracked(),
        check_readme_structure(),
        check_markdown_links(),
        check_presentation_assets(),
        check_notebooks(),
        check_sensitive_tracked_paths(),
        check_tracked_file_sizes(),
    )
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
