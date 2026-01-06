## トリプルバトルパーティ生成プログラム
* トリプルバトルで採用すると良いとされる要素を片っ端から詰め込んだパーティを動的計画法で求めるプログラムです
* 詳細はブログを参照
https://gentleman.yonnny.com/posts/triple-team-generator/

## 構成
* meta.json
  * 第6世代のポケモンメタデータ（タイプ、特性、種族値、覚える技etc）
* area_damage.py
  * 火力指数が一定値を超える範囲攻撃を事前計算して求めるプログラム
* area_damage.json
  * その実行結果
* generate_team.py
  * 本プログラムの本体

## 実行方法
```
python generate_team.py
```
* 途中経過がコマンドラインに表示される
* 全メガシンカを検証するとだいたい 1 時間くらいかかると思う（ハイスペックなマシンならもっと早いかも）
