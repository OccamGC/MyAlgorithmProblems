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

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<std::string> Grid(n);
	std::vector<std::pair<int, int>> Starts;
	for (int x = 0; x < n; ++x)
	{
		Grid[x] = Input.Token();
		for (int y = 0; y < n; ++y)
		{
			if (Grid[x][y] == '1')
			{
				Starts.emplace_back(x, y);
			}
		}
	}
	int Width = 2 * n + 1;
	std::vector<bool> Visited(Width * Width);
	Visited[n * Width + n] = true;
	const std::array<int, 4> dx{-1, 1, 0, 0};
	const std::array<int, 4> dy{0, 0, -1, 1};
	int x = 0;
	int y = 0;
	Output.Write(Starts.size(), '\n');
	for (int i = 0; i < m; ++i)
	{
		int Direction = Input.Read();
		x += dx[Direction];
		y += dy[Direction];
		if (!Starts.empty())
		{
			if (x <= -n || x >= n || y <= -n || y >= n)
			{
				Starts.clear();
			}
			else
			{
				int Index = (x + n) * Width + y + n;
				if (!Visited[Index])
				{
					Visited[Index] = true;
					std::size_t Count = 0;
					for (const auto& Start : Starts)
					{
						int Row = Start.first + x;
						int Column = Start.second + y;
						if (Row >= 0 && Row < n && Column >= 0 && Column < n && Grid[Row][Column] == '1')
						{
							Starts[Count++] = Start;
						}
					}
					Starts.resize(Count);
				}
			}
		}
		Output.Write(Starts.size(), '\n');
	}
}
