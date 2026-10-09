// Problem setter's ideas: precedence parsing and deferred error values for short-circuit operators.
// Codex (GPT-6): full grammar, left-associated conditional expressions, and explicit 32-bit arithmetic.
#include <cctype>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

struct FToken
{
	std::string Operator;
	std::uint32_t Number = 0;
};

int Priority(const std::string& Operator)
{
	if (Operator == "u+" || Operator == "u-" || Operator == "!" || Operator == "~")
	{
		return 12;
	}
	if (Operator == "*" || Operator == "/" || Operator == "%")
	{
		return 11;
	}
	if (Operator == "+" || Operator == "-")
	{
		return 10;
	}
	if (Operator == "<<" || Operator == ">>")
	{
		return 9;
	}
	if (Operator == "<" || Operator == ">" || Operator == "<=" || Operator == ">=")
	{
		return 8;
	}
	if (Operator == "==" || Operator == "!=")
	{
		return 7;
	}
	if (Operator == "&")
	{
		return 6;
	}
	if (Operator == "^")
	{
		return 5;
	}
	if (Operator == "|")
	{
		return 4;
	}
	if (Operator == "&&")
	{
		return 3;
	}
	if (Operator == "||")
	{
		return 2;
	}
	return 1;
}

int Arity(const std::string& Operator)
{
	return Operator == "?:" ? 3 : Priority(Operator) == 12 ? 1 : 2;
}

std::vector<FToken> Parse(const std::string& Expression)
{
	std::vector<std::string> Operators;
	std::vector<FToken> Postfix;
	bool bOperand = true;
	auto Pop = [&]()
	{
		Postfix.push_back(FToken{Operators.back(), 0});
		Operators.pop_back();
	};
	for (std::size_t Position = 0; Position < Expression.size();)
	{
		unsigned char Character = static_cast<unsigned char>(Expression[Position]);
		if (std::isspace(Character))
		{
			++Position;
			continue;
		}
		if (std::isdigit(Character))
		{
			std::uint32_t Number = 0;
			while (Position < Expression.size() && std::isdigit(static_cast<unsigned char>(Expression[Position])))
			{
				Number = Number * 10 + Expression[Position++] - '0';
			}
			Postfix.push_back(FToken{"", Number});
			bOperand = false;
			continue;
		}
		std::string Operator(1, Expression[Position++]);
		if (Position < Expression.size())
		{
			std::string Pair = Operator + Expression[Position];
			if (Pair == "<<" || Pair == ">>" || Pair == "<=" || Pair == ">=" || Pair == "==" || Pair == "!=" || Pair == "&&" || Pair == "||")
			{
				Operator = Pair;
				++Position;
			}
		}
		if (Operator == "(")
		{
			Operators.push_back(Operator);
			bOperand = true;
		}
		else if (Operator == ")")
		{
			while (Operators.back() != "(")
			{
				Pop();
			}
			Operators.pop_back();
			bOperand = false;
		}
		else if (Operator == ":")
		{
			while (Operators.back() != "?")
			{
				Pop();
			}
			Operators.back() = "?:";
			bOperand = true;
		}
		else
		{
			if (bOperand && (Operator == "+" || Operator == "-"))
			{
				Operator = "u" + Operator;
			}
			int CurrentPriority = Priority(Operator);
			while (!Operators.empty() && Operators.back() != "(" && Operators.back() != "?" &&
				(Priority(Operators.back()) > CurrentPriority ||
				(Priority(Operators.back()) == CurrentPriority && CurrentPriority != 12)))
			{
				Pop();
			}
			Operators.push_back(Operator);
			bOperand = true;
		}
	}
	while (!Operators.empty())
	{
		Pop();
	}
	return Postfix;
}

struct FValue
{
	std::uint32_t Bits = 0;
	bool bError = false;
};

long long Signed(std::uint32_t Bits)
{
	return Bits < 0x80000000U ? static_cast<long long>(Bits) : static_cast<long long>(Bits) - 4294967296LL;
}

