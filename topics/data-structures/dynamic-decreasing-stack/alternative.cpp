// GPT-6: block decomposition alternative and implementation.
#include <algorithm>
#include <iostream>
#include <vector>
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	const int BlockSize = 224;
	int Blocks = (n + BlockSize - 1) / BlockSize;
	std::vector<int> Values(n);
	std::vector<std::vector<int>> Records(Blocks);
	for (int& Value : Values)
	{
		std::cin >> Value;
	}
	auto Rebuild = [&](int Block)
	{
		Records[Block].clear();
		int Maximum = -1;
		for (int i = std::min(n, (Block + 1) * BlockSize) - 1; i >= Block * BlockSize; --i)
		{
			if (Values[i] > Maximum)
			{
				Maximum = Values[i];
				Records[Block].push_back(Maximum);
			}
		}
	};
	for (int Block = 0; Block < Blocks; ++Block)
	{
		Rebuild(Block);
	}
	while (m--)
	{
		int Type;
		int x;
		int y;
		std::cin >> Type >> x >> y;
		--x;
		if (Type == 1)
		{
			Values[x] = y;
			Rebuild(x / BlockSize);
			continue;
		}
		--y;
		int Maximum = -1;
		int Answer = 0;
		while (y >= x)
		{
			int Block = y / BlockSize;
			if (y == std::min(n, (Block + 1) * BlockSize) - 1 && Block * BlockSize >= x)
			{
				const auto& List = Records[Block];
				Answer += static_cast<int>(List.end() - std::upper_bound(List.begin(), List.end(), Maximum));
				Maximum = std::max(Maximum, List.back());
				y = Block * BlockSize - 1;
			}
			else
			{
				if (Values[y] > Maximum)
				{
					++Answer;
					Maximum = Values[y];
				}
				--y;
			}
		}
		std::cout << Answer << '\n';
	}
}
