// Problem setter's solution: count terminating recurrence paths. Codex (GPT-6): exact rational floor bounds, smaller modular tables, proof and portable implementation.

#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <limits>
#include <numeric>
#include <utility>
#include <vector>

class FInput
{
	char Buffer[1 << 16];
	int Position = 0;
	int Length = 0;
public:
	int Get()
	{
		if (Position == Length)
		{
			Length = static_cast<int>(std::fread(Buffer, 1, sizeof(Buffer), stdin));
			Position = 0;
			if (Length == 0)
			{
				return EOF;
			}
		}
		return Buffer[Position++];
	}
	int Read()
	{
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		bool bNegative = Character == '-';
		if (bNegative)
		{
			Character = Get();
		}
		int Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return bNegative ? -Value : Value;
	}
};

class FOutput
{
	char Buffer[1 << 16];
	int Length = 0;
public:
	void Put(char Character)
	{
		if (Length == static_cast<int>(sizeof(Buffer)))
		{
			Flush();
		}
		Buffer[Length++] = Character;
	}
	void Write(long long Value, char End = '\n')
	{
		if (Value < 0)
		{
			Put('-');
			Value = -Value;
		}
		char Digits[24];
		int Count = 0;
		do
		{
			Digits[Count++] = static_cast<char>('0' + Value % 10);
			Value /= 10;
		} while (Value > 0);
		while (Count > 0)
		{
			Put(Digits[--Count]);
		}
		Put(End);
	}
	void Flush()
	{
		std::fwrite(Buffer, 1, Length, stdout);
		Length = 0;
	}
	~FOutput()
	{
		Flush();
	}
};

constexpr int Modulus = 1000000007;

int Power(long long Base, int Exponent)
{
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
	return static_cast<int>(Result);
}

int FloorE(int Multiplier)
{
	return static_cast<int>(410105312LL * Multiplier / 150869313);
}

int main()
{
	FInput Input;
	FOutput Output;
	int A = Input.Read();
	int B = Input.Read();
	int C = Input.Read();
	int D = Input.Read();
	int m = Input.Read();
	std::vector<int> Queries(m);
	int Maximum = 0;
	for (int& t : Queries)
	{
		t = Input.Read() - B;
		Maximum = std::max(Maximum, t + 1);
	}
	std::vector<int> Factorial(Maximum + 1, 1);
	std::vector<int> InverseFactorial(Maximum + 1, 1);
	std::vector<int> PowersC(Maximum + 1, 1);
	std::vector<int> PowersD(Maximum + 1, 1);
	for (int i = 1; i <= Maximum; ++i)
	{
		Factorial[i] = static_cast<long long>(Factorial[i - 1]) * i % Modulus;
		PowersC[i] = static_cast<long long>(PowersC[i - 1]) * C % Modulus;
		PowersD[i] = static_cast<long long>(PowersD[i - 1]) * D % Modulus;
	}
	InverseFactorial[Maximum] = Power(Factorial[Maximum], Modulus - 2);
	for (int i = Maximum; i > 0; --i)
	{
		InverseFactorial[i - 1] = static_cast<long long>(InverseFactorial[i]) * i % Modulus;
	}
	auto Choose = [&](int n, int k)
	{
		return static_cast<long long>(Factorial[n]) * InverseFactorial[k] % Modulus * InverseFactorial[n - k] % Modulus;
	};
	for (int t : Queries)
	{
		long long Answer = PowersC[t + 1];
		for (int b = 1; b <= t + 1; ++b)
		{
			int High = b == 1 ? t : t - FloorE(b - 1) - 1;
			if (High < 0)
			{
				break;
			}
			int Low = std::max(0, t - FloorE(b));
			for (int a = Low; a <= High; ++a)
			{
				long long Ways = a == Low ? Choose(a + b, a) : Choose(a + b - 1, a);
				Answer = (Answer + Ways * PowersC[a] % Modulus * PowersD[b]) % Modulus;
			}
		}
		Output.Write(Answer * A % Modulus);
	}
}