FValue Apply(const std::string& Operator, FValue a, FValue b = {}, FValue c = {})
{
	if (a.bError)
	{
		return a;
	}
	if (Operator == "?:")
	{
		return a.Bits ? b : c;
	}
	if ((Operator == "&&" && a.Bits == 0) || (Operator == "||" && a.Bits != 0))
	{
		return FValue{Operator == "||" ? 1U : 0U, false};
	}
	if (Arity(Operator) == 2 && b.bError)
	{
		return b;
	}
	std::uint32_t Result = 0;
	if (Operator == "u+")
	{
		Result = a.Bits;
	}
	else if (Operator == "u-")
	{
		Result = 0U - a.Bits;
	}
	else if (Operator == "!")
	{
		Result = a.Bits == 0;
	}
	else if (Operator == "~")
	{
		Result = ~a.Bits;
	}
	else if (Operator == "+")
	{
		Result = a.Bits + b.Bits;
	}
	else if (Operator == "-")
	{
		Result = a.Bits - b.Bits;
	}
	else if (Operator == "*")
	{
		Result = static_cast<std::uint32_t>(static_cast<std::uint64_t>(a.Bits) * b.Bits);
	}
	else if (Operator == "/" || Operator == "%")
	{
		if (b.Bits == 0)
		{
			return FValue{0, true};
		}
		Result = static_cast<std::uint32_t>(Operator == "/" ? Signed(a.Bits) / Signed(b.Bits) : Signed(a.Bits) % Signed(b.Bits));
	}
	else if (Operator == "<<")
	{
		Result = a.Bits << (b.Bits & 31U);
	}
	else if (Operator == ">>")
	{
		unsigned Shift = b.Bits & 31U;
		Result = a.Bits >> Shift;
		if (Shift != 0 && (a.Bits & 0x80000000U))
		{
			Result |= 0xFFFFFFFFU << (32 - Shift);
		}
	}
	else if (Operator == "<")
	{
		Result = Signed(a.Bits) < Signed(b.Bits);
	}
	else if (Operator == ">")
	{
		Result = Signed(a.Bits) > Signed(b.Bits);
	}
	else if (Operator == "<=")
	{
		Result = Signed(a.Bits) <= Signed(b.Bits);
	}
	else if (Operator == ">=")
	{
		Result = Signed(a.Bits) >= Signed(b.Bits);
	}
	else if (Operator == "==")
	{
		Result = a.Bits == b.Bits;
	}
	else if (Operator == "!=")
	{
		Result = a.Bits != b.Bits;
	}
	else if (Operator == "&")
	{
		Result = a.Bits & b.Bits;
	}
	else if (Operator == "^")
	{
		Result = a.Bits ^ b.Bits;
	}
	else if (Operator == "|")
	{
		Result = a.Bits | b.Bits;
	}
	else if (Operator == "&&" || Operator == "||")
	{
		Result = b.Bits != 0;
	}
	return FValue{Result, false};
}

void Print(FValue Value)
{
	if (Value.bError)
	{
		std::cout << "Segmentfault\n";
	}
	else
	{
		std::cout << Signed(Value.Bits) << '\n';
	}
}

// Alternative contribution: build an explicit syntax tree and evaluate only active children.
struct FNode
{
	FToken Token;
	int Children[3] = {-1, -1, -1};
};

struct FFrame
{
	int Node;
	int Stage = 0;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string Expression;
	std::getline(std::cin, Expression);
	std::vector<FNode> Nodes;
	std::vector<int> Roots;
	for (const FToken& Token : Parse(Expression))
	{
		FNode Node;
		Node.Token = Token;
		if (!Token.Operator.empty())
		{
			for (int i = Arity(Token.Operator) - 1; i >= 0; --i)
			{
				Node.Children[i] = Roots.back();
				Roots.pop_back();
			}
		}
		Roots.push_back(static_cast<int>(Nodes.size()));
		Nodes.push_back(Node);
	}
	std::vector<FValue> Values(Nodes.size());
	std::vector<FFrame> Stack{{Roots.back(), 0}};
	while (!Stack.empty())
	{
		int Current = Stack.back().Node;
		int Stage = Stack.back().Stage;
		const FNode& Node = Nodes[Current];
		const std::string& Operator = Node.Token.Operator;
		if (Operator.empty())
		{
			Values[Current] = FValue{Node.Token.Number, false};
			Stack.pop_back();
			continue;
		}
		if (Stage == 0)
		{
			Stack.back().Stage = 1;
			Stack.push_back(FFrame{Node.Children[0], 0});
			continue;
		}
		FValue First = Values[Node.Children[0]];
		if (Stage == 1)
		{
			if (First.bError || Arity(Operator) == 1 ||
				(Operator == "&&" && First.Bits == 0) || (Operator == "||" && First.Bits != 0))
			{
				Values[Current] = Apply(Operator, First);
				Stack.pop_back();
				continue;
			}
			int Child = Operator == "?:" && First.Bits == 0 ? 2 : 1;
			Stack.back().Stage = 2;
			Stack.push_back(FFrame{Node.Children[Child], 0});
			continue;
		}
		if (Operator == "?:")
		{
			Values[Current] = Values[Node.Children[First.Bits ? 1 : 2]];
		}
		else
		{
			Values[Current] = Apply(Operator, First, Values[Node.Children[1]]);
		}
		Stack.pop_back();
	}
	Print(Values[Roots.back()]);
}
