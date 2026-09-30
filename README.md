# CIS8

> **CIS8** is an 8-bit assembly language designed for the **LIS8 CPU**, an 8-bit CPU simulation made in Scratch.

CIS8 provides a small set of instructions for:

* Memory manipulation
* Arithmetic
* Program flow
* Functions
* Conditional logic

CIS8 is designed to be **simple and close to the hardware**. Programs are written using short instructions that operate directly on memory addresses.

---

## 📖 Language Overview

CIS8 has **8 keywords**:

| Keyword | Purpose                               |
| :-----: | ------------------------------------- |
|  `ADD`  | Addition                              |
|  `SUB`  | Subtraction                           |
|  `INS`  | Insert a value into memory            |
|  `MOV`  | Move a value between memory addresses |
|  `CMP`  | Compare two memory addresses          |
|  `JMP`  | Change the program counter            |
|  `REL`  | Execute a function                    |
|  `DEF`  | Define a function                     |

Each keyword is used for a different arithmetic, logical, memory, or program-control function.

---

## ⚙️ Instruction Format

CIS8 instructions are usually **8–7 characters long** and are structured as:

```text
3-bit Opcode, 2-bit Operand, 2-bit Operand
```

For example:

```asm
add 01,02
```

The instruction contains:

```text
ADD | 01 | 02
 ↑     ↑    ↑
Opcode  A    B
```

---

# 🔧 Instructions

## `ADD`

```asm
add 01,02
```

Adds two memory addresses.

---

## `SUB`

```asm
sub 01,02
```

Subtracts two memory addresses.

---

## `INS`

```asm
ins 12,01
```

Inserts **Operand A** into the memory address specified by **Operand B**.

In this example:

```text
12 → memory address 01
```

---

## `MOV`

```asm
mov 01,02
```

Moves the value from memory address **A** to memory address **B**.

---

## `CMP`

```asm
cmp 01,02
```

Compares two memory addresses.

If the comparison returns `0`, any following instructions marked with the `f` tag execute.

This essentially provides an **if statement**.

Example:

```asm
cmp 01,02[
ins 01,02 f
]
```

If addresses `01` and `02` compare as equal, the `INS` instruction executes.

---

## `JMP`

```asm
jmp 01,00
```

Sets the **program counter (PC)** to Operand A.

In this example:

```text
PC = 01
```

---

## `REL`

```asm
rel 02,01
```

Executes a function at a specified address and then returns to the previous address.

---

## `DEF`

```asm
def 06,00
```

Creates a function with the length specified by Operand A.

---

# 💬 Comments

CIS8 supports both single-line and multiline comments.

### Single-line Comments

Single-line comments use:

```text
/ ... \
```

Example:

```asm
/ This is a comment \
```

### Multiline Comments

Multiline comments use:

```text
// ... \\
```

Example:

```asm
// This is a
multiline comment \\
```

Comments are not executed as instructions.

---

# 🔀 Conditional Blocks

`CMP` and `DEF` use square brackets to define their blocks.

**Indentation is not required.**

## CMP Example

```asm
cmp 01,02[
ins 01,02 f
]
```

The instruction marked with `f` executes when the comparison succeeds.

The `f` tag is placed at the **end of the instruction**:

```asm
ins 01,02 f
```

---

# 🧩 Function Blocks

`DEF` can also use square brackets to contain the function's instructions.

```asm
def 06,0[
ins 01,02 f
]
```

The instructions inside the brackets form the function.

---

# 💻 Using the CIS8 Compiler

CIS8 programs can be compiled using the **CIS8 compiler**.

From a terminal, run:

```bash
python "C:/Path/to/your/compiler/location/CIS8C" (yourfile).cis8
```

Replace:

```text
C:/Path/to/your/compiler/location/CIS8C
```

with the location of your CIS8 compiler and:

```text
(yourfile).cis8
```

with the CIS8 source file you want to compile.

### Example

```bash
python "C:/CIS8/CIS8C.py" program.cis8
```

If the compiler is configured correctly, the program will be compiled.

---

# 📝 Example CIS8 Program

A simple CIS8 program can look like this:

```asm
/ Simple CIS8 program \

ins 01,01

add 01,02
sub 01,02

cmp 02,03[
ins 01,05 f
]

jmp 01,00
```

This demonstrates:

* Comments
* Memory insertion
* Addition
* Subtraction
* Comparison
* Conditional execution
* Jumping

---

# 📌 Quick Reference

```text
ADD  A,B   Add two memory addresses
SUB  A,B   Subtract two memory addresses
INS  A,B   Insert A into memory address B
MOV  A,B   Move memory address A to B
CMP  A,B   Compare two memory addresses
JMP  A,B   Set PC to A
REL  A,B   Execute a function
DEF  A,B   Create a function
```

CIS8 is intended to provide a **small, straightforward assembly language for the LIS8 8-bit CPU**, while remaining simple enough to implement and experiment with in Scratch.
