// Fenwick tree of dynamic segment trees. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <vector>

struct FCharacter
{
	std::array<int, 3> Requirement;
	std::array<int, 3> Attribute;
};

struct FNode
{
	int Left = 0;
	int Right = 0;
	int Minimum = 2000000000;
	int Head = 0;
};

struct FEntry
{
	int Id;
	int Next;
};

struct FRangeForest
{
	std::vector<FNode> Nodes{FNode{}};
	std::vector<FEntry> Entries{FEntry{}};
	const std::vector<FCharacter>& Characters;

	int Insert(int Node, int l, int r, int Position, int Id)
	{
		if (Node == 0)
		{
			Node = static_cast<int>(Nodes.size());
			Nodes.emplace_back();
		}
		Nodes[Node].Minimum = std::min(Nodes[Node].Minimum, Characters[Id].Requirement[2]);
		if (l == r)
		{
			Entries.push_back({Id, Nodes[Node].Head});
			Nodes[Node].Head = static_cast<int>(Entries.size()) - 1;
		}
		else
		{
			int Mid = (l + r) / 2;
			if (Position <= Mid)
			{
				Nodes[Node].Left = Insert(Nodes[Node].Left, l, Mid, Position, Id);
			}
			else
			{
				Nodes[Node].Right = Insert(Nodes[Node].Right, Mid + 1, r, Position, Id);
			}
		}
		return Node;
	}

	void Report(int Node, int l, int r, int Bound, int Limit, std::vector<char>& Seen,
		std::vector<int>& Queue)
	{
		if (!Node || l > Bound || Nodes[Node].Minimum > Limit)
		{
			return;
		}
		FNode& Current = Nodes[Node];
		if (l == r)
		{
			while (Current.Head && Characters[Entries[Current.Head].Id].Requirement[2] <= Limit)
			{
				const FEntry& Entry = Entries[Current.Head];
				if (!Seen[Entry.Id])
				{
					Seen[Entry.Id] = true;
					Queue.push_back(Entry.Id);
				}
				Current.Head = Entry.Next;
			}
			Current.Minimum = Current.Head ? Characters[Entries[Current.Head].Id].Requirement[2] : Nodes[0].Minimum;
			return;
		}
		int Mid = (l + r) / 2;
		Report(Current.Left, l, Mid, Bound, Limit, Seen, Queue);
		Report(Current.Right, Mid + 1, r, Bound, Limit, Seen, Queue);
		Current.Minimum = std::min(Nodes[Current.Left].Minimum, Nodes[Current.Right].Minimum);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<FCharacter> Characters(n + 1);
	for (int& Value : Characters[0].Attribute)
	{
		std::cin >> Value;
	}
	for (int i = 1; i <= n; ++i)
	{
		for (int& Value : Characters[i].Requirement)
		{
			std::cin >> Value;
		}
		for (int& Value : Characters[i].Attribute)
		{
			std::cin >> Value;
		}
	}
	std::array<std::vector<int>, 2> Coordinates;
	for (int j = 0; j < 2; ++j)
	{
		auto& Axis = Coordinates[j];
		for (int i = 1; i <= n; ++i)
		{
			Axis.push_back(Characters[i].Requirement[j]);
		}
		std::sort(Axis.begin(), Axis.end());
		Axis.erase(std::unique(Axis.begin(), Axis.end()), Axis.end());
	}
	std::vector<int> Order(n);
	std::iota(Order.begin(), Order.end(), 1);
	std::sort(Order.begin(), Order.end(), [&](int a, int b)
	{
		return Characters[a].Requirement[2] > Characters[b].Requirement[2];
	});
	FRangeForest Forest{{FNode{}}, {FEntry{}}, Characters};
	int Height = static_cast<int>(Coordinates[1].size());
	std::vector<int> Root(Coordinates[0].size() + 1);
	for (int Id : Order)
	{
		const auto& Req = Characters[Id].Requirement;
		int x = std::lower_bound(Coordinates[0].begin(), Coordinates[0].end(), Req[0]) - Coordinates[0].begin() + 1;
		int y = std::lower_bound(Coordinates[1].begin(), Coordinates[1].end(), Req[1]) - Coordinates[1].begin();
		for (; x < static_cast<int>(Root.size()); x += x & -x)
		{
			Root[x] = Forest.Insert(Root[x], 0, Height - 1, y, Id);
		}
	}
	std::vector<int> Queue{0};
	std::vector<char> Seen(n + 1);
	for (std::size_t i = 0; i < Queue.size(); ++i)
	{
		const auto& Attr = Characters[Queue[i]].Attribute;
		int x = std::upper_bound(Coordinates[0].begin(), Coordinates[0].end(), Attr[0]) - Coordinates[0].begin();
		int y = std::upper_bound(Coordinates[1].begin(), Coordinates[1].end(), Attr[1]) - Coordinates[1].begin() - 1;
		for (; x > 0; x -= x & -x)
		{
			Forest.Report(Root[x], 0, Height - 1, y, Attr[2], Seen, Queue);
		}
	}
	std::cout << Queue.size() - 1 << '\n';
}
