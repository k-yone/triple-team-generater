# pokemon_scraper.py
# -*- coding: utf-8 -*-
import json
import datetime

types = [
    "ノーマル",
    "ほのお",
    "みず",
    "くさ",
    "でんき",
    "こおり",
    "かくとう",
    "どく",
    "じめん",
    "ひこう",
    "エスパー",
    "むし",
    "いわ",
    "ゴースト",
    "ドラゴン",
    "あく",
    "はがね",
    "フェアリー",
]


banned = [
    "ミュウツー",
    "ミュウ",
    "ルギア",
    "ホウオウ",
    "セレビィ",
    "カイオーガ",
    "グラードン",
    "レックウザ",
    "ジラーチ",
    "デオキシス",
    "ディアルガ",
    "パルキア",
    "ギラティナ",
    "マナフィ",
    "フィオナ",
    "ダークライ",
    "シェイミ",
    "アルセウス",
    "レシラム",
    "ゼクロム",
    "キュレム",
    "ビクティニ",
    "ケルディオ",
    "メロエッタ",
    "ゲノセクト",
    "ゼルネアス",
    "イベルタル",
    "ジガルデ",
    "ディアンシー",
    "フーパ",
    "ボルケニオン",
    "ケッキング",
    "レジギガス",
]


resistance = {
    "fire_resistance": {
        "double_damage_to": ["くさ", "こおり", "むし", "はがね", "かんそうはだ"],
        "half_damage_to": ["ほのお", "みず", "いわ", "ドラゴン", "あついしぼう"],
        "no_damage_to": ["もらいび"],
    },
    "water_resistance": {
        "double_damage_to": ["ほのお", "じめん", "いわ"],
        "half_damage_to": ["みず", "くさ", "ドラゴン"],
        "no_damage_to": ["かんそうはだ", "ちょすい", "よびみず"],
    },
    "ice_resistance": {
        "double_damage_to": ["くさ", "じめん", "ひこう", "ドラゴン"],
        "half_damage_to": ["ほのお", "みず", "こおり", "はがね", "あついしぼう"],
        "no_damage_to": [],
    },
    "ground_resistance": {
        "double_damage_to": ["ほのお", "でんき", "どく", "いわ", "はがね"],
        "half_damage_to": ["くさ", "むし"],
        "no_damage_to": ["ひこう", "ふゆう"],
    },
    "flying_resistance": {
        "double_damage_to": ["くさ", "かくとう", "むし"],
        "half_damage_to": ["でんき", "いわ", "はがね"],
        "no_damage_to": [],
    },
    "rock_resistance": {
        "double_damage_to": ["ほのお", "こおり", "ひこう", "むし"],
        "half_damage_to": ["かくとう", "じめん", "はがね"],
        "no_damage_to": [],
    },
    "fairy_resistance": {
        "double_damage_to": ["かくとう", "ドラゴン", "あく"],
        "half_damage_to": ["ほのお", "どく", "はがね"],
        "no_damage_to": [],
    },
}


move_map = {
    "fakeout": {"ねこだまし"},
    "lightscreen": {"ひかりのかべ"},
    "reflect/intimidate": {"リフレクター", "*#いかく"},
    "wideguard": {"ワイドガード"},
    # "fastguard": {"ファストガード"},
    "skillswap/gastroacid/worryseed": {
        "スキルスワップ",
        "いえき",
        "なやみのタネ",
        "なかまづくり",
    },
    # "faint/snatch": {"フェイント", "よこどり"},
    # "followme/ragepowder": {"このゆびとまれ", "いかりのこな"},
    "trickroom": {"トリックルーム"},
    # "tailwind": {"おいかぜ"},
    # "trickroom/tailwind": {"トリックルーム", "おいかぜ"},
    # "knockoff": {"はたきおとす"},
    # "brickbreak": {"かわらわり"},
    # "uturn": {"とんぼがえり", "ボルトチェンジ"},
    # "perish": {"ほろびのうた"},
    # "encore": {"アンコール"},
    # "healpulse": {"いやしのはどう"},
    "hypnosis": {"ダークホール", "キノコのほうし", "ねむりごな#ふくがん"},
}


