// Shortest-path DAG. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <array>
#include <cstdio>
#include <string>
#include <utility>
#include <vector>
#include <functional>
#include <queue>
#include <utility>

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
		long long Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return static_cast<int>(bNegative ? -Value : Value);
	}
	std::string Token()
	{
		std::string Result;
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		while (Character > ' ' && Character != EOF)
		{
			Result.push_back(static_cast<char>(Character));
			Character = Get();
		}
		return Result;
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

struct FChunk
{
	std::array<char, 5> Text{};
	int Length = 0;
	int Position = 0;
	bool bSeen = false;
};
struct FEdge
{
	int u;
	int v;
	int NextIn;
	int NextOut;
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	int k = Input.Read();
	std::vector<FChunk> Chunks(n + m + 1);
	auto Read = [&](int Id)
	{
		auto Text = Input.Token();
		std::copy(Text.begin(), Text.end(), Chunks[Id].Text.begin());
		Chunks[Id].Length = static_cast<int>(Text.size());
	};
	for (int u = 1; u <= n; ++u)
	{
		Read(u);
	}
	std::vector<int> Starts(k);
	for (int& u : Starts)
	{
		u = Input.Read();
	}
	std::vector<int> In(n + 1, -1);
	std::vector<int> Out(n + 1, -1);
	std::vector<FEdge> Edges(m);
	for (int e = 0; e < m; ++e)
	{
		int u = Input.Read();
		int v = Input.Read();
		Read(n + 1 + e);
		Edges[e] = {u, v, In[v], Out[u]};
		In[v] = e;
		Out[u] = e;
	}

	constexpr int Infinity = 1000000000;
	std::vector<int> Distance(n + 1, Infinity);
	using FEntry = std::pair<int, int>;
	std::priority_queue<FEntry, std::vector<FEntry>, std::greater<FEntry>> Heap;
	Distance[1] = Chunks[1].Length;
	Heap.emplace(Distance[1], 1);
	while (!Heap.empty())
	{
		auto [Cost, v] = Heap.top();
		Heap.pop();
		if (Distance[v] != Cost)
		{
			continue;
		}
		for (int e = In[v]; e >= 0; e = Edges[e].NextIn)
		{
			int u = Edges[e].u;
			int NewCost = Cost + Chunks[u].Length + Chunks[n + 1 + e].Length;
			if (NewCost < Distance[u])
			{
				Distance[u] = NewCost;
				Heap.emplace(NewCost, u);
			}
		}
	}
	int Length = Infinity;
	for (int u : Starts)
	{
		Length = std::min(Length, Distance[u]);
	}
	std::vector<char> Usable(m);
	for (int e = 0; e < m; ++e)
	{
		int u = Edges[e].u;
		int v = Edges[e].v;
		Usable[e] = Distance[u] == Chunks[u].Length + Chunks[n + 1 + e].Length + Distance[v];
	}
	std::vector<int> Active;
	std::vector<int> Next;
	auto Enter = [&](int Id, std::vector<int>& Set)
	{
		if (!Chunks[Id].bSeen)
		{
			Chunks[Id].bSeen = true;
			Set.push_back(Id);
		}
	};
	for (int u : Starts)
	{
		if (Distance[u] == Length)
		{
			Enter(u, Active);
		}
	}
	std::string Answer;
	for (int i = 0; i < Length; ++i)
	{
		char Least = '1';
		for (int Id : Active)
		{
			Least = std::min(Least, Chunks[Id].Text[Chunks[Id].Position]);
		}
		Answer.push_back(Least);
		Next.clear();
		for (int Id : Active)
		{
			auto& Chunk = Chunks[Id];
			if (Chunk.Text[Chunk.Position] != Least)
			{
				continue;
			}
			if (++Chunk.Position < Chunk.Length)
			{
				Next.push_back(Id);
			}
			else if (Id > n)
			{
				Enter(Edges[Id - n - 1].v, Next);
			}
			else
			{
				for (int e = Out[Id]; e >= 0; e = Edges[e].NextOut)
				{
					if (Usable[e])
					{
						Enter(n + 1 + e, Next);
					}
				}
			}
		}
		Active.swap(Next);
	}

	auto Fits = [&](int Id, int Position)
	{
		const auto& Chunk = Chunks[Id];
		return Position >= 0 && Position + Chunk.Length <= Length
			&& std::equal(Chunk.Text.begin(), Chunk.Text.begin() + Chunk.Length, Answer.begin() + Position);
	};
	std::vector<char> Reachable(n + 1);
	std::vector<int> Queue;
	for (int u : Starts)
	{
		if (Distance[u] == Length && Fits(u, 0) && !Reachable[u])
		{
			Reachable[u] = true;
			Queue.push_back(u);
		}
	}
	for (std::size_t i = 0; i < Queue.size(); ++i)
	{
		int u = Queue[i];
		for (int e = Out[u]; e >= 0; e = Edges[e].NextOut)
		{
			int v = Edges[e].v;
			Usable[e] = Usable[e] && Fits(n + 1 + e, Length - Distance[u] + Chunks[u].Length)
				&& Fits(v, Length - Distance[v]);
			if (Usable[e] && !Reachable[v])
			{
				Reachable[v] = true;
				Queue.push_back(v);
			}
		}
	}
	std::vector<int> Path{1};
	while (Distance[Path.back()] < Length)
	{
		int Smallest = n + 1;
		for (int e = In[Path.back()]; e >= 0; e = Edges[e].NextIn)
		{
			if (Usable[e] && Reachable[Edges[e].u])
			{
				Smallest = std::min(Smallest, Edges[e].u);
			}
		}
		Path.push_back(Smallest);
	}
	for (char c : Answer)
	{
		Output.Put(c);
	}
	Output.Put('\n');
	for (auto It = Path.rbegin(); It != Path.rend(); ++It)
	{
		Output.Write(*It, It + 1 == Path.rend() ? '\n' : ' ');
	}
}
