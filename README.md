delaying_fileserver
====

レスポンス遅延を設定出来る簡易ファイルサーバ

## Description

- 指定ディレクトリ以下を配信するデバッグ用の簡易ファイルサーバ
- パスを指定して遅延時間を設定できます。

ローカルでの動作確認用です。

## Requirement

Python >= 3.6

## Usage

 - `# ----- Setting Begin -----`から`# ------ Setting End -----`までの設定項目を変更.
 - `python3 server.py`

### PORT
 待ち受けポート

### DOC_ROOT
 公開ディレクトリパス. `/`で始まる場合は絶対パス

### DELAY_SETTING
 遅延パス設定

```
DELAY_SETTING = [
    [ '\/delay500\/.*', 500 ], # sleep 500 millisec
    [ '\/delay100_300\/.*', 100, 300 ], # sleep 100-300 millisec
    [ '\/delay10000\/.*', 10000 ], # sleep 10000 millisec
]
```

  - 遅延パスの正規表現
  - 遅延時間1`[milli second]`
  - 遅延時間2`[milli second]`(　省略可 ) ： 設定した場合は`遅延時間1` ～ `遅延時間2`の間のランダムな時間遅延させる

  複数条件にマッチした場合は先に設定されたものが優先される

### EXCLUDE_SETTING
 除外設定

```
EXCLUDE_SETTING = [
    '.*\/?index\.html?',
    '.*\/$',
]
```

  - 除外パスの正規表現

  DELAY_SETTINGとEXCLUDE_SETTING両方にマッチした場合EXCLUDE_SETTINGが優先されます。

## License

These codes are licensed under CC0.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)