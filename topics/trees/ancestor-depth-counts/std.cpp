#include <algorithm>
#include <array>
#include <cstdio>
#include <limits>
#include <numeric>
#include <utility>
#include <vector>

class FInput
{
	char Buffer[1 << 16];
	int Position = 0;
	int Length = 0;
public:
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
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		bool bNegative = Character == '-';
		if (bNegative)
		{
			Character = Get();
		}
		int Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return bNegative ? -Value : Value;
	}
};

class FOutput
{
	char Buffer[1 << 16];
	int Length = 0;
public:
	void Put(char Character)
	{
		if (Length == static_cast<int>(sizeof(Buffer)))
		{
			Flush();
		}
		Buffer[Length++] = Character;
	}
	void Write(long long Value, char End = '\n')
	{
		if (Value < 0)
		{
			Put('-');
			Value = -Value;
		}
		char Digits[24];
		int Count = 0;
		do
		{
			Digits[Count++] = static_cast<char>('0' + Value % 10);
			Value /= 10;
		} while (Value > 0);
		while (Count > 0)
		{
			Put(Digits[--Count]);
		}
		Put(End);
	}
	void Flush()
	{
		std::fwrite(Buffer, 1, Length, stdout);
		Length = 0;
	}
	~FOutput()
	{
		Flush();
	}
};

struct FTree
{
	int n;
	std::vector<int> Parent;
	std::vector<int> Offset;
	std::vector<int> Neighbor;
	std::vector<int> Depth;
	std::vector<int> Size;
	std::vector<int> Order;
	std::vector<long long> Total;
	explicit FTree(FInput& Input)
	{
		n = Input.Read();
		Parent.resize(n + 1);
		Offset.resize(n + 2);
		Depth.resize(n + 1);
		Size.assign(n + 1, 1);
		Total.resize(n + 1);
		Order.reserve(n);
		for (int i = 2; i <= n; ++i)
		{
			Parent[i] = Input.Read();
			++Offset[i + 1];
			++Offset[Parent[i] + 1];
		}
		for (int i = 1; i <= n + 1; ++i)
		{
			Offset[i] += Offset[i - 1];
		}
		Neighbor.resize(2 * (n - 1));
		{
			std::vector<int> Current = Offset;
			for (int i = 2; i <= n; ++i)
			{
				Neighbor[Current[i]++] = Parent[i];
				Neighbor[Current[Parent[i]]++] = i;
			}
		}
		Order.push_back(1);
		for (int Index = 0; Index < n; ++Index)
		{
			int u = Order[Index];
			for (int e = Offset[u]; e < Offset[u + 1]; ++e)
			{
				int v = Neighbor[e];
				if (v != Parent[u])
				{
					Depth[v] = Depth[u] + 1;
					Order.push_back(v);
				}
			}
		}
		for (int Index = n - 1; Index > 0; --Index)
		{
			int u = Order[Index];
			Size[Parent[u]] += Size[u];
		}
		for (int u : Order)
		{
			Total[u] = Total[Parent[u]] + Size[u];
		}
	}
};

