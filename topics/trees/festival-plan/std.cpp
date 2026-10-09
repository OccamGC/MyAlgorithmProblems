// Original centroid decomposition and monotone depth windows.
// Contribution: Codex (GPT-6): explicit traversals and repaired boundary handling.
#include <algorithm>
#include <iostream>
#include <limits>
#include <vector>

using FInt = long long;
constexpr FInt Missing = std::numeric_limits<FInt>::lowest() / 4;
constexpr int NoPath = -1061109568;

struct FVisit
{
	int Vertex;
	int ParentIndex;
	int Depth;
	FInt Sum;
	FInt Best = Missing;
};

static void PairSides(std::vector<FVisit>& From, const std::vector<FVisit>& To,
	int L, int R, FInt CoreValue)
{
	std::vector<FInt> Maximum(To.back().Depth + 1, Missing);
	for (const FVisit& Visit : To)
	{
		Maximum[Visit.Depth] = std::max(Maximum[Visit.Depth], Visit.Sum);
	}
	std::vector<int> Queue(Maximum.size());
	int Head = 0;
	int Tail = 0;
	int Next = static_cast<int>(Maximum.size()) - 1;
	for (FVisit& Visit : From)
	{
		const int Low = std::max(0, L - Visit.Depth);
		const int High = R - Visit.Depth;
		while (Next >= Low)
		{
			while (Tail > Head && Maximum[Queue[Tail - 1]] <= Maximum[Next])
			{
				--Tail;
			}
			Queue[Tail++] = Next--;
		}
		while (Head < Tail && Queue[Head] > High)
		{
			++Head;
		}
		if (Head < Tail && Maximum[Queue[Head]] != Missing)
		{
			Visit.Best = Visit.Sum + Maximum[Queue[Head]] - CoreValue;
		}
	}
}

static void Propagate(std::vector<FVisit>& Visits, std::vector<FInt>& Answer)
{
	for (int i = static_cast<int>(Visits.size()) - 1; i >= 0; --i)
	{
		const FVisit& Visit = Visits[i];
		Answer[Visit.Vertex] = std::max(Answer[Visit.Vertex], Visit.Best);
		if (Visit.ParentIndex >= 0)
		{
			FVisit& Parent = Visits[Visit.ParentIndex];
			Parent.Best = std::max(Parent.Best, Visit.Best);
		}
	}
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int L;
	int R;
	std::cin >> n >> L >> R;
	--L;
	--R;
	std::vector<int> Value(n);
	for (int& v : Value)
	{
		std::cin >> v;
	}
	std::vector<std::vector<int>> Graph(n);
	for (int i = 1; i < n; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Graph[--u].push_back(--v);
		Graph[v].push_back(u);
	}
	std::vector<int> RootParent(n, -1);
	std::vector<int> Order{0};
	for (int i = 0; i < n; ++i)
	{
		const int u = Order[i];
		for (int v : Graph[u])
		{
			if (v != RootParent[u])
			{
				RootParent[v] = u;
				Order.push_back(v);
			}
		}
	}
	std::vector<int> Parent(n);
	std::vector<int> Size(n);
	std::vector<char> Removed(n, false);
	std::vector<FInt> Answer(n, Missing);
	std::vector<int> Tasks{0};
	while (!Tasks.empty())
	{
		const int Start = Tasks.back();
		Tasks.pop_back();
		Order.assign(1, Start);
		Parent[Start] = -1;
		for (std::size_t i = 0; i < Order.size(); ++i)
		{
			const int u = Order[i];
			Size[u] = 1;
			for (int v : Graph[u])
			{
				if (!Removed[v] && v != Parent[u])
				{
					Parent[v] = u;
					Order.push_back(v);
				}
			}
		}
		const int Total = static_cast<int>(Order.size());
		if (Total <= 8)
		{
			for (int Bottom : Order)
			{
				FInt Sum = 0;
				int Length = 0;
				for (int Top = Bottom; Top >= 0 && !Removed[Top]; Top = RootParent[Top], ++Length)
				{
					Sum += Value[Top];
					if (L <= Length && Length <= R)
					{
						for (int u = Bottom; ; u = RootParent[u])
						{
							Answer[u] = std::max(Answer[u], Sum);
							if (u == Top)
							{
								break;
							}
						}
					}
				}
			}
			for (int u : Order)
			{
				Removed[u] = true;
			}
			continue;
		}
		int Core = Start;
		int Balance = Total;
		for (int i = Total - 1; i >= 0; --i)
		{
			const int u = Order[i];
			int Largest = 0;
			for (int v : Graph[u])
			{
				if (!Removed[v] && Parent[v] == u)
				{
					Size[u] += Size[v];
					Largest = std::max(Largest, Size[v]);
				}
			}
			Largest = std::max(Largest, Total - Size[u]);
			if (Largest < Balance)
			{
				Core = u;
				Balance = Largest;
			}
		}
		std::vector<FVisit> Ancestors{{Core, -1, 0, Value[Core]}};
		while (Ancestors.back().Depth < R)
		{
			const FVisit Last = Ancestors.back();
			const int Up = RootParent[Last.Vertex];
			if (Up < 0 || Removed[Up])
			{
				break;
			}
			Ancestors.push_back({Up, static_cast<int>(Ancestors.size()) - 1,
				Last.Depth + 1, Last.Sum + Value[Up]});
		}
		std::vector<FVisit> Descendants{{Core, -1, 0, Value[Core]}};
		for (std::size_t i = 0; i < Descendants.size(); ++i)
		{
			const FVisit Visit = Descendants[i];
			if (Visit.Depth == R)
			{
				continue;
			}
			for (int v : Graph[Visit.Vertex])
			{
				if (!Removed[v] && v != RootParent[Visit.Vertex])
				{
					Descendants.push_back({v, static_cast<int>(i), Visit.Depth + 1, Visit.Sum + Value[v]});
				}
			}
		}
		PairSides(Ancestors, Descendants, L, R, Value[Core]);
		PairSides(Descendants, Ancestors, L, R, Value[Core]);
		Propagate(Ancestors, Answer);
		Propagate(Descendants, Answer);
		Removed[Core] = true;
		for (int v : Graph[Core])
		{
			if (!Removed[v])
			{
				Tasks.push_back(v);
			}
		}
	}
	for (FInt Result : Answer)
	{
		std::cout << (Result == Missing ? NoPath : Result) << '\n';
	}
}
