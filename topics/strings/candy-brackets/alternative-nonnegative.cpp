// Nonnegative-weight subtask. C++17 implementation by Codex (GPT-6).
// Nonnegative-weight subtask only. Signed inputs require std.cpp.
#include <algorithm>
#include <deque>
#include <iostream>
#include <vector>

struct FBlock
{
	long long Sum;
	int Type;
};

class FSequence
{
private:
	std::deque<FBlock> Elements;
	long long Best = 0;

public:
	void Insert(int Position, int Type, long long Value)
	{
		const bool bLeft = Position == 0;
		const FBlock Element = {Value, Type};
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
				At(1).Sum += At(0).Sum;
				Pop();
			}
			else if (At(0).Type == Opening && At(1).Type == Closing)
			{
				At(1) = {At(0).Sum + At(1).Sum, 2};
				Pop();
			}
			else if (Elements.size() >= 3 && At(0).Type == Opening &&
				At(1).Type == 2 && At(2).Type == Closing)
			{
				At(2) = {At(0).Sum + At(1).Sum + At(2).Sum, 2};
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
			Best = std::max(Best, At(0).Sum);
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
