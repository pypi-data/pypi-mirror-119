algo-method-tools
===================

![image](https://img.shields.io/pypi/v/algo-method-tools)
![image](https://img.shields.io/pypi/pyversions/algo-method-tools)
![image](https://img.shields.io/pypi/l/algo-method-tools)

algo-method用の環境構築用コマンドラインツール

入力例, 出力例を含むディレクトリを自動生成する.

**このプロジェクトの仕様は予告なしに変更される可能性があります (testコマンドに対応すると 変更されることが予想されます).**

## インストール方法

``` bash
$ pip install algo-method-tools
```


## 使い方

``` bash
$ algo-tools --help
Usage: algo-tools [OPTIONS] TASK_NO

Arguments:
  TASK_NO  [required]

Options:
  --base-dir PATH       [default: /home/yassu/algo-methods]
  --template-file TEXT
  --help                Show this message and exit.
```


## 使用例

``` bash bash
$ algo-tools 316
write into /home/yassu/algo-methods/316
$ cat ~/algo-methods/316/
in_1.txt   main.py    out_1.txt
$ cat ~/algo-methods/316/main.py
$ cat ~/algo-methods/316/in_1.txt
2 3
1 2 3
4 3 2
$ cat ~/algo-methods/316/out_1.txt
5


# algo-tools/template.pyは自分用のテンプレートファイル
$ algo-tools 316 --base-dir ~/repos/algo-tools --template-file ~/algo-tools/template.py
write into /home/yassu/repos/algo-tools/316
$ ls ~/repos/algo-tools/316/
in_1.txt  main.py  out_1.txt
$ cat ~/repos/algo-tools/316/main.py
from pprint import pprint
from sys import setrecursionlimit, stdin
from typing import Dict, Iterable, Set
INF: int = 2**62
...
$ cat ~/repos/algo-tools/316/in_1.txt
2 3
1 2 3
4 3 2
$ cat ~/repos/algo-tools/316/out_1.txt
5
```


## オプション

* `--template-file, -t`: 使用するテンプレートファイルを指定する(指定しなければ使用されない)
* `--base-dir, -b`: ファイルを格納するディレクトリを指定する
