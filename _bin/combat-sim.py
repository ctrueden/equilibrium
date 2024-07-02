"""
A combat simulator for the party!
"""

from pathlib import Path
from queue import Queue
from random import choice, randint
from typing import Callable, Dict, List


# -- Constants --


iteration_count = 1
enemy_count = 5


with open(Path(__file__).with_name("names.txt")) as f:
    names = [line.strip() for line in f.readlines()]


# -- Classes --


class Action:
    """ An action performable by an actor, such as a spell or attack. """

    def __init__(self, name: str, f: Callable):
        self.name = name
        self.f = f

    def maybe_do(self, e: "Encounter") -> bool:
        """
        Take the action in appropriate circumstances.
        Returns True iff the action was taken.
        """
        return self.f(e)


class Actor:
    """ Someone participating in an encounter. IMMUTABLE STATE. """

    def __init__(
        self,
        name: str,
        max_hp: int,
        armor_class: int,
        actions: List[Action],
        initiative: int = 0,
        str_save: int = 0,
        dex_save: int = 0,
        con_save: int = 0,
        int_save: int = 0,
        wis_save: int = 0,
        cha_save: int = 0,
    ):
        self.name = name
        self.max_hp = max_hp
        self.armor_class = armor_class
        self.actions = actions
        self.initiative = initiative
        self.str_save = str_save
        self.dex_save = dex_save
        self.con_save = con_save
        self.int_save = int_save
        self.wis_save = wis_save
        self.cha_save = cha_save


    def roll_initiative(self, adv: bool = False, disadv: bool = False) -> int:
        return roll_die(adv=adv, disadv=disadv) + self.initiative


    # NB: For sortability of initiative sequence.
    def __lt__(self, other):
        return False


class Effect:
    """ Some kind of effect in play, typically caused by an action. """
    def __init__(self, mods: Dict[str, int], targets: List[Actor], duration: int, f=None):
        self.mods = mods
        self.targets = targets
        self.duration = duration
        self.f = f

    def __get__(self, name: str):
        return mods.get(name, 0)

    def apply(self, e: "Encounter"):
        if self.f is not None: self.f(e)


class Result:
    pass


class Encounter:
    """ An ongoing combat encounter. """

    def __init__(self, heroes: List[Actor], enemies: List[Actor]):
        self.heroes = heroes
        self.enemies = enemies
        self.armor_class = {actor: actor.armor_class for actor in heroes + enemies}
        self.hp = {actor: actor.max_hp for actor in heroes + enemies}
        self.actions = {actor: actor.actions[:] for actor in heroes + enemies}
        self.effects: List[Effect] = []

    @property
    def heroes_conscious(self) -> int:
        return sum(1 for hero in self.heroes if self.hp[hero] > 0)

    @property
    def enemies_conscious(self) -> int:
        return sum(1 for enemy in self.enemies if self.hp[enemy] > 0)

    def run(self) -> Result:
        """ Run the combat encounter. """

        # Roll initiative!
        actors = self.heroes + self.enemies
        sequence = sorted([(actor.roll_initiative(), actor) for actor in actors], reverse=True)
        queue = Queue()
        for _, actor in sequence: queue.put(actor)
        print("INITIATIVE ORDER:")
        for n, actor in sequence:
            print(f"* {n:2} {actor.name}")

        # Run combat rounds.
        while self.heroes_conscious > 0 and self.enemies_conscious > 0:
            # WHAT'S NEXT?!
            thing = queue.get()
            print(f"== {thing.name} ==")

            # Is this thing actually just an effect in play?
            if isinstance(thing, Effect):
                # Apply the effect and tick down the duration.
                thing.duration -= 1
                if thing.duration > 0:
                    # Effect continues.
                    thing.apply()
                    queue.put(thing)
                else:
                    # Effect ends.
                    self.effects.remove(thing)
                continue

            # Thing must be an Actor; take an action.
            remaining_actions = self.actions[thing]
            done_action = None
            for action in remaining_actions:
                if action.maybe_do(self):
                    done_action = action
                    break

            if done_action is None:
                raise RuntimeError(f"{thing.name} did nothing!")

            # TODO: consider whether some actions should be reusable?
            # For now, we just hardcode the final action as reusable.
            if len(remaining_actions) > 1:
                remaining_actions.remove(done_action)

            queue.put(thing)


        # Accumulate and report results.

        # TODO: report damage taken by actors on each side.
        # - how many rounds combat took.
        # - option for verbose mode showing everything happening.

        print(f"Remaining heroes: {self.heroes_conscious}")
        print(f"Remaining enemies: {self.enemies_conscious}")

        return Result()


# -- Actions --

def attack(e: Encounter, target: Actor) -> bool:
    damage = randint(1, 20)
    e.hp[target] -= damage
    message = f"Attacked {target.name} for {damage} damage! "
    if e.hp[target] > 0: message += f"HP -> {e.hp[target]}/{target.max_hp}"
    else: message += f">>> {target.name} IS DOWN! <<<"
    print(message)
    return True


def attack_hero() -> Action:
    return Action(
        "ATTACKS A HERO",
        lambda e: attack(e, choice([hero for hero in e.heroes if e.hp[hero] > 0]))
    )


def attack_enemy() -> Action:
    return Action(
        "ATTACKS AN ENEMY",
        lambda e: attack(e, choice([enemy for enemy in e.enemies if e.hp[enemy] > 0]))
    )


# -- Functions --


