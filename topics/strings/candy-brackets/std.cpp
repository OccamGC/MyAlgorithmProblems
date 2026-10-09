// Problem setter's solution: endpoint reductions for nonnegative weights.
// Codex (GPT-6): signed-weight extension using legal prefix/suffix/substrings.
#include <algorithm>
#include <deque>
#include <iostream>
#include <vector>

struct FBlock
{
	long long Sum;
	long long Prefix;
	long long Suffix;
	long long Best;
	int Type;
};

FBlock MakeCandy(long long Value)
{
	const long long Best = std::max(0LL, Value);
	return {Value, Best, Best, Best, 2};
}

FBlock Concatenate(const FBlock& Left, const FBlock& Right)
{
	return {
		Left.Sum + Right.Sum,
		std::max(Left.Prefix, Left.Sum + Right.Prefix),
		std::max(Right.Suffix, Right.Sum + Left.Suffix),
		std::max({Left.Best, Right.Best, Left.Suffix + Right.Prefix}),
		2
	};
}

FBlock Wrap(const FBlock& Middle, long long BracketSum)
{
	const long long Sum = Middle.Sum + BracketSum;
	const long long Edge = std::max(0LL, Sum);
	return {Sum, Edge, Edge, std::max(Middle.Best, Edge), 2};
}

class FSequence
{
private:
	std::deque<FBlock> Elements;
	long long Best = 0;

public:
	void Insert(int Position, int Type, long long Value)
	{
		const bool bLeft = Position == 0;
		const FBlock Element = Type == 2 ? MakeCandy(Value) : FBlock{Value, 0, 0, 0, Type};
		if (bLeft)
		{
			Elements.push_front(Element);
		}
		else
		{
			Elements.push_back(Element);
		}
		auto At = [&](int Offset) -> FBlock&
		{
			return Elements[bLeft ? Offset : Elements.size() - 1 - Offset];
		};
		auto Pop = [&]()
		{
			if (bLeft)
			{
				Elements.pop_front();
			}
			else
			{
				Elements.pop_back();
			}
		};
		const int Opening = bLeft ? 0 : 1;
		const int Closing = bLeft ? 1 : 0;
		while (Elements.size() >= 2)
		{
			if (At(0).Type == 2 && At(1).Type == 2)
			{
				// Prefix and suffix refer to physical left-to-right order.
				At(1) = bLeft ? Concatenate(At(0), At(1)) : Concatenate(At(1), At(0));
				Pop();
			}
			else if (At(0).Type == Opening && At(1).Type == Closing)
			{
				At(1) = MakeCandy(At(0).Sum + At(1).Sum);
				Pop();
			}
			else if (Elements.size() >= 3 && At(0).Type == Opening &&
				At(1).Type == 2 && At(2).Type == Closing)
			{
				At(2) = Wrap(At(1), At(0).Sum + At(2).Sum);
				Pop();
				Pop();
			}
			else
			{
				break;
			}
		}
		if (At(0).Type == 2)
		{
			Best = std::max(Best, At(0).Best);
		}
	}

	long long GetAnswer() const
	{
		return Best;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	if (!(std::cin >> N >> M))
	{
		return 0;
	}
	std::vector<unsigned char> Types(N);
	for (unsigned char& Type : Types)
	{
		int InputType;
		std::cin >> InputType;
		Type = static_cast<unsigned char>(InputType);
	}
	FSequence Sequence;
	for (int Type : Types)
	{
		long long Value;
		std::cin >> Value;
		Sequence.Insert(1, Type, Value);
	}
	std::cout << Sequence.GetAnswer() << '\n';
	for (int i = 0; i < M; ++i)
	{
		int Position;
		int Type;
		long long Value;
		std::cin >> Position >> Type >> Value;
		Sequence.Insert(Position, Type, Value);
		std::cout << Sequence.GetAnswer() << '\n';
	}
	return 0;
}
