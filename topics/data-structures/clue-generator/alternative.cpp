// Problem setter's block decomposition. Codex (GPT-6): complete block answers and occurrence-list binary searches to remove the block-by-value matrix, proof and implementation.

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

template<bool bSparse>
class FZeroQueries
{
	int Size;
	int Width = 1;
	int Blocks;
	int Kinds;
	std::vector<int> Values;
	std::vector<int> Offsets;
	std::vector<int> Positions;
	std::vector<long long> PositionSums;
	std::vector<int> Boundaries;
	std::vector<long long> Answers;
	std::vector<int> Counts;
	std::vector<long long> Sums;
	std::vector<int> MiddleCounts;
	std::vector<long long> MiddleSums;
	std::pair<int, long long> Middle(int Value, int First, int Last) const
	{
		int Begin;
		int End;
		int Offset = Offsets[Value];
		if constexpr (bSparse)
		{
			auto Start = Positions.begin() + Offset + 1;
			auto Finish = Positions.begin() + Offsets[Value + 1];
			Begin = static_cast<int>(std::lower_bound(Start, Finish, First) - Start);
			End = static_cast<int>(std::lower_bound(Start, Finish, Last) - Start);
		}
		else
		{
			Begin = Boundaries[static_cast<std::size_t>(First / Width) * Kinds + Value];
			End = Boundaries[static_cast<std::size_t>(Last / Width) * Kinds + Value];
		}
		return {End - Begin, PositionSums[Offset + End] - PositionSums[Offset + Begin]};
	}
public:
	FZeroQueries(FInput& Input, int n) : Size(n + 1), Values(Size)
	{
		while (Width * Width < Size)
		{
			++Width;
		}
		Blocks = (Size + Width - 1) / Width;
		std::vector<long long> Prefix(Size);
		for (int i = 1; i < Size; ++i)
		{
			Prefix[i] = Prefix[i - 1] + Input.Read();
		}
		auto Sorted = Prefix;
		std::sort(Sorted.begin(), Sorted.end());
		Sorted.erase(std::unique(Sorted.begin(), Sorted.end()), Sorted.end());
		Kinds = static_cast<int>(Sorted.size());
		Offsets.assign(Kinds + 1, 1);
		Offsets[0] = 0;
		for (int i = 0; i < Size; ++i)
		{
			Values[i] = static_cast<int>(std::lower_bound(Sorted.begin(), Sorted.end(), Prefix[i]) - Sorted.begin());
			++Offsets[Values[i] + 1];
		}
		for (int v = 0; v < Kinds; ++v)
		{
			Offsets[v + 1] += Offsets[v];
		}
		Positions.resize(Offsets.back());
		PositionSums.resize(Offsets.back());
		Counts.assign(Kinds, 0);
		Sums.assign(Kinds, 0);
		MiddleCounts.resize(Kinds);
		MiddleSums.resize(Kinds);
		for (int i = 0; i < Size; ++i)
		{
			int v = Values[i];
			int Index = Offsets[v] + ++Counts[v];
			Positions[Index] = i;
			PositionSums[Index] = PositionSums[Index - 1] + i;
		}
		if constexpr (!bSparse)
		{
			Boundaries.assign(static_cast<std::size_t>(Blocks + 1) * Kinds, 0);
			for (int b = 0; b < Blocks; ++b)
			{
				auto Previous = Boundaries.begin() + static_cast<std::size_t>(b) * Kinds;
				auto Current = Previous + Kinds;
				std::copy(Previous, Current, Current);
				for (int i = b * Width; i < std::min(Size, (b + 1) * Width); ++i)
				{
					++Current[Values[i]];
				}
			}
		}
		Answers.resize(Blocks * Blocks);
		for (int b = 0; b < Blocks; ++b)
		{
			std::fill(Counts.begin(), Counts.end(), 0);
			std::fill(Sums.begin(), Sums.end(), 0);
			long long Answer = 0;
			for (int i = b * Width; i < Size; ++i)
			{
				int v = Values[i];
				Answer += static_cast<long long>(Counts[v]) * i - Sums[v];
				++Counts[v];
				Sums[v] += i;
				if ((i + 1) % Width == 0 || i + 1 == Size)
				{
					Answers[b * Blocks + i / Width] = Answer;
				}
			}
		}
		std::fill(Counts.begin(), Counts.end(), 0);
		std::fill(Sums.begin(), Sums.end(), 0);
	}
	long long Query(int Left, int Right)
	{
		int First = (Left / Width + 1) * Width;
		int Last = (Right / Width) * Width;
		bool bMiddle = First < Last;
		long long Answer = bMiddle ? Answers[(First / Width) * Blocks + Last / Width - 1] : 0;
		auto Add = [&](int i)
		{
			int v = Values[i];
			Answer += static_cast<long long>(Counts[v]) * i - Sums[v];
			if (bMiddle)
			{
				if (Counts[v] == 0)
				{
					auto MiddleStats = Middle(v, First, Last);
					MiddleCounts[v] = MiddleStats.first;
					MiddleSums[v] = MiddleStats.second;
				}
				long long Cross = MiddleSums[v] - static_cast<long long>(MiddleCounts[v]) * i;
				Answer += i < First ? Cross : -Cross;
			}
			++Counts[v];
			Sums[v] += i;
		};
		auto Clear = [&](int i)
		{
			Counts[Values[i]] = 0;
			Sums[Values[i]] = 0;
		};
		if (bMiddle)
		{
			for (int i = Left; i < First; ++i)
			{
				Add(i);
			}
			for (int i = Last; i <= Right; ++i)
			{
				Add(i);
			}
			for (int i = Left; i < First; ++i)
			{
				Clear(i);
			}
			for (int i = Last; i <= Right; ++i)
			{
				Clear(i);
			}
		}
		else
		{
			for (int i = Left; i <= Right; ++i)
			{
				Add(i);
			}
			for (int i = Left; i <= Right; ++i)
			{
				Clear(i);
			}
		}
		return Answer;
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	FZeroQueries<true> Solver(Input, n);
	long long LastAnswer = 0;
	for (int i = 0; i < m; ++i)
	{
		int Left = static_cast<int>((Input.Read() ^ LastAnswer) % n);
		int Right = static_cast<int>((Input.Read() ^ LastAnswer) % n);
		if (Left > Right)
		{
			std::swap(Left, Right);
		}
		LastAnswer = Solver.Query(Left, Right + 1);
		Output.Write(LastAnswer);
	}
}
