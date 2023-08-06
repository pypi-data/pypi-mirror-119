#!/usr/bin/env python
"""fns for clang-format, clang-tidy, oclint"""
import argparse
import difflib
import os
import re
import shutil
import subprocess as sp
import sys


class Command:
    """Super class that all commands inherit"""

    def __init__(self, command, look_behind, args):
        self.args = args
        self.look_behind = look_behind
        self.command = command
        self.set_file_regex()
        # Will be [] if not run using pre-commit or if there are no committed files
        self.files = self.get_added_files()
        self.edit_in_place = False

        self.stdout = b""
        self.stderr = b""
        self.returncode = 0

    def set_file_regex(self):
        """Get the file regex for a command's target files from the .pre-commit-hooks.yaml."""
        file_regex = {
            "clang-format": r".*\.(?:c|cc|cxx|cpp|h|hpp|hxx|m|mm|java)$",
            "oclint": r".*\.(?:c|cc|cxx|cpp|h|hpp|hxx|m)$",
            "clang-tidy": r".*\.(?:c|cc|cxx|cpp|h|hpp|hxx|m)$",
            "cppcheck": r".*\.(?:c|cc|cxx|cpp|h|hpp|hxx|m)$",
            "uncrustify": r".*\.(?:c|cc|cxx|cpp|h|hpp|hxx|m|mm|d|java|vala)$",
            "cpplint": r".*\.(?:c|cc|cpp|cu|cuh|cxx|h|hh|hpp|hxx)$",
            "include-what-you-use": r".*\.(?:c|cc|cxx|cpp|cu|h|hpp|hxx)$",
        }
        self.file_regex = file_regex[self.command]

    def check_installed(self):
        """Check if command is installed and fail exit if not."""
        path = shutil.which(self.command)
        if path is None:
            website = "https://github.com/pocc/pre-commit-hooks#example-usage"
            problem = self.command + " not found"
            details = """Make sure {} is installed and on your PATH.\nFor more info: {}""".format(
                self.command, website
            )  # noqa: E501
            self.raise_error(problem, details)

    def get_added_files(self):
        """Find added files using git. Taken from https://github.com/pre-commit/pre-commit-hooks/blob/master/pre_commit_hooks/util.py"""
        cmd = ["git", "diff", "--staged", "--name-only", "--diff-filter=A"]
        sp_child = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        if sp_child.stderr or sp_child.returncode != 0:
            self.raise_error("Problem determining which files are being committed using git.", sp_child.stderr.decode())
        added_files = sp_child.stdout.decode().splitlines()
        # If no unstaged files, match the file regex against sys argv
        if not added_files:
            added_files = sys.argv
        added_files = [f for f in added_files if re.search(self.file_regex, f)]
        return added_files

    def parse_args(self, args):
        """Parse the args into usable variables"""
        self.args = list(sys.argv[1:])  # don't include calling function
        for arg in sys.argv:
            if arg in self.files:
                self.args.remove(arg)
            if arg.startswith("--version"):
                # If --version is passed in as 2 arguments, where the second is version
                if arg == "--version" and sys.argv.index(arg) != len(sys.argv) - 1:
                    expected_version = sys.argv[sys.argv.index(arg) + 1]
                # Expected split of --version=8.0.0 or --version 8.0.0 with as many spaces as needed
                else:
                    expected_version = arg.replace(" ", "").replace("=", "").replace("--version", "")
                actual_version = self.get_version_str()
                self.assert_version(actual_version, expected_version)
        # All commands other than clang-tidy or oclint require files, --version ok
        is_cmd_clang_analyzer = self.command == "clang-tidy" or self.command == "oclint"
        has_args = self.files or self.args or "version" in self.args
        if not has_args and not is_cmd_clang_analyzer:
            self.raise_error("Missing arguments", "No file arguments found and no files are pending commit.")

    def add_if_missing(self, new_args):
        """Add a default if it's missing from the command. This library
        exists to force checking, so prefer those options.
        len(new_args) should be 1, or 2 for options like --key=value

        If first arg is missing, add new_args to command's args
        Do not change an option - in those cases return."""
        new_arg_key = new_args[0].split("=")[0]
        for arg in self.args:
            existing_arg_key = arg.split("=")[0]
            if existing_arg_key == new_arg_key:
                return
        self.args += new_args

    def assert_version(self, actual_ver, expected_ver):
        """--version hook arg enforces specific versions of tools."""
        expected_len = len(expected_ver)  # allows for fuzzy versions
        if expected_ver not in actual_ver[:expected_len]:
            problem = "Version of " + self.command + " is wrong"
            details = """Expected version: {}
Found version: {}
Edit your pre-commit config or use a different version of {}.""".format(
                expected_ver, actual_ver, self.command
            )
            self.raise_error(problem, details)

    def raise_error(self, problem, details):
        """Raise a formatted error."""
        format_list = [self.command, problem, details]
        stderr_str = """Problem with {}: {}\n{}\n""".format(*format_list)
        # All strings are generated by this program, so decode should be safe
        self.stderr = stderr_str.encode()
        self.returncode = 1
        sys.stderr.buffer.write(self.stderr)
        sys.exit(self.returncode)

    def get_version_str(self):
        """Get the version string like 8.0.0 for a given command."""
        args = [self.command, "--version"]
        sp_child = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)
        version_str = str(sp_child.stdout, encoding="utf-8")
        # After version like `8.0.0` is expected to be '\n' or ' '
        if not re.search(self.look_behind, version_str):
            details = """The version format for this command has changed.
Create an issue at github.com/pocc/pre-commit-hooks."""
            self.raise_error("getting version", details)
        regex = self.look_behind + r"((?:\d+\.)+[\d+_\+\-a-z]+)"
        version = re.search(regex, version_str).group(1)
        return version


