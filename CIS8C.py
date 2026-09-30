import argparse
import re
import sys
from pathlib import Path


VERSION = "CIS8C 0.2"


# ============================================================
# CIS8 OPCODES
# ============================================================

OPCODES = {
    "add": "000",
    "sub": "001",
    "ins": "010",
    "mov": "100",
    "cmp": "011",
    "jmp": "101",
    "rel": "010",
    "def": "111",
}


class CIS8CompileError(Exception):
    pass


# ============================================================
# COMMENT REMOVAL
# ============================================================

def remove_comments(source):
    """
    CIS8 comments:

        / This is a comment \

    Multiline comments:

        // This is a
           multiline comment
        \\
    """

    # --------------------------------------------------------
    # Remove multiline comments first
    # Format:
    #
    # // comment
    # comment
    # \\
    # --------------------------------------------------------

    source = re.sub(
        r"//.*?\\\\",
        "",
        source,
        flags=re.DOTALL
    )

    # --------------------------------------------------------
    # Remove single-line comments
    # Format:
    #
    # / comment \
    # --------------------------------------------------------

    source = re.sub(
        r"/.*?\\",
        "",
        source
    )

    return source


# ============================================================
# COMPILE ONE INSTRUCTION
# ============================================================

def compile_instruction(line, line_number):

    original = line.strip()

    if not original:
        return None

    # --------------------------------------------------------
    # Check for f modifier
    # --------------------------------------------------------

    conditional = False

    if re.search(
        r"\bf\s*$",
        original,
        re.IGNORECASE
    ):
        conditional = True

        original = re.sub(
            r"\bf\s*$",
            "",
            original,
            flags=re.IGNORECASE
        ).strip()

    # --------------------------------------------------------
    # Find instruction mnemonic
    # --------------------------------------------------------

    match = re.match(
        r"^([A-Za-z]+)\s*(.*)$",
        original
    )

    if not match:

        raise CIS8CompileError(
            f"Line {line_number}: invalid instruction: "
            f"{original}"
        )

    mnemonic = match.group(1).lower()
    operands = match.group(2).strip()

    # --------------------------------------------------------
    # Check opcode
    # --------------------------------------------------------

    if mnemonic not in OPCODES:

        raise CIS8CompileError(
            f"Line {line_number}: unknown instruction "
            f"'{mnemonic}'"
        )

    opcode = OPCODES[mnemonic]

    # --------------------------------------------------------
    # Check operands
    # --------------------------------------------------------

    if not operands:

        raise CIS8CompileError(
            f"Line {line_number}: missing operands"
        )

    # Remove spaces
    operands = operands.replace(" ", "")

    # Remove commas
    operands = operands.replace(",", "")

    # --------------------------------------------------------
    # CIS8 currently expects:
    #
    # 01,02
    #
    # which becomes:
    #
    # 0102
    # --------------------------------------------------------

    if not re.fullmatch(
        r"\d+",
        operands
    ):

        raise CIS8CompileError(
            f"Line {line_number}: invalid operands "
            f"'{operands}'"
        )

    if len(operands) != 4:

        raise CIS8CompileError(
            f"Line {line_number}: expected two "
            f"2-digit operands, for example 01,02"
        )

    # --------------------------------------------------------
    # Build compiled instruction
    # --------------------------------------------------------

    result = opcode + operands

    # Preserve f
    if conditional:
        result += "f"

    return result


# ============================================================
# COMPILE SOURCE
# ============================================================

