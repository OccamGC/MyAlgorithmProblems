// Space-oriented companion: four-list heap streams, following Schroeppel-Shamir.
// Codex (GPT-6): weighted product adaptation, modular implementation and verification.
#define SWORDS_LIBRARY_ONLY
#include "std.cpp"
#include <queue>
#include <utility>

namespace Streaming
{
using namespace Swords;

FInt CappedProduct(FInt a, FInt b, FInt Cap)
{
	return a > (Cap - 1) / b ? Cap : a * b;
}

struct FNode
{
	FState State;
	int Row;
	int Column;
};

struct FCompare
{
	bool bIncreasing;
	bool operator()(const FNode& a, const FNode& b) const
	{
		return bIncreasing ? b.State.Product < a.State.Product : a.State.Product < b.State.Product;
	}
};

class FProductStream
{
	const std::vector<FState>& Rows;
	const std::vector<FState>& Columns;
	FInt Cap;
	bool bIncreasing;
	std::priority_queue<FNode, std::vector<FNode>, FCompare> Heap;

	FNode MakeNode(int Row, int Column) const
	{
		const auto& a = Rows[Row];
		const auto& b = Columns[Column];
		return {{CappedProduct(a.Product, b.Product, Cap),
			static_cast<int>(static_cast<FInt>(a.Probability) * b.Probability % Mod)}, Row, Column};
	}

public:
	FProductStream(const std::vector<FState>& InRows, const std::vector<FState>& InColumns,
		FInt InCap, bool bInIncreasing)
		: Rows(InRows), Columns(InColumns), Cap(InCap), bIncreasing(bInIncreasing), Heap(FCompare{bIncreasing})
	{
		std::vector<FNode> Nodes;
		Nodes.reserve(Rows.size());
		const int FirstColumn = bIncreasing ? 0 : static_cast<int>(Columns.size()) - 1;
		for (int Row = 0; Row < static_cast<int>(Rows.size()); ++Row)
		{
			Nodes.push_back(MakeNode(Row, FirstColumn));
		}
		Heap = decltype(Heap)(FCompare{bIncreasing}, std::move(Nodes));
	}

	bool HasNext() const
	{
		return !Heap.empty();
	}

	const FState& Peek() const
	{
		return Heap.top().State;
	}

	FState Take()
	{
		const FNode Node = Heap.top();
		Heap.pop();
		const int Next = Node.Column + (bIncreasing ? 1 : -1);
		if (Next >= 0 && Next < static_cast<int>(Columns.size()))
		{
			Heap.push(MakeNode(Node.Row, Next));
		}
		return Node.State;
	}
};

std::vector<int> SolveStreaming(const std::vector<FSword>& Items, const std::vector<FInt>& Thresholds)
{
	if (UseDp(Items.size(), Thresholds))
	{
		return Solve(Items, Thresholds);
	}
	int Scale;
	const auto Odds = PrepareOdds(Items, Scale);
	const int n = static_cast<int>(Items.size());
	const int Middle = n / 2;
	const FInt Cap = *std::max_element(Thresholds.begin(), Thresholds.end());
	const auto A = BuildSorted(Odds, 0, Middle / 2, Cap);
	const auto B = BuildSorted(Odds, Middle / 2, Middle, Cap);
	const auto C = BuildSorted(Odds, Middle, Middle + (n - Middle) / 2, Cap);
	const auto D = BuildSorted(Odds, Middle + (n - Middle) / 2, n, Cap);
	std::vector<int> Answers;
	for (FInt K : Thresholds)
	{
		if (K == 1)
		{
			Answers.push_back(1);
			continue;
		}
		FProductStream Left(A, B, Cap, true);
		FProductStream Right(C, D, Cap, false);
		int Prefix = static_cast<FInt>(TotalWeight(C)) * TotalWeight(D) % Mod;
		int Answer = 0;
		while (Left.HasNext())
		{
			const auto State = Left.Take();
			if (State.Product >= K)
			{
				break;
			}
			const FInt Limit = (K - 1) / State.Product;
			while (Right.HasNext() && Right.Peek().Product > Limit)
			{
				Prefix -= Right.Take().Probability;
				if (Prefix < 0)
				{
					Prefix += Mod;
				}
			}
			Answer = (Answer + static_cast<FInt>(State.Probability) * Prefix) % Mod;
		}
		Answers.push_back((1 - static_cast<FInt>(Answer) * Scale % Mod + Mod) % Mod);
	}
	return Answers;
}
}

int main()
{
	return Swords::Run(Streaming::SolveStreaming);
}
