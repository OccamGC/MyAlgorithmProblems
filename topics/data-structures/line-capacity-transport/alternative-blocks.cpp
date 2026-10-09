// Problem setter's residual-flow model; square-root decomposition implementation: GPT-6.
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

class FFlow
{
	static constexpr int BlockSize = 320;
	int n;
	int Blocks;
	std::vector<int> Value;
	std::vector<int> Weight;
	std::vector<int> Lazy;
	std::vector<std::vector<std::pair<int, int>>> Sorted;
	std::vector<std::vector<int>> Prefix;
	void Rebuild(int Block)
	{
		int l = Block * BlockSize;
		int r = std::min(n, l + BlockSize);
		Sorted[Block].clear();
		for (int i = l; i < r; ++i)
		{
			Sorted[Block].emplace_back(Value[i], Weight[i]);
		}
		std::sort(Sorted[Block].begin(), Sorted[Block].end());
		Prefix[Block].assign(r - l + 1, 0);
		for (int i = 0; i < r - l; ++i)
		{
			Prefix[Block][i + 1] = Prefix[Block][i] + Sorted[Block][i].second;
		}
	}
public:
	explicit FFlow(const std::vector<int>& Distance)
		: n(static_cast<int>(Distance.size())), Blocks((n + BlockSize - 1) / BlockSize),
		  Value(n), Weight(Distance), Lazy(Blocks), Sorted(Blocks), Prefix(Blocks)
	{
		for (int Block = 0; Block < Blocks; ++Block)
		{
			Rebuild(Block);
		}
	}
	int Cost(int l, int r, int Direction) const
	{
		int Result = 0;
		for (int Block = l / BlockSize; Block <= r / BlockSize; ++Block)
		{
			int From = Block * BlockSize;
			int To = std::min(n, From + BlockSize) - 1;
			if (l <= From && To <= r)
			{
				// Forward cost is negative exactly for flow < 0.
				// Backward cost is negative exactly for flow > 0.
				int Threshold = -Lazy[Block] + (Direction == -1 ? 1 : 0);
				auto Position = std::lower_bound(Sorted[Block].begin(), Sorted[Block].end(),
					std::make_pair(Threshold, std::numeric_limits<int>::min()));
				int Count = static_cast<int>(Position - Sorted[Block].begin());
				int Below = Prefix[Block][Count];
				int Total = Prefix[Block].back();
				Result += Direction == 1 ? Total - 2 * Below : 2 * Below - Total;
			}
			else
			{
				for (int i = std::max(l, From); i <= std::min(r, To); ++i)
				{
					int Flow = Value[i] + Lazy[Block];
					bool bNegative = Direction == 1 ? Flow < 0 : Flow > 0;
					Result += bNegative ? -Weight[i] : Weight[i];
				}
			}
		}
		return Result;
	}
	void Add(int l, int r, int Delta)
	{
		for (int Block = l / BlockSize; Block <= r / BlockSize; ++Block)
		{
			int From = Block * BlockSize;
			int To = std::min(n, From + BlockSize) - 1;
			if (l <= From && To <= r)
			{
				Lazy[Block] += Delta;
			}
			else
			{
				for (int i = std::max(l, From); i <= std::min(r, To); ++i)
				{
					Value[i] += Delta;
				}
				Rebuild(Block);
			}
		}
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<int> Capacity(n + 2);
	std::set<int> Available;
	for (int i = 1; i <= n; ++i)
	{
		Capacity[i] = Input.Read();
		if (Capacity[i] != 0)
		{
			Available.insert(i);
		}
	}
	Capacity[n + 1] = m + 1;
	Available.insert(n + 1);
	std::vector<int> Distance(n);
	for (int& Value : Distance)
	{
		Value = Input.Read();
	}
	FFlow Flow(Distance);
	long long Answer = 0;
	for (int i = 0; i < m; ++i)
	{
		int p = Input.Read();
		int Destination = p;
		if (Capacity[p] == 0)
		{
			auto Right = Available.lower_bound(p);
			int r = *Right;
			int RightCost = Flow.Cost(p - 1, r - 2, 1);
			int LeftCost = std::numeric_limits<int>::max();
			int l = -1;
			if (Right != Available.begin())
			{
				l = *std::prev(Right);
				LeftCost = Flow.Cost(l - 1, p - 2, -1);
			}
			if (LeftCost <= RightCost)
			{
				Destination = l;
				Answer += LeftCost;
				Flow.Add(l - 1, p - 2, -1);
			}
			else
			{
				Destination = r;
				Answer += RightCost;
				Flow.Add(p - 1, r - 2, 1);
			}
		}
		if (--Capacity[Destination] == 0)
		{
			Available.erase(Destination);
		}
		Output.Write(Answer, '\n');
	}
}
