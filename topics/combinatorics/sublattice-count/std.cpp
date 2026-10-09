// Problem setter's solution: search with forced membership and rollback.
// Codex (GPT-6): zero-based C++17 implementation and invariants.

#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int MaximumSize = 22;
int n;
std::array<std::array<int, MaximumSize>, MaximumSize> Operation{};

std::array<int, MaximumSize> Selected{};

int Search(int Position)
{
	if (Position == n)
	{
		return 1;
	}
	int Answer = 0;
	if (Selected[Position] == 0)
	{
		Answer += Search(Position + 1);
	}
	for (int j = 0; j < n; ++j)
	{
		if (Selected[j] != 0)
		{
			const int First = Operation[Position][j];
			const int Second = Operation[j][Position];
			if ((First < Position && Selected[First] == 0) ||
				(Second < Position && Selected[Second] == 0))
			{
				return Answer;
			}
		}
	}
	const int Stamp = Position + 1;
	for (int j = 0; j < n; ++j)
	{
		if (Selected[j] != 0)
		{
			const int First = Operation[Position][j];
			const int Second = Operation[j][Position];
			if (Selected[First] == 0)
			{
				Selected[First] = Stamp;
			}
			if (Selected[Second] == 0)
			{
				Selected[Second] = Stamp;
			}
		}
	}
	if (Selected[Position] == 0)
	{
		Selected[Position] = Stamp;
	}
	Answer += Search(Position + 1);
	for (int j = 0; j < n; ++j)
	{
		if (Selected[j] == Stamp)
		{
			Selected[j] = 0;
		}
	}
	return Answer;
}


int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::cin >> n;
	for (int i = 0; i < n; ++i)
	{
		for (int j = 0; j < n; ++j)
		{
			std::cin >> Operation[i][j];
			--Operation[i][j];
		}
	}
	std::cout << Search(0) - 1 << '\n';
}