def read_area_damage():
    with open("./area_damage.json", "r") as f:
        return json.load(f)


def read_poke_meta():
    with open("./meta.json", "r") as f:
        return json.load(f)


area_damage = read_area_damage()
poke_meta = read_poke_meta()


def init_result_map():
    result = {
        "area_damage": False,
    }

    for k in resistance.keys():
        result[k] = False

    for k in move_map.keys():
        result[k] = False

    return result


def area_damage_type(poke, damage):
    for p in area_damage:
        if (
            p["poke"]["name"] == poke["name"]
            and p["poke"]["ability"] == poke["ability"]
            and p["max_damage_move"]["damage"] >= damage
        ):
            return p["max_damage_move"]["type"]

    return None


def is_resistance(poke, type, damage):
    # 各種範囲攻撃に対して４発以上耐える耐性を持つか
    stat = "B" if type in ["ground_resistance", "rock_resistance"] else "D"
    base = (poke["base_stats"]["H"] + 75) * (poke["base_stats"][stat] + 20)

    res = damage * 0.44 * 2 / 3 / base

    for t in poke["type"]:
        if t in resistance[type]["double_damage_to"]:
            res *= 2
        elif t in resistance[type]["half_damage_to"]:
            res *= 0.5
        elif t in resistance[type]["no_damage_to"]:
            res *= 0

    if poke["ability"] in resistance[type]["double_damage_to"]:
        res *= 2
    elif poke["ability"] in resistance[type]["half_damage_to"]:
        res *= 0.5
    elif poke["ability"] in resistance[type]["no_damage_to"]:
        res *= 0

    return res < 0.25


def is_banned(poke):
    return len([x for x in banned if x in poke["name"]]) > 0


def check_sheet():
    results = []

    for poke in poke_meta:
        if is_banned(poke):
            continue

        # 実質種族値の計算
        effective_stats = (
            poke["base_stats"]["H"]
            + poke["base_stats"]["B"]
            + poke["base_stats"]["D"]
            + max(poke["base_stats"]["A"], poke["base_stats"]["C"])
            + poke["base_stats"]["S"]
        )

        for ability in poke["abilities"]:
            poke["ability"] = ability

            result = init_result_map()

            # 火力指数25000以上の範囲攻撃を持っているか（別途計算済み）
            result["area_damage"] = area_damage_type(poke, 25000)

            # 各種範囲攻撃に対して耐性があるか
            for type in resistance.keys():
                result[type] = is_resistance(poke, type, 25000)

            # 各種有力な技を持っているか
            for fact in move_map:
                if any(
                    move_map[fact]
                    & (
                        set(poke["moves"])
                        | set([m + "#" + ability for m in poke["moves"]])
                    )
                ):
                    result[fact] = True

            # 技の組み合わせを列挙
            combinations = []
            facts = [k for k, v in result.items() if k in move_map.keys() and v]
            if len(facts) <= 3:
                combinations.append(facts)
            else:
                for i in range(len(facts)):
                    for j in range(i + 1, len(facts)):
                        for k in range(j + 1, len(facts)):
                            combinations.append([facts[i], facts[j], facts[k]])

            # 組み合わせの数だけ results に追加
            for combination in combinations:
                modified = result.copy()
                for fact in move_map:
                    # false で初期化
                    modified[fact] = False

                    # 技枠使わずに埋まる要素があれば true
                    if "*#" + ability in move_map[fact]:
                        modified[fact] = True

                    modified[fact] = fact in combination

                results.append(
                    {
                        "name": poke["name"],
                        "result": modified,
                        "stats": effective_stats,
                        "ability": ability,
                        "dex_no": poke["dex_no"],
                        "is_mega": poke["is_mega"],
                    }
                )

    # ドーブルだけ別途追加
    sp_moves = list(move_map.keys())
    for a in range(len(sp_moves) - 3):
        for b in range(a + 1, len(sp_moves) - 2):
            for c in range(b + 1, len(sp_moves) - 1):
                d = len(sp_moves) - 1

                # 催眠と同時採用しない要素を除く
                if any(
                    {"skillswap/gastroacid/worryseed", "uturn", "knockoff"}
                    & set([sp_moves[a], sp_moves[b], sp_moves[c]])
                ):
                    continue

                result = init_result_map()

                for k in sp_moves:
                    result[k] = False
                result[sp_moves[a]] = True
                result[sp_moves[b]] = True
                result[sp_moves[c]] = True
                result[sp_moves[d]] = True

                results.append(
                    {
                        "name": "ドーブル",
                        "result": result,
                        "stats": 230,
                        "ability": "ムラっけ",
                        "dex_no": "235",
                        "is_mega": False,
                    }
                )

    # results を評価値降順にソートする
    results = sorted(results, key=lambda x: team_score([x]), reverse=True)

    return results


