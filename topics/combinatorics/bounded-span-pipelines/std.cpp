// Codex (GPT-6): reduce realizable straight pipes to a laminar matching,
// then combine a prefix DP with rolling short-interval tables.
#include <algorithm>
#include <cstdio>
#include <vector>

constexpr int Mod = 998244353;
int main()
{
	int n;
	int k;
	int m;
	std::scanf("%d%d%d", &n, &k, &m);
	std::vector<int> Partner(n + 1);
	std::vector<int> Weight(n + 1);
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		int e;
		std::scanf("%d%d%d", &u, &v, &e);
		Partner[u] = v;
		Partner[v] = u;
		Weight[u] = Weight[v] = e == 1 ? 1 : 2;
	}
	int Short[20][20] = {};
	for (int i = 0; i < 20; ++i)
	{
		Short[i][0] = 1;
	}
	std::vector<int> Prefix(n + 1);
	Prefix[0] = 1;
	for (int r = 1; r <= n; ++r)
	{
		int Row = r % 20;
		for (int Length = 1; Length < k && Length <= r; ++Length)
		{
			int l = r - Length + 1;
			int Value = Partner[r] == 0 ? Short[(r - 1) % 20][Length - 1] : 0;
			for (int j = l; j < r; ++j)
			{
				int Ways = Partner[r] == j ? Weight[r] :
					(Partner[r] == 0 && Partner[j] == 0 ? 2 : 0);
				if (Ways != 0)
				{
					long long Term = 1LL * Ways * Short[(j - 1) % 20][j - l]
						* Short[(r - 1) % 20][r - j - 1] % Mod;
					Value = (Value + Term) % Mod;
				}
			}
			Short[Row][Length] = Value;
		}
		int Value = Partner[r] == 0 ? Prefix[r - 1] : 0;
		for (int j = std::max(1, r - k); j < r; ++j)
		{
			int Ways = Partner[r] == j ? Weight[r] :
				(Partner[r] == 0 && Partner[j] == 0 ? 2 : 0);
			if (Ways != 0)
			{
				long long Term = 1LL * Ways * Prefix[j - 1]
					* Short[(r - 1) % 20][r - j - 1] % Mod;
				Value = (Value + Term) % Mod;
			}
		}
		Prefix[r] = Value;
	}
	std::printf("%d\n", Prefix[n]);
}