class StaticAnalyzerCmd(Command):
    """Commmands that analyze code and are not formatters.s"""

    def __init__(self, command, look_behind, args):
        super().__init__(command, look_behind, args)

    def run_command(self, args):
        """Run the command and check for errors. Args includes options and filepaths"""
        args = [self.command, *args]
        sp_child = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)
        self.stdout += sp_child.stdout
        self.stderr += sp_child.stderr
        self.returncode = sp_child.returncode

    def exit_on_error(self):
        if self.returncode != 0:
            sys.stderr.buffer.write(self.stdout + self.stderr)
            sys.exit(self.returncode)


class FormatterCmd(Command):
    """Commands that format code: clang-format, uncrustify"""

    def __init__(self, command, look_behind, args):
        super().__init__(command, look_behind, args)
        self.file_flag = None

    def set_diff_flag(self):
        self.no_diff_flag = "--no-diff" in self.args
        if self.no_diff_flag:
            self.args.remove("--no-diff")

    def compare_to_formatted(self, filename_str: str) -> None:
        """Compare the expected formatted output to file contents."""
        # This string encode is from argparse, so we should be able to trust it.
        filename = filename_str.encode()
        actual = self.get_filelines(filename)
        expected = self.get_formatted_lines(filename)
        if self.edit_in_place:
            # If edit in place is used, the formatter will fix in place with
            # no stdout. So compare the before/after file for hook pass/fail
            expected = self.get_filelines(filename)
        diff = list(
            difflib.diff_bytes(difflib.unified_diff, actual, expected, fromfile=b"original", tofile=b"formatted")
        )
        if len(diff) > 0:
            if not self.no_diff_flag:
                header = filename + b"\n" + 20 * b"=" + b"\n"
                self.stderr += header + b"\n".join(diff) + b"\n"
            self.returncode = 1

    def get_filename_opts(self, filename: bytes):
        """uncrustify, to get stdout like clang-format, requires -f flag"""
        if self.file_flag and not self.edit_in_place:
            return [self.file_flag, filename]
        return [filename]

    def get_formatted_lines(self, filename: bytes):
        """Get the expected output for a command applied to a file."""
        filename_opts = self.get_filename_opts(filename)
        args = [self.command, *self.args, *filename_opts]
        child = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)
        if len(child.stderr) > 0 or child.returncode != 0:
            problem = f"Unexpected Stderr/return code received when analyzing {filename}.\nArgs: {args}"
            self.raise_error(problem, child.stdout.decode() + child.stderr.decode())
        if child.stdout == b"":
            return []
        return child.stdout.split(b"\x0a")

    def get_filelines(self, filename):
        """Get the lines in a file."""
        if not os.path.exists(filename):
            self.raise_error(f"File {filename} not found", "Check your path to the file.")
        with open(filename, "rb") as f:
            filetext = f.read()
        return filetext.split(b"\x0a")
