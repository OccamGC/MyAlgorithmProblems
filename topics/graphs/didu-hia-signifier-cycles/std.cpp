// Problem setter's solution: follow each path and mark its active stack.
// Codex (GPT-6): repair the input helper, port to C++17 and validate empty graphs.

#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Next(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Next[i];
	}
	int Answer = 0;

	std::vector<bool> Visited(n + 1, false);
	std::vector<int> Position(n + 1, -1);
	std::vector<int> Path;
	for (int Start = 1; Start <= n; ++Start)
	{
		if (Visited[Start])
		{
			continue;
		}
		int Vertex = Start;
		while (!Visited[Vertex])
		{
			Visited[Vertex] = true;
			Position[Vertex] = static_cast<int>(Path.size());
			Path.push_back(Vertex);
			Vertex = Next[Vertex];
		}
		if (Position[Vertex] >= 0)
		{
			Answer += static_cast<int>(Path.size()) - Position[Vertex];
		}
		for (int Item : Path)
		{
			Position[Item] = -1;
		}
		Path.clear();
	}
	std::cout << Answer << '\n';
}
