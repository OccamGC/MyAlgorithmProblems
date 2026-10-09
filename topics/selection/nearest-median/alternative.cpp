// Codex (GPT-6): sorting and merging the two distance-ordered sides of the median.
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int k;
	std::cin >> n >> k;
	std::vector<long long> Values(n);
	for (long long& Value : Values)
	{
		std::cin >> Value;
	}
	std::sort(Values.begin(), Values.end());
	long long TwiceMedian = Values[(n - 1) / 2] + Values[n / 2];
	int Left = n / 2 - 1;
	int Right = n / 2;
	long long Sum = 0;
	while (k--)
	{
		bool bTakeRight = Left < 0 || (Right < n &&
			std::abs(Values[Right] * 2 - TwiceMedian) <= std::abs(Values[Left] * 2 - TwiceMedian));
		Sum += bTakeRight ? Values[Right++] : Values[Left--];
	}
	std::cout << Sum << '\n';
}
