import itertools

def mid(day1, day2):
    if (day2 < day1): day2 += 360
    return ((day1 + day2) // 2) % 360

def num_days(solstice, index):
    start = solstice[index]
    end = solstice[(index + 2) % 8]
    if end < start: end += 360
    return end - start

def compute_score(summer, autumn, winter, spring):
    rup = 3
    if summer[rup] <= max(autumn[rup], winter[rup], spring[rup]):
        # RUP's summer is not longer than its other seasons
        return float("inf")
    if winter[rup] >= min(spring[rup], summer[rup], autumn[rup]):
        # RUP's winter is not shorter than its other seasons
        return float("inf")
    if summer[rup] <= max(summer[0:rup] + summer[rup+1:]):
        # RUP doesn't have the longest summer of all the nations
        return float("inf")
    # we have a candidate -- more even seasons across all nations are better
    lengths = sorted(summer + autumn + winter + spring)
    score = 0
    for len1, len2 in itertools.combinations(lengths, 2):
        score += len2 - len1
    return score

# W=0, NW=1, N=2, NE=3, E=4, SE=5, S=6, SW=7
regions = ["Ocean", "Trell", "Zephyr", "RUP", "Mountain", "Selva", "Elyria", "Arallu"]
w = 0
best_score = float("inf")
increment = 30
for nw, n, ne, e, se, s, sw in itertools.combinations(range(increment, 360, increment), 7):
    #if n != 90 or e != 180 or s != 270: continue
    solstice = [w, nw, n, ne, e, se, s, sw]
    summer = []
    autumn = []
    winter = []
    spring = []
    for r in range(8):
        i_su = r
        i_au = (r + 2) % 8
        i_wi = (r + 4) % 8
        i_sp = (r + 6) % 8
        summer.append(num_days(solstice, i_su))
        autumn.append(num_days(solstice, i_au))
        winter.append(num_days(solstice, i_wi))
        spring.append(num_days(solstice, i_sp))

    score = compute_score(summer, autumn, winter, spring)
    if score < best_score: # lower is better
        best_score = score
        best_config = (w, n, e, s, summer, autumn, winter, spring)
        print("--------------")
        print("NEW BEST SCORE");
        print("--------------")
        print(f"solstices by element: aquan     ={w:3} | {'':14} | auran     ={n:3} | {'':14} | ignan     ={e:3} | {'':14} | terran    ={s:3}")
        print("solstices by country: " + " | ".join(f"{regions[r]:10}={solstice[r]:3}" for r in range(8)))
        print("day counts per season by region:")
        for r in range(8):
            print(f"  {regions[r]:10}: summer={summer[r]:3} autumn={autumn[r]:3} winter={winter[r]:3} spring={spring[r]:3}")
        print(f"score = {score}")
