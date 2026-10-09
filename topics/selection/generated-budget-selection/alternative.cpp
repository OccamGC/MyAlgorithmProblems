// Codex (GPT-6): sorting baseline with deterministic O(n log n) time.
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

	std::sort(Values.begin(), Values.end());
	for (int Value : Values)
	{
		if (Value > L)
		{
			break;
		}
		L -= Value;
		++Answer;
	}

	std::cout << Answer << '\n';
}
