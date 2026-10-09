#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

// Codex (GPT-6): emit version intervals through a bounded shared-suffix cache.
void Emit(int Version, int Start, int Count, int CachedVersion, const std::vector<char>& Cache,
	const std::vector<int>& Length, const std::vector<int>& Position)
{
	if (Count == 0)
	{
		return;
	}
	while (Version > CachedVersion && Start >= Length[Version] - Length[Version - 1])
	{
		Start -= Length[Version] - Length[Version - 1];
		--Version;
	}
	if (Version <= CachedVersion)
	{
		std::cout.write(Cache.data() + Length[CachedVersion] - Length[Version] + Start, Count);
		return;
	}
	int Previous = Length[Version - 1];
	int Added = Length[Version] - Previous;
	int Take = std::min(Count, Added - Start);
	int Mapped = (Position[Version - 1] + Start) % Previous;
	int First = std::min(Take, Previous - Mapped);
	Emit(Version - 1, Mapped, First, CachedVersion, Cache, Length, Position);
	Emit(Version - 1, 0, Take - First, CachedVersion, Cache, Length, Position);
	Emit(Version - 1, 0, Count - Take, CachedVersion, Cache, Length, Position);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string Initial;
	int n, m;
	std::cin >> Initial >> n >> m;
	std::vector<int> Length(n + 1), Position(n);
	Length[0] = static_cast<int>(Initial.size());
	for (int i = 0; i < n; ++i)
	{
		std::cin >> Position[i];
		Length[i + 1] = Length[i] + (Length[i] + 4) / 5;
	}
	constexpr int CacheLimit = 65536;
	int CachedVersion = 0;
	while (CachedVersion < n && Length[CachedVersion + 1] <= CacheLimit)
	{
		++CachedVersion;
	}
	std::vector<char> Cache(Length[CachedVersion]);
	int Start = Length[CachedVersion] - Length[0];
	std::copy(Initial.begin(), Initial.end(), Cache.begin() + Start);
	for (int i = 0; i < CachedVersion; ++i)
	{
		int Added = Length[i + 1] - Length[i];
		for (int j = 0; j < Added; ++j)
		{
			Cache[Start - Added + j] = Cache[Start + (Position[i] + j) % Length[i]];
		}
		Start -= Added;
	}
	for (int i = 0; i < m; ++i)
	{
		int Version;
		std::cin >> Version;
		Emit(Version, 0, Length[Version], CachedVersion, Cache, Length, Position);
		std::cout << '\n';
	}
}
