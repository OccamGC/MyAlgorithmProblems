// Explicit-stack simulation. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdio>
#include <string>
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
	std::string Token()
	{
		std::string Result;
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		while (Character > ' ' && Character != EOF)
		{
			Result.push_back(static_cast<char>(Character));
			Character = Get();
		}
		return Result;
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

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::string Operations = m == 0 ? std::string{} : Input.Token();
	int Waiting = 0;
	int Needed = 0;
	for (char Operation : Operations)
	{
		if (Operation == '0')
		{
			++Waiting;
		}
		else if (Waiting > 0)
		{
			--Waiting;
			++Needed;
		}
	}
	// IDs above Needed cannot be used, even if the input offers more stacks.
	int Slots = std::min(n, Needed);
	std::vector<int> Top(Slots + 1);
	std::vector<int> Previous(Slots + 1);
	std::vector<int> Following(Slots + 1);
	std::vector<int> Free;
	for (int i = 1; i <= Slots; ++i)
	{
		Free.push_back(i);
	}
	std::vector<int> Owner(Needed + 1);
	std::vector<int> Below(Needed + 1);
	auto Acquire = [&]()
	{
		int Id = Free.back();
		Free.pop_back();
		int First = Following[0];
		Following[Id] = First;
		Previous[Id] = 0;
		Previous[First] = Id;
		Following[0] = Id;
		return Id;
	};
	auto Release = [&](int Id)
	{
		Following[Previous[Id]] = Following[Id];
		Previous[Following[Id]] = Previous[Id];
		Free.push_back(Id);
	};
	auto Push = [&](int Item, int Id)
	{
		Owner[Item] = Id;
		Below[Item] = Top[Id];
		Top[Id] = Item;
	};
	int Pushed = 0;
	int Popped = 0;
	int Cost = 0;
	for (char Operation : Operations)
	{
		if (Operation == '0' && Pushed < Needed)
		{
			int Id = Free.empty() ? Owner[Pushed] : Acquire();
			Push(++Pushed, Id);
			++Cost;
		}
		else if (Operation == '1' && Popped < Pushed)
		{
			int Target = ++Popped;
			int Id = Owner[Target];
			if (Top[Id] != Target)
			{
				int Other = Following[0] == Id ? Following[Id] : Following[0];
				if (Other == 0)
				{
					Other = Acquire();
				}
				while (Top[Id] != Target)
				{
					int Item = Top[Id];
					Top[Id] = Below[Item];
					Push(Item, Other);
					Cost += 2;
				}
			}
			Top[Id] = Below[Target];
			++Cost;
			if (Top[Id] == 0)
			{
				Release(Id);
			}
		}
	}
	Output.Write(Cost);
}
