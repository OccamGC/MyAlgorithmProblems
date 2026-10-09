// Problem setter's Hanoi recursion and direct block indexing from the accompanying editorial.
// Codex (GPT-6): preserve complete name lines and organize C++17 implementation.
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

void Move(int Index, int Source, int Target, int Helper)
{
	if (Index == static_cast<int>(Block.size()))
	{
		return;
	}
	Move(Index + 1, Source, Helper, Target);
	Print(Index, Source, Target);
	Move(Index + 1, Helper, Target, Source);
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
	Move(0, 0, 1, 2);
}
