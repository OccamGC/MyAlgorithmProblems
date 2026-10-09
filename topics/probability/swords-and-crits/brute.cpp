// Independent small-instance enumeration, without deterministic preprocessing or odds.
// Codex (GPT-6). Intended for n <= 22, not for the full data.
#define SWORDS_LIBRARY_ONLY
#include "std.cpp"

void Enumerate(int Index, Swords::FInt Product, int Weight,
	const std::vector<Swords::FSword>& Items, const std::vector<Swords::FInt>& Thresholds,
	Swords::FInt Cap, std::vector<int>& Answers)
{
	using namespace Swords;
	if (Index == static_cast<int>(Items.size()))
	{
		for (std::size_t j = 0; j < Thresholds.size(); ++j)
		{
			if (!(Product < Thresholds[j]))
			{
				Answers[j] += Weight;
				if (Answers[j] >= Mod)
				{
					Answers[j] -= Mod;
				}
			}
		}
		return;
	}
	const auto Item = Items[Index];
	Enumerate(Index + 1, Product, static_cast<FInt>(Weight) * (ProbabilityScale - Item.Probability) % Mod,
		Items, Thresholds, Cap, Answers);
	const FInt Triggered = Product > (Cap / Item.Multiplier) ? Cap : Product * Item.Multiplier;
	Enumerate(Index + 1, Triggered, static_cast<FInt>(Weight) * Item.Probability % Mod,
		Items, Thresholds, Cap, Answers);
}

int main()
{
	using namespace Swords;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int TestCount;
	std::cin >> TestCount;
	while (TestCount-- > 0)
	{
		int n;
		int q;
		std::cin >> n >> q;
		if (n > 22)
		{
			return 2;
		}
		std::vector<FSword> Items(n);
		for (auto& Item : Items)
		{
			std::cin >> Item.Probability >> Item.Multiplier;
		}
		std::vector<FInt> Thresholds(q);
		for (auto& K : Thresholds)
		{
			std::cin >> K;
		}
		std::vector<int> Answers(q, 0);
		Enumerate(0, 1, 1, Items, Thresholds, *std::max_element(Thresholds.begin(), Thresholds.end()), Answers);
		const int Scale = Power(Power(ProbabilityScale, Mod - 2), n);
		for (int Answer : Answers)
		{
			std::cout << static_cast<FInt>(Answer) * Scale % Mod << '\n';
		}
	}
}
