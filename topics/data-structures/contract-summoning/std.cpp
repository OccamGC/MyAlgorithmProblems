// Codex (GPT-6): static range tree with deletable copies for 3D dominance reporting.
// A single reachable summoner must satisfy all three requirements at once.
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <vector>

struct FCharacter
{
	std::array<int, 3> Requirement;
	std::array<int, 3> Attribute;
};

struct FBucket
{
	std::vector<int> Ids;
	std::vector<int> Minimum;
	int Base = 1;
	static constexpr int Infinity = 2000000000;

	void Build(const std::vector<FCharacter>& Characters)
	{
		if (Ids.empty())
		{
			return;
		}
		while (Base < static_cast<int>(Ids.size()))
		{
			Base *= 2;
		}
		Minimum.assign(2 * Base, Infinity);
		for (std::size_t i = 0; i < Ids.size(); ++i)
		{
			Minimum[Base + i] = Characters[Ids[i]].Requirement[2];
		}
		for (int i = Base - 1; i > 0; --i)
		{
			Minimum[i] = std::min(Minimum[2 * i], Minimum[2 * i + 1]);
		}
	}

	int Find(int Node, int l, int r, int Bound, int Limit) const
	{
		if (l >= Bound || Minimum[Node] > Limit)
		{
			return -1;
		}
		if (r - l == 1)
		{
			return l;
		}
		int Middle = (l + r) / 2;
		int Position = Find(2 * Node, l, Middle, Bound, Limit);
		if (Position == -1)
		{
			Position = Find(2 * Node + 1, Middle, r, Bound, Limit);
		}
		return Position;
	}

	void Report(const std::array<int, 3>& Attribute,
		const std::vector<FCharacter>& Characters, std::vector<char>& Seen, std::vector<int>& Queue)
	{
		if (Ids.empty())
		{
			return;
		}
		int Bound = static_cast<int>(std::upper_bound(Ids.begin(), Ids.end(), Attribute[1],
			[&](int Value, int Id)
			{
				return Value < Characters[Id].Requirement[1];
			}) - Ids.begin());
		while (true)
		{
			int Position = Find(1, 0, Base, Bound, Attribute[2]);
			if (Position == -1)
			{
				return;
			}
			int Id = Ids[Position];
			if (!Seen[Id])
			{
				Seen[Id] = true;
				Queue.push_back(Id);
			}
			int Node = Base + Position;
			Minimum[Node] = Infinity;
			while (Node > 1)
			{
				Node /= 2;
				Minimum[Node] = std::min(Minimum[2 * Node], Minimum[2 * Node + 1]);
			}
		}
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<FCharacter> Characters(n + 1);
	for (int& Value : Characters[0].Attribute)
	{
		std::cin >> Value;
	}
	for (int i = 1; i <= n; ++i)
	{
		for (int& Value : Characters[i].Requirement)
		{
			std::cin >> Value;
		}
		for (int& Value : Characters[i].Attribute)
		{
			std::cin >> Value;
		}
	}
	std::vector<int> ByStrength(n);
	std::iota(ByStrength.begin(), ByStrength.end(), 1);
	std::sort(ByStrength.begin(), ByStrength.end(), [&](int a, int b)
	{
		return Characters[a].Requirement[0] < Characters[b].Requirement[0];
	});
	std::vector<int> Position(n + 1);
	for (int i = 0; i < n; ++i)
	{
		Position[ByStrength[i]] = i;
	}
	int Base = 1;
	while (Base < n)
	{
		Base *= 2;
	}
	std::vector<FBucket> Buckets(2 * Base);
	std::vector<int> ByIntelligence = ByStrength;
	std::sort(ByIntelligence.begin(), ByIntelligence.end(), [&](int a, int b)
	{
		return Characters[a].Requirement[1] < Characters[b].Requirement[1];
	});
	for (int Id : ByIntelligence)
	{
		for (int Node = Base + Position[Id]; Node > 0; Node /= 2)
		{
			Buckets[Node].Ids.push_back(Id);
		}
	}
	for (FBucket& Bucket : Buckets)
	{
		Bucket.Build(Characters);
	}
	std::vector<char> Seen(n + 1);
	std::vector<int> Queue = {0};
	for (std::size_t i = 0; i < Queue.size(); ++i)
	{
		const auto Attribute = Characters[Queue[i]].Attribute;
		int Bound = static_cast<int>(std::upper_bound(ByStrength.begin(), ByStrength.end(), Attribute[0],
			[&](int Value, int Id)
			{
				return Value < Characters[Id].Requirement[0];
			}) - ByStrength.begin());
		int l = Base;
		int r = Base + Bound;
		while (l < r)
		{
			if (l & 1)
			{
				Buckets[l++].Report(Attribute, Characters, Seen, Queue);
			}
			if (r & 1)
			{
				Buckets[--r].Report(Attribute, Characters, Seen, Queue);
			}
			l /= 2;
			r /= 2;
		}
	}
	std::cout << Queue.size() - 1 << '\n';
}
