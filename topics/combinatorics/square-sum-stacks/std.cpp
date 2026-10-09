#include <iostream>

int Capacity(int n)
{
	return (n + 1) * (n + 1) / 2 - 1;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	for (int Column = 0; Column < n; ++Column)
	{
		int Size = n;
		int Position = Column;
		if (n % 2 == 0)
		{
			std::cout << Capacity(n) - Column;
			if (Column == n - 1)
			{
				std::cout << '\n';
				continue;
			}
			std::cout << ' ';
			--Size;
		}
		while (Size > 1)
		{
			int Top = Capacity(Size) - Size + 1 + Position;
			int Below = Capacity(Size) - Size - Position;
			std::cout << Top << ' ' << Below;
			if (Position == 0 || Position == Size - 1)
			{
				break;
			}
			std::cout << ' ';
			--Position;
			Size -= 2;
		}
		if (Size == 1)
		{
			std::cout << 1;
		}
		std::cout << '\n';
	}
}
