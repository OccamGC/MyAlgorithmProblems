// Problem setter's solution; portable implementation and analysis: GPT-6.
#include <queue>
#include <array>
#include <iterator>

#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <string>
#include <set>
#include <limits>
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
		long long Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return static_cast<int>(bNegative ? -Value : Value);
	}
	std::string Token()
	{
		std::string Result;
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		while (Character > ' ' && Character != EOF)
		{
			Result.push_back(static_cast<char>(Character));
			Character = Get();
		}
		return Result;
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
	static constexpr int Words = 12;
	std::array<std::uint64_t, Words> Data{};
	static FWide Power(int Bit)
	{
		FWide Result;
		Result.Data[Bit / 64] = std::uint64_t(1) << (Bit % 64);
		return Result;
	}
	FWide operator+(const FWide& Other) const
	{
		FWide Result;
		std::uint64_t Carry = 0;
		for (int i = 0; i < Words; ++i)
		{
			std::uint64_t Partial = Data[i] + Other.Data[i];
			std::uint64_t FirstCarry = Partial < Data[i];
			Result.Data[i] = Partial + Carry;
			Carry = FirstCarry | (Result.Data[i] < Partial);
		}
		return Result;
	}
	FWide operator-(const FWide& Other) const
	{
		FWide Result;
		std::uint64_t Borrow = 0;
		for (int i = 0; i < Words; ++i)
		{
			std::uint64_t Partial = Data[i] - Other.Data[i];
			std::uint64_t FirstBorrow = Data[i] < Other.Data[i];
			Result.Data[i] = Partial - Borrow;
			Borrow = FirstBorrow | (Partial < Borrow);
		}
		return Result;
	}
	bool operator<(const FWide& Other) const
	{
		bool bNegative = (Data.back() >> 63) != 0;
		bool bOtherNegative = (Other.Data.back() >> 63) != 0;
		if (bNegative != bOtherNegative)
		{
			return bNegative;
		}
		for (int i = Words - 1; i >= 0; --i)
		{
			if (Data[i] != Other.Data[i])
			{
				return Data[i] < Other.Data[i];
			}
		}
		return false;
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	std::vector<std::vector<int>> a(n + 1, std::vector<int>(n + 1));
	for (int i = 1; i <= n; ++i)
	{
		for (int j = 1; j <= n; ++j)
		{
			a[i][j] = Input.Read();
		}
	}
	std::array<FWide, 71> Cost;
	FWide Zero;
	for (int Grade = 0; Grade <= 70; ++Grade)
	{
		Cost[Grade] = Zero - FWide::Power(9 * Grade);
	}
	FWide Infinity = FWide::Power(740);
	std::vector<FWide> u(n + 1);
	std::vector<FWide> v(n + 1);
	std::vector<int> Match(n + 1);
	std::vector<int> Previous(n + 1);
	for (int Row = 1; Row <= n; ++Row)
	{
		Match[0] = Row;
		int Column = 0;
		std::vector<FWide> Best(n + 1, Infinity);
		std::vector<bool> Used(n + 1);
		do
		{
			Used[Column] = true;
			int Active = Match[Column];
			int NextColumn = 0;
			FWide Delta = Infinity;
			for (int j = 1; j <= n; ++j)
			{
				if (!Used[j])
				{
					FWide Reduced = Cost[a[Active][j]] - u[Active] - v[j];
					if (Reduced < Best[j])
					{
						Best[j] = Reduced;
						Previous[j] = Column;
					}
					if (Best[j] < Delta)
					{
						Delta = Best[j];
						NextColumn = j;
					}
				}
			}
			for (int j = 0; j <= n; ++j)
			{
				if (Used[j])
				{
					u[Match[j]] = u[Match[j]] + Delta;
					v[j] = v[j] - Delta;
				}
				else
				{
					Best[j] = Best[j] - Delta;
				}
			}
			Column = NextColumn;
		}
		while (Match[Column] != 0);
		do
		{
			int NextColumn = Previous[Column];
			Match[Column] = Match[NextColumn];
			Column = NextColumn;
		}
		while (Column != 0);
	}
	std::array<int, 71> Answer{};
	for (int j = 1; j <= n; ++j)
	{
		++Answer[a[Match[j]][j]];
	}
	for (int Grade = 70; Grade >= 0; --Grade)
	{
		Output.Write(Answer[Grade], Grade == 0 ? '\n' : ' ');
	}
}
