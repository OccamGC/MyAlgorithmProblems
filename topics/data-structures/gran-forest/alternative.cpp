// Heavy-light decomposition and sorted blocks with assignment/addition tags.
// Codex (GPT-6): iterative forest traversal and explicit lazy-tag composition.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

using FInt = std::int64_t;

struct FBlock
{
	int Begin;
	int End;
	FInt Addition = 0;
	FInt Assigned = 0;
	bool bAssigned = false;
	std::vector<FInt> Sorted;
	std::vector<FInt> Prefix;
};

class FBlocks
{
	std::vector<FInt> Values;
	std::vector<FBlock> Blocks;
	int Width;

	void Rebuild(FBlock& Block)
	{
		Block.Sorted.assign(Values.begin() + Block.Begin, Values.begin() + Block.End);
		std::sort(Block.Sorted.begin(), Block.Sorted.end());
		Block.Prefix.assign(Block.Sorted.size() + 1, 0);
		for (std::size_t i = 0; i < Block.Sorted.size(); ++i)
		{
			Block.Prefix[i + 1] = Block.Prefix[i] + Block.Sorted[i];
		}
	}

	void Push(FBlock& Block)
	{
		for (int i = Block.Begin; i < Block.End; ++i)
		{
			Values[i] = Block.bAssigned ? Block.Assigned : Values[i] + Block.Addition;
		}
		Block.bAssigned = false;
		Block.Addition = 0;
	}

public:
	explicit FBlocks(std::vector<FInt> Initial) : Values(std::move(Initial))
	{
		int n = static_cast<int>(Values.size());
		Width = std::max(1, static_cast<int>(std::sqrt(n)));
		for (int l = 0; l < n; l += Width)
		{
			FBlock Block;
			Block.Begin = l;
			Block.End = std::min(n, l + Width);
			Rebuild(Block);
			Blocks.push_back(std::move(Block));
		}
	}

	FInt Operate(int Operation, int l, int r, FInt Value)
	{
		FInt Answer = 0;
		while (l <= r)
		{
			FBlock& Block = Blocks[l / Width];
			int End = std::min(r + 1, Block.End);
			bool bWhole = l == Block.Begin && End == Block.End;
			if (Operation <= 2)
			{
				if (bWhole)
				{
					if (Operation == 2)
					{
						Block.bAssigned = true;
						Block.Assigned = Value;
						Block.Addition = 0;
					}
					else if (Block.bAssigned)
					{
						Block.Assigned += Value;
					}
					else
					{
						Block.Addition += Value;
					}
				}
				else
				{
					Push(Block);
					for (int i = l; i < End; ++i)
					{
						Values[i] = Operation == 1 ? Values[i] + Value : Value;
					}
					Rebuild(Block);
				}
			}
			else if (Block.bAssigned)
			{
				if (Block.Assigned >= Value)
				{
					Answer += FInt(End - l) * (Operation == 3 ? 1 : Block.Assigned);
				}
			}
			else if (bWhole)
			{
				auto It = std::lower_bound(Block.Sorted.begin(), Block.Sorted.end(), Value - Block.Addition);
				int Position = static_cast<int>(It - Block.Sorted.begin());
				FInt Count = static_cast<int>(Block.Sorted.size()) - Position;
				Answer += Operation == 3 ? Count : Block.Prefix.back() - Block.Prefix[Position] + Count * Block.Addition;
			}
			else
			{
				for (int i = l; i < End; ++i)
				{
					FInt Current = Values[i] + Block.Addition;
					if (Current >= Value)
					{
						Answer += Operation == 3 ? 1 : Current;
					}
				}
			}
			l = End;
		}
		return Answer;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int q;
	std::cin >> n >> m >> q;
	std::vector<FInt> Initial(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Initial[i];
	}
	std::vector<std::vector<int>> Graph(n + 1);
	for (int i = 0; i < m; ++i)
	{
		int a;
		int b;
		std::cin >> a >> b;
		Graph[a].push_back(b);
		Graph[b].push_back(a);
	}
	std::vector<int> Parent(n + 1, -1);
	std::vector<int> Depth(n + 1);
	std::vector<int> Size(n + 1, 1);
	std::vector<int> Heavy(n + 1);
	std::vector<int> Top(n + 1);
	std::vector<int> Position(n + 1);
	std::vector<int> Order;
	Order.reserve(n);
	for (int Root = 1; Root <= n; ++Root)
	{
		if (Parent[Root] != -1)
		{
			continue;
		}
		Parent[Root] = 0;
		std::size_t Start = Order.size();
		Order.push_back(Root);
		for (std::size_t i = Start; i < Order.size(); ++i)
		{
			int v = Order[i];
			for (int u : Graph[v])
			{
				if (u != Parent[v])
				{
					Parent[u] = v;
					Depth[u] = Depth[v] + 1;
					Order.push_back(u);
				}
			}
		}
	}
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		int v = *It;
		int p = Parent[v];
		if (p != 0)
		{
			Size[p] += Size[v];
			if (Heavy[p] == 0 || Size[v] > Size[Heavy[p]])
			{
				Heavy[p] = v;
			}
		}
	}
	std::vector<FInt> Linear(n);
	int Index = 0;
	for (int v : Order)
	{
		if (Parent[v] != 0 && Heavy[Parent[v]] == v)
		{
			continue;
		}
		for (int u = v; u != 0; u = Heavy[u])
		{
			Top[u] = v;
			Position[u] = Index;
			Linear[Index++] = Initial[u];
		}
	}
	FBlocks Blocks(std::move(Linear));
	for (int i = 0; i < q; ++i)
	{
		int Operation;
		int a;
		int b;
		FInt Value;
		std::cin >> Operation >> a >> b >> Value;
		FInt Answer = 0;
		while (Top[a] != Top[b])
		{
			if (Depth[Top[a]] < Depth[Top[b]])
			{
				std::swap(a, b);
			}
			Answer += Blocks.Operate(Operation, Position[Top[a]], Position[a], Value);
			a = Parent[Top[a]];
		}
		Answer += Blocks.Operate(Operation, std::min(Position[a], Position[b]), std::max(Position[a], Position[b]), Value);
		if (Operation >= 3)
		{
			std::cout << Answer << '\n';
		}
	}
}
