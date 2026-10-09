// Problem setter's solution: split inorder intervals at the next preorder root.
// Codex (GPT-6): explicit work stack preserves postorder at million-node depth.
#include <iostream>
#include <vector>

struct FTask
{
	int Left;
	int Right;
	int Root; // Zero: visit an interval. Nonzero: emit this root.
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Preorder(n);
	std::vector<int> Position(n + 1);
	for (int& Value : Preorder)
	{
		std::cin >> Value;
	}
	for (int i = 0; i < n; ++i)
	{
		int Value;
		std::cin >> Value;
		Position[Value] = i;
	}
	std::vector<FTask> Stack;
	Stack.reserve(2 * n);
	Stack.push_back({0, n - 1, 0});
	int Cursor = 0;
	bool bFirst = true;
	while (!Stack.empty())
	{
		FTask Task = Stack.back();
		Stack.pop_back();
		if (Task.Root != 0)
		{
			if (!bFirst)
			{
				std::cout << ' ';
			}
			bFirst = false;
			std::cout << Task.Root;
			continue;
		}
		int Root = Preorder[Cursor++];
		int Middle = Position[Root];
		Stack.push_back({0, 0, Root});
		if (Middle < Task.Right)
		{
			Stack.push_back({Middle + 1, Task.Right, 0});
		}
		if (Task.Left < Middle)
		{
			Stack.push_back({Task.Left, Middle - 1, 0});
		}
	}
	std::cout << '\n';
}
