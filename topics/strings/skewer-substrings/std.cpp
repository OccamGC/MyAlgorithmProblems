// Problem setter's task: count all starts, including overlapping occurrences.
// Codex (GPT-6): application of KMP for a linear worst-case bound per query.
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string S;
	int M;
	std::cin >> S >> M;
	while (M-- > 0)
	{
		int l;
		int r;
		std::string t;
		std::cin >> l >> r >> t;
		int Length = static_cast<int>(t.size());
		std::vector<int> Prefix(Length);
		for (int i = 1; i < Length; ++i)
		{
			int j = Prefix[i - 1];
			while (j > 0 && t[i] != t[j])
			{
				j = Prefix[j - 1];
			}
			if (t[i] == t[j])
			{
				++j;
			}
			Prefix[i] = j;
		}
		int Matched = 0;
		int Answer = 0;
		for (int i = l - 1; i < r; ++i)
		{
			while (Matched > 0 && S[i] != t[Matched])
			{
				Matched = Prefix[Matched - 1];
			}
			if (S[i] == t[Matched])
			{
				++Matched;
			}
			if (Matched == Length)
			{
				++Answer;
				Matched = Prefix[Matched - 1];
			}
		}
		std::cout << Answer << '\n';
	}
}
