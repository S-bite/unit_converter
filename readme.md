# unit_converter
ある物理単位を、別の単位の組み合わせに変換します。

# Requirement
* python3.x
* argparse
* copy


# Usage
`python convert.py target_unit use_units`

target_unitで指定した単位を、use_unitsで指定した単位の組み合わせに変換します。

例；ニュートンをキログラム、メートル、秒の組み合わせに変換する場合。

`python convert.py N kg,m,s `

use_unitsに複数の単位を指定する場合は、`,`で区切ってください。
target_unitは複数の単位の組み合わせでも大丈夫です。単位を\*でつなげて、同じ単位は＾でまとめてください。例:kg\*m^2\*s^-3

単位の実装には、Wikipediaの[SI基本単位](https://ja.wikipedia.org/wiki/SI基本単位)および[SI組立単位](https://ja.wikipedia.org/wiki/SI組立単位)を参考にしています。現在入力として使える単位は以下の通りです。
|単位名|シンボル|
---- |----
|メートル|m|
|キログラム|kg|
|秒|s|
|アンペア|A|
|ケルビン|K|
|カンデラ|cd|
|モル|mol|
|速度|ｖ|
|加速度|a|
|ニュートン|N|
|ジュール|J|
|ワット|W|
|クーロン|C|
|パスカル|Pa|
|ボルト| V|
|ファラド|F|

# Others
* 組み合わせの検索には動的計画法を使っています。入力によっては組み合わせの発見に失敗することがあるかもしれません。

