// Codex (GPT-6): monotone Boolean circuit, iterative parsing and event propagation.
// AND/OR gates and work-list evaluation are standard techniques.
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
struct FCircuit
{
	std::vector<int> Head;
	std::vector<int> Need;
	std::vector<int> To;
	std::vector<int> Next;
	explicit FCircuit(int Count) : Head(Count, -1), Need(Count, 1)
	{
	}
	void Link(int From, int Target)
	{
		To.push_back(Target);
		Next.push_back(Head[From]);
		Head[From] = static_cast<int>(To.size()) - 1;
	}
	int Gate(int Left, int Right, char Operator)
	{
		int Id = static_cast<int>(Head.size());
		Head.push_back(-1);
		Need.push_back(Operator == '&' ? 2 : 1);
		Link(Left, Id);
		Link(Right, Id);
		return Id;
	}
	int Parse(const std::string& Text)
	{
		std::vector<int> Values;
		std::vector<char> Operators;
		auto Reduce = [&]()
		{
			int Right = Values.back();
			Values.pop_back();
			int Left = Values.back();
			Values.pop_back();
			char Operator = Operators.back();
			Operators.pop_back();
			Values.push_back(Gate(Left, Right, Operator));
		};
		for (std::size_t i = 0; i < Text.size();)
		{
			unsigned char Symbol = static_cast<unsigned char>(Text[i]);
			if (std::isspace(Symbol))
			{
				++i;
			}
			else if (std::isdigit(Symbol))
			{
				int Id = 0;
				while (i < Text.size() && std::isdigit(static_cast<unsigned char>(Text[i])))
				{
					Id = Id * 10 + Text[i++] - '0';
				}
				Values.push_back(Id - 1);
			}
			else if (Symbol == '(')
			{
				Operators.push_back('(');
				++i;
			}
			else if (Symbol == ')')
			{
				while (Operators.back() != '(')
				{
					Reduce();
				}
				Operators.pop_back();
				++i;
			}
			else
			{
				char Operator = Text[i];
				i += 2;
				while (!Operators.empty() && Operators.back() != '(' && (Operator == '|' || Operators.back() == '&'))
				{
					Reduce();
				}
				Operators.push_back(Operator);
			}
		}
		while (!Operators.empty())
		{
			Reduce();
		}
		return Values.back();
	}
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	FCircuit Circuit(N + M);
	std::string Text;
	std::getline(std::cin, Text);
	for (int i = 0; i < M; ++i)
	{
		std::getline(std::cin, Text);
		int Root = Circuit.Parse(Text);
		Circuit.Link(Root, N + i);
	}
	std::vector<int> Queue;
	for (int i = 0; i < N; ++i)
	{
		Circuit.Need[i] = 0;
		Queue.push_back(i);
	}
	for (std::size_t Front = 0; Front < Queue.size(); ++Front)
	{
		int u = Queue[Front];
		for (int Edge = Circuit.Head[u]; Edge != -1; Edge = Circuit.Next[Edge])
		{
			int v = Circuit.To[Edge];
			if (Circuit.Need[v] > 0 && --Circuit.Need[v] == 0)
			{
				Queue.push_back(v);
			}
		}
	}
	for (int i = 0; i < M; ++i)
	{
		std::cout << (Circuit.Need[N + i] == 0 ? 1 : 0) << '\n';
	}
}
