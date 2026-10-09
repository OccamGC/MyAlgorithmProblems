// Problem setter's alternative: align depths, then ascend together.
// Codex (GPT-6): portable integer depth computation and proof.
#include <iostream>
#include <utility>

int Depth(unsigned long long Label)
{
	int Result = 0;
	while (Label > 1)
	{
		Label /= 2;
		++Result;
	}
	return Result;
}

int Distance(unsigned long long a, unsigned long long b)
{
	int DepthA = Depth(a);
	int DepthB = Depth(b);
	if (DepthA < DepthB)
	{
		std::swap(a, b);
		std::swap(DepthA, DepthB);
	}
	int Answer = DepthA - DepthB;
	while (DepthA > DepthB)
	{
		a /= 2;
		--DepthA;
	}
	while (a != b)
	{
		a /= 2;
		b /= 2;
		Answer += 2;
	}
	return Answer;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int m;
	std::cin >> m;
	for (int i = 1; i <= m; ++i)
	{
		unsigned long long a;
		unsigned long long b;
		std::cin >> a >> b;
		std::cout << "Case #" << i << ": " << Distance(a, b) << '\n';
	}
}
