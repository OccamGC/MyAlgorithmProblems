// Skip list. C++17 implementation by Codex (GPT-6).
#include <iostream>
#include <array>
#include <random>
#include <utility>
#include <vector>

class FSkipList
{
	// One node per participant. Updating an ID reuses its tower.
	static constexpr int Levels = 24;
	std::vector<int> Offset;
	std::vector<int> Links;
	std::vector<int> Value;
	std::vector<char> Present;

	int& Next(int Id, int Level)
	{
		return Links[Offset[Id] + Level];
	}

	std::array<int, Levels> Before(int Lucky, int Id)
	{
		std::array<int, Levels> Path;
		int u = 0;
		for (int Level = Levels - 1; Level >= 0; --Level)
		{
			int v = Next(u, Level);
			while (v && (Value[v] < Lucky || (Value[v] == Lucky && v < Id)))
			{
				u = v;
				v = Next(u, Level);
			}
			Path[Level] = u;
		}
		return Path;
	}
public:
	explicit FSkipList(int n) : Offset(n + 2), Value(n + 1), Present(n + 1, true)
	{
		std::mt19937 Random(20261126);
		std::array<int, Levels> Tail{};
		Links.resize(Levels);
		for (int Id = 1; Id <= n; ++Id)
		{
			unsigned Bits = Random();
			int Height = 1;
			while (Height < Levels && (Bits & 1))
			{
				++Height;
				Bits >>= 1;
			}
			Offset[Id] = static_cast<int>(Links.size());
			Links.resize(Links.size() + Height);
			for (int Level = 0; Level < Height; ++Level)
			{
				Next(Tail[Level], Level) = Id;
				Tail[Level] = Id;
			}
			Value[Id] = Id;
		}
		Offset[n + 1] = static_cast<int>(Links.size());
	}

	void Remove(int Id)
	{
		if (!Present[Id])
		{
			return;
		}
		auto Path = Before(Value[Id], Id);
		for (int Level = 0; Level < Offset[Id + 1] - Offset[Id]; ++Level)
		{
			Next(Path[Level], Level) = Next(Id, Level);
		}
		Present[Id] = false;
	}
	void Change(int Id, int Lucky)
	{
		Remove(Id);
		auto Path = Before(Lucky, Id);
		Value[Id] = Lucky;
		for (int Level = 0; Level < Offset[Id + 1] - Offset[Id]; ++Level)
		{
			Next(Id, Level) = Next(Path[Level], Level);
			Next(Path[Level], Level) = Id;
		}
		Present[Id] = true;
	}

	int Winner(int t)
	{
		int Left = Before(t, static_cast<int>(Value.size()))[0];
		int Right = Next(Left, 0);
		if (!Left || (Right && Value[Right] - t < t - Value[Left]))
		{
			return Right;
		}
		return Left;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	long long A;
	long long B;
	long long C;
	int n;
	int m;
	int q;
	int k;
	std::cin >> A >> B >> C >> n >> m >> q >> k;
	std::vector<int> Queries(q);
	std::vector<std::pair<int, int>> Changes(k);
	for (int& Position : Queries)
	{
		std::cin >> Position;
	}
	for (auto& Change : Changes)
	{
		std::cin >> Change.first >> Change.second;
	}
	FSkipList Active(n);
	int QueryIndex = 0;
	int ChangeIndex = 0;
	for (int i = 1; i <= m; ++i)
	{
		A = (A * B + C) % n + 1;
		const int t = static_cast<int>(A);
		if (QueryIndex < q && Queries[QueryIndex] == i)
		{
			++QueryIndex;
			std::cout << Active.Winner(t) << '\n';
		}
		else if (ChangeIndex < k && Changes[ChangeIndex].first == i)
		{
			const int Person = Changes[ChangeIndex++].second;
			Active.Change(Person, t);
		}
		else
		{
			Active.Remove(t);
		}
	}
}
