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

class FSegmentTree
{
	static constexpr int Infinity = std::numeric_limits<int>::max();
	int n;
	std::vector<int> Minimum;
	std::vector<int> Count;
	void Pull(int Node)
	{
		Minimum[Node] = std::min(Minimum[Node * 2], Minimum[Node * 2 + 1]);
		Count[Node] = Count[Node * 2] + Count[Node * 2 + 1];
	}
	void Build(int Node, int Left, int Right, const std::vector<int>& Values)
	{
		if (Left == Right)
		{
			Minimum[Node] = Values[Left];
			Count[Node] = 1;
			return;
		}
		int Middle = (Left + Right) / 2;
		Build(Node * 2, Left, Middle, Values);
		Build(Node * 2 + 1, Middle + 1, Right, Values);
		Pull(Node);
	}
	void Erase(int Node, int Left, int Right, int Bound, int Value)
	{
		if (Left > Bound || Minimum[Node] > Value)
		{
			return;
		}
		if (Left == Right)
		{
			Minimum[Node] = Infinity;
			Count[Node] = 0;
			return;
		}
		int Middle = (Left + Right) / 2;
		Erase(Node * 2, Left, Middle, Bound, Value);
		Erase(Node * 2 + 1, Middle + 1, Right, Bound, Value);
		Pull(Node);
	}
	int Query(int Node, int Left, int Right, int First, int Last) const
	{
		if (Right < First || Last < Left || Count[Node] == 0)
		{
			return 0;
		}
		if (First <= Left && Right <= Last)
		{
			return Count[Node];
		}
		int Middle = (Left + Right) / 2;
		return Query(Node * 2, Left, Middle, First, Last) + Query(Node * 2 + 1, Middle + 1, Right, First, Last);
	}
public:
	explicit FSegmentTree(const std::vector<int>& Values)
		: n(static_cast<int>(Values.size()) - 1), Minimum(4 * n + 4), Count(4 * n + 4)
	{
		Build(1, 1, n, Values);
	}
	void Erase(int Bound, int Value)
	{
		Erase(1, 1, n, Bound, Value);
	}
	int Query(int First, int Last) const
	{
		return Query(1, 1, n, First, Last);
	}
};

struct FQuery
{
	int Left;
	int Right;
	int Index;
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<int> Values(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		Values[i] = Input.Read();
	}
	std::vector<FQuery> Queries(m);
	for (int i = 0; i < m; ++i)
	{
		Queries[i] = {Input.Read(), Input.Read(), i};
	}
	std::sort(Queries.begin(), Queries.end(), [](const FQuery& Left, const FQuery& Right)
	{
		return Left.Right < Right.Right;
	});
	FSegmentTree Tree(Values);
	std::vector<int> Answers(m);
	int Processed = 0;
	for (const FQuery& Query : Queries)
	{
		while (Processed < Query.Right)
		{
			++Processed;
			Tree.Erase(Processed - 1, Values[Processed]);
		}
		Answers[Query.Index] = Tree.Query(Query.Left, Query.Right);
	}
	for (int Answer : Answers)
	{
		Output.Write(Answer);
	}
}
