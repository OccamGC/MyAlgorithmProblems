// Problem setter's quotient events and monotone defence sweep.
// Exact bounded comparisons, portable wide buckets and implementation: GPT-6.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <vector>

using Integer = long long;
constexpr Integer End = std::numeric_limits<Integer>::max() / 4;

Integer CeilPositive(Integer Numerator, Integer Denominator)
{
	return Numerator <= 0 ? 0 : (Numerator - 1) / Denominator + 1;
}

struct FEnemy
{
	Integer Number;
	Integer Health;
	Integer Defence;
	Integer Attack;
	Integer Turns = 0;
};
std::vector<FEnemy> Enemies;
Integer InitialAttack;
Integer AttackStep;

Integer NextEvent(int Index, Integer x)
{
	const FEnemy& Enemy = Enemies[Index];
	Integer Damage = InitialAttack + x * AttackStep - Enemy.Defence;
	Integer Turns = CeilPositive(Enemy.Health, Damage);
	if (Turns <= 1)
	{
		return End;
	}
	Integer NextDamage = CeilPositive(Enemy.Health, Turns - 1);
	return CeilPositive(Enemy.Defence + NextDamage - InitialAttack, AttackStep);
}

struct FWideBucket
{
	static constexpr std::uint64_t Base = 1000000000;
	std::uint64_t High = 0;
	std::uint64_t Low = 0;
	void Add(std::uint64_t Value)
	{
		Low += Value % Base;
		High += Value / Base + Low / Base;
		Low %= Base;
	}
	void Subtract(std::uint64_t Value)
	{
		std::uint64_t Remainder = Value % Base;
		High -= Value / Base;
		if (Low < Remainder)
		{
			--High;
			Low += Base;
		}
		Low -= Remainder;
	}
	bool Fits(Integer Bound) const
	{
		return High < static_cast<std::uint64_t>(Bound) / Base
			|| (High == static_cast<std::uint64_t>(Bound) / Base
				&& Low <= static_cast<std::uint64_t>(Bound) % Base);
	}
	Integer SmallValue() const
	{
		return static_cast<Integer>(High * Base + Low);
	}
};

struct FEvent
{
	Integer Attack;
	int Enemy;
	bool operator>(const FEvent& Other) const
	{
		return Attack != Other.Attack ? Attack > Other.Attack : Enemy > Other.Enemy;
	}
};

class FHeapSchedule
{
private:
	std::priority_queue<FEvent, std::vector<FEvent>, std::greater<FEvent>> Queue;
public:
	FHeapSchedule(Integer Low, Integer, Integer InitialDefence)
	{
		for (int i = 0; i < static_cast<int>(Enemies.size()); ++i)
		{
			if (Enemies[i].Attack > InitialDefence)
			{
				Reschedule(i, Low);
			}
		}
	}
	Integer Next()
	{
		return Queue.empty() ? End : Queue.top().Attack;
	}
	int Pop()
	{
		int Result = Queue.top().Enemy;
		Queue.pop();
		return Result;
	}
	void Reschedule(int Index, Integer x)
	{
		Integer NextAttack = NextEvent(Index, x);
		if (NextAttack != End)
		{
			Queue.push({NextAttack, Index});
		}
	}
};

class FArraySchedule
{
private:
	struct FLink
	{
		int Enemy;
		int Next;
	};
	std::vector<int> Head;
	std::vector<FLink> Links;
	int Cursor;
public:
	FArraySchedule(Integer Low, Integer High, Integer InitialDefence) : Head(High + 1, -1),
		Cursor(static_cast<int>(Low))
	{
		std::size_t Reserve = 0;
		for (const FEnemy& Enemy : Enemies)
		{
			if (Enemy.Attack > InitialDefence)
			{
				Reserve += 2 * static_cast<int>(std::sqrt(static_cast<double>(Enemy.Health))) + 4;
			}
		}
		Links.reserve(Reserve);
		for (int i = 0; i < static_cast<int>(Enemies.size()); ++i)
		{
			if (Enemies[i].Attack <= InitialDefence)
			{
				continue;
			}
			for (Integer x = NextEvent(i, Low); x <= High; x = NextEvent(i, x))
			{
				Links.push_back({i, Head[x]});
				Head[x] = static_cast<int>(Links.size()) - 1;
			}
		}
	}
	Integer Next()
	{
		while (Cursor < static_cast<int>(Head.size()) && Head[Cursor] == -1)
		{
			++Cursor;
		}
		return Cursor == static_cast<int>(Head.size()) ? End : Cursor;
	}
	int Pop()
	{
		int Index = Head[Cursor];
		Head[Cursor] = Links[Index].Next;
		return Links[Index].Enemy;
	}
	void Reschedule(int, Integer)
	{
	}
};

