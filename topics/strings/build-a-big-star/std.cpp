#include <algorithm>
#include <cstddef>
#include <deque>
#include <iostream>

struct FBlock
{
	char Type;
	int Length;
};

class FStarBelt
{
private:
	enum class EEnd
	{
		Front,
		Back
	};

public:
	void InsertLeft(char Mark)
	{
		Blocks.push_front({Mark == '*' ? 'N' : Mark, 1});
		if (Mark == '*')
		{
			Best = std::max(Best, 1);
		}
		while (ReduceEnd(EEnd::Front))
		{
		}
	}

	void InsertRight(char Mark)
	{
		Blocks.push_back({Mark == '*' ? 'N' : Mark, 1});
		if (Mark == '*')
		{
			Best = std::max(Best, 1);
		}
		while (ReduceEnd(EEnd::Back))
		{
		}
	}

	int GetAnswer() const
	{
		return Best;
	}

private:
	std::deque<FBlock> Blocks;
	int Best = 0;

	void AddNeutralBack(int Length)
	{
		Blocks.push_back({'N', Length});
		Best = std::max(Best, Length);
	}

	void AddNeutralFront(int Length)
	{
		Blocks.push_front({'N', Length});
		Best = std::max(Best, Length);
	}

	bool ReduceEnd(EEnd End)
	{
		const bool bFront = End == EEnd::Front;
		if (Blocks.size() < 2)
		{
			return false;
		}

		// Read blocks from the updated end toward the center.
		auto AtEnd = [this, bFront](std::size_t Offset) -> const FBlock&
		{
			return bFront ? Blocks[Offset] : Blocks[Blocks.size() - 1 - Offset];
		};
		const char NearShell = bFront ? '<' : '>';
		const char FarShell = bFront ? '>' : '<';
		int RemovedCount = 0;
		int Length = 0;

		if (AtEnd(0).Type == 'N' && AtEnd(1).Type == 'N')
		{
			RemovedCount = 2;
			Length = AtEnd(0).Length + AtEnd(1).Length;
		}
		else if (AtEnd(0).Type == NearShell && AtEnd(1).Type == FarShell)
		{
			RemovedCount = 2;
			Length = 2;
		}
		else if (Blocks.size() >= 3 && AtEnd(0).Type == NearShell && AtEnd(1).Type == 'N' && AtEnd(2).Type == FarShell)
		{
			RemovedCount = 3;
			Length = AtEnd(1).Length + 2;
		}
		else
		{
			return false;
		}

		for (int i = 0; i < RemovedCount; ++i)
		{
			if (bFront)
			{
				Blocks.pop_front();
			}
			else
			{
				Blocks.pop_back();
			}
		}
		if (bFront)
		{
			AddNeutralFront(Length);
		}
		else
		{
			AddNeutralBack(Length);
		}
		return true;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int n;
	int m;
	if (!(std::cin >> n >> m))
	{
		return 0;
	}
	FStarBelt StarBelt;
	char Mark;
	for (int i = 0; i < n; ++i)
	{
		std::cin >> Mark;
		StarBelt.InsertRight(Mark);
	}
	std::cout << StarBelt.GetAnswer() << '\n';
	for (int i = 0; i < m; ++i)
	{
		int Side;
		std::cin >> Side >> Mark;
		if (Side == 1)
		{
			StarBelt.InsertLeft(Mark);
		}
		else
		{
			StarBelt.InsertRight(Mark);
		}
		std::cout << StarBelt.GetAnswer() << '\n';
	}
}
