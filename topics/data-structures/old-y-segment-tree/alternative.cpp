// Codex (GPT-6): persistent prefix-stack membership; each decoded query counts a version's marked suffix.
#include <cstdint>
#include <iostream>
#include <vector>

struct FNode
{
	int Left = 0;
	int Right = 0;
	int Sum = 0;
};

class FPersistentTree
{
private:
	std::vector<FNode> Nodes{{}};
public:
	int Set(int Root, int Left, int Right, int Position, int Value)
	{
		int Current = static_cast<int>(Nodes.size());
		Nodes.push_back(Nodes[Root]);
		if (Left == Right)
		{
			Nodes[Current].Sum = Value;
			return Current;
		}
		int Mid = (Left + Right) / 2;
		if (Position <= Mid)
		{
			int Child = Set(Nodes[Current].Left, Left, Mid, Position, Value);
			Nodes[Current].Left = Child;
		}
		else
		{
			int Child = Set(Nodes[Current].Right, Mid + 1, Right, Position, Value);
			Nodes[Current].Right = Child;
		}
		Nodes[Current].Sum = Nodes[Nodes[Current].Left].Sum + Nodes[Nodes[Current].Right].Sum;
		return Current;
	}
	int Suffix(int Root, int Left, int Right, int Begin) const
	{
		if (Root == 0 || Right < Begin)
		{
			return 0;
		}
		if (Begin <= Left)
		{
			return Nodes[Root].Sum;
		}
		int Mid = (Left + Right) / 2;
		return Suffix(Nodes[Root].Left, Left, Mid, Begin) + Suffix(Nodes[Root].Right, Mid + 1, Right, Begin);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	std::vector<int> Values(N + 1);
	std::vector<int> Versions(N + 1);
	std::vector<int> Stack;
	FPersistentTree Tree;
	for (int i = 1; i <= N; ++i)
	{
		std::cin >> Values[i];
		int Root = Versions[i - 1];
		while (!Stack.empty() && Values[Stack.back()] <= Values[i])
		{
			Root = Tree.Set(Root, 1, N, Stack.back(), 0);
			Stack.pop_back();
		}
		Stack.push_back(i);
		Versions[i] = Tree.Set(Root, 1, N, i, 1);
	}
	std::uint32_t Last = 0;
	while (M--)
	{
		std::uint32_t u;
		std::uint32_t v;
		std::cin >> u >> v;
		int Left = static_cast<int>((u ^ Last) % N) + 1;
		int Right = static_cast<int>((v ^ Last) % N) + 1;
		if (Left > Right)
		{
			std::swap(Left, Right);
		}
		Last = Tree.Suffix(Versions[Right], 1, N, Left);
		std::cout << Last << '\n';
	}
}
