#include <iostream>
#include <string>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int q;
	std::cin >> q;
	while (q--)
	{
		int n;
		int m;
		std::string Text;
		std::cin >> n >> m >> Text;
		int Half = n / 2;
		int Different = 0;
		for (int i = 0; i < Half; ++i)
		{
			Different += Text[i] != Text[i + Half + 1];
		}
		if (m < Different)
		{
			std::cout << "failed\n";
			continue;
		}
		for (int i = 0; i < Half; ++i)
		{
			char Left = Text[i];
			char Right = Text[i + Half + 1];
			Different -= Left != Right;
			int Maximum = 2 * (Half - i - 1) + 1;
			for (char Value = '0'; Value <= '3'; ++Value)
			{
				int Cost = (Value != Left) + (Value != Right);
				if (Different <= m - Cost && m - Cost <= Maximum)
				{
					Text[i] = Value;
					Text[i + Half + 1] = Value;
					m -= Cost;
					break;
				}
			}
		}
		if (m == 1)
		{
			Text[Half] = Text[Half] == '0' ? '1' : '0';
		}
		std::cout << Text << '\n';
	}
}