def roll_die(
    dietype: int = 20,
    adv: bool = False,
    disadv: bool = False,
) -> int:
    die_value1 = randint(1, dietype)
    die_value2 = randint(1, dietype)

    if adv and not disadv:
        # Take the better of two rolls.
        return max(die_value1, die_value2)

    if disadv and not adv:
        # Take the worse of two rolls.
        return max(die_value1, die_value2)

    return die_value1


def check_passes(
    dc: int,
    die_value: int,
    total_result: int,
    autopass_on_20: bool = False,
    autofail_on_1: bool = False,
) -> bool:
    """ Return True iff the check meets or exceeds the given DC. """
    if autopass_on_20 and die_value == 20: return True
    if autofail_on_1 and die_value == 1: return False
    return total_result >= dc


def modify_roll(
    die_value: int,
    modifier: int = 0,
) -> int:
    return die_value + modifier


def run_simulation(
    heroes: List[Actor],
    enemies: List[Actor],
    iteration_count,
) -> List[Result]:
    """ Run the entire simulation. """
    return [Encounter(heroes, enemies).run() for _ in range(iteration_count)]


def random_actor():
    return Actor(
        name = choice(names),
        max_hp = 70,
        armor_class = 15,
        actions = [attack_hero()],
    )


# -- Main --


def main():
    # Define PCs.
    bec = Actor(
        # level = 9,
        name = "Bec",
        max_hp = 65, # 8d6 + 33 (average 65)
        armor_class = 13,
        actions = [attack_enemy()],
        # attack_str = 4 + 1
        # attack_dex = 4 + 3
        # attack_int = 4 + 5
        initiative = 3,
        str_save = 1,
        dex_save = 3,
        con_save = 3,
        int_save = 5 + 4, # ERROR: sheet says 5
        wis_save = 3 + 4, # ERROR: sheet says 3
        cha_save = 2,
    )
    cal = Actor(
        # level = 10,
        name = "Cal",
        max_hp = 119, # 4d8 + 5d12 + 58 (average 113)
        armor_class = 20,
        actions = [attack_enemy()],
        # attack_str = 4 + 3
        # attack_dex = 4 + 3
        # sneak_attack = 3d6
        # attack_whip = +8 / 1d4+4
        # attack_torch = +7 / 1d4
        # attack_sunblade = +9 / 1d8+5
        # vs_undead = +2 atk, +2d6+2 dmg
        initiative = 3,
        str_save = 3,
        dex_save = 3 + 4,
        con_save = 5,
        int_save = 0 + 4, # ERROR: sheet says 5
        wis_save = 0,
        cha_save = -1,
    )
    callie = Actor(
        # level = 10,
        name = "Callie",
        max_hp = 85, # 9d8 + 48 (average 93)
        armor_class = 14,
        actions = [attack_enemy()],
        # attack_str = 4 - 1
        # attack_dex = 4 + 0
        # attack_int = 4 + 4
        # attack_wis = 4 + 3
        # attack_cha = 4 + 2
        initiative = 0,
        str_save = -1,
        dex_save = 0,
        con_save = 4,
        int_save = 4,
        wis_save = 3 + 4,
        cha_save = 2 + 4,
    )
    freki = Actor(
        # level = 10,
        name = "Freki",
        max_hp = 65, # 9d10 + 20 (average 74)
        armor_class = 17,
        actions = [attack_enemy()],
        # two attacks per turn, plus swift shot bonus action
        # attack_str = 4 + 2
        # attack_dex = 4 + 5
        initiative = 5, # with advantage in favored terrain
        str_save = 2,
        dex_save = 5 + 4,
        con_save = 1,
        int_save = 1,
        wis_save = 4 + 4,
        cha_save = -1,
    )
    # TODO: freki wolf
    oz = Actor(
        # level = 10,
        name = "Oz",
        max_hp = 110, # 9d8 + 48 (average 93, max 120) # Possible ERROR--or rolled REALLY well?
        armor_class = 18 + 1, # From sheet: why +1?
        actions = [attack_enemy()],
        # attack_str = 4 + 0 + 1 # ioun stone mastery
        # attack_dex = 4 + 5 + 1 # ioun stone mastery
        # sneak_attack = 5d6
        # attack_hornblade = +13 / 1d8+3
        # attack_dagger = +11 / 1d4+1
        initiative = 8,
        str_save = 0,
        dex_save = 5 + 4 + 1,
        con_save = 4,
        int_save = -1 + 4 + 1, # ERROR: sheet says 6
        wis_save = 1,
        cha_save = 3,
    )
    vondal = Actor(
        # level = 10,
        name = "Vondal",
        max_hp = 50,
        armor_class = 13,
        actions = [attack_enemy()],
        # attack_cha = 5 + 4 + 2 # +2 from wand of wonder
        initiative = 0,
        # NB: +1 to ability checks and saves from Luckstone
        str_save = -1 + 1, # ERROR: sheet says -1
        dex_save = 0 + 1, # ERROR: sheet says 0
        con_save = 1 + 4 + 1, # ERROR: sheet says 1
        int_save = 2 + 1, # ERROR: sheet says 2
        wis_save = 2 + 1, # ERROR: sheet says 2
        cha_save = 5 + 4 + 1, # ERROR: sheet says 5
    )
    heroes = [bec, cal, callie, freki, oz, vondal]

    # Randomize enemies.
    enemies = [random_actor() for i in range(enemy_count)]

    # Simulate the encounter repeatedly.
    results = run_simulation(heroes, enemies, iteration_count)

    # Report statistics.
    # TODO: Report final averages, etc.
    print(results)


main()
