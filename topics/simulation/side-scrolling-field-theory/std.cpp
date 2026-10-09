// Problem setter's solution: relative direction and modular position updates.
// Codex (GPT-6): clearer fields, whitespace-safe input and reduced step lengths.
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	std::vector<int> Facing(N);
	std::vector<char> Label(N);
	for (int i = 0; i < N; ++i)
	{
		std::cin >> Facing[i] >> Label[i];
	}
	int Current = 0;
	for (int i = 0; i < M; ++i)
	{
		int d;
		long long p;
		std::cin >> d >> p;
		int Step = static_cast<int>(p % N);
		if (d != Facing[Current])
		{
			Current = (Current + Step) % N;
		}
		else
		{
			Current = (Current - Step + N) % N;
		}
		std::cout << Label[Current] << '\n';
	}
}