using FSchedule = FHeapSchedule;

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	Integer InitialHealth;
	Integer InitialDefence;
	Integer HealthPrice;
	Integer DefencePrice;
	Integer DefenceStep;
	Integer AttackPrice;
	std::cin >> n >> InitialHealth >> InitialDefence >> InitialAttack;
	std::cin >> HealthPrice >> DefencePrice >> DefenceStep >> AttackPrice >> AttackStep;
	Enemies.resize(n);
	Integer Low = 0;
	Integer High = 0;
	Integer DefenceCount = 0;
	for (FEnemy& Enemy : Enemies)
	{
		std::cin >> Enemy.Number >> Enemy.Health >> Enemy.Defence >> Enemy.Attack;
		Low = std::max(Low, CeilPositive(Enemy.Defence + 1 - InitialAttack, AttackStep));
		High = std::max(High, CeilPositive(Enemy.Defence + Enemy.Health - InitialAttack, AttackStep));
		DefenceCount = std::max(DefenceCount, CeilPositive(Enemy.Attack - InitialDefence, DefenceStep));
	}
	FSchedule Schedule(Low, High, InitialDefence);
	std::vector<Integer> BucketTimes(DefenceCount + 1);
	std::vector<FWideBucket> BucketValue(DefenceCount + 1);
	Integer ActiveTimes = 0;
	Integer Damage = 0;
	for (FEnemy& Enemy : Enemies)
	{
		Enemy.Turns = CeilPositive(Enemy.Health, InitialAttack + Low * AttackStep - Enemy.Defence);
		if (Enemy.Attack <= InitialDefence)
		{
			continue;
		}
		Integer Position = (Enemy.Attack - InitialDefence) / DefenceStep;
		Integer Times = Enemy.Number * Enemy.Turns;
		if (Position >= DefenceCount)
		{
			ActiveTimes += Times;
		}
		else
		{
			BucketTimes[Position] += Times;
			BucketValue[Position].Add(Times * ((Enemy.Attack - InitialDefence) % DefenceStep));
		}
	}
	std::array<Integer, 4> Best{End, End, End, End};
	for (Integer x = Low; x != End; x = Schedule.Next())
	{
		while (Schedule.Next() == x)
		{
			int Index = Schedule.Pop();
			FEnemy& Enemy = Enemies[Index];
			Integer Turns = CeilPositive(Enemy.Health, InitialAttack + x * AttackStep - Enemy.Defence);
			Integer Decrease = Enemy.Number * (Enemy.Turns - Turns);
			Enemy.Turns = Turns;
			Integer Position = (Enemy.Attack - InitialDefence) / DefenceStep;
			if (Position >= DefenceCount)
			{
				ActiveTimes -= Decrease;
				Damage -= Decrease * (Enemy.Attack - InitialDefence - DefenceCount * DefenceStep);
			}
			else
			{
				BucketTimes[Position] -= Decrease;
				BucketValue[Position].Subtract(Decrease * ((Enemy.Attack - InitialDefence) % DefenceStep));
			}
			Schedule.Reschedule(Index, x);
		}
		while (DefenceCount > 0)
		{
			Integer ExtraHealth = std::max(Damage + 1 - InitialHealth, 0LL);
			Integer Allowance = InitialHealth - 1 + ExtraHealth
				+ (DefencePrice - 1) / HealthPrice - Damage;
			const FWideBucket& Value = BucketValue[DefenceCount - 1];
			if (!Value.Fits(Allowance))
			{
				break;
			}
			Integer Remainder = Value.SmallValue();
			if (ActiveTimes > (Allowance - Remainder) / DefenceStep)
			{
				break;
			}
			Damage += ActiveTimes * DefenceStep + Remainder;
			--DefenceCount;
			ActiveTimes += BucketTimes[DefenceCount];
		}
		Integer ExtraHealth = std::max(Damage + 1 - InitialHealth, 0LL);
		Integer Cost = x * AttackPrice + DefenceCount * DefencePrice + ExtraHealth * HealthPrice;
		std::array<Integer, 4> Candidate{Cost, InitialHealth + ExtraHealth,
			InitialDefence + DefenceCount * DefenceStep, InitialAttack + x * AttackStep};
		Best = std::min(Best, Candidate);
	}
	std::cout << Best[0] << '\n' << Best[1] << ' ' << Best[2] << ' ' << Best[3] << '\n';
}
