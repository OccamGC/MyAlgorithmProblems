// Suffix automaton with end-position occurrence counts.
// GPT-6: adaptation to distinct/unique sampling, implementation and verification.
#include <array>
#include <string>
#include <vector>
#include "expectation.hpp"
struct FState
{
	std::array<int, 94> Next{};
	int Link = -1;
	int Length = 0;
	int Occurrences = 0;
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int Q;
	std::string Text;
	std::cin >> n >> Q >> Text;
	std::vector<FState> States;
	States.reserve(2 * n);
	States.emplace_back();
	int Last = 0;
	for (unsigned char Character : Text)
	{
		int Symbol = Character - 33;
		int Current = static_cast<int>(States.size());
		States.emplace_back();
		States[Current].Length = States[Last].Length + 1;
		States[Current].Occurrences = 1;
		int p = Last;
		while (p >= 0 && States[p].Next[Symbol] == 0)
		{
			States[p].Next[Symbol] = Current;
			p = States[p].Link;
		}
		if (p == -1)
		{
			States[Current].Link = 0;
		}
		else
		{
			int q = States[p].Next[Symbol];
			if (States[p].Length + 1 == States[q].Length)
			{
				States[Current].Link = q;
			}
			else
			{
				int Clone = static_cast<int>(States.size());
				States.push_back(States[q]);
				States[Clone].Length = States[p].Length + 1;
				States[Clone].Occurrences = 0;
				while (p >= 0 && States[p].Next[Symbol] == q)
				{
					States[p].Next[Symbol] = Clone;
					p = States[p].Link;
				}
				States[q].Link = Clone;
				States[Current].Link = Clone;
			}
		}
		Last = Current;
	}
	std::vector<int> Count(n + 1);
	std::vector<int> Order(States.size());
	for (const FState& State : States)
	{
		++Count[State.Length];
	}
	for (int i = 1; i <= n; ++i)
	{
		Count[i] += Count[i - 1];
	}
	for (int i = 0; i < static_cast<int>(States.size()); ++i)
	{
		Order[--Count[States[i].Length]] = i;
	}
	for (int i = static_cast<int>(Order.size()) - 1; i > 0; --i)
	{
		int u = Order[i];
		States[States[u].Link].Occurrences += States[u].Occurrences;
	}
	FInt Distinct = 0;
	FInt Unique = 0;
	for (int i = 1; i < static_cast<int>(States.size()); ++i)
	{
		int Contribution = States[i].Length - States[States[i].Link].Length;
		Distinct += Contribution;
		if (States[i].Occurrences == 1)
		{
			Unique += Contribution;
		}
	}
	AnswerQueries(Distinct, Unique, Q);
}
