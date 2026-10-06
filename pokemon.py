import sys
import time
import random
from dataclasses import dataclass


def delay_print(text: str, delay: float = 0.03):
    # retro terminal feel
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# type effectiveness map: attacker -> defender -> multiplier
TYPE_CHART = {
    "Fire":  {"Grass": 2.0, "Water": 0.5, "Fire": 0.5},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Water": 0.5},
    "Grass": {"Water": 2.0, "Fire": 0.5, "Grass": 0.5},
}


@dataclass
class Pokemon:
    name: str
    pokemon_type: str
    moves: list[str]
    attack: int
    defense: int
    max_bars: int = 20
    current_bars: int = 20

    def __post_init__(self):
        self.current_bars = self.max_bars

    @property
    def level(self) -> int:
        return int(3 * (1 + (self.attack + self.defense) / 2))

    @property
    def health_bar(self) -> str:
        filled = max(0, int((self.current_bars / self.max_bars) * 20))
        return f"[{'=' * filled}{' ' * (20 - filled)}] {max(0, self.current_bars)}/{self.max_bars} HP"

    def get_effectiveness(self, opponent_type: str) -> tuple[float, str]:
        multiplier = TYPE_CHART.get(self.pokemon_type, {}).get(opponent_type, 1.0)
        if multiplier > 1.0:
            return multiplier, "It's super effective!"
        elif multiplier < 1.0:
            return multiplier, "It's not very effective..."
        return multiplier, "Normal effectiveness."

    def choose_move(self, is_bot: bool = False) -> str:
        # AI choice
        if is_bot:
            chosen = random.choice(self.moves)
            time.sleep(0.6)
            return chosen

        print(f"\nGo {self.name}!")
        for idx, move in enumerate(self.moves, 1):
            print(f"  {idx}. {move}")

        while True:
            choice = input(f"Pick a move (1-{len(self.moves)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(self.moves):
                return self.moves[int(choice) - 1]
            print(f"Invalid option. Please enter a number between 1 and {len(self.moves)}.")

    def fight(self, opponent: "Pokemon", opponent_is_bot: bool = True):
        print("\n" + "=" * 25 + " POKÉMON BATTLE " + "=" * 25)
        for p in (self, opponent):
            print(f"\n{p.name.upper()} (Type: {p.pokemon_type})")
            print(f"  Level:   {p.level}")
            print(f"  Attack:  {p.attack} | Defense: {p.defense}")
        print("\n" + "=" * 66 + "\n")
        time.sleep(1.5)

        turn = 0
        combatants = [(self, opponent, False), (opponent, self, opponent_is_bot)]

        while self.current_bars > 0 and opponent.current_bars > 0:
            attacker, defender, is_bot = combatants[turn % 2]

            # display battle field
            print(f"\n{self.name.ljust(15)} {self.health_bar}")
            print(f"{opponent.name.ljust(15)} {opponent.health_bar}\n")

            # move selection & execution
            move = attacker.choose_move(is_bot=is_bot)
            delay_print(f"{attacker.name} used {move}!")

            # damage calculation
            multiplier, message = attacker.get_effectiveness(defender.pokemon_type)
            delay_print(f"-> {message}")

            raw_damage = max(1, attacker.attack * multiplier - (defender.defense * 0.25))
            defender.current_bars = max(0, int(defender.current_bars - raw_damage))

            time.sleep(0.8)

            if defender.current_bars <= 0:
                print(f"\n{self.name.ljust(15)} {self.health_bar}")
                print(f"{opponent.name.ljust(15)} {opponent.health_bar}\n")
                delay_print(f"*** {defender.name} fainted! ***")
                break

            turn += 1

        # post-battle resolution
        if self.current_bars > 0:
            reward = random.randint(500, 3000)
            delay_print(f"\nYou won the battle! Opponent paid you ${reward}.\n")
        else:
            delay_print(f"\nYou were defeated by {opponent.name}...\n")


if __name__ == "__main__":
    charizard = Pokemon(
        name="Charizard",
        pokemon_type="Fire",
        moves=["Flamethrower", "Fly", "Blast Burn", "Fire Punch"],
        attack=12,
        defense=8,
    )
    blastoise = Pokemon(
        name="Blastoise",
        pokemon_type="Water",
        moves=["Water Gun", "Bubble Beam", "Hydro Pump", "Surf"],
        attack=10,
        defense=10,
    )

    # battle starts
    blastoise.fight(charizard, opponent_is_bot=True)