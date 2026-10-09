// Problem setter's solution: precomputed answers for the fixed domain.
// Codex (GPT-6): portable implementation and independently verified table.
// alternative.cpp reproduces this table by inclusion-exclusion.
#include <cstdio>

int main()
{
	constexpr int Answer[] =
	{
		1, 1, 5, 230, 38154, 23837323, 867090702,
		313119612, 923973197, 462403141, 840792457,
		982585751, 463056058, 199254391, 8125702,
		241056829, 669505845, 625652964, 167694588,
		415136241, 104359615
	};
	for (int Value : Answer)
	{
		std::printf("%d\n", Value);
	}
}
