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
        self.actions = []
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


def attack(
    e: Encounter,
    attacker: Actor,
    hit_mod: int,
    damage_dice: List[int],
    damage_base: int,
    targets: List[Actor]
) -> bool:
    target = choice([target for target in targets if e.hp[target] > 0])
    print(f"{attacker.name} attacks {target.name}!")

    die_value = roll_die()
    check_result = die_value + hit_mod
    target_ac = e.armor_class[target]
    hit = die_value == 20 or (die_value != 1 and check_result >= target_ac)
    print(f"* Rolled {die_value} -> {check_result} vs AC {target_ac}: {'HIT' if hit else 'MISS'}")

    if hit:
        damage = sum(roll_die(damage_die) for damage_die in damage_dice) + damage_base
        e.hp[target] -= damage
        message = f"* {target.name} takes {damage} damage! "
        if e.hp[target] > 0: message += f"HP -> {e.hp[target]}/{target.max_hp}"
        else: message += f">>> {target.name} IS DOWN! <<<"
        print(message)

    return True


def attack_hero(attacker: Actor, hit_mod: int, damage_dice: List[int], damage_base: int) -> Action:
    return Action(
        "{attacker.name} ATTACKS",
        lambda e: attack(e, attacker, hit_mod, damage_dice, damage_base, e.heroes)
    )


def attack_enemy(attacker: Actor, hit_mod: int, damage_dice: List[int], damage_base: int) -> Action:
    return Action(
        f"{attacker.name} ATTACKS",
        lambda e: attack(e, attacker, hit_mod, damage_dice, damage_base, e.enemies)
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


def random_enemy():
    enemy = Actor(
        name = choice(names),
        max_hp = 70,
        armor_class = 15,
    )
    enemy.actions += [attack_hero(enemy, 8, [12, 12], 5)] # TODO: Use better numbers.
    return enemy


# -- Main --


def main():
    # -- Define PCs --

    bec = Actor(
        # level = 9,
        name = "Bec",
        max_hp = 65, # 8d6 + 33 (average 65)
        armor_class = 13,
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
    bec.actions += [
        attack_enemy(bec, 9, [6, 6, 6], 3) # TODO
    ]

    cal = Actor(
        # level = 10,
        name = "Cal",
        max_hp = 119, # 4d8 + 5d12 + 58 (average 113)
        armor_class = 20,
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
    cal.actions += [
        # TODO: two attacks -- sneak attack only once upon hitting
        attack_enemy(cal, 9, [8, 6, 6, 6], 5), # sunblade
        #attack_enemy(cal, 8, [4, 6, 6, 6], 4), # whip
        #attack_enemy(cal, 7, [4, 6, 6, 6], 0), # torch
    ]
    # ERROR: Cal's speed should be 35, not 25, due to Fast Movement.

    callie = Actor(
        # level = 10,
        name = "Callie",
        max_hp = 85, # 9d8 + 48 (average 93)
        armor_class = 14,
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
    callie.actions += [
        attack_enemy(callie, 3, [4], -1) # dagger
    ]

    freki = Actor(
        # level = 10,
        name = "Freki",
        max_hp = 65, # 9d10 + 20 (average 74)
        armor_class = 17,
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
    freki.actions += [
        # TODO: two attacks plus bonus action swift shot
        attack_enemy(freki, 9, [8], 5) # TODO
    ]

    # TODO: freki wolf

    oz = Actor(
        # level = 10,
        name = "Oz",
        max_hp = 110, # 9d8 + 48 (average 93, max 120) # Possible ERROR--or rolled REALLY well?
        armor_class = 18 + 1, # From sheet: why +1?
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
    oz.actions += [
        # TODO: two attacks from two-weapon fighting -- sneak attack only once upon hitting
        attack_enemy(oz, 9, [6, 6, 6, 6, 6, 6], 5) # TODO
    ]

    vondal = Actor(
        # level = 10,
        name = "Vondal",
        max_hp = 50,
        armor_class = 13,
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
    vondal.actions += [
        attack_enemy(vondal, 9, [4, 4, 4, 4], 4) # TODO
    ]

    heroes = [bec, cal, callie, freki, oz, vondal]

    # Randomize enemies.
    enemies = [random_enemy() for i in range(enemy_count)]

    # Simulate the encounter repeatedly.
    results = run_simulation(heroes, enemies, iteration_count)

    # Report statistics.
    # TODO: Report final averages, etc.
    print(results)


main()
