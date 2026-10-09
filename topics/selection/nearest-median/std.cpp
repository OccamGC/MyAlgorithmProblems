// Problem setter's solution: select the middle values, then select by distance.
// Codex (GPT-6): in-place representation, explicit even median and 64-bit arithmetic.
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
	int Mid = n / 2;
	std::nth_element(Values.begin(), Values.begin() + Mid, Values.end());
	long long TwiceMedian = Values[Mid] * 2;
	if (n % 2 == 0)
	{
		TwiceMedian = Values[Mid] + *std::max_element(Values.begin(), Values.begin() + Mid);
	}
	auto Closer = [TwiceMedian](long long Left, long long Right)
	{
		long long LeftDistance = std::abs(Left * 2 - TwiceMedian);
		long long RightDistance = std::abs(Right * 2 - TwiceMedian);
		return LeftDistance != RightDistance ? LeftDistance < RightDistance : Left > Right;
	};
	if (k < n)
	{
		std::nth_element(Values.begin(), Values.begin() + k, Values.end(), Closer);
	}
	long long Sum = 0;
	for (int i = 0; i < k; ++i)
	{
		Sum += Values[i];
	}
	std::cout << Sum << '\n';
}
