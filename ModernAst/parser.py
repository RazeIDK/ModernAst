from objects import *
import keyword
from enum import Enum, auto
from typing import List, Any


# контекст
class Context(Enum):
    NULL = auto()

    NAME = auto()

    IMPORT_CREATE = auto()

    FUNCTION_CREATE = auto()
    FUNCTION_NAME = auto()

    FUNCTION_CALL = auto()
    METHOD_CALL = auto()

    IFCONSTRUCT_CREATE = auto()
    IFCONSTRUCT_CONDITION = auto()
    
    ELIF_CREATE = auto()
    ELSE_CREATE = auto()


# строитель блоков
class BlockBuilder:
    def __init__(self, token_objects: List[Any]):
        self.tokens_objects = token_objects
    
    def build(self):
        root = Block(level=0, tokens=[], parent=None)
        stack = [root]
        
        for token in self.tokens_objects:
            if token.t_name == "INDENT":
                new_block = Block(
                    level=len(stack),
                    tokens=[],
                    parent=stack[-1]
                )
                stack[-1].children.append(new_block)
                stack.append(new_block)
                
            elif token.t_name == "DEDENT":
                if len(stack) > 1:
                    stack.pop()
                    
            else:
                stack[-1].tokens.append(token)
        
        self._clean_tokens(root)
        self._remove_empty_blocks(root)
        
        return root
    
    def _clean_tokens(self, block):
        block.tokens = [t for t in block.tokens if t.t_name not in ("INDENT", "DEDENT")]
        for child in block.children:
            self._clean_tokens(child)
    
    def _remove_empty_blocks(self, block):
        """
        Удаляет пустые блоки
        """
        for child in block.children[:]:
            self._remove_empty_blocks(child)
            if not child.tokens and not child.children:
                block.children.remove(child)


