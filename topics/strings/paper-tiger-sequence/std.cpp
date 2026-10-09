// Problem setter's suffix-sharing algorithm; dynamic version bounds and C++17 organization by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string Initial;
	int n, m;
	std::cin >> Initial >> n >> m;
	std::vector<int> Length(n + 1), Position(n);
	Length[0] = static_cast<int>(Initial.size());
	for (int i = 0; i < n; ++i)
	{
		std::cin >> Position[i];
		Length[i + 1] = Length[i] + (Length[i] + 4) / 5;
	}
	std::vector<char> Text(Length[n]);
	int Start = Length[n] - Length[0];
	std::copy(Initial.begin(), Initial.end(), Text.begin() + Start);
	for (int i = 0; i < n; ++i)
	{
		int Added = Length[i + 1] - Length[i];
		for (int j = 0; j < Added; ++j)
		{
			Text[Start - Added + j] = Text[Start + (Position[i] + j) % Length[i]];
		}
		Start -= Added;
	}
	for (int i = 0; i < m; ++i)
	{
		int Version;
		std::cin >> Version;
		std::cout.write(Text.data() + Length[n] - Length[Version], Length[Version]);
		std::cout << '\n';
	}
}
