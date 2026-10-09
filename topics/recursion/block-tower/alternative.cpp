// Codex (GPT-6): supply and verify the established step-number Hanoi construction.
#include <array>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

std::array<std::string, 3> Platform;
std::vector<std::string> Block;

void Print(int Index, int Source, int Target)
{
	std::cout << "Move " << Block[Index] << " from " << Platform[Source]
		<< " to " << Platform[Target] << ".\n";
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	for (std::string& Name : Platform)
	{
		std::getline(std::cin, Name);
	}
	Block.resize(n);
	for (std::string& Name : Block)
	{
		std::getline(std::cin, Name);
	}
	for (int Step = 1; Step < (1 << n); ++Step)
	{
		int d = 1;
		int Remaining = Step;
		while (Remaining % 2 == 0)
		{
			++d;
			Remaining /= 2;
		}
		int Direction = (n - d) % 2 == 0 ? 1 : 2;
		int EarlierMoves = Step >> d;
		int Source = EarlierMoves * Direction % 3;
		int Target = (Source + Direction) % 3;
		Print(n - d, Source, Target);
	}
}
