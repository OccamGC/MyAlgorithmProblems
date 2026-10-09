// Contribution: Codex (GPT-6): iterative centroid traversal, range maxima,
// and propagation of endpoint candidates to every vertex on their paths.
#include <algorithm>
#include <iostream>
#include <vector>

constexpr int Missing = -2000000000;
constexpr int NoPath = -1061109568;
constexpr bool bDownwardOnly = false;

struct FChoice
{
	int Value = Missing;
	int Color = -2;
};

struct FBestTwo
{
	FChoice First;
	FChoice Second;
	void Add(FChoice Choice)
	{
		if (Choice.Value == Missing)
		{
			return;
		}
		if (Choice.Color == First.Color)
		{
			First.Value = std::max(First.Value, Choice.Value);
		}
		else if (Choice.Value > First.Value)
		{
			Second = First;
			First = Choice;
		}
		else if (Choice.Value > Second.Value)
		{
			Second = Choice;
		}
	}
	void Merge(const FBestTwo& Other)
	{
		Add(Other.First);
		Add(Other.Second);
	}
	int Except(int Color) const
	{
		return First.Color == Color ? Second.Value : First.Value;
	}
};

struct FVisit
{
	int Vertex;
	int ParentIndex;
	int Depth;
	int Sum;
	int Color;
	int Best = Missing;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int L;
	int R;
	std::cin >> n >> L >> R;
	if (bDownwardOnly)
	{
		--L;
		--R;
	}
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
		int u = Order[i];
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
	std::vector<int> Answer(n, Missing);
	std::vector<char> Removed(n, false);
	std::vector<int> Tasks{0};
	while (!Tasks.empty())
	{
		int Start = Tasks.back();
		Tasks.pop_back();
		Order.assign(1, Start);
		Parent[Start] = -1;
		for (std::size_t i = 0; i < Order.size(); ++i)
		{
			int u = Order[i];
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
		int Total = static_cast<int>(Order.size());
		int Core = Start;
		int Balance = Total;
		for (int i = Total - 1; i >= 0; --i)
		{
			int u = Order[i];
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
				Balance = Largest;
				Core = u;
			}
		}
		std::vector<FVisit> Visits{{Core, -1, 0, Value[Core], -1}};
		int MaxDepth = 0;
		for (std::size_t i = 0; i < Visits.size(); ++i)
		{
			FVisit Current = Visits[i];
			if (Current.Depth == R)
			{
				continue;
			}
			for (int v : Graph[Current.Vertex])
			{
				if (Removed[v] || (Current.ParentIndex >= 0 && v == Visits[Current.ParentIndex].Vertex))
				{
					continue;
				}
				int Color = i == 0 ? v : Current.Color;
				if (bDownwardOnly)
				{
					if (i == 0)
					{
						Color = v == RootParent[Core] ? 1 : 0;
					}
					else if (Color == 1 && v != RootParent[Current.Vertex])
					{
						continue;
					}
				}
				Visits.push_back({v, static_cast<int>(i), Current.Depth + 1, Current.Sum + Value[v], Color});
				MaxDepth = std::max(MaxDepth, Current.Depth + 1);
			}
		}
		int Base = 1;
		while (Base <= MaxDepth)
		{
			Base *= 2;
		}
		std::vector<FBestTwo> Tree(2 * Base);
		for (const FVisit& Visit : Visits)
		{
			Tree[Base + Visit.Depth].Add({Visit.Sum, Visit.Color});
		}
		for (int i = Base - 1; i > 0; --i)
		{
			Tree[i] = Tree[2 * i];
			Tree[i].Merge(Tree[2 * i + 1]);
		}
		for (FVisit& Visit : Visits)
		{
			int Left = std::max(0, L - Visit.Depth) + Base;
			int Right = std::min(MaxDepth, R - Visit.Depth) + Base + 1;
			FBestTwo Best;
			while (Left < Right)
			{
				if (Left & 1)
				{
					Best.Merge(Tree[Left++]);
				}
				if (Right & 1)
				{
					Best.Merge(Tree[--Right]);
				}
				Left /= 2;
				Right /= 2;
			}
			// The centroid may pair with itself, giving a zero-edge path.
			int Other = Best.Except(Visit.Color == -1 ? -2 : Visit.Color);
			if (Other != Missing)
			{
				Visit.Best = Visit.Sum + Other - Value[Core];
			}
		}
		for (int i = static_cast<int>(Visits.size()) - 1; i >= 0; --i)
		{
			FVisit& Visit = Visits[i];
			Answer[Visit.Vertex] = std::max(Answer[Visit.Vertex], Visit.Best);
			if (Visit.ParentIndex >= 0)
			{
				FVisit& Up = Visits[Visit.ParentIndex];
				Up.Best = std::max(Up.Best, Visit.Best);
			}
		}
		Removed[Core] = true;
		for (int v : Graph[Core])
		{
			if (!Removed[v])
			{
				Tasks.push_back(v);
			}
		}
	}
	for (int Result : Answer)
	{
		std::cout << (Result == Missing ? NoPath : Result) << '\n';
	}
}
