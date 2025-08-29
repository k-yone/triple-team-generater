# pokemon_scraper.py
# -*- coding: utf-8 -*-
import json
import os

move_meta = {
    "あわ": {"power": 40, "type": "みず", "stats": "C", "sheer": False},
    "いにしえのうた": {"power": 75, "type": "ノーマル", "stats": "C", "sheer": True},
    "いわなだれ": {"power": 75, "type": "いわ", "stats": "A", "sheer": True},
    "エアカッター": {"power": 60, "type": "ひこう", "stats": "C", "sheer": False},
    "エレキネット": {"power": 55, "type": "でんき", "stats": "C", "sheer": True},
    "グランドフォース": {"power": 90, "type": "じめん", "stats": "A", "sheer": False},
    "こごえるかぜ": {"power": 55, "type": "こおり", "stats": "C", "sheer": True},
    "こなゆき": {"power": 40, "type": "こおり", "stats": "C", "sheer": True},
    "こんげんのはどう": {"power": 110, "type": "みず", "stats": "C", "sheer": False},
    "しおふき": {"power": 150, "type": "みず", "stats": "C", "sheer": False},
    "スピードスター": {"power": 60, "type": "ノーマル", "stats": "C", "sheer": False},
    "だくりゅう": {"power": 90, "type": "みず", "stats": "C", "sheer": True},
    "たつまき": {"power": 40, "type": "ドラゴン", "stats": "C", "sheer": True},
    "だんがいのつるぎ": {"power": 120, "type": "じめん", "stats": "A", "sheer": False},
    "チャームボイス": {"power": 40, "type": "フェアリー", "stats": "C", "sheer": False},
    "なみのり": {"power": 90, "type": "みず", "stats": "C", "sheer": False},
    "ねっぷう": {"power": 95, "type": "ほのお", "stats": "C", "sheer": True},
    "バークアウト": {"power": 55, "type": "あく", "stats": "C", "sheer": True},
    "ハイパーボイス": {"power": 90, "type": "ノーマル", "stats": "C", "sheer": False},
    "はっぱカッター": {"power": 55, "type": "くさ", "stats": "C", "sheer": False},
    "ふぶき": {"power": 110, "type": "こおり", "stats": "C", "sheer": True},
    "ふんか": {"power": 150, "type": "ほのお", "stats": "C", "sheer": False},
    "マジカルシャイン": {
        "power": 80,
        "type": "フェアリー",
        "stats": "C",
        "sheer": False,
    },
    "むしのていこう": {"power": 50, "type": "むし", "stats": "C", "sheer": True},
    "やきつくす": {"power": 60, "type": "ほのお", "stats": "C", "sheer": True},
    "ようかいえき": {"power": 40, "type": "どく", "stats": "C", "sheer": True},
    "かえんだん": {"power": 100, "type": "ほのお", "stats": "C", "sheer": True},
    "じしん": {"power": 100, "type": "じめん", "stats": "A", "sheer": False},
    "じならし": {"power": 60, "type": "じめん", "stats": "A", "sheer": True},
    "ばくおんぱ": {"power": 140, "type": "ノーマル", "stats": "C", "sheer": False},
    "はなふぶき": {"power": 90, "type": "くさ", "stats": "A", "sheer": False},
    "パラボラチャージ": {"power": 50, "type": "でんき", "stats": "C", "sheer": False},
    "ふんえん": {"power": 80, "type": "ほのお", "stats": "C", "sheer": True},
    "ヘドロウェーブ": {"power": 95, "type": "どく", "stats": "C", "sheer": True},
    "ほうでん": {"power": 80, "type": "でんき", "stats": "C", "sheer": True},
}

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
]


def is_banned(poke):
    return len([x for x in banned if x in poke["name"]]) > 0


def calculate_damage():
    with open("./meta.json", "r") as f:
        poke_meta = json.load(f)

    results = []

    for poke in poke_meta:
        if is_banned(poke):
            continue

        for ability in poke["abilities"]:
            max_damage = 0
            best_move = None
            for move in poke.get("moves", []):
                if move in move_meta:
                    meta = move_meta[move]
                    power = meta["power"]

                    stats_key = meta["stats"]
                    st = poke["base_stats"][stats_key]

                    damage = (st + 52) * 1.1 * power

                    sp_ability = None

                    if stats_key == "A" and ability in ["ちからもち", "ヨガパワー"]:
                        sp_ability = ability
                        damage *= 2

                    if meta["type"] in poke["type"] or ability == "へんげんじざい":
                        if ability == "へんげんじざい":
                            sp_ability = ability
                            damage *= 1.5
                        elif ability == "てきおうりょく":
                            sp_ability = ability
                            damage *= 2
                        else:
                            damage *= 1.5

                    if (
                        ability
                        in ["フェアリースキン", "スカイスキン", "フリーズスキン"]
                        and meta["type"] == "ノーマル"
                    ):
                        sp_ability = ability
                        damage *= 1.3 * 1.5

                    if ability == "ちからづく" and meta["sheer"]:
                        sp_ability = ability
                        damage *= 1.3

                    if (ability == "ひでり" and meta["type"] == "ほのお") or (
                        ability == "あめふらし" and meta["type"] == "みず"
                    ):
                        sp_ability = ability
                        damage *= 1.5

                    if damage > max_damage:
                        max_damage = damage
                        best_move = {
                            "move": move,
                            "ability": sp_ability,
                            "type": meta["type"],
                            "damage": damage,
                        }

            if best_move:
                poke["ability"] = ability
                results.append(
                    {
                        "poke": poke,
                        "max_damage_move": best_move,
                    }
                )

    sorted_results = sorted(
        results, key=lambda x: x["max_damage_move"]["damage"], reverse=True
    )

    for result in sorted_results[:100]:
        print(
            f'{result["poke"]["name"]}:\t{result["max_damage_move"]["move"]}{"("+result["max_damage_move"]["ability"]+")" if result["max_damage_move"]["ability"] else ""}\t{result["max_damage_move"]["damage"]}'
        )

    # ファイル書き出し
    with open("area_damage.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(sorted_results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    calculate_damage()
