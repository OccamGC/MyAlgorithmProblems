// Codex (GPT-6): application of classical monotone-stack DP to groups of left endpoints, portable wide arithmetic, proof and implementation.

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

struct FWide
{
	std::uint64_t Low = 0;
	std::uint64_t High = 0;
	FWide() = default;
	explicit FWide(long long Value)
		: Low(static_cast<std::uint64_t>(Value)), High(Value < 0 ? ~std::uint64_t{0} : 0)
	{
	}
	bool IsNegative() const
	{
		return (High >> 63) != 0;
	}
	FWide operator-() const
	{
		FWide Result;
		Result.Low = ~Low + 1;
		Result.High = ~High + (Result.Low == 0);
		return Result;
	}
	FWide operator+(const FWide& Other) const
	{
		FWide Result;
		Result.Low = Low + Other.Low;
		Result.High = High + Other.High + (Result.Low < Low);
		return Result;
	}
	FWide operator-(const FWide& Other) const
	{
		return *this + (-Other);
	}
	FWide Multiply(int Factor) const
	{
		bool bNegative = IsNegative() != (Factor < 0);
		FWide Magnitude = IsNegative() ? -*this : *this;
		std::uint64_t Absolute = Factor < 0 ? -static_cast<long long>(Factor) : Factor;
		std::array<std::uint32_t, 4> Words{static_cast<std::uint32_t>(Magnitude.Low), static_cast<std::uint32_t>(Magnitude.Low >> 32), static_cast<std::uint32_t>(Magnitude.High), static_cast<std::uint32_t>(Magnitude.High >> 32)};
		std::uint64_t Carry = 0;
		for (auto& Word : Words)
		{
			std::uint64_t Product = Word * Absolute + Carry;
			Word = static_cast<std::uint32_t>(Product);
			Carry = Product >> 32;
		}
		FWide Result;
		Result.Low = Words[0] | (static_cast<std::uint64_t>(Words[1]) << 32);
		Result.High = Words[2] | (static_cast<std::uint64_t>(Words[3]) << 32);
		return bNegative ? -Result : Result;
	}
	static FWide Product(long long First, long long Second)
	{
		bool bNegative = (First < 0) != (Second < 0);
		std::uint64_t a = static_cast<std::uint64_t>(First);
		std::uint64_t b = static_cast<std::uint64_t>(Second);
		if (First < 0)
		{
			a = 0 - a;
		}
		if (Second < 0)
		{
			b = 0 - b;
		}
		std::array<std::uint32_t, 2> Left{static_cast<std::uint32_t>(a), static_cast<std::uint32_t>(a >> 32)};
		std::array<std::uint32_t, 2> Right{static_cast<std::uint32_t>(b), static_cast<std::uint32_t>(b >> 32)};
		std::array<std::uint32_t, 4> Words{};
		for (int i = 0; i < 2; ++i)
		{
			std::uint64_t Carry = 0;
			for (int j = 0; j < 2; ++j)
			{
				std::uint64_t Value = static_cast<std::uint64_t>(Left[i]) * Right[j] + Words[i + j] + Carry;
				Words[i + j] = static_cast<std::uint32_t>(Value);
				Carry = Value >> 32;
			}
			Words[i + 2] = static_cast<std::uint32_t>(Carry);
		}
		FWide Result;
		Result.Low = Words[0] | (static_cast<std::uint64_t>(Words[1]) << 32);
		Result.High = Words[2] | (static_cast<std::uint64_t>(Words[3]) << 32);
		return bNegative ? -Result : Result;
	}
	void Write(FOutput& Output) const
	{
		FWide Magnitude = IsNegative() ? -*this : *this;
		if (IsNegative())
		{
			Output.Put('-');
		}
		std::array<std::uint32_t, 4> Words{static_cast<std::uint32_t>(Magnitude.Low), static_cast<std::uint32_t>(Magnitude.Low >> 32), static_cast<std::uint32_t>(Magnitude.High), static_cast<std::uint32_t>(Magnitude.High >> 32)};
		char Digits[40];
		int Count = 0;
		do
		{
			std::uint64_t Remainder = 0;
			for (int i = 3; i >= 0; --i)
			{
				std::uint64_t Value = (Remainder << 32) | Words[i];
				Words[i] = static_cast<std::uint32_t>(Value / 10);
				Remainder = Value % 10;
			}
			Digits[Count++] = static_cast<char>('0' + Remainder);
		} while (Words[0] || Words[1] || Words[2] || Words[3]);
		while (Count > 0)
		{
			Output.Put(Digits[--Count]);
		}
		Output.Put('\n');
	}
};

static_assert(sizeof(FWide) == 16, "FWide stores exactly 128 bits");

struct FGroup
{
	int Minimum;
	int Count;
	FWide PrefixSum;
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	std::vector<FGroup> Stack;
	Stack.reserve(n);
	long long Prefix = 0;
	long long WeightedCount = 0;
	FWide WeightedPrefix;
	FWide Answer;
	for (int i = 0; i < n; ++i)
	{
		int Value = Input.Read();
		int Count = 1;
		FWide Sum(Prefix);
		while (!Stack.empty() && Stack.back().Minimum >= Value)
		{
			const FGroup& Group = Stack.back();
			Count += Group.Count;
			Sum = Sum + Group.PrefixSum;
			WeightedCount -= static_cast<long long>(Group.Minimum) * Group.Count;
			WeightedPrefix = WeightedPrefix - Group.PrefixSum.Multiply(Group.Minimum);
			Stack.pop_back();
		}
		Stack.push_back({Value, Count, Sum});
		WeightedCount += static_cast<long long>(Value) * Count;
		WeightedPrefix = WeightedPrefix + Sum.Multiply(Value);
		Prefix += Value;
		Answer = Answer + (FWide::Product(Prefix, WeightedCount) - WeightedPrefix);
	}
	Answer.Write(Output);
}
