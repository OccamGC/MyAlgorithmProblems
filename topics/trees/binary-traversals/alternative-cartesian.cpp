// Codex (GPT-6): preorder ranks turn reconstruction into a minimum Cartesian tree.
// The monotone-stack Cartesian-tree algorithm is an established technique.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Rank(n + 1);
	std::vector<int> Inorder(n);
	for (int i = 0; i < n; ++i)
	{
		int Value;
		std::cin >> Value;
		Rank[Value] = i;
	}
	for (int& Value : Inorder)
	{
		std::cin >> Value;
	}
	std::vector<int> Left(n, -1);
	std::vector<int> Right(n, -1);
	std::vector<int> Stack;
	Stack.reserve(n);
	for (int i = 0; i < n; ++i)
	{
		int Last = -1;
		while (!Stack.empty() && Rank[Inorder[Stack.back()]] > Rank[Inorder[i]])
		{
			Last = Stack.back();
			Stack.pop_back();
		}
		Left[i] = Last;
		if (!Stack.empty())
		{
			Right[Stack.back()] = i;
		}
		Stack.push_back(i);
	}
	int Root = Stack.front();
	Stack.clear();
	Stack.push_back(Root);
	std::vector<int> Order;
	Order.reserve(n);
	while (!Stack.empty())
	{
		int u = Stack.back();
		Stack.pop_back();
		Order.push_back(Inorder[u]);
		if (Left[u] != -1)
		{
			Stack.push_back(Left[u]);
		}
		if (Right[u] != -1)
		{
			Stack.push_back(Right[u]);
		}
	}
	std::reverse(Order.begin(), Order.end());
	for (int i = 0; i < n; ++i)
	{
		std::cout << (i == 0 ? "" : " ") << Order[i];
	}
	std::cout << '\n';
}
