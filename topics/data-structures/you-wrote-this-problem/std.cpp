// GPT-6: completed XOR specification, block-pair matrix with 2D Fenwick tree,
// per-value AVL order statistics, implementation and verification.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using FInt = std::int64_t;
struct FNode
{
	int Left = 0;
	int Right = 0;
	int Height = 0;
	int Size = 0;
};
class FPositions
{
	std::vector<FNode> Nodes;
	void Pull(int Root)
	{
		Nodes[Root].Height = 1 + std::max(Nodes[Nodes[Root].Left].Height, Nodes[Nodes[Root].Right].Height);
		Nodes[Root].Size = 1 + Nodes[Nodes[Root].Left].Size + Nodes[Nodes[Root].Right].Size;
	}
	int RotateLeft(int Root)
	{
		int Next = Nodes[Root].Right;
		Nodes[Root].Right = Nodes[Next].Left;
		Nodes[Next].Left = Root;
		Pull(Root);
		Pull(Next);
		return Next;
	}
	int RotateRight(int Root)
	{
		int Next = Nodes[Root].Left;
		Nodes[Root].Left = Nodes[Next].Right;
		Nodes[Next].Right = Root;
		Pull(Root);
		Pull(Next);
		return Next;
	}
	int Balance(int Root)
	{
		Pull(Root);
		int Left = Nodes[Root].Left;
		int Right = Nodes[Root].Right;
		if (Nodes[Left].Height > Nodes[Right].Height + 1)
		{
			if (Nodes[Nodes[Left].Right].Height > Nodes[Nodes[Left].Left].Height)
			{
				Nodes[Root].Left = RotateLeft(Left);
			}
			return RotateRight(Root);
		}
		if (Nodes[Right].Height > Nodes[Left].Height + 1)
		{
			if (Nodes[Nodes[Right].Left].Height > Nodes[Nodes[Right].Right].Height)
			{
				Nodes[Root].Right = RotateRight(Right);
			}
			return RotateLeft(Root);
		}
		return Root;
	}
	int ExtractFirst(int Root, int& First)
	{
		if (Nodes[Root].Left == 0)
		{
			First = Root;
			return Nodes[Root].Right;
		}
		Nodes[Root].Left = ExtractFirst(Nodes[Root].Left, First);
		return Balance(Root);
	}
public:
	explicit FPositions(int n) : Nodes(n + 1)
	{
	}
	int Insert(int Root, int Position)
	{
		if (Root == 0)
		{
			Nodes[Position] = {0, 0, 1, 1};
			return Position;
		}
		if (Position < Root)
		{
			Nodes[Root].Left = Insert(Nodes[Root].Left, Position);
		}
		else
		{
			Nodes[Root].Right = Insert(Nodes[Root].Right, Position);
		}
		return Balance(Root);
	}
	int Erase(int Root, int Position)
	{
		if (Root == Position)
		{
			int Left = Nodes[Root].Left;
			int Right = Nodes[Root].Right;
			if (Right == 0)
			{
				return Left;
			}
			int Next = 0;
			Right = ExtractFirst(Right, Next);
			Nodes[Next].Left = Left;
			Nodes[Next].Right = Right;
			return Balance(Next);
		}
		if (Position < Root)
		{
			Nodes[Root].Left = Erase(Nodes[Root].Left, Position);
		}
		else
		{
			Nodes[Root].Right = Erase(Nodes[Root].Right, Position);
		}
		return Balance(Root);
	}
	int Rank(int Root, int Position) const
	{
		int Answer = 0;
		while (Root)
		{
			if (Root <= Position)
			{
				Answer += 1 + Nodes[Nodes[Root].Left].Size;
				Root = Nodes[Root].Right;
			}
			else
			{
				Root = Nodes[Root].Left;
			}
		}
		return Answer;
	}
};
class FMatrix
{
	int Size;
	std::vector<FInt> Tree;
	FInt Prefix(int x, int y) const
	{
		FInt Answer = 0;
		for (int i = x; i > 0; i -= i & -i)
		{
			for (int j = y; j > 0; j -= j & -j)
			{
				Answer += Tree[i * (Size + 1) + j];
			}
		}
		return Answer;
	}
public:
	explicit FMatrix(int Size) : Size(Size), Tree((Size + 1) * (Size + 1))
	{
	}
	void Add(int x, int y, FInt Delta)
	{
		for (int i = x + 1; i <= Size; i += i & -i)
		{
			for (int j = y + 1; j <= Size; j += j & -j)
			{
				Tree[i * (Size + 1) + j] += Delta;
			}
		}
	}
	FInt Rectangle(int Left1, int Right1, int Left2, int Right2) const
	{
		if (Left1 >= Right1 || Left2 >= Right2)
		{
			return 0;
		}
		return Prefix(Right1, Right2) - Prefix(Left1, Right2)
			- Prefix(Right1, Left2) + Prefix(Left1, Left2);
	}
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	const int BlockSize = 400;
	int Blocks = (n + BlockSize - 1) / BlockSize;
	std::vector<FInt> Values(n + 1);
	std::vector<std::map<FInt, int>> Frequency(Blocks);
	std::map<FInt, int> Roots;
	FPositions Positions(n);
	FMatrix Matrix(Blocks);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Values[i];
		++Frequency[(i - 1) / BlockSize][Values[i]];
		Roots[Values[i]] = Positions.Insert(Roots[Values[i]], i);
	}
	std::map<FInt, std::vector<std::pair<int, int>>> Groups;
	for (int Block = 0; Block < Blocks; ++Block)
	{
		for (const auto& Entry : Frequency[Block])
		{
			Groups[Entry.first].push_back({Block, Entry.second});
		}
	}
	std::vector<FInt> Initial(Blocks * Blocks);
	for (const auto& Group : Groups)
	{
		for (const auto& First : Group.second)
		{
			for (const auto& Second : Group.second)
			{
				Initial[First.first * Blocks + Second.first] += static_cast<FInt>(First.second) * Second.second;
			}
		}
	}
	for (int i = 0; i < Blocks; ++i)
	{
		for (int j = 0; j < Blocks; ++j)
		{
			Matrix.Add(i, j, Initial[i * Blocks + j]);
		}
	}
	Groups.clear();
	Initial.clear();
	auto FrequencyOf = [&](int Block, FInt Value)
	{
		auto Entry = Frequency[Block].find(Value);
		return Entry == Frequency[Block].end() ? 0 : Entry->second;
	};
	auto Count = [&](FInt Value, int Left, int Right)
	{
		int Root = Roots.find(Value)->second;
		return Positions.Rank(Root, Right) - Positions.Rank(Root, Left - 1);
	};
	std::uint64_t Last = 0;
	auto Read = [&]()
	{
		std::uint64_t Raw;
		std::cin >> Raw;
		return Raw ^ Last;
	};
	while (m--)
	{
		int Type = static_cast<int>(Read());
		if (Type == 1)
		{
			int Position = static_cast<int>(Read());
			std::uint64_t Bits = Read();
			FInt Value = Bits >> 63 ? -1 - static_cast<FInt>(~Bits) : static_cast<FInt>(Bits);
			FInt Old = Values[Position];
			if (Old == Value)
			{
				continue;
			}
			int Block = (Position - 1) / BlockSize;
			for (int Other = 0; Other < Blocks; ++Other)
			{
				FInt Delta = FrequencyOf(Other, Value) - FrequencyOf(Other, Old);
				if (Other == Block)
				{
					Matrix.Add(Block, Block, 2 * (Delta + 1));
				}
				else
				{
					Matrix.Add(Block, Other, Delta);
					Matrix.Add(Other, Block, Delta);
				}
			}
			if (--Frequency[Block][Old] == 0)
			{
				Frequency[Block].erase(Old);
			}
			++Frequency[Block][Value];
			Roots[Old] = Positions.Erase(Roots[Old], Position);
			if (Roots[Old] == 0)
			{
				Roots.erase(Old);
			}
			Roots[Value] = Positions.Insert(Roots[Value], Position);
			Values[Position] = Value;
		}
		else
		{
			int l1 = static_cast<int>(Read());
			int r1 = static_cast<int>(Read());
			int l2 = static_cast<int>(Read());
			int r2 = static_cast<int>(Read());
			int Left1 = (l1 + BlockSize - 2) / BlockSize;
			int Right1 = r1 / BlockSize;
			int Left2 = (l2 + BlockSize - 2) / BlockSize;
			int Right2 = r2 / BlockSize;
			FInt Answer = Matrix.Rectangle(Left1, Right1, Left2, Right2);
			auto Fringe = [&](int Left, int Right, int FullLeft, int FullRight, int OtherLeft, int OtherRight)
			{
				if (OtherLeft > OtherRight)
				{
					return;
				}
				for (int i = Left; i <= Right; ++i)
				{
					if (FullLeft < FullRight && i == FullLeft * BlockSize + 1)
					{
						i = FullRight * BlockSize;
						continue;
					}
					Answer += Count(Values[i], OtherLeft, OtherRight);
				}
			};
			Fringe(l1, r1, Left1, Right1, l2, r2);
			if (Left1 < Right1)
			{
				Fringe(l2, r2, Left2, Right2, Left1 * BlockSize + 1, Right1 * BlockSize);
			}
			std::cout << Answer << '\n';
			Last = static_cast<std::uint64_t>(Answer);
		}
	}
}