def get_check_box(team):
    keys = sorted(list(team[0]["result"].keys()))

    check_box = {}

    for k in keys:
        for p in team:
            if p["result"][k]:
                if k == "area_damage":
                    check_box[k] = check_box.get(k, set()) | {p["result"][k]}
                else:
                    check_box[k] = check_box.get(k, 0) + 1

    if "area_damage" in check_box:
        check_box["area_damage"].discard(None)

    return check_box


def resistance_score(key, value):
    return min(2, value)


def team_score(team):
    # team に含まれる要素数を数え上げる
    # cache のための工夫としてどの要素を満たしているかを小数で表す

    check_box = get_check_box(team)

    score = 0

    keys = sorted(list(team[0]["result"].keys()))
    for k in keys:
        if k == "area_damage":
            score += min(4, len(check_box.get(k, set())))
        elif k.endswith("_resistance"):
            score += resistance_score(k, check_box.get(k, 0))
        else:
            if k in check_box:
                score += 1

    stats = sum([x["stats"] for x in team])
    score += pow(10, -5) * stats

    return score


# 特定の要素を持つポケモン一覧
cached_filtered_check_sheet = {}


def filter_check_sheet(cs, key):
    if key not in cached_filtered_check_sheet:
        cached_filtered_check_sheet[key] = [x for x in cs if x["result"][key]]
    return cached_filtered_check_sheet[key]


def find_missing_key(team):
    valid = [x for x in team if x != None]
    for key in valid[0]["result"].keys():
        if not any([p["result"][key] for p in valid]):
            return key
    return "area_damage"


def erase_skippable(cs):
    score = {}
    for x in cs:
        h = json.dumps(x["result"])
        if h not in score:
            score[h] = x
        else:
            if team_score([score[h]]) < team_score([x]):
                score[h] = x

    return list(score.values())


def get_megas(cs):
    return [x for x in cs if x["is_mega"]]


def erase_megas(cs):
    return [x for x in cs if not x["is_mega"]]


def cache_key(team):
    check_box = get_check_box(team)
    for k in check_box:
        if k == "area_damage":
            if len(check_box[k]) < 3:
                check_box[k] = sorted(list(check_box[k]))
            else:
                check_box[k] = "FULL"
        elif k.endswith("_resistance"):
            check_box[k] = resistance_score(k, check_box[k])
        else:
            check_box[k] = min(1, check_box[k])

    return f"{json.dumps(check_box)}#{len(team)}"


cache_map = {}


def find_cache(team):
    key = cache_key(team)

    if key in cache_map:
        for rest in cache_map[key]:
            if not any({x["dex_no"] for x in team} & {x["dex_no"] for x in rest}):
                return rest

    return None


def save_cache(team, rest):
    key = cache_key(team)
    if key not in cache_map:
        cache_map[key] = []
    cache_map[key].append(rest)

    if len(cache_map[key]) == 5:
        print("")
        print(team)
        print(key)
        print(cache_map[key])


