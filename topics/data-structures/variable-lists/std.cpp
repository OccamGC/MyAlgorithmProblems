// Problem setter's solution: doubly linked lists with an ID-indexed node pool.
// Codex (GPT-6): explicit initialization, stable storage and boundary validation.
#include <iostream>
#include <vector>

struct FNode
{
	FNode* Previous = nullptr;
	FNode* Next = nullptr;
	int Value = 0;
	int Owner = 0;
	bool bAlive = false;
};

struct FListBank
{
	std::vector<FNode> Pool;
	std::vector<FNode*> Heads;
	std::vector<FNode*> Tails;
	int LastId = 0;

	FListBank(int Count, int Capacity)
		: Pool(Capacity + 1), Heads(Count + 1, nullptr), Tails(Count + 1, nullptr)
	{
	}

	FNode* Find(int Id)
	{
		if (Id < 1 || Id > LastId || !Pool[Id].bAlive)
		{
			return nullptr;
		}
		return &Pool[Id];
	}

	void Insert(int Owner, bool bAtHead)
	{
		FNode* Node = &Pool[++LastId];
		Node->Value = LastId;
		Node->Owner = Owner;
		Node->bAlive = true;
		if (bAtHead)
		{
			Node->Next = Heads[Owner];
			if (Node->Next != nullptr)
			{
				Node->Next->Previous = Node;
			}
			else
			{
				Tails[Owner] = Node;
			}
			Heads[Owner] = Node;
		}
		else
		{
			Node->Previous = Tails[Owner];
			if (Node->Previous != nullptr)
			{
				Node->Previous->Next = Node;
			}
			else
			{
				Heads[Owner] = Node;
			}
			Tails[Owner] = Node;
		}
	}

	void Erase(int Id)
	{
		FNode* Node = Find(Id);
		if (Node == nullptr)
		{
			return;
		}
		if (Node->Previous != nullptr)
		{
			Node->Previous->Next = Node->Next;
		}
		else
		{
			Heads[Node->Owner] = Node->Next;
		}
		if (Node->Next != nullptr)
		{
			Node->Next->Previous = Node->Previous;
		}
		else
		{
			Tails[Node->Owner] = Node->Previous;
		}
		Node->bAlive = false;
	}

	void PrintValue(const FNode* Node)
	{
		if (Node == nullptr)
		{
			std::cout << "NULL";
		}
		else
		{
			std::cout << Node->Value;
		}
	}

	void Query(int Id)
	{
		const FNode* Node = Find(Id);
		if (Node == nullptr)
		{
			std::cout << "NULL NULL NULL\n";
			return;
		}
		PrintValue(Node->Previous);
		std::cout << ' ';
		PrintValue(Node);
		std::cout << ' ';
		PrintValue(Node->Next);
		std::cout << '\n';
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Counts(n + 1);
	int InitialCount = 0;
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Counts[i];
		InitialCount += Counts[i];
	}
	int m;
	std::cin >> m;
	FListBank Lists(n, InitialCount + m);
	for (int i = 1; i <= n; ++i)
	{
		for (int j = 0; j < Counts[i]; ++j)
		{
			Lists.Insert(i, false);
		}
	}
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		int Id;
		std::cin >> Operation >> Id;
		if (Operation == 1)
		{
			Lists.Query(Id);
		}
		else if (Operation == 2)
		{
			Lists.Erase(Id);
		}
		else if (Operation == 3 || Operation == 4)
		{
			Lists.Insert(Id, Operation == 3);
		}
		else
		{
			int x;
			std::cin >> x;
			FNode* Node = Lists.Find(Id);
			if (Node != nullptr)
			{
				Node->Value = x;
			}
		}
	}
}
