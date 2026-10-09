// Codex (GPT-6): balanced recursive decomposition with logarithmic call depth.

#include <algorithm>
#include <iostream>
#include <vector>

int FindMaximum(const std::vector<int>& Values, int Left, int Right)
{
	if (Right - Left == 1)
	{
		return Values[Left];
	}
	const int Middle = Left + (Right - Left) / 2;
	const int LeftMaximum = FindMaximum(Values, Left, Middle);
	const int RightMaximum = FindMaximum(Values, Middle, Right);
	return std::max(LeftMaximum, RightMaximum);
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
