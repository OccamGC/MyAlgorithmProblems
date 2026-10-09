#include <algorithm>
#include <array>
#include <cstdio>
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

constexpr int Modulus = 998244353;

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	int Energy = Input.Read();
	std::vector<int> Height(n);
	for (int& Value : Height)
	{
		Value = Input.Read();
	}
	std::vector<std::pair<int, int>> Pairs(m);
	for (auto& Edge : Pairs)
	{
		Edge.first = Input.Read() - 1;
		Edge.second = Input.Read() - 1;
		if (Edge.first > Edge.second)
		{
			std::swap(Edge.first, Edge.second);
		}
	}
	std::sort(Pairs.begin(), Pairs.end());
	Pairs.erase(std::unique(Pairs.begin(), Pairs.end()), Pairs.end());
	std::vector<std::vector<int>> Neighbors(n);
	for (const auto& Edge : Pairs)
	{
		Neighbors[Edge.first].push_back(Edge.second);
		if (Edge.first != Edge.second)
		{
			Neighbors[Edge.second].push_back(Edge.first);
		}
	}
	std::vector<int> Order(n);
	std::iota(Order.begin(), Order.end(), 0);
	std::sort(Order.begin(), Order.end(), [&](int u, int v)
	{
		return Height[u] < Height[v];
	});
	std::array<std::vector<int>, 3> Ways;
	for (auto& Layer : Ways)
	{
		Layer.resize(n);
	}
	for (int e = 0; e <= Energy; ++e)
	{
		auto& Current = Ways[e % 3];
		for (int u : Order)
		{
			int Value = 1;
			for (int v : Neighbors[u])
			{
				int Cost = Height[v] < Height[u] ? 0 : (Height[v] == Height[u] ? 1 : 2);
				if (Cost <= e)
				{
					Value += Ways[(e - Cost) % 3][v];
					if (Value >= Modulus)
					{
						Value -= Modulus;
					}
				}
			}
			Current[u] = Value;
		}
	}
	int Answer = 0;
	for (int Value : Ways[Energy % 3])
	{
		Answer += Value;
		if (Answer >= Modulus)
		{
			Answer -= Modulus;
		}
	}
	Output.Write(Answer);
}
