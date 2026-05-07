# ModernAst

**ModernAst** is a lightweight Python module for syntactic analysis of source code. It parses Python-like code structures and generates an Abstract Syntax Tree (AST) representation.

## ✨ Currently Supported Nodes

- `import` – module imports  
- `if-elif-else` – conditional constructs  
- `pass` – no-operation statement  
- `def` – function definitions  
- `call` – function calls  

Additional nodes and language features are planned for future releases.

---

## 📘 Example

### Input Source Code

```python
import os

def main():
    if True == True:
        os.getpid()

if __name__ == '__main__':
    main()
```

### Generated AST Output
```python
[
    Import(
        node_pos=Position(start=(2, 0), end=(2, 9)),
        module=Module(
            node_pos=Position(start=(2, 7), end=(2, 9)),
            name='os'
        )
    ),
    Function(
        node_pos=Position(start=(4, 4), end=(4, 11)),
        name='main',
        body=[
            IfConstruct(
                node_pos=Position(start=(5, 7), end=(5, 20)),
                condition=BinaryOp(
                    node_pos=Position(start=(5, 7), end=(5, 19)),
                    left=BooleanLiteral(
                        node_pos=Position(start=(5, 7), end=(5, 11)),
                        value=True
                    ),
                    operator='==',
                    right=BooleanLiteral(
                        node_pos=Position(start=(5, 15), end=(5, 19)),
                        value=True
                    )
                ),
                body=[
                    Call(
                        node_pos=Position(start=(6, 8), end=(6, 19)),
                        objects=Variable(
                            node_pos=Position(start=(6, 8), end=(6, 10)),
                            name='os'
                        ),
                        args=[]
                    )
                ],
                elif_branches=[],
                else_body=None
            )
        ],
        args=[]
    ),
    IfConstruct(
        node_pos=Position(start=(8, 3), end=(8, 26)),
        condition=BinaryOp(
            node_pos=Position(start=(8, 3), end=(8, 25)),
            left=Variable(
                node_pos=Position(start=(8, 3), end=(8, 11)),
                name='__name__'
            ),
            operator='==',
            right=StringLiteral(
                node_pos=Position(start=(8, 15), end=(8, 25)),
                value='__main__'
            )
        ),
        body=[
            Call(
                node_pos=Position(start=(9, 4), end=(9, 10)),
                objects=Variable(
                    node_pos=Position(start=(9, 4), end=(9, 8)),
                    name='main'
                ),
                args=[]
            )
        ],
        elif_branches=[],
        else_body=None
    )
]
```