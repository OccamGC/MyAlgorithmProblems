// Fixed-center parity construction. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <string>

// With a fixed center, an all-equal suffix permits only even edit costs.
// Any unequal pair bridges the two parities throughout the feasible interval.
bool Feasible(int Edits, int Pairs, int Unequal)
{
	return Edits >= Unequal && Edits <= 2 * Pairs && (Unequal > 0 || Edits % 2 == 0);
}

std::string Candidate(const std::string& Text, int m, int CenterCost, int Unequal)
{
	int h = static_cast<int>(Text.size()) / 2;
	int Edits = m - CenterCost;
	if (!Feasible(Edits, h, Unequal))
	{
		return {};
	}
	std::string Half;
	Half.reserve(h + 1);
	for (int i = 0; i < h; ++i)
	{
		char a = Text[i];
		char b = Text[h + i + 1];
		Unequal -= a != b;
		for (char c = '0'; c <= '3'; ++c)
		{
			int Cost = (a != c) + (b != c);
			if (Feasible(Edits - Cost, h - i - 1, Unequal))
			{
				Half.push_back(c);
				Edits -= Cost;
				break;
			}
		}
	}
	Half.push_back(CenterCost ? (Text[h] == '0' ? '1' : '0') : Text[h]);
	return Half;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int q;
	std::cin >> q;
	while (q--)
	{
		int n;
		int m;
		std::string Text;
		std::cin >> n >> m >> Text;
		int h = n / 2;
		int Unequal = 0;
		for (int i = 0; i < h; ++i)
		{
			Unequal += Text[i] != Text[h + i + 1];
		}
		auto Keep = Candidate(Text, m, 0, Unequal);
		auto Change = Candidate(Text, m, 1, Unequal);
		if (Keep.empty() || (!Change.empty() && Change < Keep))
		{
			Keep.swap(Change);
		}
		if (Keep.empty())
		{
			std::cout << "failed\n";
		}
		else
		{
			std::cout << Keep;
			std::cout.write(Keep.data(), h);
			std::cout << '\n';
		}
	}
}
