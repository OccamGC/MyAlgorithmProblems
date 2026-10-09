#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

constexpr long long Modulus = 1004535809;

long long Normalize(long long Value)
{
	Value %= Modulus;
	return Value < 0 ? Value + Modulus : Value;
}

long long Power(long long Base, long long Exponent)
{
	Base = Normalize(Base);
	long long Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Result * Base % Modulus;
		}
		Base = Base * Base % Modulus;
		Exponent >>= 1;
	}
	return Result;
}

struct FInput
{
	long long a = 0;
	int b;
	int c;
	long long Exponent = 0;
	bool bZero = true;
	void Read()
	{
		std::string Text;
		std::cin >> Text;
		for (char Digit : Text)
		{
			a = (10 * a + Digit - '0') % Modulus;
		}
		std::cin >> b >> c >> Text;
		for (char Digit : Text)
		{
			Exponent = (10 * Exponent + Digit - '0') % (Modulus - 1);
			bZero = bZero && Digit == '0';
		}
	}
	long long Evaluate(int Index) const
	{
		long long Base = Normalize(a - b - c + Index);
		return Base == 0 && !bZero ? 0 : Power(Base, Exponent);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	FInput Input;
	Input.Read();
	int Degree = 2 * (Input.b + Input.c);
	std::vector<long long> Inverse(Degree + 2);
	Inverse[1] = 1;
	for (int i = 2; i <= Degree; ++i)
	{
		Inverse[i] = Modulus - (Modulus / i) * Inverse[Modulus % i] % Modulus;
	}
	std::array<long long, 4> Recent = {Input.c % 2 ? Modulus - 1 : 1, 0, 0, 0};
	long long Answer = Recent[0] * Input.Evaluate(0) % Modulus;
	for (int k = 0; k < Degree; ++k)
	{
		std::array<long long, 4> Weights = {2LL * k - 2LL * Input.c, 2LL * Input.b - 2LL * Input.c, 2LL * k - 4 - 4LL * Input.b - 2LL * Input.c, k - 3LL - 2LL * Input.b - 2LL * Input.c};
		long long Next = 0;
		for (int j = 0; j < 4; ++j)
		{
			Next = Normalize(Next + Weights[j] * Recent[j] % Modulus);
		}
		Next = Next * Inverse[k + 1] % Modulus;
		for (int j = 3; j > 0; --j)
		{
			Recent[j] = Recent[j - 1];
		}
		Recent[0] = Next;
		Answer = (Answer + Next * Input.Evaluate(k + 1)) % Modulus;
	}
	Answer = Answer * Power((Modulus + 1) / 2, Input.b + Input.c) % Modulus;
	std::cout << Answer << '\n';
}
