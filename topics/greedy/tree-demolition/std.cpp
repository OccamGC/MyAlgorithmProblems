// Problem setter's solution; portable implementation and analysis: GPT-6.
#include <queue>
#include <array>
#include <iterator>

#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <string>
#include <set>
#include <limits>
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

struct FBlock
{
	long long Sum;
	int Size;
	int Root;
	int Last;
	int Version;
	bool operator<(const FBlock& Other) const
	{
		long long Left = Sum * Other.Size;
		long long Right = Other.Sum * Size;
		return Left != Right ? Left < Right : Last < Other.Last;
	}
};

int Find(std::vector<int>& Representative, int u)
{
	int Root = u;
	while (Representative[Root] != Root)
	{
		Root = Representative[Root];
	}
	while (Representative[u] != u)
	{
		int Next = Representative[u];
		Representative[u] = Root;
		u = Next;
	}
	return Root;
}

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	std::vector<int> p(n + 1);
	std::vector<int> Head(n + 1, -1);
	std::vector<int> To(2 * (n - 1));
	std::vector<int> Next(2 * (n - 1));
	for (int u = 1; u <= n; ++u)
	{
		p[u] = Input.Read();
	}
	for (int i = 0; i < n - 1; ++i)
	{
		int u = Input.Read();
		int v = Input.Read();
		To[2 * i] = v;
		Next[2 * i] = Head[u];
		Head[u] = 2 * i;
		To[2 * i + 1] = u;
		Next[2 * i + 1] = Head[v];
		Head[v] = 2 * i + 1;
	}
	std::vector<int> Parent(n + 1);
	std::vector<int> Order{1};
	for (int i = 0; i < n; ++i)
	{
		int u = Order[i];
		for (int e = Head[u]; e != -1; e = Next[e])
		{
			int v = To[e];
			if (v != Parent[u])
			{
				Parent[v] = u;
				Order.push_back(v);
			}
		}
	}
	// A linked list stores each root-first block, including interleaved subtrees.
	std::vector<int> Representative(n + 1);
	std::vector<int> Last(n + 1);
	std::vector<int> Successor(n + 1);
	std::vector<int> Size(n + 1, 1);
	std::vector<int> Version(n + 1);
	std::vector<long long> Sum(p.begin(), p.end());
	std::priority_queue<FBlock> Heap;
	for (int u = 1; u <= n; ++u)
	{
		Representative[u] = u;
		Last[u] = u;
		if (u != 1)
		{
			Heap.push({Sum[u], 1, u, u, 0});
		}
	}
	while (!Heap.empty())
	{
		FBlock Block = Heap.top();
		Heap.pop();
		int u = Block.Root;
		if (Representative[u] != u || Block.Version != Version[u])
		{
			continue;
		}
		int v = Find(Representative, Parent[u]);
		Successor[Last[v]] = u;
		Last[v] = Last[u];
		Sum[v] += Sum[u];
		Size[v] += Size[u];
		Representative[u] = v;
		++Version[v];
		if (v != 1)
		{
			Heap.push({Sum[v], Size[v], v, Last[v], Version[v]});
		}
	}
	Order.clear();
	for (int u = 1; u != 0; u = Successor[u])
	{
		Order.push_back(u);
	}
	std::reverse(Order.begin(), Order.end());
	long long Answer = 0;
	for (int i = 0; i < n; ++i)
	{
		Answer += 1LL * i * p[Order[i]];
	}
	Output.Write(Answer, '\n');
	for (int i = 0; i < n; ++i)
	{
		Output.Write(Order[i], i + 1 == n ? '\n' : ' ');
	}
}
