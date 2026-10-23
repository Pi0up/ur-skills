"""Command-line interface (CLI) for UR Tools.
Provides entry points for companion skills and automated CI checks.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ur_tools.id_allocator import IdAllocator
from ur_tools.init_repo import init_repository
from ur_tools.validator import RepoValidator
from ur_tools.verbatim_checker import VerbatimChecker
from ur_tools.views_generator import ViewsGenerator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ur-tools",
        description="CLI tool suite and validation engine for User Research (UR) knowledge repositories (socle-ur-spec v0.5)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize repository folder structure")
    init_parser.add_argument("--path", default=".", help="Repository root path")

    # allocate-id
    alloc_parser = subparsers.add_parser("allocate-id", help="Allocate next sequential ID and generate slug filename")
    alloc_parser.add_argument("--prefix", required=True, help="Atom prefix (e.g. INS, EVD, SRC, JOB)")
    alloc_parser.add_argument("--title", required=True, help="Atom title for slug generation")
    alloc_parser.add_argument("--year", type=int, default=None, help="Year (default: current year)")

    # validate
    val_parser = subparsers.add_parser("validate", help="Validate repository against normative rules (Section 17)")
    val_parser.add_argument("--profile", choices=["starter", "standard", "strict"], default=None, help="Validation profile override")

    # check-verbatim
    verb_parser = subparsers.add_parser("check-verbatim", help="Check that an evidence quote appears verbatim in its source")
    verb_parser.add_argument("--evidence", required=True, help="Path to EVD-*.md file")

    # generate-views
    view_parser = subparsers.add_parser("generate-views", help="Generate mandatory human views into /views/ (Section 20.4)")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "init":
        created = init_repository(args.path)
        print(f"UR repository structure initialized successfully. ({len(created)} directories created or verified)")
        return 0

    elif args.command == "allocate-id":
        allocator = IdAllocator()
        atom_id, filename = allocator.allocate(args.prefix, args.title, args.year)
        print(f"Allocated ID : {atom_id}")
        print(f"File name    : {filename}")
        return 0

    elif args.command == "validate":
        validator = RepoValidator()
        if args.profile:
            validator.profile = args.profile
        print(f"Running UR repository validation [Profile: {validator.profile}]...")
        report = validator.validate_all()

        for err in report.errors:
            print(f"[ERROR] (Rule {err.rule_number} - {err.rule_name}) in {err.file_path.name}: {err.message}")

        for warn in report.warnings:
            print(f"[WARN]  (Rule {warn.rule_number} - {warn.rule_name}) in {warn.file_path.name}: {warn.message}")

        print(f"\nResult: {len(report.errors)} error(s), {len(report.warnings)} warning(s).")
        return 0 if report.is_valid else 1

    elif args.command == "check-verbatim":
        checker = VerbatimChecker()
        res = checker.check(args.evidence)
        if res.is_valid:
            print(f"[OK] {res.message}")
            if res.matched_snippet:
                print(f"Matched snippet: \"{res.matched_snippet}\"")
            return 0
        else:
            print(f"[FAIL] {res.message}")
            return 1

    elif args.command == "generate-views":
        gen = ViewsGenerator()
        res = gen.generate_all()
        print("Generated views:")
        for k, p in res.items():
            print(f" - {k}: {p}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
