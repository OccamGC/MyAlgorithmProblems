// Codex (GPT-6): segment-tree acceleration of the setter's checked flat-memory simulation; binary-string copies use two range assignments.
#include <algorithm>
#include <iostream>
#include <vector>

class FMemory
{
private:
	int Length;
	std::vector<int> ZeroCount;
	std::vector<int> Lazy;
	void Apply(int Node, int Left, int Right, int Value)
	{
		ZeroCount[Node] = Value == 0 ? Right - Left : 0;
		Lazy[Node] = Value;
	}
	void Push(int Node, int Left, int Right)
	{
		if (Lazy[Node] != -1 && Right - Left > 1)
		{
			int Mid = (Left + Right) / 2;
			Apply(Node * 2, Left, Mid, Lazy[Node]);
			Apply(Node * 2 + 1, Mid, Right, Lazy[Node]);
			Lazy[Node] = -1;
		}
	}
	void Assign(int Node, int Left, int Right, int Begin, int End, int Value)
	{
		if (Begin <= Left && Right <= End)
		{
			Apply(Node, Left, Right, Value);
			return;
		}
		Push(Node, Left, Right);
		int Mid = (Left + Right) / 2;
		if (Begin < Mid)
		{
			Assign(Node * 2, Left, Mid, Begin, End, Value);
		}
		if (End > Mid)
		{
			Assign(Node * 2 + 1, Mid, Right, Begin, End, Value);
		}
		ZeroCount[Node] = ZeroCount[Node * 2] + ZeroCount[Node * 2 + 1];
	}
	int Find(int Node, int Left, int Right, int Begin)
	{
		if (Right <= Begin || ZeroCount[Node] == 0)
		{
			return Length;
		}
		if (Right - Left == 1)
		{
			return Left;
		}
		Push(Node, Left, Right);
		int Mid = (Left + Right) / 2;
		int Result = Find(Node * 2, Left, Mid, Begin);
		return Result != Length ? Result : Find(Node * 2 + 1, Mid, Right, Begin);
	}
public:
	explicit FMemory(const std::vector<int>& Initial) : Length(static_cast<int>(Initial.size())), ZeroCount(4 * Length), Lazy(4 * Length, -1)
	{
		for (int i = 0; i < Length; ++i)
		{
			Fill(i, i + 1, Initial[i]);
		}
	}
	int Size() const
	{
		return Length;
	}
	void Fill(int Left, int Right, int Value)
	{
		if (Left < Right)
		{
			Assign(1, 0, Length, Left, Right, Value);
		}
	}
	int FirstZero(int Position)
	{
		return Find(1, 0, Length, Position);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Start(n + 1);
	for (int i = 0; i < n; ++i)
	{
		int Length;
		std::cin >> Length;
		Start[i + 1] = Start[i] + Length;
	}
	std::vector<int> Initial(Start[n]);
	for (int& Value : Initial)
	{
		std::cin >> Value;
	}
	FMemory Memory(Initial);
	auto InArray = [&](int Array, long long Left, long long End)
	{
		return Start[Array] <= Left && End <= Start[Array + 1];
	};
	int k;
	std::cin >> k;
	while (k--)
	{
		int Operation;
		int Array;
		long long Offset;
		std::cin >> Operation >> Array >> Offset;
		long long Begin = Start[Array] + Offset;
		if (Operation == 0)
		{
			int Value;
			long long Count;
			std::cin >> Value >> Count;
			if (Count == 0)
			{
				std::cout << "true\n";
				continue;
			}
			long long End = Begin + Count;
			if (Begin < 0 || End > Memory.Size())
			{
				std::cout << "overflow\n";
				continue;
			}
			bool bWarning = !InArray(Array, Begin, End);
			Memory.Fill(static_cast<int>(Begin), static_cast<int>(End), Value);
			std::cout << (bWarning ? "wtrue\n" : "true\n");
			continue;
		}
		int DestinationArray = 0;
		long long Destination = 0;
		if (Operation == 1)
		{
			std::cin >> DestinationArray >> Offset;
			Destination = Start[DestinationArray] + Offset;
		}
		if (Begin < 0 || Begin >= Memory.Size())
		{
			std::cout << "overflow\n";
			continue;
		}
		int Zero = Memory.FirstZero(static_cast<int>(Begin));
		if (Zero == Memory.Size())
		{
			std::cout << "overflow\n";
			continue;
		}
		long long Count = Zero - Begin + 1;
		bool bWarning = !InArray(Array, Begin, Zero + 1);
		if (Operation == 2)
		{
			std::cout << (bWarning ? "w" : "") << Count - 1 << '\n';
			continue;
		}
		long long End = Destination + Count;
		if (Destination < 0 || End > Memory.Size())
		{
			std::cout << "overflow\n";
			continue;
		}
		if (std::max(Begin, Destination) < std::min(Begin + Count, End))
		{
			std::cout << "overwrite\n";
			continue;
		}
		bWarning = bWarning || !InArray(DestinationArray, Destination, End);
		Memory.Fill(static_cast<int>(Destination), static_cast<int>(End - 1), 1);
		Memory.Fill(static_cast<int>(End - 1), static_cast<int>(End), 0);
		std::cout << (bWarning ? "wtrue\n" : "true\n");
	}
}
