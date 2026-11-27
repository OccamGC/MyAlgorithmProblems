// Direct tree simulation. C++17 implementation by Codex (GPT-6).
#include <cstdio>
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

struct FNode
{
	int Value;
	int Count = 1;
	int Parent = 0;
	int Left = 0;
	int Right = 0;
};

class FSearchTree
{
	std::vector<FNode> Nodes{FNode{0}};
	int Root = 0;
public:
	void Insert(int Value)
	{
		int Current = Root;
		int Parent = 0;
		bool bRight = false;
		while (Current != 0)
		{
			if (Nodes[Current].Value == Value)
			{
				++Nodes[Current].Count;
				return;
			}
			Parent = Current;
			bRight = Value > Nodes[Current].Value;
			Current = bRight ? Nodes[Current].Right : Nodes[Current].Left;
		}
		int Node = static_cast<int>(Nodes.size());
		Nodes.push_back({Value, 1, Parent, 0, 0});
		if (Parent == 0)
		{
			Root = Node;
		}
		else if (bRight)
		{
			Nodes[Parent].Right = Node;
		}
		else
		{
			Nodes[Parent].Left = Node;
		}
	}
	void Erase(int Value)
	{
		int Node = Root;
		while (Node != 0 && Nodes[Node].Value != Value)
		{
			Node = Value < Nodes[Node].Value ? Nodes[Node].Left : Nodes[Node].Right;
		}
		if (Node == 0)
		{
			return;
		}
		if (--Nodes[Node].Count != 0)
		{
			return;
		}
		if (Nodes[Node].Left != 0 && Nodes[Node].Right != 0)
		{
			int Other = Nodes[Node].Right;
			while (Nodes[Other].Left != 0)
			{
				Other = Nodes[Other].Left;
			}
			Nodes[Node].Value = Nodes[Other].Value;
			Nodes[Node].Count = Nodes[Other].Count;
			Node = Other;
		}
		int Child = Nodes[Node].Left != 0 ? Nodes[Node].Left : Nodes[Node].Right;
		int Parent = Nodes[Node].Parent;
		if (Parent == 0)
		{
			Root = Child;
		}
		else if (Nodes[Parent].Left == Node)
		{
			Nodes[Parent].Left = Child;
		}
		else
		{
			Nodes[Parent].Right = Child;
		}
		if (Child != 0)
		{
			Nodes[Child].Parent = Parent;
		}
	}
	void Print(FOutput& Output) const
	{
		std::vector<int> Stack;
		if (Root != 0)
		{
			Stack.push_back(Root);
		}
		while (!Stack.empty())
		{
			int Node = Stack.back();
			Stack.pop_back();
			if (Nodes[Node].Right != 0)
			{
				Stack.push_back(Nodes[Node].Right);
			}
			if (Nodes[Node].Left != 0)
			{
				Stack.push_back(Nodes[Node].Left);
			}
			Output.Write(Nodes[Node].Value, Stack.empty() ? '\n' : ' ');
		}
		if (Root == 0)
		{
			Output.Put('\n');
		}
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FSearchTree Tree;
	int m = Input.Read();
	for (int i = 0; i < m; ++i)
	{
		int Operation = Input.Read();
		if (Operation == 0)
		{
			Tree.Print(Output);
		}
		else if (Operation == 1)
		{
			Tree.Insert(Input.Read());
		}
		else
		{
			Tree.Erase(Input.Read());
		}
	}
}
