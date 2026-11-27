// Shrinking-strip. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

int main()
{
	int n;
	int m;
	int k;
	std::cin >> n >> m >> k;
	std::vector<std::pair<int, int>> Buildings(k);
	std::vector<int> Rows{0, n + 1};
	std::vector<int> Columns{0, m + 1};
	for (auto& [x, y] : Buildings)
	{
		std::cin >> x >> y;
		Rows.push_back(x);
		Columns.push_back(y);
	}
	for (auto* Coordinates : {&Rows, &Columns})
	{
		std::sort(Coordinates->begin(), Coordinates->end());
		Coordinates->erase(std::unique(Coordinates->begin(), Coordinates->end()), Coordinates->end());
	}
	std::vector<std::vector<int>> InColumn(Columns.size());
	for (auto [x, y] : Buildings)
	{
		int Row = std::lower_bound(Rows.begin(), Rows.end(), x) - Rows.begin();
		int Column = std::lower_bound(Columns.begin(), Columns.end(), y) - Columns.begin();
		InColumn[Column].push_back(Row);
	}
	int Answer = 0;
	const int LastColumn = static_cast<int>(Columns.size()) - 1;
	for (int l = 0; l < LastColumn; ++l)
	{
		std::vector<int> Count(Rows.size());
		for (int r = l + 1; r < LastColumn; ++r)
		{
			for (int Row : InColumn[r])
			{
				++Count[Row];
			}
		}
		std::vector<int> PrevRow(Rows.size());
		std::vector<int> NextRow(Rows.size());
		int Previous = 0;
		int Gap = 0;
		for (int i = 1; i < static_cast<int>(Rows.size()); ++i)
		{
			if (Count[i] > 0 || i + 1 == static_cast<int>(Rows.size()))
			{
				NextRow[Previous] = i;
				PrevRow[i] = Previous;
				Gap = std::max(Gap, Rows[i] - Rows[Previous] - 1);
				Previous = i;
			}
		}
		for (int r = LastColumn; r > l; --r)
		{
			for (int Row : InColumn[r])
			{
				if (--Count[Row] == 0)
				{
					NextRow[PrevRow[Row]] = NextRow[Row];
					PrevRow[NextRow[Row]] = PrevRow[Row];
					Gap = std::max(Gap, Rows[NextRow[Row]] - Rows[PrevRow[Row]] - 1);
				}
			}
			Answer = std::max(Answer, std::min(Gap, Columns[r] - Columns[l] - 1));
		}
	}
	std::cout << Answer << '\n';
}