class FDistanceSums
{
	const FTree& Tree;
	std::vector<char> Removed;
	std::vector<int> ComponentParent;
	std::vector<int> ComponentSize;
	std::vector<int> Work;
	std::vector<int> Parent;
	std::vector<int> Level;
	std::vector<std::vector<int>> Distance;
	std::vector<int> Count;
	std::vector<int> SubCount;
	std::vector<long long> Sum;
	std::vector<long long> SubSum;
	void Decompose(int Entry, int Above, int Layer)
	{
		Work.clear();
		Work.push_back(Entry);
		ComponentParent[Entry] = 0;
		for (std::size_t Index = 0; Index < Work.size(); ++Index)
		{
			int u = Work[Index];
			ComponentSize[u] = 1;
			for (int e = Tree.Offset[u]; e < Tree.Offset[u + 1]; ++e)
			{
				int v = Tree.Neighbor[e];
				if (!Removed[v] && v != ComponentParent[u])
				{
					ComponentParent[v] = u;
					Work.push_back(v);
				}
			}
		}
		for (int Index = static_cast<int>(Work.size()) - 1; Index > 0; --Index)
		{
			int u = Work[Index];
			ComponentSize[ComponentParent[u]] += ComponentSize[u];
		}
		int Center = Entry;
		int ComponentCount = static_cast<int>(Work.size());
		for (int u : Work)
		{
			int Largest = ComponentCount - ComponentSize[u];
			for (int e = Tree.Offset[u]; e < Tree.Offset[u + 1]; ++e)
			{
				int v = Tree.Neighbor[e];
				if (!Removed[v] && ComponentParent[v] == u)
				{
					Largest = std::max(Largest, ComponentSize[v]);
				}
			}
			if (Largest * 2 <= ComponentCount)
			{
				Center = u;
				break;
			}
		}
		if (Layer == static_cast<int>(Distance.size()))
		{
			Distance.emplace_back(Tree.n + 1);
		}
		Parent[Center] = Above;
		Level[Center] = Layer;
		Work.clear();
		Work.push_back(Center);
		ComponentParent[Center] = 0;
		Distance[Layer][Center] = 0;
		for (std::size_t Index = 0; Index < Work.size(); ++Index)
		{
			int u = Work[Index];
			for (int e = Tree.Offset[u]; e < Tree.Offset[u + 1]; ++e)
			{
				int v = Tree.Neighbor[e];
				if (!Removed[v] && v != ComponentParent[u])
				{
					ComponentParent[v] = u;
					Distance[Layer][v] = Distance[Layer][u] + 1;
					Work.push_back(v);
				}
			}
		}
		Removed[Center] = true;
		for (int e = Tree.Offset[Center]; e < Tree.Offset[Center + 1]; ++e)
		{
			int v = Tree.Neighbor[e];
			if (!Removed[v])
			{
				Decompose(v, Center, Layer + 1);
			}
		}
	}
public:
	explicit FDistanceSums(const FTree& InTree)
		: Tree(InTree), Removed(Tree.n + 1), ComponentParent(Tree.n + 1), ComponentSize(Tree.n + 1), Parent(Tree.n + 1), Level(Tree.n + 1), Count(Tree.n + 1), SubCount(Tree.n + 1), Sum(Tree.n + 1), SubSum(Tree.n + 1)
	{
		Work.reserve(Tree.n);
		Decompose(1, 0, 0);
	}
	void Insert(int Vertex)
	{
		int Below = 0;
		for (int Center = Vertex; Center != 0; Center = Parent[Center])
		{
			int Length = Distance[Level[Center]][Vertex];
			++Count[Center];
			Sum[Center] += Length;
			if (Below != 0)
			{
				++SubCount[Below];
				SubSum[Below] += Length;
			}
			Below = Center;
		}
	}
	long long Query(int Vertex) const
	{
		long long Answer = 0;
		int Below = 0;
		for (int Center = Vertex; Center != 0; Center = Parent[Center])
		{
			int Length = Distance[Level[Center]][Vertex];
			Answer += Sum[Center] + static_cast<long long>(Count[Center]) * Length;
			if (Below != 0)
			{
				Answer -= SubSum[Below] + static_cast<long long>(SubCount[Below]) * Length;
			}
			Below = Center;
		}
		return Answer;
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FTree Tree(Input);
	FDistanceSums Sums(Tree);
	std::vector<long long> Less(Tree.n + 1);
	std::vector<long long> Equal(Tree.n + 1);
	long long Count = 0;
	long long DepthSum = 0;
	int Start = 0;
	while (Start < Tree.n)
	{
		int End = Start;
		int Depth = Tree.Depth[Tree.Order[Start]];
		while (End < Tree.n && Tree.Depth[Tree.Order[End]] == Depth)
		{
			++End;
		}
		for (int i = Start; i < End; ++i)
		{
			int u = Tree.Order[i];
			Less[u] = ((Depth + 2LL) * Count + DepthSum - Sums.Query(u)) / 2;
		}
		for (int i = Start; i < End; ++i)
		{
			Sums.Insert(Tree.Order[i]);
			++Count;
			DepthSum += Depth;
		}
		for (int i = Start; i < End; ++i)
		{
			int u = Tree.Order[i];
			Equal[u] = ((Depth + 2LL) * Count + DepthSum - Sums.Query(u)) / 2 - Less[u];
		}
		Start = End;
	}
	for (int u = 1; u <= Tree.n; ++u)
	{
		Output.Write(Less[u], ' ');
		Output.Write(Equal[u], ' ');
		Output.Write(Tree.Total[u] - Less[u] - Equal[u]);
	}
}
