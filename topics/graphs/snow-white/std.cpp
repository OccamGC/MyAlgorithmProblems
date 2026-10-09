// Codex (GPT-6): minimum-height-cost augmentation, source/sink bounds by
// height, and an ascending chain through carefully selected local paths.
// The DFS source/sink ordering follows Raghavan's corrected ST procedure.
#include <algorithm>
#include <cstdio>
#include <numeric>
#include <utility>
#include <vector>

struct FInput
{
	char Buffer[65536];
	int Position = 0;
	int Length = 0;
	int Get()
	{
		if (Position == Length)
		{
			Length = static_cast<int>(std::fread(Buffer, 1, sizeof(Buffer), stdin));
			Position = 0;
			if (Length == 0)
			{
				return EOF;
			}
		}
		return Buffer[Position++];
	}
	int Read()
	{
		int c = Get();
		while (c <= ' ' && c != EOF)
		{
			c = Get();
		}
		int Sign = 1;
		if (c == '-')
		{
			Sign = -1;
			c = Get();
		}
		int Value = 0;
		while (c >= '0' && c <= '9')
		{
			Value = Value * 10 + c - '0';
			c = Get();
		}
		return Sign * Value;
	}
};

struct FFrame
{
	int Vertex;
	std::size_t Next;
};
struct FPath
{
	int Start = -1;
	int End = -1;
};
class FBuilder
{
public:
	std::vector<std::vector<int>> Forward;
	std::vector<std::vector<int>> Reverse;
	std::vector<bool> HasIncoming;
	std::vector<bool> HasOutgoing;
	std::vector<bool> FromHigher;
	std::vector<bool> ToLower;
	std::vector<bool> Visited;
	std::vector<bool> UsedSource;
	std::vector<bool> UsedSink;
	std::vector<int> Stamp;
	std::vector<int> SinkStamp;
	int SearchId = 0;
	int OpenId = 0;
	std::vector<std::pair<int, int>> Added;

	explicit FBuilder(int Count) : Forward(Count + 1), Reverse(Count + 1),
		HasIncoming(Count + 1), HasOutgoing(Count + 1), FromHigher(Count + 1),
		ToLower(Count + 1), Visited(Count + 1), UsedSource(Count + 1),
		UsedSink(Count + 1), Stamp(Count + 1), SinkStamp(Count + 1)
	{
	}
	FPath Open(const std::vector<int>& Sources, const std::vector<int>& Sinks,
		std::vector<std::vector<int>>& Graph)
	{
		++OpenId;
		for (int u : Sinks)
		{
			SinkStamp[u] = OpenId;
		}
		std::vector<std::pair<int, int>> Pairs;
		std::vector<FFrame> Stack;
		for (int Source : Sources)
		{
			if (Visited[Source])
			{
				continue;
			}
			Visited[Source] = true;
			Stack.clear();
			Stack.push_back({Source, 0});
			int Found = SinkStamp[Source] == OpenId ? Source : -1;
			while (!Stack.empty() && Found == -1)
			{
				FFrame& Frame = Stack.back();
				if (Frame.Next == Graph[Frame.Vertex].size())
				{
					Stack.pop_back();
					continue;
				}
				int v = Graph[Frame.Vertex][Frame.Next++];
				if (Visited[v])
				{
					continue;
				}
				Visited[v] = true;
				Stack.push_back({v, 0});
				if (SinkStamp[v] == OpenId)
				{
					Found = v;
				}
			}
			if (Found != -1)
			{
				Pairs.push_back({Source, Found});
				UsedSource[Source] = true;
				UsedSink[Found] = true;
			}
		}
		std::vector<int> FreeSources;
		std::vector<int> FreeSinks;
		for (int u : Sources)
		{
			if (!UsedSource[u])
			{
				FreeSources.push_back(u);
			}
		}
		for (int u : Sinks)
		{
			if (!UsedSink[u])
			{
				FreeSinks.push_back(u);
			}
		}
		std::size_t Paired = std::min(FreeSources.size(), FreeSinks.size());
		for (std::size_t i = 0; i < Paired; ++i)
		{
			Added.push_back({FreeSinks[i], FreeSources[i]});
		}
		if (Pairs.empty())
		{
			const std::vector<int>& Chain = FreeSources.size() > Paired ? FreeSources : FreeSinks;
			if (Chain.size() == Paired)
			{
				return {};
			}
			for (std::size_t i = Paired + 1; i < Chain.size(); ++i)
			{
				Added.push_back({Chain[i - 1], Chain[i]});
			}
			return {Chain[Paired], Chain.back()};
		}
		for (std::size_t i = 1; i < Pairs.size(); ++i)
		{
			Added.push_back({Pairs[i - 1].second, Pairs[i].first});
		}
		FPath Path{Pairs.front().first, Pairs.back().second};
		for (std::size_t i = Paired; i < FreeSources.size(); ++i)
		{
			Added.push_back({Path.End, FreeSources[i]});
		}
		for (std::size_t i = Paired; i < FreeSinks.size(); ++i)
		{
			Added.push_back({Path.End, FreeSinks[i]});
			Path.End = FreeSinks[i];
		}
		return Path;
	}
	bool Reaches(int Start, const std::vector<std::vector<int>>& Graph,
		const std::vector<bool>& Target)
	{
		++SearchId;
		std::vector<int> Stack(1, Start);
		Stamp[Start] = SearchId;
		while (!Stack.empty())
		{
			int u = Stack.back();
			Stack.pop_back();
			if (Target[u])
			{
				return true;
			}
			for (int v : Graph[u])
			{
				if (Stamp[v] != SearchId)
				{
					Stamp[v] = SearchId;
					Stack.push_back(v);
				}
			}
		}
		return false;
	}
};

