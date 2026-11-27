// Full materialization. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string Text;
	int q;
	std::cin >> Text >> q;
	std::vector<int> Versions(q);
	int Last = 1;
	for (int& Version : Versions)
	{
		std::cin >> Version;
		Last = std::max(Last, Version);
	}
	std::vector<std::size_t> Length(Last + 1);
	Length[1] = Text.size();
	for (int v = 2; v <= Last; ++v)
	{
		Length[v] = Length[v - 1] + (Length[v - 1] + 4) / 5;
	}
	Text.reserve(Length.back());
	for (int v = 2; v <= Last; ++v)
	{
		Text.append(Text, 0, Length[v] - Length[v - 1]);
	}
	for (int v : Versions)
	{
		std::cout.write(Text.data(), Length[v]);
		std::cout << '\n';
	}
}
