#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

struct FAffine
{
	long double a = 1;
	long double b = 0;
	long double c = 0;
	long double d = 1;
	long double x = 0;
	long double y = 0;
};

FAffine Compose(const FAffine& After, const FAffine& Before)
{
	return {
		After.a * Before.a + After.b * Before.c,
		After.a * Before.b + After.b * Before.d,
		After.c * Before.a + After.d * Before.c,
		After.c * Before.b + After.d * Before.d,
		After.a * Before.x + After.b * Before.y + After.x,
		After.c * Before.x + After.d * Before.y + After.y
	};
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
			Transform.d = -1;
		}
		else if (Operation == 3)
		{
			Transform.a = -1;
		}
		else if (Operation == 4 || Operation == 5)
		{
			Transform.a = Transform.d = 0;
			Transform.b = Transform.c = Operation == 4 ? 1 : -1;
		}
		else
		{
			int Degrees;
			std::cin >> Degrees;
			long double Angle = Degrees * std::acos(-1.0L) / 180;
			Transform.a = Transform.d = std::cos(Angle);
			Transform.c = std::sin(Angle);
			Transform.b = -Transform.c;
		}
		Tree.Change(l, r, Transform);
	}
	Tree.Print(1, n);
}
