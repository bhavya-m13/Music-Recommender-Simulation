"""
bias_audit.py — surfaces filter bubbles and structural biases in score_song().

Each section targets one specific bias, prints the raw numbers that expose it,
and includes a plain-English verdict so the cause is unambiguous.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from recommender import load_songs, score_song

SONGS = load_songs("data/songs.csv")

SEP  = "=" * 52
DASH = "-" * 52

# ── helpers ───────────────────────────────────────────
def base_prefs(**overrides):
    """Return a neutral profile with specific fields overridden."""
    p = {
        "genre": "__none__", "mood": "__none__",
        "energy": 0.5, "valence": 0.5, "danceability": 0.5,
        "likes_acoustic": True,          # disable acoustic penalty for isolation
    }
    p.update(overrides)
    return p


# ══════════════════════════════════════════════════════
# BIAS 1 — Energy gap is linear: extreme users get wider
#          score spreads, but mid-range users' worst songs
#          still earn significant energy points.
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 1: Linear energy gap — who benefits?")
print(SEP)

for user_e in [0.0, 0.5, 1.0]:
    prefs = base_prefs(energy=user_e)
    e_scores = sorted(
        [(s["title"], round((1 - abs(s["energy"] - user_e)) * 4.0, 2)) for s in SONGS],
        key=lambda x: x[1], reverse=True
    )
    best  = e_scores[0]
    worst = e_scores[-1]
    spread = round(best[1] - worst[1], 2)
    print(f"\n  User energy = {user_e}")
    print(f"    Best  energy match : {best[0]:<30}  +{best[1]:.2f}")
    print(f"    Worst energy match : {worst[0]:<30}  +{worst[1]:.2f}")
    print(f"    Spread (best−worst): {spread:.2f} pts")
    # floor: how many songs still earn ≥ 2.0 energy pts even for this user?
    above_half = sum(1 for _, sc in e_scores if sc >= 2.0)
    print(f"    Songs earning ≥ 2.0/4.0 energy pts : {above_half} / {len(SONGS)}")

print(f"\n  VERDICT: mid-range (0.5) users have the smallest spread ({DASH[:6]})")
print("  because every song sits within ±0.5 of them — energy barely")
print("  differentiates. Extreme (0.0 / 1.0) users have a larger spread")
print("  but the catalog's actual energy distribution may leave their")
print("  sweet spot thinly stocked.")


# ══════════════════════════════════════════════════════
# BIAS 2 — Catalog energy distribution: bimodal gap
#          There are few songs near the 0.5–0.65 middle,
#          so mid-energy users always get imprecise matches.
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 2: Catalog energy distribution")
print(SEP)

bins = {"0.0–0.39": [], "0.40–0.59": [], "0.60–0.79": [], "0.80–1.0": []}
for s in SONGS:
    e = s["energy"]
    if   e < 0.40: bins["0.0–0.39"].append(s["title"])
    elif e < 0.60: bins["0.40–0.59"].append(s["title"])
    elif e < 0.80: bins["0.60–0.79"].append(s["title"])
    else:          bins["0.80–1.0"].append(s["title"])

for label, songs in bins.items():
    bar = "█" * len(songs)
    print(f"  {label}  {bar:20}  {len(songs):2} songs")
    for t in songs:
        print(f"              {t}")

print(f"\n  VERDICT: 0.40–0.59 band has only {len(bins['0.40–0.59'])} songs.")
print("  Users preferring mid energy have the thinnest catalog coverage.")


# ══════════════════════════════════════════════════════
# BIAS 3 — Acoustic asymmetry: `likes_acoustic: True`
#          earns NO bonus. Only `False` suffers a penalty.
#          Acoustic fans are invisible to the scorer.
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 3: Acoustic asymmetry")
print(SEP)

high_acoustic = [s for s in SONGS if s["acousticness"] > 0.7]
print(f"\n  Songs with acousticness > 0.7: {len(high_acoustic)}")

for likes in [True, False]:
    prefs = base_prefs(likes_acoustic=likes)
    for s in sorted(high_acoustic, key=lambda x: x["acousticness"], reverse=True)[:3]:
        sc, reasons = score_song(prefs, s)
        acoustic_reason = next((r for r in reasons if "acoustic" in r), "no acoustic term")
        print(f"  likes_acoustic={likes!s:<5}  {s['title']:<28}  "
              f"acousticness={s['acousticness']}  → {acoustic_reason}")

print(f"\n  VERDICT: likes_acoustic=True contributes 0.0 to any song score.")
print("  likes_acoustic=False deducts 1.0 from highly acoustic songs.")
print("  The system can express 'I hate acoustic' but not 'I love acoustic'.")


# ══════════════════════════════════════════════════════
# BIAS 4 — Genre catalog count: pop fans have 5× more
#          genre-match opportunities than single-song genres.
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 4: Genre match opportunity inequality")
print(SEP)

from collections import Counter
genre_counts = Counter(s["genre"] for s in SONGS)
print(f"\n  {'Genre':<16}  Songs  Max genre pts earnable")
for genre, count in genre_counts.most_common():
    reachable = count  # number of songs that can award the +1.0 bonus
    bar = "█" * count
    print(f"  {genre:<16}  {count:>2}     {bar}")

pop_opportunities   = genre_counts["pop"]
rock_opportunities  = genre_counts["rock"]
print(f"\n  VERDICT: A 'pop' user has {pop_opportunities} songs that can award genre +1.0.")
print(f"  A 'rock' user has {rock_opportunities}. Niche-genre fans earn the genre bonus")
print("  far less often — mood + energy carry all the weight for them.")


# ══════════════════════════════════════════════════════
# BIAS 5 — Exact string genre matching: related genres
#          score zero. "pop" ≠ "indie pop" ≠ "dream pop".
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 5: Exact-match genre — related genres score 0")
print(SEP)

pop_variants = [s for s in SONGS if "pop" in s["genre"]]
prefs_pop = base_prefs(genre="pop")
print(f"\n  User genre = 'pop'. Songs whose genre contains 'pop':")
for s in pop_variants:
    sc, _ = score_song(prefs_pop, s)
    match = "MATCH (+1.0)" if s["genre"] == "pop" else f"NO MATCH  (+0.0)  ← genre is '{s['genre']}'"
    print(f"    {s['title']:<30}  {match}")

print(f"\n  VERDICT: 'indie pop' and 'dream pop' songs are penalised as")
print("  genre strangers even though they share most sonic DNA with 'pop'.")


# ══════════════════════════════════════════════════════
# BIAS 6 — Mood filter bubble: mood weight (3.0) is 28.6%
#          of max score. Users with rare or absent moods
#          have a permanently lower score ceiling.
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 6: Mood filter bubble — reachable score ceiling")
print(SEP)

mood_counts = Counter(s["mood"] for s in SONGS)
MAX_SCORE   = 10.5
MOOD_WEIGHT = 3.0

print(f"\n  {'Mood':<12}  Songs  Mood bonus earnable  Reachable ceiling")
for mood, count in mood_counts.most_common():
    ceiling = MAX_SCORE if count >= 1 else MAX_SCORE - MOOD_WEIGHT
    print(f"  {mood:<12}  {count:>2}     {'yes (+3.0)' if count else 'NO  (  0.0)'}         "
          f"  {ceiling:.1f} / {MAX_SCORE}")

absent = ["sad", "angry", "bored", "anxious"]
print(f"\n  Moods NOT in catalog (0 songs): {absent}")
for m in absent:
    print(f"    User mood='{m}': mood bonus never fires → ceiling = {MAX_SCORE - MOOD_WEIGHT:.1f} / {MAX_SCORE}")

print(f"\n  VERDICT: Any user whose preferred mood doesn't exist in the catalog")
print(f"  is silently capped at {MAX_SCORE - MOOD_WEIGHT:.1f}/{MAX_SCORE} — 28.6% of the score is permanently locked out.")
print("  No warning is shown. Recommendations appear confident but are degraded.")


# ══════════════════════════════════════════════════════
# BIAS 7 — Proximity scores are always ≥ 0: there is no
#          active penalty for a terrible match, only a
#          smaller reward. Wrong songs still earn points.
# ══════════════════════════════════════════════════════
print(f"\n{SEP}")
print("  BIAS 7: No negative proximity — wrong songs earn free points")
print(SEP)

# User who loves maximum energy and max positivity
prefs_extreme = base_prefs(energy=1.0, valence=1.0, danceability=1.0)
worst_match   = next(s for s in SONGS if s["title"] == "Spacewalk Thoughts")  # energy=0.28
sc, reasons   = score_song(prefs_extreme, worst_match)

print(f"\n  User: energy=1.0, valence=1.0, danceability=1.0")
print(f"  Song: Spacewalk Thoughts  energy=0.28, valence=0.65, dance=0.41")
print(f"  Despite being a near-perfect MISMATCH on every axis:")
for r in reasons:
    print(f"    {r}")
print(f"  Total score: {sc:.2f}  (not 0.0, not negative — still earns points)")

print(f"\n  VERDICT: No signal in the system can produce a negative score")
print("  from proximity alone. A song maximally wrong on energy + valence")
print("  + danceability still scores > 0. This compresses the ranking —")
print("  truly bad matches aren't punished, just rewarded less.")

print(f"\n{SEP}\n")
