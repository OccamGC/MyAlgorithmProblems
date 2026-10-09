// Contribution: Codex (GPT-6): rebuilt the event-batched greedy implementation,
// including zero-resource stations, waiting barriers, and overflow-safe modular sums.
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

using FInt = long long;
constexpr FInt Infinity = 4000000000000000000LL;
constexpr FInt Modulus = 1000000009;

class FMinimumTree
{
private:
	int Size;
	std::vector<FInt> Minimum;
	std::vector<FInt> Lazy;
	void Build(int Node, int Left, int Right, const std::vector<FInt>& Values)
	{
		if (Left == Right)
		{
			Minimum[Node] = Values[Left];
			return;
		}
		int Middle = (Left + Right) / 2;
		Build(2 * Node, Left, Middle, Values);
		Build(2 * Node + 1, Middle + 1, Right, Values);
		Pull(Node);
	}
	void Apply(int Node, FInt Delta)
	{
		Minimum[Node] += Delta;
		Lazy[Node] += Delta;
	}
	void Push(int Node)
	{
		Apply(2 * Node, Lazy[Node]);
		Apply(2 * Node + 1, Lazy[Node]);
		Lazy[Node] = 0;
	}
	void Pull(int Node)
	{
		Minimum[Node] = std::min(Minimum[2 * Node], Minimum[2 * Node + 1]);
	}
	void Add(int Node, int Left, int Right, int From, int To, FInt Delta)
	{
		if (From > Right || To < Left)
		{
			return;
		}
		if (From <= Left && Right <= To)
		{
			Apply(Node, Delta);
			return;
		}
		Push(Node);
		int Middle = (Left + Right) / 2;
		Add(2 * Node, Left, Middle, From, To, Delta);
		Add(2 * Node + 1, Middle + 1, Right, From, To, Delta);
		Pull(Node);
	}
	FInt Query(int Node, int Left, int Right, int From, int To)
	{
		if (From > Right || To < Left)
		{
			return Infinity;
		}
		if (From <= Left && Right <= To)
		{
			return Minimum[Node];
		}
		Push(Node);
		int Middle = (Left + Right) / 2;
		return std::min(Query(2 * Node, Left, Middle, From, To),
			Query(2 * Node + 1, Middle + 1, Right, From, To));
	}
	void Zeros(int Node, int Left, int Right, int From, int To, std::vector<int>& Result)
	{
		if (From > Right || To < Left || Minimum[Node] > 0)
		{
			return;
		}
		if (Left == Right)
		{
			Result.push_back(Left);
			return;
		}
		Push(Node);
		int Middle = (Left + Right) / 2;
		Zeros(2 * Node, Left, Middle, From, To, Result);
		Zeros(2 * Node + 1, Middle + 1, Right, From, To, Result);
	}
public:
	explicit FMinimumTree(const std::vector<FInt>& Values)
		: Size(static_cast<int>(Values.size())), Minimum(4 * Size), Lazy(4 * Size)
	{
		Build(1, 0, Size - 1, Values);
	}
	void Add(int Left, int Right, FInt Delta)
	{
		Add(1, 0, Size - 1, Left, Right, Delta);
	}
	FInt Query(int Left, int Right)
	{
		return Left > Right ? Infinity : Query(1, 0, Size - 1, Left, Right);
	}
	void Zeros(int Left, int Right, std::vector<int>& Result)
	{
		if (Left <= Right)
		{
			Zeros(1, 0, Size - 1, Left, Right, Result);
		}
	}
};

struct FBlock
{
	FInt Gain;
	int Left;
	int Right;
	bool operator<(const FBlock& Other) const
	{
		return Gain < Other.Gain;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	FInt K;
	std::cin >> n >> K;
	std::vector<FInt> Num(n);
	std::vector<FInt> Ready(n);
	std::vector<FInt> Travel(n);
	std::vector<FInt> Arrival(n);
	std::vector<FInt> Delivered(n);
	std::vector<FInt> Prefix(n);
	std::vector<FInt> Slack(n);
	std::vector<FInt> Difference(n + 1);
	for (int i = 0; i + 1 < n; ++i)
	{
		std::cin >> Num[i] >> Ready[i] >> Travel[i];
		if (Num[i] == 0)
		{
			Ready[i] = 0;
		}
		Arrival[i + 1] = std::max(Arrival[i], Ready[i]) + Travel[i];
		Delivered[i + 1] = Delivered[i] + Num[i];
		Prefix[i + 1] = Prefix[i] + Delivered[i + 1];
	}
	for (int i = 0; i < n; ++i)
	{
		Slack[i] = Arrival[i] - Ready[i];
	}
	FMinimumTree Tree(Slack);
	std::priority_queue<FBlock> Heap;
	auto Insert = [&](int Left, int Right)
	{
		while (Left < Right && Travel[Left] == 0)
		{
			++Left;
		}
		if (Left < Right)
		{
			Heap.push({Prefix[Right] - Prefix[Left], Left, Right});
		}
	};
	std::vector<int> Boundaries{0};
	Tree.Zeros(1, n - 2, Boundaries);
	Boundaries.push_back(n - 1);
	for (std::size_t i = 1; i < Boundaries.size(); ++i)
	{
		Insert(Boundaries[i - 1], Boundaries[i]);
	}
	while (K > 0 && !Heap.empty() && Heap.top().Gain > 0)
	{
		FBlock Block = Heap.top();
		Heap.pop();
		int Left = Block.Left;
		int Right = Block.Right;
		FInt Delta = std::min({K, Travel[Left], Tree.Query(Left + 1, Right - 1)});
		K -= Delta;
		Travel[Left] -= Delta;
		Tree.Add(Left + 1, Right, -Delta);
		Difference[Left + 1] -= Delta;
		Difference[Right + 1] += Delta;
		Boundaries.assign(1, Left);
		Tree.Zeros(Left + 1, Right - 1, Boundaries);
		Boundaries.push_back(Right);
		for (std::size_t i = 1; i < Boundaries.size(); ++i)
		{
			Insert(Boundaries[i - 1], Boundaries[i]);
		}
	}
	FInt Answer = 0;
	FInt Change = 0;
	for (int i = 0; i < n; ++i)
	{
		Change += Difference[i];
		FInt FinalArrival = Arrival[i] + Change;
		Answer = (Answer + FinalArrival % Modulus * (Delivered[i] % Modulus)) % Modulus;
		FInt Production = (n - 1LL - i) * (Ready[i] % Modulus) % Modulus;
		Production = Production * (Num[i] % Modulus) % Modulus;
		Answer = (Answer - Production + Modulus) % Modulus;
	}
	std::cout << Answer << '\n';
}
