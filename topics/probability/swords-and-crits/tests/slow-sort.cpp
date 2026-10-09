// Correct comparison witness: quotient DP + O(n * 2^(n/2)) comparison sorting.
#define SWORDS_LIBRARY_ONLY
#include "../std.cpp"

std::vector<Swords::FState> BuildUnsorted(const std::vector<Swords::FSword>& Items,
	int Begin, int End, Swords::FInt K)
{
	using namespace Swords;
	std::vector<FState> States;
	States.reserve(std::size_t{1} << (End - Begin));
	States.push_back({1, 1});
	for (int i = Begin; i < End; ++i)
	{
		const std::size_t Count = States.size();
		const int p = Items[i].Probability;
		const FInt m = Items[i].Multiplier;
		const FInt SafeLimit = (K - 1) / m;
		for (std::size_t j = 0; j < Count; ++j)
		{
			const auto State = States[j];
			if (State.Product <= SafeLimit)
			{
				States.push_back({State.Product * m,
					static_cast<int>(static_cast<FInt>(State.Probability) * p % Mod)});
			}
		}
	}
	std::sort(States.begin(), States.end(), [](const FState& a, const FState& b)
	{
		return a.Product < b.Product;
	});
	return States;
}

std::vector<int> SolveSlowSort(const std::vector<Swords::FSword>& Items,
	const std::vector<Swords::FInt>& Thresholds)
{
	using namespace Swords;
	if (UseDp(Items.size(), Thresholds))
	{
		return Solve(Items, Thresholds);
	}
	const FInt Cap = *std::max_element(Thresholds.begin(), Thresholds.end());
	const int Middle = static_cast<int>(Items.size()) / 2;
	int Scale;
	const auto Odds = PrepareOdds(Items, Scale);
	auto Left = BuildUnsorted(Odds, 0, Middle, Cap);
	MakePrefix(Left);
	auto Right = BuildUnsorted(Odds, Middle, static_cast<int>(Items.size()), Cap);
	MakePrefix(Right);
	std::vector<int> Answers;
	for (FInt K : Thresholds)
	{
		Answers.push_back(K == 1 ? 1 : (1 - static_cast<FInt>(JoinLinear(Left, Right, K)) * Scale % Mod + Mod) % Mod);
	}
	return Answers;
}

int main()
{
	return Swords::Run(SolveSlowSort);
}
