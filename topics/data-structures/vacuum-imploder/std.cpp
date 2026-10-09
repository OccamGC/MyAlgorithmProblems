// Contribution: Codex (GPT-6): long-double specialized tags and safe chronological composition.
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

// Original swap/sign/rotation/translation tags, composed in that order.
struct FAffine
{
	bool bSwap = false;
	bool bNegativeX = false;
	bool bNegativeY = false;
	bool bRotated = false;
	long double Cosine = 1;
	long double Sine = 0;
	long double x = 0;
	long double y = 0;
};

FAffine Compose(const FAffine& After, FAffine Before)
{
	if (After.bSwap)
	{
		std::swap(Before.x, Before.y);
		std::swap(Before.bNegativeX, Before.bNegativeY);
		Before.bSwap = !Before.bSwap;
		Before.Sine = -Before.Sine;
	}
	if (After.bNegativeX)
	{
		Before.x = -Before.x;
		Before.bNegativeX = !Before.bNegativeX;
		Before.Sine = -Before.Sine;
	}
	if (After.bNegativeY)
	{
		Before.y = -Before.y;
		Before.bNegativeY = !Before.bNegativeY;
		Before.Sine = -Before.Sine;
	}
	if (After.bRotated)
	{
		const long double x = Before.x;
		const long double Cosine = Before.Cosine;
		Before.x = After.Cosine * x - After.Sine * Before.y;
		Before.y = After.Sine * x + After.Cosine * Before.y;
		Before.Cosine = After.Cosine * Cosine - After.Sine * Before.Sine;
		Before.Sine = After.Sine * Cosine + After.Cosine * Before.Sine;
		Before.bRotated = true;
	}
	Before.x += After.x;
	Before.y += After.y;
	return Before;
}

class FTransformTree
{
private:

	int n;
	std::vector<FAffine> Tags;

	void Push(int Node)
	{
		Tags[2 * Node] = Compose(Tags[Node], Tags[2 * Node]);
		Tags[2 * Node + 1] = Compose(Tags[Node], Tags[2 * Node + 1]);
		Tags[Node] = FAffine{};
	}

	void Build(int Node, int Left, int Right)
	{
		if (Left == Right)
		{
			std::cin >> Tags[Node].x >> Tags[Node].y;
			return;
		}
		int Middle = (Left + Right) / 2;
		Build(2 * Node, Left, Middle);
		Build(2 * Node + 1, Middle + 1, Right);
	}

	void Change(int Node, int Left, int Right, int l, int r, const FAffine& Transform)
	{
		if (l <= Left && Right <= r)
		{
			Tags[Node] = Compose(Transform, Tags[Node]);
			return;
		}
		Push(Node);
		int Middle = (Left + Right) / 2;
		if (l <= Middle)
		{
			Change(2 * Node, Left, Middle, l, r, Transform);
		}
		if (r > Middle)
		{
			Change(2 * Node + 1, Middle + 1, Right, l, r, Transform);
		}
	}

	void Print(int Node, int Left, int Right, int l, int r)
	{
		if (Left == Right)
		{
			std::cout << Tags[Node].x << ' ' << Tags[Node].y << '\n';
			return;
		}
		Push(Node);
		int Middle = (Left + Right) / 2;
		if (l <= Middle)
		{
			Print(2 * Node, Left, Middle, l, r);
		}
		if (r > Middle)
		{
			Print(2 * Node + 1, Middle + 1, Right, l, r);
		}
	}

public:

	explicit FTransformTree(int Size) : n(Size), Tags(4 * n)
	{
		Build(1, 1, n);
	}

	void Change(int l, int r, const FAffine& Transform)
	{
		Change(1, 1, n, l, r, Transform);
	}

	void Print(int l, int r)
	{
		Print(1, 1, n, l, r);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::cout << std::fixed << std::setprecision(8);
	int n;
	int m;
	std::cin >> n >> m;
	FTransformTree Tree(n);
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		int l;
		int r;
		std::cin >> Operation >> l;
		if (Operation == 7)
		{
			Tree.Print(l, l);
			continue;
		}
		std::cin >> r;
		FAffine Transform;
		if (Operation == 0 || Operation == 1)
		{
			long double Delta;
			std::cin >> Delta;
			(Operation == 0 ? Transform.x : Transform.y) = Delta;
		}
		else if (Operation == 2)
		{
			Transform.bNegativeY = true;
		}
		else if (Operation == 3)
		{
			Transform.bNegativeX = true;
		}
		else if (Operation == 4 || Operation == 5)
		{
			Transform.bSwap = true;
			Transform.bNegativeX = Transform.bNegativeY = Operation == 5;
		}
		else
		{
			int Degrees;
			std::cin >> Degrees;
			long double Angle = Degrees * std::acos(-1.0L) / 180;
			Transform.bRotated = Degrees % 360 != 0;
			Transform.Cosine = std::cos(Angle);
			Transform.Sine = std::sin(Angle);
		}
		Tree.Change(l, r, Transform);
	}
	Tree.Print(1, n);
}
