# CIS8

**CIS8** is an 8-bit assembly language designed for the **LIS8 CPU**, an 8-bit CPU simulation i made in scratch. It provides a small set of instructions for manipulating memory, performing arithmetic, controlling program flow, and creating simple conditional logic.

CIS8 is designed to be simple and close to the hardware. Programs are written using short instructions that operate directly on memory addresses.

## 1. Basic Program Structure

A CIS8 program is made up of instructions executed sequentially.

```asm
ins 01,01
add 01,02
sub 01,02
```

Each instruction normally contains:

```text
instruction operand,operand
```

Operands are generally two-digit memory addresses.

## 2. Comments

CIS8 supports single-line comments using `/`.

```asm
/ This is a comment \
```

Multiline comments use `//` and `\\`.

```asm
// This is
a multiline comment. \\
```

Comments are ignored by the compiler.

## 3. Memory

CIS8 programs work directly with memory addresses.

For example:

```asm
ins 25,10
```

stores the value `25` in memory address `10`.

Memory can then be used by arithmetic instructions:

```asm
add 10,11
```

The exact behavior of an instruction depends on the operation being performed.

## 4. Instructions

### INS

```asm
ins value,address
```

Stores a value in a memory address.

Example:

```asm
ins 10,01
```

Memory address `01` now contains `10`.

---

### ADD

```asm
add address,address
```

Adds the values associated with the two operands.

Example:

```asm
add 01,02
```

---

### SUB

```asm
sub address,address
```

Subtracts the second operand from the first.

Example:

```asm
sub 01,02
```

---

### INC

```asm
inc address
```

Increments a memory value by `1`.

Example:

```asm
inc 05
```

This increases the value stored at address `05`.

---

### DEC

```asm
dec address
```

Decrements a memory value by `1`.

Example:

```asm
dec 05
```

---

### MOV

```asm
mov source,destination
```

Moves a value from one memory address to another.

Example:

```asm
mov 01,05
```

---

### CMP

```asm
cmp address,address
```

Compares two values.

A `CMP` can be followed by a conditional block:

```asm
cmp 02,03[
inc 05 f
]
```

The instructions marked with `f` execute when the comparison evaluates as equal.

In this example, address `05` is incremented when addresses `02` and `03` contain equal values.

The `f` suffix identifies a conditional instruction.

## 5. Conditional Blocks

A conditional block begins with `[` and ends with `]`.

```asm
cmp 01,02[
add 01,03 f
inc 05 f
]
```

Instructions inside the block can be marked with `f`.

The compiler can automatically add the `f` suffix to instructions inside a conditional block when it is omitted.

For example:

```asm
cmp 01,02[
inc 05
]
```

can be compiled as:

```asm
cmp 01,02
inc 05f
```

## 6. Program Flow

### JMP

```asm
jmp address,00
```

Changes the program counter to the specified address.

Example:

```asm
jmp 01,00
```

`JMP` can be used to create loops and other forms of program flow.

## 7. Functions

CIS8 provides `DEF` and `REL` for defining and calling functions.

### DEF

```asm
def length,00
```

Defines a function with the specified length.

### REL

```asm
rel address,00
```

Calls a function at the specified address and returns to the previous execution location.

Function behavior depends on the CIS8 runtime and memory layout.

## 8. Example Program

The following program increments memory address `05` whenever addresses `02` and `03` contain equal values:

```asm
ins 01,01

add 01,02
sub 01,02

cmp 02,03[
inc 05 f
]
```

Another simple example:

```asm
ins 10,01
ins 20,02

add 01,02
```

This initializes two memory locations and then performs an addition.

## 9. Instruction Summary

| Instruction | Purpose                          |
| ----------- | -------------------------------- |
| `INS`       | Store a value in memory          |
| `ADD`       | Add values                       |
| `SUB`       | Subtract values                  |
| `INC`       | Increment a value                |
| `DEC`       | Decrement a value                |
| `MOV`       | Move a value                     |
| `CMP`       | Compare values                   |
| `JMP`       | Change program execution address |
| `REL`       | Call a function                  |
| `DEF`       | Define a function                |

## 10. Design Philosophy

CIS8 is intentionally small.

Instead of providing many high-level features, CIS8 exposes basic operations that can be combined to create more complex behavior. This makes the language suitable for small processors, emulators, operating-system experiments, and other systems where keeping the instruction set simple is useful.

CIS8 is also intended to serve as the low-level language to use the LIS8 CPU

where the compiler has assigned `counter` to memory address `05`.

## 11. File Format

CIS8 source files can use the `.cis8` extension.

Example:

```text
program.cis8
```

The CIS8 compiler converts the source code into the compiled representation used by the LIS8 processor.
