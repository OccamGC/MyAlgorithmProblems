// Problem setter's modeling: stack matching into a nesting forest.
// Codex (GPT-6): maximum matching on its incomparability graph, summarized
// by subtree size and matching deficiency, with proof and streaming implementation.
// The setter's longest-stem greedy has a counterexample documented in the solution.
#include <algorithm>
#include <vector>
#include "buffered-input.hpp"

struct FFrame
{
	int Total = 0;
	int MaximumTerm = 0;
};
int main()
{
	FInput Input;
	int n = Input.Read();
	std::vector<FFrame> Stack;
	Stack.reserve(n + 1);
	Stack.push_back({0, 0});
	for (int i = 0; i < n; ++i)
	{
		int c = Input.NonSpace();
		if (c == '1')
		{
			Stack.push_back({0, 0});
		}
		else if (Stack.size() > 1)
		{
			FFrame Children = Stack.back();
			Stack.pop_back();
			int Size = Children.Total + 1;
			int Deficiency = 1 + std::max(Children.Total % 2, Children.MaximumTerm - Children.Total);
			Stack.back().Total += Size;
			Stack.back().MaximumTerm = std::max(Stack.back().MaximumTerm, Size + Deficiency);
		}
	}
	while (Stack.size() > 1)
	{
		FFrame Children = Stack.back();
		Stack.pop_back();
		Stack.back().Total += Children.Total;
		Stack.back().MaximumTerm = std::max(Stack.back().MaximumTerm, Children.MaximumTerm);
	}
	FFrame Forest = Stack.back();
	int Deficiency = std::max(Forest.Total % 2, Forest.MaximumTerm - Forest.Total);
	std::printf("%d\n", (Forest.Total - Deficiency) / 2);
}
