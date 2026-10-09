// Problem setter's solution: shunting-yard conversion and postfix evaluation.
// Codex (GPT-6): explicit portable 32-bit wrapping arithmetic and iterative parsing.
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

int Priority(char Operator)
{
	if (Operator == 'P' || Operator == 'N' || Operator == '~')
	{
		return 4;
	}
	if (Operator == '*' || Operator == '/' || Operator == '%')
	{
		return 3;
	}
	if (Operator == '+' || Operator == '-')
	{
		return 2;
	}
	return 1;
}

long long Signed(std::uint32_t Value)
{
	return Value < 0x80000000U ? static_cast<long long>(Value) : static_cast<long long>(Value) - 4294967296LL;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string Expression;
	std::cin >> Expression;
	std::vector<char> Operators;
	std::vector<char> Postfix;
	bool bOperand = true;
	for (char Token : Expression)
	{
		if ('0' <= Token && Token <= '9')
		{
			Postfix.push_back(Token);
			bOperand = false;
		}
		else if (Token == '(')
		{
			Operators.push_back(Token);
			bOperand = true;
		}
		else if (Token == ')')
		{
			while (Operators.back() != '(')
			{
				Postfix.push_back(Operators.back());
				Operators.pop_back();
			}
			Operators.pop_back();
			bOperand = false;
		}
		else
		{
			if (bOperand && Token == '+')
			{
				Token = 'P';
			}
			if (bOperand && Token == '-')
			{
				Token = 'N';
			}
			while (!Operators.empty() && Operators.back() != '(' &&
				(Priority(Operators.back()) > Priority(Token) ||
				(Priority(Operators.back()) == Priority(Token) && !bOperand)))
			{
				Postfix.push_back(Operators.back());
				Operators.pop_back();
			}
			Operators.push_back(Token);
			bOperand = true;
		}
	}
	while (!Operators.empty())
	{
		Postfix.push_back(Operators.back());
		Operators.pop_back();
	}
	std::vector<std::uint32_t> Values;
	for (char Token : Postfix)
	{
		if ('0' <= Token && Token <= '9')
		{
			Values.push_back(Token - '0');
			continue;
		}
		std::uint32_t Right = Values.back();
		Values.pop_back();
		if (Token == 'P' || Token == 'N' || Token == '~')
		{
			Values.push_back(Token == 'P' ? Right : Token == 'N' ? 0U - Right : ~Right);
			continue;
		}
		std::uint32_t Left = Values.back();
		Values.pop_back();
		std::uint32_t Result = 0;
		if ((Token == '/' || Token == '%') && Right == 0)
		{
			std::cout << "Runtime Error\n";
			return 0;
		}
		switch (Token)
		{
		case '+': Result = Left + Right; break;
		case '-': Result = Left - Right; break;
		case '*': Result = static_cast<std::uint32_t>(static_cast<std::uint64_t>(Left) * Right); break;
		case '/': Result = static_cast<std::uint32_t>(Signed(Left) / Signed(Right)); break;
		case '%': Result = static_cast<std::uint32_t>(Signed(Left) % Signed(Right)); break;
		case '<': Result = Signed(Left) < Signed(Right); break;
		case '>': Result = Signed(Left) > Signed(Right); break;
		}
		Values.push_back(Result);
	}
	std::cout << Signed(Values.back()) << '\n';
}
