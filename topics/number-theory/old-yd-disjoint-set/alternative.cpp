// Problem setter's solution: terminating-path enumeration. Codex (GPT-6): rolling weighted binomial coefficients using one inverse table, exact floor bounds, proof and implementation.

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
	std::vector<int> Inverse(Maximum + 1, 1);
	for (int i = 2; i <= Maximum; ++i)
	{
		Inverse[i] = Modulus - static_cast<long long>(Modulus / i) * Inverse[Modulus % i] % Modulus;
	}
	int InverseC = Power(C, Modulus - 2);
	for (int t : Queries)
	{
		int a = t + 1;
		long long Weight = Power(C, a);
		long long Answer = Weight;
		for (int b = 1; b <= t + 1; ++b)
		{
			int High = b == 1 ? t : t - FloorE(b - 1) - 1;
			if (High < 0)
			{
				break;
			}
			int Low = std::max(0, t - FloorE(b));
			while (a > Low)
			{
				Weight = Weight * a % Modulus * Inverse[a + b - 1] % Modulus * InverseC % Modulus;
				--a;
			}
			Weight = Weight * (a + b) % Modulus * Inverse[b] % Modulus * D % Modulus;
			Answer = (Answer + Weight) % Modulus;
			long long Term = Weight;
			for (int j = a + 1; j <= High; ++j)
			{
				Term = Term * (j == a + 1 ? b : j + b - 1) % Modulus * Inverse[j] % Modulus * C % Modulus;
				Answer = (Answer + Term) % Modulus;
			}
		}
		Output.Write(Answer * A % Modulus);
	}
}