def compile_source(source):

    # Remove comments
    source = remove_comments(source)

    output = []

    # --------------------------------------------------------
    # Track whether we are inside a CMP or DEF block
    # --------------------------------------------------------

    block_type = None

    lines = source.splitlines()

    for line_number, line in enumerate(
        lines,
        start=1
    ):

        line = line.strip()

        if not line:
            continue

        # ----------------------------------------------------
        # Opening a block
        #
        # Example:
        #
        # cmp 01,02[
        #
        # or:
        #
        # def 06,00[
        # ----------------------------------------------------

        if line.endswith("["):

            line = line[:-1].strip()

            if not line:

                raise CIS8CompileError(
                    f"Line {line_number}: empty block"
                )

            # Compile opening instruction
            compiled = compile_instruction(
                line,
                line_number
            )

            if compiled is not None:
                output.append(compiled)

            # Find instruction name
            parts = line.split()

            if not parts:

                raise CIS8CompileError(
                    f"Line {line_number}: invalid block"
                )

            instruction = parts[0].lower()

            # Only CMP and DEF can open blocks
            if instruction == "cmp":

                block_type = "cmp"

            elif instruction == "def":

                block_type = "def"

            else:

                raise CIS8CompileError(
                    f"Line {line_number}: only CMP and DEF "
                    f"can open blocks"
                )

            continue

        # ----------------------------------------------------
        # Closing a block
        # ----------------------------------------------------

        if line == "]":

            if block_type is None:

                raise CIS8CompileError(
                    f"Line {line_number}: unexpected ]"
                )

            block_type = None

            continue

        # ----------------------------------------------------
        # Prevent another block from opening accidentally
        # ----------------------------------------------------

        if "[" in line or "]" in line:

            raise CIS8CompileError(
                f"Line {line_number}: invalid block syntax"
            )

        # ----------------------------------------------------
        # Instructions inside CMP / DEF
        #
        # f is optional.
        #
        # Without f:
        #
        #     ins 12,03
        #
        # becomes:
        #
        #     ins 12,03 f
        #
        # If f already exists, it is left alone.
        # ----------------------------------------------------

        if block_type in ("cmp", "def"):

            has_f = bool(
                re.search(
                    r"\bf\s*$",
                    line,
                    re.IGNORECASE
                )
            )

            if not has_f:

                line += " f"

        # ----------------------------------------------------
        # Compile instruction
        # ----------------------------------------------------

        compiled = compile_instruction(
            line,
            line_number
        )

        if compiled is not None:

            output.append(compiled)

    # --------------------------------------------------------
    # Check for unclosed block
    # --------------------------------------------------------

    if block_type is not None:

        raise CIS8CompileError(
            f"Unclosed {block_type.upper()} block"
        )

    return "\n".join(output)


# ============================================================
# COMPILE FILE
# ============================================================

def compile_file(
    source_path,
    output_path=None
):

    source_path = Path(source_path)

    # --------------------------------------------------------
    # Check source file
    # --------------------------------------------------------

    if not source_path.exists():

        raise CIS8CompileError(
            f"source file not found: "
            f"{source_path}"
        )

    if not source_path.is_file():

        raise CIS8CompileError(
            f"source path is not a file: "
            f"{source_path}"
        )

    # --------------------------------------------------------
    # Read source
    # --------------------------------------------------------

    try:

        source = source_path.read_text(
            encoding="utf-8"
        )

    except OSError as error:

        raise CIS8CompileError(
            f"could not read source file: "
            f"{error}"
        )

    # --------------------------------------------------------
    # Compile
    # --------------------------------------------------------

    compiled = compile_source(source)

    # --------------------------------------------------------
    # Automatically create .bin path
    # --------------------------------------------------------

    if output_path is None:

        output_path = source_path.with_suffix(
            ".bin"
        )

    else:

        output_path = Path(output_path)

    # --------------------------------------------------------
    # Write binary output
    # --------------------------------------------------------

    try:

        output_path.write_text(
            compiled + "\n",
            encoding="utf-8"
        )

    except OSError as error:

        raise CIS8CompileError(
            f"could not write output file: "
            f"{error}"
        )

    return output_path


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        prog="CIS8C",
        description="CIS8 source code compiler"
    )

    # --------------------------------------------------------
    # Source file
    # --------------------------------------------------------

    parser.add_argument(
        "source",
        help="CIS8 source file"
    )

    # --------------------------------------------------------
    # Optional output file
    # --------------------------------------------------------

    parser.add_argument(
        "-o",
        "--output",
        help="output .bin file",
        default=None
    )

    # --------------------------------------------------------
    # Version
    # --------------------------------------------------------

    parser.add_argument(
        "--version",
        action="version",
        version=VERSION
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Compile
    # --------------------------------------------------------

    try:

        output_path = compile_file(
            args.source,
            args.output
        )

    except CIS8CompileError as error:

        print(
            f"CIS8C error: {error}"
        )

        return 1

    except Exception as error:

        print(
            f"CIS8C unexpected error: {error}"
        )

        return 1

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print(
        f"CIS8C: compiled {args.source}"
    )

    print(
        f"CIS8C: output  {output_path}"
    )

    return 0


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    sys.exit(main())