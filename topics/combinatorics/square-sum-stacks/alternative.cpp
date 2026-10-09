#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<std::vector<int>> Columns(n);
	int Size = n;
	int Start = 0;
	int Next = (n + 1) * (n + 1) / 2 - 1;
	if (Size % 2 == 0)
	{
		for (int i = 0; i < Size; ++i)
		{
			Columns[i].push_back(Next--);
		}
		--Size;
	}
	while (Size > 1)
	{
		for (int i = Start + Size - 1; i >= Start; --i)
		{
			Columns[i].push_back(Next--);
		}
		for (int i = Start; i < Start + Size; ++i)
		{
			Columns[i].push_back(Next--);
		}
		++Start;
		Size -= 2;
	}
	Columns[Start].push_back(1);
	for (const auto& Column : Columns)
	{
		for (int i = 0; i < static_cast<int>(Column.size()); ++i)
		{
			if (i > 0)
			{
				std::cout << ' ';
			}
			std::cout << Column[i];
		}
		std::cout << '\n';
	}
}
