// Problem setter's solution: take nonpositive values, then partition positive values by a pivot. Codex (GPT-6): full-size allocation, three-way partition and 64-bit safe recurrence.
#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	long long A;
	long long B;
	long long C;
	long long Mod;
	long long L;
	std::cin >> n >> A >> B >> C >> Mod >> L;
	std::vector<int> Values;
	Values.reserve(n);
	int Answer = 0;
	for (int i = 0; i < n; ++i)
	{
		A = C + (A * B) % Mod;
		if (A <= 0)
		{
			L -= A;
			++Answer;
		}
		else
		{
			Values.push_back(static_cast<int>(A));
		}
	}
	if (L < 0)
	{
		std::cout << "0\n";
		return 0;
	}

	std::mt19937 Random(20261001);
	int Left = 0;
	int Right = static_cast<int>(Values.size());
	while (Left < Right)
	{
		int Pivot = Values[std::uniform_int_distribution<int>(Left, Right - 1)(Random)];
		int Less = Left;
		int Scan = Left;
		int Greater = Right;
		long long Sum = 0;
		while (Scan < Greater)
		{
			if (Values[Scan] < Pivot)
			{
				Sum += Values[Scan];
				std::swap(Values[Scan++], Values[Less++]);
			}
			else if (Values[Scan] > Pivot)
			{
				std::swap(Values[Scan], Values[--Greater]);
			}
			else
			{
				++Scan;
			}
		}
		if (Sum > L)
		{
			Right = Less;
			continue;
		}
		Answer += Less - Left;
		L -= Sum;
		long long Take = std::min<long long>(Greater - Less, L / Pivot);
		Answer += static_cast<int>(Take);
		L -= Take * Pivot;
		if (Take < Greater - Less)
		{
			break;
		}
		Left = Greater;
	}

	std::cout << Answer << '\n';
}
