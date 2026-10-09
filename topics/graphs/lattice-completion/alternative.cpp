// Codex (GPT-6): indegree peeling to isolate functional-graph cycles.

#include <iostream>
#include <queue>
#include <vector>

bool CanComplete(const std::vector<int>& Next)
{
	const int n = static_cast<int>(Next.size());
	std::vector<int> InDegree(n, 0);
	for (int Destination : Next)
	{
		++InDegree[Destination];
	}
	std::queue<int> Queue;
	for (int i = 0; i < n; ++i)
	{
		if (InDegree[i] == 0)
		{
			Queue.push(i);
		}
	}
	while (!Queue.empty())
	{
		const int Current = Queue.front();
		Queue.pop();
		if (--InDegree[Next[Current]] == 0)
		{
			Queue.push(Next[Current]);
		}
	}
	for (int i = 0; i < n; ++i)
	{
		if (InDegree[i] > 0 && Next[Next[i]] != i)
		{
			return false;
		}
	}
	return true;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		int N;
		std::cin >> N;
		std::vector<int> Next(N);
		for (int& Destination : Next)
		{
			std::cin >> Destination;
			--Destination;
		}
		std::cout << (CanComplete(Next) ? 'Y' : 'N') << '\n';
	}
}
