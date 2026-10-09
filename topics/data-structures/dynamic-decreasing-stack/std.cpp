// GPT-6: explicit pop-on-equality specification, visibility segment tree, implementation.
#include <algorithm>
#include <iostream>
#include <vector>
struct FNode
{
	int Maximum = -1;
	int Count = 0;
};
class FTree
{
	std::vector<FNode> Nodes;
	int CountAbove(int Node, int Left, int Right, int Threshold) const
	{
		if (Nodes[Node].Maximum <= Threshold)
		{
			return 0;
		}
		if (Left == Right)
		{
			return 1;
		}
		int Middle = (Left + Right) / 2;
		if (Nodes[Node * 2 + 1].Maximum <= Threshold)
		{
			return CountAbove(Node * 2, Left, Middle, Threshold);
		}
		return CountAbove(Node * 2 + 1, Middle + 1, Right, Threshold)
			+ Nodes[Node].Count - Nodes[Node * 2 + 1].Count;
	}
	void Pull(int Node, int Left, int Right)
	{
		int Middle = (Left + Right) / 2;
		Nodes[Node].Maximum = std::max(Nodes[Node * 2].Maximum, Nodes[Node * 2 + 1].Maximum);
		Nodes[Node].Count = Nodes[Node * 2 + 1].Count
			+ CountAbove(Node * 2, Left, Middle, Nodes[Node * 2 + 1].Maximum);
	}
public:
	explicit FTree(int n) : Nodes(4 * n)
	{
	}
	void Build(int Node, int Left, int Right, const std::vector<int>& Values)
	{
		if (Left == Right)
		{
			Nodes[Node] = {Values[Left], 1};
			return;
		}
		int Middle = (Left + Right) / 2;
		Build(Node * 2, Left, Middle, Values);
		Build(Node * 2 + 1, Middle + 1, Right, Values);
		Pull(Node, Left, Right);
	}
	void Update(int Node, int Left, int Right, int Position, int Value)
	{
		if (Left == Right)
		{
			Nodes[Node] = {Value, 1};
			return;
		}
		int Middle = (Left + Right) / 2;
		if (Position <= Middle)
		{
			Update(Node * 2, Left, Middle, Position, Value);
		}
		else
		{
			Update(Node * 2 + 1, Middle + 1, Right, Position, Value);
		}
		Pull(Node, Left, Right);
	}
	int Query(int Node, int Left, int Right, int l, int r, int& Threshold) const
	{
		if (r < Left || Right < l)
		{
			return 0;
		}
		if (l <= Left && Right <= r)
		{
			int Answer = CountAbove(Node, Left, Right, Threshold);
			Threshold = std::max(Threshold, Nodes[Node].Maximum);
			return Answer;
		}
		int Middle = (Left + Right) / 2;
		int Answer = Query(Node * 2 + 1, Middle + 1, Right, l, r, Threshold);
		return Answer + Query(Node * 2, Left, Middle, l, r, Threshold);
	}
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Values(n);
	for (int& Value : Values)
	{
		std::cin >> Value;
	}
	FTree Tree(n);
	Tree.Build(1, 0, n - 1, Values);
	while (m--)
	{
		int Type;
		int x;
		int y;
		std::cin >> Type >> x >> y;
		if (Type == 1)
		{
			Tree.Update(1, 0, n - 1, x - 1, y);
		}
		else
		{
			int Threshold = -1;
			std::cout << Tree.Query(1, 0, n - 1, x - 1, y - 1, Threshold) << '\n';
		}
	}
}
