// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Count inversions and strict prefix minima; no quadratic simulation.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

using FVector = std::pair<int, int>;

std::int64_t SortAndCount(std::vector<FVector>& Values, std::vector<FVector>& Buffer, int Left, int Right)
{
	if (Right - Left <= 1)
	{
		return 0;
	}
	int Middle = (Left + Right) / 2;
	std::int64_t Result = SortAndCount(Values, Buffer, Left, Middle);
	Result += SortAndCount(Values, Buffer, Middle, Right);
	int a = Left;
	int b = Middle;
	int Position = Left;
	while (a < Middle && b < Right)
	{
		if (Values[b] < Values[a])
		{
			Result += Middle - a;
			Buffer[Position++] = Values[b++];
		}
		else
		{
			Buffer[Position++] = Values[a++];
		}
	}
	while (a < Middle)
	{
		Buffer[Position++] = Values[a++];
	}
	while (b < Right)
	{
		Buffer[Position++] = Values[b++];
	}
	std::copy(Buffer.begin() + Left, Buffer.begin() + Right, Values.begin() + Left);
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<FVector> Values(n);
	for (auto& Value : Values)
	{
		std::cin >> Value.first >> Value.second;
	}
	FVector Minimum = Values[0];
	int Records = 1;
	for (int i = 1; i < n; ++i)
	{
		if (Values[i] < Minimum)
		{
			Minimum = Values[i];
			++Records;
		}
	}
	std::vector<FVector> Buffer(n);
	std::int64_t Inversions = SortAndCount(Values, Buffer, 0, n);
	std::cout << 2 * Inversions + n - Records << '\n';
}
