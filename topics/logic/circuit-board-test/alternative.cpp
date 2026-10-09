// Direct predicate evaluation with the accompanying editorial's safe range screening.
// Codex (GPT-6): evaluate bounded integer products exactly.
#include <iostream>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		long long x;
		std::cin >> x;
		bool Accepted = false;
		if (0 < x && x <= 14)
		{
			long long Square = x * x;
			Accepted = Square * x < 3000 && Square >= 10
				&& (Square > 2000 || Square < 700);
		}
		std::cout << (Accepted ? "T\n" : "F\n");
	}
}