int main()
{
	FInput Input;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<int> Height(n);
	for (int& h : Height)
	{
		h = Input.Read();
	}
	std::vector<std::vector<int>> Graph(n);
	std::vector<std::vector<int>> Back(n);
	for (int i = 0; i < m; ++i)
	{
		int u = Input.Read() - 1;
		int v = Input.Read() - 1;
		Graph[u].push_back(v);
		Back[v].push_back(u);
	}
	std::vector<bool> Visited(n);
	std::vector<int> Order;
	std::vector<FFrame> Stack;
	for (int Start = 0; Start < n; ++Start)
	{
		if (Visited[Start])
		{
			continue;
		}
		Visited[Start] = true;
		Stack.push_back({Start, 0});
		while (!Stack.empty())
		{
			FFrame& Frame = Stack.back();
			if (Frame.Next == Graph[Frame.Vertex].size())
			{
				Order.push_back(Frame.Vertex);
				Stack.pop_back();
				continue;
			}
			int v = Graph[Frame.Vertex][Frame.Next++];
			if (!Visited[v])
			{
				Visited[v] = true;
				Stack.push_back({v, 0});
			}
		}
	}
	std::vector<int> Component(n, -1);
	std::vector<int> Representative;
	std::vector<int> Work;
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		int Start = *It;
		if (Component[Start] != -1)
		{
			continue;
		}
		int Id = static_cast<int>(Representative.size());
		Representative.push_back(Start);
		Component[Start] = Id;
		Work.push_back(Start);
		while (!Work.empty())
		{
			int u = Work.back();
			Work.pop_back();
			for (int v : Back[u])
			{
				if (Component[v] == -1)
				{
					Component[v] = Id;
					Work.push_back(v);
				}
			}
		}
	}
	int Count = static_cast<int>(Representative.size());
	if (Count == 1)
	{
		std::puts("0\n0");
		return 0;
	}
	std::vector<int> Sorted(Count);
	std::iota(Sorted.begin(), Sorted.end(), 0);
	std::sort(Sorted.begin(), Sorted.end(), [&](int u, int v)
	{
		return Height[Representative[u]] < Height[Representative[v]];
	});
	std::vector<int> Level(Count);
	std::vector<std::vector<int>> Groups;
	for (int u : Sorted)
	{
		if (Groups.empty() || Height[Representative[Groups.back().back()]] != Height[Representative[u]])
		{
			Groups.emplace_back();
		}
		Level[u] = static_cast<int>(Groups.size()) - 1;
		Groups.back().push_back(u);
	}
	int Levels = static_cast<int>(Groups.size());
	FBuilder Builder(Count);
	std::vector<int> Crossings(Levels + 1);
	for (int u = 0; u < n; ++u)
	{
		for (int v : Graph[u])
		{
			int a = Component[u];
			int b = Component[v];
			if (a == b)
			{
				continue;
			}
			Builder.HasOutgoing[a] = true;
			Builder.HasIncoming[b] = true;
			if (Level[a] == Level[b])
			{
				Builder.Forward[a].push_back(b);
				Builder.Reverse[b].push_back(a);
			}
			else
			{
				Builder.FromHigher[b] = true;
				Builder.ToLower[a] = true;
				++Crossings[Level[b] + 1];
				--Crossings[Level[a] + 1];
			}
		}
	}
	int Active = 0;
	for (int i = 1; i < Levels; ++i)
	{
		Active += Crossings[i];
		if (Active == 0)
		{
			std::puts("-1");
			return 0;
		}
	}
	std::vector<FPath> Stops;
	for (int i = 0; i < Levels; ++i)
	{
		std::vector<int> Sources;
		std::vector<int> Sinks;
		for (int u : Groups[i])
		{
			if (!Builder.HasIncoming[u])
			{
				Sources.push_back(u);
			}
			if (!Builder.HasOutgoing[u])
			{
				Sinks.push_back(u);
			}
		}
		std::size_t Begin = Builder.Added.size();
		FPath Path;
		if (Levels == 1)
		{
			Path = Builder.Open(Sources, Sinks, Builder.Forward);
			Builder.Added.push_back({Path.End, Path.Start});
		}
		else if (i == 0 || i == Levels - 1)
		{
			bool bLowest = i == 0;
			auto& Local = bLowest ? Builder.Forward : Builder.Reverse;
			auto& Entering = bLowest ? Builder.FromHigher : Builder.ToLower;
			for (int u : Groups[i])
			{
				if (Entering[u])
				{
					Local[Count].push_back(u);
				}
			}
			if (!bLowest)
			{
				Sources.swap(Sinks);
			}
			Sources.insert(Sources.begin(), Count);
			Builder.Visited[Count] = false;
			Builder.UsedSource[Count] = false;
			Path = Builder.Open(Sources, Sinks, Local);
			Stops.push_back({Path.End, Path.End});
			if (!bLowest)
			{
				for (std::size_t j = Begin; j < Builder.Added.size(); ++j)
				{
					std::swap(Builder.Added[j].first, Builder.Added[j].second);
				}
			}
			Local[Count].clear();
		}
		else
		{
			Path = Builder.Open(Sources, Sinks, Builder.Forward);
			if (Path.Start != -1)
			{
				for (std::size_t j = Begin; j < Builder.Added.size(); ++j)
				{
					auto e = Builder.Added[j];
					Builder.Forward[e.first].push_back(e.second);
					Builder.Reverse[e.second].push_back(e.first);
				}
				bool bIn = Builder.Reaches(Path.End, Builder.Reverse, Builder.FromHigher);
				bool bOut = Builder.Reaches(Path.Start, Builder.Forward, Builder.ToLower);
				if (bIn && bOut)
				{
					Builder.Added.push_back({Path.End, Path.Start});
				}
				else
				{
					Stops.push_back(Path);
				}
			}
		}
	}
	for (std::size_t i = 1; i < Stops.size(); ++i)
	{
		Builder.Added.push_back({Stops[i - 1].End, Stops[i].Start});
	}
	long long Cost = 1LL * Height[Representative[Sorted.back()]] - Height[Representative[Sorted.front()]];
	std::printf("%lld\n%zu\n", Cost, Builder.Added.size());
	for (auto e : Builder.Added)
	{
		std::printf("%d %d\n", Representative[e.first] + 1, Representative[e.second] + 1);
	}
}