def get_best_team(team, cs, info):
    if len(team) == 6:
        return team

    if len(team) == 4:
        print(
            "\r",
            f"{info["mega"]} {info['ijl'][0][0]}/{info['ijl'][0][1]} {info['ijl'][1][0]}/{info['ijl'][1][1]} {info['ijl'][2][0]}/{info['ijl'][2][1]}         ",
            end="",
            flush=True,
        )

    cache = find_cache(team)
    if cache:
        return team + cache

    missing = find_missing_key(team)
    filtered = filter_check_sheet(cs, missing)
    filtered = [x for x in filtered if x["dex_no"] not in [p["dex_no"] for p in team]]

    score = 0
    best = None
    ijl = info.get("ijl", []).copy()
    for i in range(len(filtered)):
        info["ijl"] = ijl + [[i, len(filtered)]]

        best_team = get_best_team(team + [filtered[i]], cs, info)
        if team_score(best_team) > score:
            score = team_score(best_team)
            best = best_team[len(team) :]

    save_cache(team, best)
    return team + best


def dynamic():
    cs = check_sheet()

    # ファイル書き出し
    with open("check_sheet.json", "w") as f:
        json.dump(cs, f, indent=2, ensure_ascii=False)

    megas = get_megas(cs)
    megas = erase_skippable(megas)

    # ファイル書き出し
    with open("megas.json", "w") as f:
        json.dump(megas, f, indent=2, ensure_ascii=False)

    # 実験用
    # megas = [x for x in megas if x["name"] in ["メガリザードンY","メガユキノオー"]]

    cs = erase_megas(cs)
    cs = erase_skippable(cs)

    # ファイル書き出し
    with open("check_sheet_skippable.json", "w") as f:
        json.dump(cs, f, indent=2, ensure_ascii=False)

    teams = []
    for i in range(len(megas)):
        team = get_best_team([megas[i]], cs, {"mega": megas[i]["name"]})
        team_short = [x["name"] for x in team]

        print("\r", f"{team_short} {team_score(team)}")
        teams.append(
            {
                "team_short": team_short,
                "team": team,
                "score": team_score(team),
                "result": {
                    a: any([p["result"][a] for p in team])
                    for a in team[0]["result"].keys()
                },
            }
        )

    teams = sorted(teams, key=lambda x: x["score"], reverse=True)
    result_map = {}
    for team in teams:
        key = team["team"][0]["dex_no"]
        if key not in result_map:
            result_map[key] = team

    print("")
    for team in result_map.values():
        print(team["team_short"])
        print(team["score"])

    # 結果をファイル出力
    with open(
        f"result/result{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json", "w"
    ) as f:
        json.dump(result_map, f, indent=2, ensure_ascii=False)


def greedy():
    cs = check_sheet()

    # ファイル書き出し
    with open("check_sheet.json", "w") as f:
        json.dump(cs, f, indent=2, ensure_ascii=False)

    megas = [
        x
        for x in cs
        if (
            x["name"].startswith("メガ")
            and x["name"] not in ["メガニウム", "メガヤンマ"]
        )
    ]
    megas = erase_skippable(megas)
    # 実験用
    # megas = [x for x in megas if x["name"] in ["メガバシャーモ","メガリザードンY","メガユキノオー"]]
    # megas = [x for x in cs if (x["name"].startswith("メガエルレイド"))]

    # ファイル書き出し
    with open("megas.json", "w") as f:
        json.dump(megas, f, indent=2, ensure_ascii=False)

    cs = erase_megas(cs)
    cs = erase_skippable(cs)

    # ファイル書き出し
    with open("check_sheet_skippable.json", "w") as f:
        json.dump(cs, f, indent=2, ensure_ascii=False)

    team = []

    best_score = 0
    best_poke = None
    # for i in range(len(megas)):
    #     score = team_score(team + [megas[i]])
    #     if score > best_score:
    #         best_score = score
    #         best_poke = megas[i]
    # team.append(best_poke)
    # best_poke = None

    # for i in range(len(cs)):
    #     if cs[i]["name"] == "カメックス":
    #         team.append(cs[i])
    #         break

    for i in range(len(megas)):
        if megas[i]["name"] == "メガバンギラス":
            team.append(megas[i])
            break

    for n in range(4):
        for j in range(len(cs)):
            score = team_score(team + [cs[j]])
            if score > best_score:
                best_score = score
                best_poke = cs[j]
        team.append(best_poke)
        best_poke = None

    print(team)


if __name__ == "__main__":
    dynamic()
    # greedy()
