#include <array>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct FNode
{
	std::array<int, 2> Next{{-1, -1}};
	int Fail = 0;
	bool bTerminal = false;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int n;
	std::string Text;
	if (!(std::cin >> n >> Text))
	{
		return 0;
	}

	std::vector<FNode> Trie(1);
	for (int i = 0; i < n; ++i)
	{
		std::string Pattern;
		std::cin >> Pattern;
		int State = 0;
		for (char Digit : Pattern)
		{
			const int Bit = Digit - '0';
			if (Trie[State].Next[Bit] == -1)
			{
				Trie[State].Next[Bit] = static_cast<int>(Trie.size());
				Trie.emplace_back();
			}
			State = Trie[State].Next[Bit];
		}
		Trie[State].bTerminal = true;
	}

	std::queue<int> Bfs;
	for (int Bit = 0; Bit < 2; ++Bit)
	{
		int Child = Trie[0].Next[Bit];
		if (Child == -1)
		{
			Trie[0].Next[Bit] = 0;
		}
		else
		{
			Bfs.push(Child);
		}
	}
	while (!Bfs.empty())
	{
		int State = Bfs.front();
		Bfs.pop();
		Trie[State].bTerminal = Trie[State].bTerminal || Trie[Trie[State].Fail].bTerminal;
		for (int Bit = 0; Bit < 2; ++Bit)
		{
			int Child = Trie[State].Next[Bit];
			if (Child == -1)
			{
				Trie[State].Next[Bit] = Trie[Trie[State].Fail].Next[Bit];
			}
			else
			{
				Trie[Child].Fail = Trie[Trie[State].Fail].Next[Bit];
				Bfs.push(Child);
			}
		}
	}

	int Answer = 0;
	int State = 0;
	for (char Digit : Text)
	{
		State = Trie[State].Next[Digit - '0'];
		if (Trie[State].bTerminal)
		{
			++Answer;
			State = 0;
		}
	}
	std::cout << Answer << '\n';
}
