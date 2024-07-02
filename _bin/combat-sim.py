"""
A combat simulator for the party!
"""

from queue import Queue
from random import choice, randint
from typing import Callable, Dict, List


# -- Constants --


iteration_count = 1
enemy_count = 5

with open("names.txt") as f:
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
            print(f"It's {thing.name}'s turn!")

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


def attack_hero(e: Encounter) -> bool:
    return attack(e, choice([hero for hero in e.heroes if e.hp[hero] > 0]))


def attack_enemy(e: Encounter) -> bool:
    return attack(e, choice([enemy for enemy in e.enemies if e.hp[enemy] > 0]))


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
        actions = [Action("ATTACKS A HERO", attack_hero)],
    )


# -- Main --


def main():
    # Define PCs.
    bec = Actor(
        name = "Bec",
        max_hp = 50,
        armor_class = 12,
        actions = [Action("ATTACKS AN ENEMY", attack_enemy)],
    )
    cal = Actor(
        name = "Cal",
        max_hp = 90,
        armor_class = 20,
        actions = [Action("ATTACKS AN ENEMY", attack_enemy)],
    )
    callie = Actor(
        name = "Callie",
        max_hp = 70,
        armor_class = 12,
        actions = [Action("ATTACKS AN ENEMY", attack_enemy)],
    )
    freki = Actor(
        name = "Freki",
        max_hp = 50,
        armor_class = 18,
        actions = [Action("ATTACKS AN ENEMY", attack_enemy)],
    )
    oz = Actor(
        name = "Oz",
        max_hp = 65,
        armor_class = 17,
        actions = [Action("ATTACKS AN ENEMY", attack_enemy)],
    )
    vondal = Actor(
        name = "Vondal",
        max_hp = 50,
        armor_class = 13,
        actions = [Action("ATTACKS AN ENEMY", attack_enemy)],
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
