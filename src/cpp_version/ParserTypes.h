#ifndef PARSER_TYPES_H
#define PARSER_TYPES_H

#include <iostream>
#include <string>
#include <vector>
#include "Tokens.h"

class Expression {
public:
    virtual std::string toString() const {
        return "Expression()";
    }
};

class Statement {
public:
    virtual std::string toString() const {
        return "Statement()";
    }
};

class ExpressionStatement : public Statement {
private:
    Expression* expr;

public:
    ExpressionStatement(Expression* expr) : expr(expr) {}

    std::string toString() const override {
        return "ExpressionStatement(" + expr->toString() + ")";
    }

    // Destructor to properly manage memory
    virtual ~ExpressionStatement() {
        delete expr;
    }
};

class Block : public Statement {
private:
    std::vector<Statement*> statements;

public:
    Block(const std::vector<Statement*>& statements) : statements(statements) {}

    std::string toString() const override {
        return "Block(...)";
    }
};

class ReturnStatement : public Statement {
private:
    Expression* value;

public:
    ReturnStatement(Expression* value) : value(value) {}

    std::string toString() const override {
        return "ReturnStatement(...)";
    }
};

class FunctionDeclaration : public Statement {
private:
    std::string name;
    std::vector<std::string> parameters;
    Block* body;

public:
    FunctionDeclaration(const std::string& name, const std::vector<std::string>& parameters, Block* body) : name(name), parameters(parameters), body(body) {}

    std::string toString() const override {
        return "FunctionDeclaration(...)";
    }
};

class VariableDeclaration : public Statement {
private:
    std::string name;
    Expression* value;

public:
    VariableDeclaration(const std::string& name, Expression* value) : name(name), value(value) {}

    std::string toString() const override {
        return "VariableDeclaration(" + name + ")";
    }
};

class NumberLiteral : public Expression {
private:
    std::string type;
    std::string value;

public:
    NumberLiteral(const std::string& type, const std::string& value) : type(type), value(value) {}

    std::string toString() const override {
        return "NumberLiteral(...)";
    }
};

class StringLiteral : public Expression {
private:
    std::string value;

public:
    StringLiteral(const std::string& value) : value(value) {}

    std::string toString() const override {
        return "StringLiteral(...)";
    }
};

class BooleanLiteral : public Expression {
private:
    bool value;

public:
    BooleanLiteral(bool value) : value(value) {}

    std::string toString() const override {
        return "BooleanLiteral(...)";
    }
};

class Variable : public Expression {
private:
    std::string name;

public:
    Variable(const std::string& name) : name(name) {}

    std::string toString() const override {
        return "Variable(...)";
    }
};

class FunctionCall : public Expression {
private:
    std::string name;
    std::vector<Expression*> arguments;

public:
    FunctionCall(const std::string& name, const std::vector<Expression*>& arguments) : name(name), arguments(arguments) {}

    std::string toString() const override {
        return "FunctionCall(...)";
    }
};

class Assignment : public Statement {
private:
    Variable* variable;
    Expression* value;

public:
    Assignment(Variable* variable, Expression* value) : variable(variable), value(value) {}

    std::string toString() const override {
        return "Assignment(...)";
    }
};

class BinaryOperation : public Expression {
private:
    Expression* left;
    TOKENTYPE op;
    Expression* right;

public:
    BinaryOperation(Expression* left, const TOKENTYPE& op, Expression* right) : left(left), op(op), right(right) {}

    std::string toString() const override {
        return "BinaryOperation(...)";
    }
};

class ComparisonOperation : public Expression {
private:
    Expression* left;
    TOKENTYPE op;
    Expression* right;

public:
    ComparisonOperation(Expression* left, const TOKENTYPE& op, Expression* right) : left(left), op(op), right(right) {}

    std::string toString() const override {
        return "ComparisonOperation(...)";
    }
};

class UnaryOperation : public Expression {
private:
    TOKENTYPE op;
    Expression* operand;

public:
    UnaryOperation(const TOKENTYPE& op, Expression* operand) : op(op), operand(operand) {}

    std::string toString() const override {
        return "UnaryOperation(...)";
    }
};

class IfStatement : public Statement {
private:
    Expression* condition;
    Block* if_body;
    Block* else_body;

public:
    IfStatement(Expression* condition, Block* if_body, Block* else_body = nullptr) : condition(condition), if_body(if_body), else_body(else_body) {}

    std::string toString() const override {
        return "IfStatement(...)";
    }
};

class WhileStatement : public Statement {
private:
    Expression* condition;
    Block* body;

public:
    WhileStatement(Expression* condition, Block* body) : condition(condition), body(body) {}

    std::string toString() const override {
        return "WhileStatement(...)";
    }
};

#endif // PARSER_TYPES_H