# построение AST
class AstBuilder:
    def __init__(self, tokens_objects: list):
        self._tokens_objects = tokens_objects
        self._keywords = keyword.kwlist
        self._ast = []

        self.block_builder = BlockBuilder(self._tokens_objects)
        self.block = self.block_builder.build()

    def traverse(self):
        self._walk_block(self.block, level=0)
        print("ast:")
        print(self._ast)
    
    def parent_priorities(self, tokens):
        """
        Расставление приоритетов в скобках  
        """
        count_tokens = len(tokens)
        tokens_priorities = []
        paren_depth = 0
        paren_positions = {}

        for i in range(count_tokens):
            token_object = tokens[i]

            if token_object.t_string == "(":
                paren_depth += 1
                paren_positions[i] = paren_depth
                tokens_priorities.append((token_object, paren_depth, "OPEN"))

            elif token_object.t_string == ")":
                open_pos = None
                for pos, depth in paren_positions.items():
                    if depth == paren_depth:
                        open_pos = pos
                        break
                tokens_priorities.append((token_object, paren_depth, "CLOSE"))
                paren_depth -= 1

            elif token_object.t_name == "OP" and token_object.t_string in Operator.get_all_symbols():
                priority = self._get_operator_priority(token_object.t_string)
                total_priority = priority + (paren_depth * 100)
                tokens_priorities.append((token_object, total_priority, "OPERATOR"))

            else:
                tokens_priorities.append((token_object, paren_depth, "OPERAND"))

        return tokens_priorities

    def _get_operator_priority(self, operator):
        priorities = {
            "**": 10,
            "~": 9,
            "*": 8, "/": 8, "//": 8, "%": 8,
            "+": 7, "-": 7,
            "<<": 6, ">>": 6,
            "<": 5, ">": 5, "<=": 5, ">=": 5, "==": 5, "!=": 5,
            "not": 4,
            "and": 3,
            "or": 2,
        }
        return priorities.get(operator, 0)

    def build_expression_from_tokens(self, tokens):
        if not tokens:
            return None

        while len(tokens) > 1 and tokens[0].t_string == "(" and tokens[-1].t_string == ")":
            depth = 0
            valid = True
            for i, t in enumerate(tokens):
                if t.t_string == "(":
                    depth += 1
                elif t.t_string == ")":
                    depth -= 1
                    if depth == 0 and i != len(tokens) - 1:
                        valid = False
                        break
            if valid and depth == 0:
                tokens = tokens[1:-1]
            else:
                break

        if len(tokens) == 1:
            return self._token_to_expression(tokens[0])

        min_priority_index = -1
        min_priority = float('inf')
        
        for i, token in enumerate(tokens):
            if hasattr(token, 't_string') and token.t_string in ("and", "or"):
                priority = self._get_operator_priority(token.t_string)
                if priority < min_priority:
                    min_priority = priority
                    min_priority_index = i
        
        if min_priority_index == -1:
            token_priorities = self.parent_priorities(tokens)
            for i, (token, priority, token_type) in enumerate(token_priorities):
                if token_type == "OPERATOR" and priority < min_priority:
                    min_priority = priority
                    min_priority_index = i

        if min_priority_index == -1:
            return self._token_to_expression(tokens[0])

        left_tokens = tokens[:min_priority_index]
        right_tokens = tokens[min_priority_index + 1:]
        operator_token = tokens[min_priority_index]

        left_expr = self.build_expression_from_tokens(left_tokens)
        right_expr = self.build_expression_from_tokens(right_tokens)

        if left_expr and right_expr:
            return BinaryOp(
                node_pos=Position(
                    left_expr.node_pos.start,
                    right_expr.node_pos.end
                ),
                left=left_expr,
                operator=operator_token.t_string,
                right=right_expr
                )

        return None

    def _token_to_expression(self, token):
        """
        TOken > expression
        """
        if token.t_name == "NUMBER":
            return NumberLiteral(
                node_pos=token.t_pos,
                value=int(token.t_string)
            )
        elif token.t_name == "STRING":
            return StringLiteral(
                node_pos=token.t_pos,
                value=token.t_string.strip('"\'')
            )
        elif token.t_name == "NAME":
            if token.t_string == "True":
                return BooleanLiteral(node_pos=token.t_pos, value=True)
            elif token.t_string == "False":
                return BooleanLiteral(node_pos=token.t_pos, value=False)
            else:
                return Variable(node_pos=token.t_pos, name=token.t_string)
        return None

    def _walk_block(self, block, level=0):
        """
        Обход блоков для присваивания в тела
        """
        if not hasattr(block, 'nodes'):
            block.nodes = self._parse_tokens(block.tokens)

        child_idx = 0
        children_list = [child for child in block.children if child.level == level + 1]

        for node in block.nodes:
            if isinstance(node, IfConstruct):
                if child_idx < len(children_list):
                    child = children_list[child_idx]
                    self._walk_block(child, level + 1)
                    node.body = child.nodes
                    child_idx += 1
                else:
                    node.body = []

                new_elif_branches = []
                for cond, _ in node.elif_branches:
                    if child_idx < len(children_list):
                        child = children_list[child_idx]
                        self._walk_block(child, level + 1)
                        new_elif_branches.append((cond, child.nodes))
                        child_idx += 1
                    else:
                        new_elif_branches.append((cond, []))
                node.elif_branches = new_elif_branches

                if node.else_body is not None:
                    if child_idx < len(children_list):
                        child = children_list[child_idx]
                        self._walk_block(child, level + 1)
                        node.else_body = child.nodes
                        child_idx += 1
                    else:
                        node.else_body = []

            elif hasattr(node, "body"):
                if child_idx < len(children_list):
                    child = children_list[child_idx]
                    self._walk_block(child, level + 1)
                    node.body = child.nodes
                    child_idx += 1
                else:
                    node.body = []

            if level == 0:
                self._ast.append(node)

    def _parse_tokens(self, tokens):
        """
        Парсит токены в AST
        """

        count_tokens = len(tokens)
        context = Context.NULL
        stack = []
        local_ast = []
        i = 0
        current_if = None

        while i < count_tokens:
            token_object = tokens[i]

            match token_object.t_name:
                case "NUMBER":
                    match context:
                        case Context.IFCONSTRUCT_CREATE | Context.ELIF_CREATE | Context.ELSE_CREATE:
                            stack.append(token_object)
                        case _:
                            num_node = NumberLiteral(node_pos=token_object.t_pos, value=int(token_object.t_string))
                            local_ast.append(num_node)

                case "STRING":
                    match context:
                        case Context.IFCONSTRUCT_CREATE | Context.ELIF_CREATE | Context.ELSE_CREATE:
                            stack.append(token_object)
                        case _:
                            str_node = StringLiteral(node_pos=token_object.t_pos, value=token_object.t_string.strip('"\''))
                            local_ast.append(str_node)

                case "NAME":
                    if token_object.t_string in self._keywords:
                        match token_object.t_string:
                            case "def":
                                stack = []
                                context = Context.FUNCTION_CREATE
                                stack.append(token_object)
                            case "if":
                                stack = []
                                context = Context.IFCONSTRUCT_CREATE
                                current_if = None
                            case "elif":
                                context = Context.ELIF_CREATE
                                stack = []
                            case "else":
                                context = Context.ELSE_CREATE
                                stack = []
                            case "import":
                                context = Context.IMPORT_CREATE
                                stack = []
                                stack.append(token_object)
                            case "pass":
                                pass_object = Pass(node_pos=token_object.t_pos)
                                local_ast.append(pass_object)
                            case "True":
                                if context in (Context.IFCONSTRUCT_CREATE, Context.ELIF_CREATE, Context.ELSE_CREATE):
                                    stack.append(token_object)
                                else:
                                    bool_node = BooleanLiteral(node_pos=token_object.t_pos, value=True)
                                    local_ast.append(bool_node)
                            case "False":
                                if context in (Context.IFCONSTRUCT_CREATE, Context.ELIF_CREATE, Context.ELSE_CREATE):
                                    stack.append(token_object)
                                else:
                                    bool_node = BooleanLiteral(node_pos=token_object.t_pos, value=False)
                                    local_ast.append(bool_node)
                            case "and" | "or" | "not":
                                if context in (Context.IFCONSTRUCT_CREATE, Context.ELIF_CREATE):
                                    stack.append(token_object)
                                else:
                                    var_node = Variable(node_pos=token_object.t_pos, name=token_object.t_string)
                                    local_ast.append(var_node)
                            case _:
                                if context in (Context.IFCONSTRUCT_CREATE, Context.ELIF_CREATE, Context.ELSE_CREATE):
                                    stack.append(token_object)
                                elif context == Context.FUNCTION_CREATE:
                                    stack.append(token_object)
                                else:
                                    var_node = Variable(node_pos=token_object.t_pos, name=token_object.t_string)
                                    local_ast.append(var_node)
                    else:
                        match context:
                            case Context.FUNCTION_CREATE:
                                stack.append(token_object)
                                context = Context.FUNCTION_NAME
                            case Context.IFCONSTRUCT_CREATE | Context.ELIF_CREATE | Context.ELSE_CREATE:
                                stack.append(token_object)
                            case Context.NULL:
                                if i + 1 < count_tokens and tokens[i + 1].t_string == "(":
                                    context = Context.FUNCTION_CALL
                                    stack.append(token_object)
                                else:
                                    context = Context.NAME
                                    stack.append(token_object)
                            case Context.METHOD_CALL:
                                stack.append(token_object)
                            case Context.IMPORT_CREATE:
                                context = Context.NULL
                                start = stack[0].t_pos.start
                                end = token_object.t_pos.end
                                pos = Position(start, end)
                                module = Module(token_object.t_pos, token_object.t_string)
                                import_node = Import(pos, module)
                                local_ast.append(import_node)
                                stack = []

                case "OP":
                    if context != Context.NULL:
                        match context:
                            case Context.FUNCTION_CALL:
                                match token_object.t_string:
                                    case "(":
                                        stack.append(token_object)
                                    case ")":
                                        context = Context.NULL
                                        func_name_token = None
                                        for item in stack:
                                            if hasattr(item, "t_name") and item.t_name == "NAME":
                                                func_name_token = item
                                                break
                                        if func_name_token:
                                            start = func_name_token.t_pos.start
                                            end = token_object.t_pos.end
                                            pos = Position(start, end)
                                            call_function = Call(pos, Variable(func_name_token.t_pos, func_name_token.t_string))
                                            local_ast.append(call_function)
                                        stack = []
                                    case _:
                                        stack.append(token_object)

                            case Context.METHOD_CALL:
                                match token_object.t_string:
                                    case "(":
                                        stack.append(token_object)
                                    case ")":
                                        context = Context.NULL
                                        len_names = (len(stack) + 1) // 2
                                        start = stack[0].t_pos.start
                                        end = stack[1].t_pos.end
                                        pos = Position(start, end)
                                        var_node = Variable(stack[0].t_pos, stack[0].t_string)
                                        method_node = Method(stack[-1].t_pos, stack[-1].t_string)
                                        if len_names == 2:
                                            call_node = Call(pos, (var_node, method_node))
                                        else:
                                            attrs = []
                                            for obj in stack[1:-1]:
                                                if obj.t_name == "NAME":
                                                    attrs.append(Attribute(obj.t_pos, obj.t_string))
                                            attrs.append(method_node)
                                            attrs.insert(0, var_node)
                                            call_node = Call(pos, attrs)
                                        local_ast.append(call_node)
                                        stack = []
                                    case _:
                                        stack.append(token_object)

                            case Context.NAME:
                                match token_object.t_string:
                                    case "=":
                                        if len(stack) == 1 and i + 1 < count_tokens:
                                            var_node = stack[0]
                                            right_tokens = []
                                            j = i + 1
                                            while j < count_tokens and tokens[j].t_name != "NEWLINE":
                                                right_tokens.append(tokens[j])
                                                j += 1
                                            right_expr = self.build_expression_from_tokens(right_tokens)
                                            if right_expr:
                                                assign_node = Assign(
                                                    node_pos=Position(var_node.t_pos.start, right_expr.node_pos.end),
                                                    left=Variable(var_node.t_pos, var_node.t_string),
                                                    right=right_expr
                                                )
                                                local_ast.append(assign_node)
                                            i = j - 1
                                            context = Context.NULL
                                            stack = []
                                    case "(":
                                        context = Context.FUNCTION_CALL
                                        stack.append(token_object)
                                    case _:
                                        stack.append(token_object)

                            case Context.FUNCTION_NAME:
                                if token_object.t_string == ":":
                                    if len(stack) >= 2:
                                        start_pos = stack[1].t_pos.start if len(stack) > 1 else stack[0].t_pos.start
                                        end_pos = token_object.t_pos.end
                                        pos = Position(start_pos, end_pos)
                                        name_function = stack[1].t_string if len(stack) > 1 else stack[0].t_string
                                        function_object = Function(
                                            node_pos=pos,
                                            name=name_function,
                                            args=[],
                                            body=[]
                                        )
                                        local_ast.append(function_object)
                                    context = Context.NULL
                                    stack = []
                                else:
                                    stack.append(token_object)

                            case Context.IFCONSTRUCT_CREATE:
                                if token_object.t_string in Operator.get_all_symbols():
                                    stack.append(token_object)
                                elif token_object.t_string == ":":
                                    context = Context.NULL
                                    condition = self.build_expression_from_tokens(stack)
                                    if_node = IfConstruct(
                                        node_pos=Position(
                                            stack[0].t_pos.start if stack else token_object.t_pos.start,
                                            token_object.t_pos.end
                                        ),
                                        condition=condition,
                                        body=[],
                                        elif_branches=[],
                                        else_body=None
                                    )
                                    local_ast.append(if_node)
                                    current_if = if_node
                                    stack = []
                                elif token_object.t_string == "(":
                                    stack.append(token_object)
                                elif token_object.t_string == ")":
                                    stack.append(token_object)
                                else:
                                    stack.append(token_object)

                            case Context.ELIF_CREATE:
                                if token_object.t_string in Operator.get_all_symbols():
                                    stack.append(token_object)
                                elif token_object.t_string == ":":
                                    condition = self.build_expression_from_tokens(stack)
                                    if current_if:
                                        current_if.elif_branches.append((condition, []))
                                    context = Context.NULL
                                    stack = []
                                elif token_object.t_string == "(":
                                    stack.append(token_object)
                                elif token_object.t_string == ")":
                                    stack.append(token_object)
                                else:
                                    stack.append(token_object)

                            case Context.ELSE_CREATE:
                                if token_object.t_string == ":":
                                    if current_if:
                                        current_if.else_body = []
                                    context = Context.NULL
                                    stack = []
                                else:
                                    stack.append(token_object)

                            case _:
                                stack.append(token_object)
                    else:
                        if token_object.t_name == "OP" and token_object.t_string in Operator.get_all_symbols():
                            stack.append(token_object)
                        else:
                            stack.append(token_object)

                case _:
                    pass
            i += 1

        return local_ast