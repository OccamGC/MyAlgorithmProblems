// Problem setter's solution: recursively remove the last element.
// Codex (GPT-6): portable implementation and boundary proof.

#include <algorithm>
#include <iostream>
#include <vector>

int FindMaximum(const std::vector<int>& Values, int Left, int Right)
{
	if (Right - Left == 1)
	{
		return Values[Left];
	}
	return std::max(FindMaximum(Values, Left, Right - 1), Values[Right - 1]);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Values(n);
	for (int& Value : Values)
	{
		std::cin >> Value;
	}
	std::cout << FindMaximum(Values, 0, n) << '\n';
}
