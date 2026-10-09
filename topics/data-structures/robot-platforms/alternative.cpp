// Codex (GPT-6): implicit treap application, with circular movement by rank.
// Treaps are an established data structure; priorities affect runtime only.
#include <cstdint>
#include <iostream>
#include <vector>

struct FNode
{
	int Left = 0;
	int Right = 0;
	int Size = 1;
	std::uint64_t Priority = 0;
};

class FSequence
{
public:
	std::vector<FNode> Nodes;
	std::uint64_t State = 2026093017;

	explicit FSequence(int Capacity) : Nodes(Capacity + 1)
	{
		Nodes[0].Size = 0;
	}

	void Create(int Id)
	{
		std::uint64_t z = (State += UINT64_C(0x9e3779b97f4a7c15));
		z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
		z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
		Nodes[Id].Priority = z ^ (z >> 31);
	}

	void Pull(int Root)
	{
		Nodes[Root].Size = 1 + Nodes[Nodes[Root].Left].Size + Nodes[Nodes[Root].Right].Size;
	}

	int Merge(int Left, int Right)
	{
		if (Left == 0 || Right == 0)
		{
			return Left + Right;
		}
		if (Nodes[Left].Priority > Nodes[Right].Priority)
		{
			Nodes[Left].Right = Merge(Nodes[Left].Right, Right);
			Pull(Left);
			return Left;
		}
		Nodes[Right].Left = Merge(Left, Nodes[Right].Left);
		Pull(Right);
		return Right;
	}

	void Split(int Root, int Count, int& Left, int& Right)
	{
		if (Root == 0)
		{
			Left = 0;
			Right = 0;
			return;
		}
		int LeftSize = Nodes[Nodes[Root].Left].Size;
		if (Count <= LeftSize)
		{
			Right = Root;
			Split(Nodes[Root].Left, Count, Left, Nodes[Root].Left);
		}
		else
		{
			Left = Root;
			Split(Nodes[Root].Right, Count - LeftSize - 1, Nodes[Root].Right, Right);
		}
		Pull(Root);
	}

	int Select(int Root, int Rank) const
	{
		while (Root != 0)
		{
			int LeftSize = Nodes[Nodes[Root].Left].Size;
			if (Rank == LeftSize)
			{
				return Root;
			}
			if (Rank < LeftSize)
			{
				Root = Nodes[Root].Left;
			}
			else
			{
				Rank -= LeftSize + 1;
				Root = Nodes[Root].Right;
			}
		}
		return -1;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	FSequence Tree(n + m);
	int Root = 0;
	for (int i = 1; i <= n; ++i)
	{
		Tree.Create(i);
		Root = Tree.Merge(Root, i);
	}
	int LastId = n;
	int CurrentRank = 0;
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		std::cin >> Operation;
		int Size = Tree.Nodes[Root].Size;
		if (Operation == 0 && Size > 0)
		{
			int Left;
			int Right;
			int Removed;
			Tree.Split(Root, CurrentRank, Left, Right);
			Tree.Split(Right, 1, Removed, Right);
			Root = Tree.Merge(Left, Right);
			CurrentRank = Size == 1 ? 0 : CurrentRank % (Size - 1);
		}
		else if (Operation == 1)
		{
			int Left;
			int Right;
			Tree.Create(++LastId);
			Tree.Split(Root, Size == 0 ? 0 : CurrentRank + 1, Left, Right);
			Root = Tree.Merge(Tree.Merge(Left, LastId), Right);
		}
		else if (Operation == 2 || Operation == 3)
		{
			long long x;
			std::cin >> x;
			if (Size > 0)
			{
				x = Operation == 2 ? x : -x;
				CurrentRank = static_cast<int>(((CurrentRank + x) % Size + Size) % Size);
			}
		}
		else if (Operation == 4)
		{
			std::cout << Tree.Select(Root, CurrentRank) << '\n';
		}
	}
}
