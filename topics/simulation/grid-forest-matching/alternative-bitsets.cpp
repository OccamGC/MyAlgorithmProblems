// Problem setter's offset filtering; word-parallel implementation: GPT-6.
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

int Population(std::uint64_t Value)
{
	Value -= (Value >> 1) & UINT64_C(0x5555555555555555);
	Value = (Value & UINT64_C(0x3333333333333333)) + ((Value >> 2) & UINT64_C(0x3333333333333333));
	Value = (Value + (Value >> 4)) & UINT64_C(0x0f0f0f0f0f0f0f0f);
	return static_cast<int>((Value * UINT64_C(0x0101010101010101)) >> 56);
}

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	int Words = (n + 63) / 64;
	std::vector<std::vector<std::uint64_t>> Road(n, std::vector<std::uint64_t>(Words));
	int Count = 0;
	for (int x = 0; x < n; ++x)
	{
		std::string Row = Input.Token();
		for (int y = 0; y < n; ++y)
		{
			if (Row[y] == '1')
			{
				Road[x][y / 64] |= std::uint64_t(1) << (y % 64);
				++Count;
			}
		}
	}
	auto Starts = Road;
	int Width = 2 * n + 1;
	std::vector<bool> Visited(Width * Width);
	Visited[n * Width + n] = true;
	const std::array<int, 4> dx{-1, 1, 0, 0};
	const std::array<int, 4> dy{0, 0, -1, 1};
	int x = 0;
	int y = 0;
	Output.Write(Count, '\n');
	for (int i = 0; i < m; ++i)
	{
		int Direction = Input.Read();
		x += dx[Direction];
		y += dy[Direction];
		if (Count != 0)
		{
			if (x <= -n || x >= n || y <= -n || y >= n)
			{
				Count = 0;
			}
			else
			{
				int Index = (x + n) * Width + y + n;
				if (!Visited[Index])
				{
					Visited[Index] = true;
					Count = 0;
					for (int Row = 0; Row < n; ++Row)
					{
						for (int Word = 0; Word < Words; ++Word)
						{
							std::uint64_t Mask = 0;
							int TargetRow = Row + x;
							if (TargetRow >= 0 && TargetRow < n)
							{
								int Position = 64 * Word + y;
								int First = Position >= 0 ? Position / 64 : (Position - 63) / 64;
								int Shift = Position - 64 * First;
								if (First >= 0 && First < Words)
								{
									Mask |= Road[TargetRow][First] >> Shift;
								}
								if (Shift != 0 && First + 1 >= 0 && First + 1 < Words)
								{
									Mask |= Road[TargetRow][First + 1] << (64 - Shift);
								}
							}
							Starts[Row][Word] &= Mask;
							Count += Population(Starts[Row][Word]);
						}
					}
				}
			}
		}
		Output.Write(Count, '\n');
	}
}
