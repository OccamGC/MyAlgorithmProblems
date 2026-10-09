// Problem setter's solution: extract the interval and repeatedly use string::find.
// Codex (GPT-6): portable formatting; advance one position to retain overlaps.
#include <iostream>
#include <string>

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
		std::string Interval = S.substr(l - 1, r - l + 1);
		std::size_t Position = 0;
		int Answer = 0;
		while ((Position = Interval.find(t, Position)) != std::string::npos)
		{
			++Answer;
			++Position;
		}
		std::cout << Answer << '\n';
	}
}
