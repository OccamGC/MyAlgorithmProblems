// Problem setter's solution: reflexivity, transitivity, joins and meets.
// Codex (GPT-6): factor the dual checks into one shared implementation.

#include <iostream>
#include <vector>
using FRelation = std::vector<std::vector<int>>;

bool IsPreorder(const FRelation& Relation)
{
	const int n = static_cast<int>(Relation.size());
	for (int i = 0; i < n; ++i)
	{
		if (!Relation[i][i])
		{
			return false;
		}
		for (int j = 0; j < n; ++j)
		{
			if (!Relation[i][j])
			{
				continue;
			}
			for (int k = 0; k < n; ++k)
			{
				if (Relation[j][k] && !Relation[i][k])
				{
					return false;
				}
			}
		}
	}
	return true;
}

bool HasJoins(const FRelation& Relation)
{
	const int n = static_cast<int>(Relation.size());
	for (int i = 0; i < n; ++i)
	{
		for (int j = 0; j < n; ++j)
		{
			int Candidate = -1;
			for (int k = 0; k < n; ++k)
			{
				if (Relation[i][k] && Relation[j][k] &&
					(Candidate == -1 || Relation[k][Candidate]))
				{
					Candidate = k;
				}
			}
			if (Candidate == -1)
			{
				return false;
			}
			for (int k = 0; k < n; ++k)
			{
				if (Relation[i][k] && Relation[j][k] && !Relation[Candidate][k])
				{
					return false;
				}
			}
		}
	}
	return true;
}

bool IsLattice(const FRelation& Relation)
{
	if (!IsPreorder(Relation) || !HasJoins(Relation))
	{
		return false;
	}
	const int n = static_cast<int>(Relation.size());
	FRelation Dual(n, std::vector<int>(n));
	for (int i = 0; i < n; ++i)
	{
		for (int j = 0; j < n; ++j)
		{
			Dual[i][j] = Relation[j][i];
		}
	}
	return HasJoins(Dual);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		int n;
		std::cin >> n;
		FRelation Relation(n, std::vector<int>(n));
		for (auto& Row : Relation)
		{
			for (int& Value : Row)
			{
				std::cin >> Value;
			}
		}
		std::cout << (IsLattice(Relation) ? 'Y' : 'N') << '\n';
	}
}
