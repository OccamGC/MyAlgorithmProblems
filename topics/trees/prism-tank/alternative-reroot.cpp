// Rerooting DP. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

struct FMessage
{
	long double Value;
	int From;
};

struct FLine
{
	long double Slope;
	long double Intercept;
	long double At(long double x) const
	{
		return Slope * x + Intercept;
	}
};

// Slopes arrive in increasing order (equal slopes are possible at p = 1).
void Insert(std::vector<FLine>& Hull, FLine Line)
{
	if (!Hull.empty() && Line.Slope == Hull.back().Slope)
	{
		if (Line.Intercept <= Hull.back().Intercept)
		{
			return;
		}
		Hull.pop_back();
	}
	while (Hull.size() >= 2)
	{
		const FLine& a = Hull[Hull.size() - 2];
		const FLine& b = Hull.back();
		if ((a.Intercept - b.Intercept) * (Line.Slope - b.Slope)
			< (b.Intercept - Line.Intercept) * (b.Slope - a.Slope))
		{
			break;
		}
		Hull.pop_back();
	}
	Hull.push_back(Line);
}

long double Evaluate(const std::vector<FLine>& Hull, long double x)
{
	int l = 0;
	int r = static_cast<int>(Hull.size()) - 1;
	while (l < r)
	{
		int Mid = (l + r) / 2;
		if (Hull[Mid].At(x) <= Hull[Mid + 1].At(x))
		{
			l = Mid + 1;
		}
		else
		{
			r = Mid;
		}
	}
	return Hull[l].At(x);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int BlockLimit;
	int e;
	long double RoundingOffset;
	std::cin >> n >> BlockLimit >> e >> RoundingOffset;
	std::vector<std::vector<int>> Graph(n);
	for (int i = 0; i < e; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Graph[u - 1].push_back(v - 1);
		Graph[v - 1].push_back(u - 1);
	}
	std::vector<long double> Damage(n);
	std::vector<long double> p(n);
	for (auto& Value : Damage)
	{
		std::cin >> Value;
	}
	for (auto& Value : p)
	{
		std::cin >> Value;
	}
	std::vector<int> Parent(n, -2);
	std::vector<int> Order;
	for (int Root = 0; Root < n; ++Root)
	{
		if (Parent[Root] != -2)
		{
			continue;
		}
		int Begin = static_cast<int>(Order.size());
		Parent[Root] = -1;
		Order.push_back(Root);
		for (int i = Begin; i < static_cast<int>(Order.size()); ++i)
		{
			int u = Order[i];
			for (int v : Graph[u])
			{
				if (v != Parent[u])
				{
					Parent[v] = u;
					Order.push_back(v);
				}
			}
		}
	}

	std::vector<long double> Down(n);
	std::vector<long double> Up(n);
	long double Answer = 0;
	// Step 0 sends child-to-parent messages. Step 1 knows every incoming message.
	for (int Step = 0; Step < 2; ++Step)
	{
		for (int i = 0; i < n; ++i)
		{
			int u = Order[Step == 0 ? n - 1 - i : i];
			std::vector<FMessage> In;
			for (int v : Graph[u])
			{
				if (v != Parent[u])
				{
					In.push_back({Down[v], v});
				}
				else if (Step == 1)
				{
					In.push_back({Up[u], v});
				}
			}
			if (BlockLimit > 0)
			{
				std::sort(In.begin(), In.end(), [](const FMessage& a, const FMessage& b)
				{
					return a.Value > b.Value;
				});
			}
			int d = static_cast<int>(In.size());
			auto Factor = [&](int k) { return p[u] + (1 - p[u]) / k; };
			std::vector<long double> Sum(d + 1);
			std::vector<long double> Best(d + 1);
			for (int k = 1; k <= d; ++k)
			{
				Sum[k] = Sum[k - 1] + In[k - 1].Value;
				Best[k] = BlockLimit ? std::max(Best[k - 1], Sum[k] * Factor(k)) : Sum[k] * Factor(k);
			}
			if (Step == 0)
			{
				Down[u] = Damage[u] + Best[d];
				continue;
			}
			Answer = std::max(Answer, Damage[u] + Best[d]);
			std::vector<FLine> Hull;
			for (int j = d - 1; j >= 0; --j)
			{
				long double Value = 0;
				if (BlockLimit > 0)
				{
					int k = j + 1;
					if (k < d)
					{
						Insert(Hull, {Factor(k), Factor(k) * Sum[k + 1]});
					}
					Value = Best[j];
					if (!Hull.empty())
					{
						Value = std::max(Value, Evaluate(Hull, -In[j].Value));
					}
				}
				else if (d > 1)
				{
					Value = Factor(d - 1) * (Sum[d] - In[j].Value);
				}
				if (In[j].From != Parent[u])
				{
					Up[In[j].From] = Damage[u] + Value;
				}
			}
		}
	}
	std::cout << static_cast<long long>(std::floor(Answer + RoundingOffset + 0.5L)) << '\n';
}
