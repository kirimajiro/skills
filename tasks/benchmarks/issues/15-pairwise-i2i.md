# 15 一対比較を i2i の問題用紙に広げる

Type: task
Story: pairwise
Status: open
Blocked by: 14

## 目的

t2i で固めたツールを i2i（画像編集）に広げる。i2i は元画像と参照画像を見ながら判定するので、レイアウトと観点が t2i と異なる。

## 手順

1. 観点セットの i2i 版を決める（実行・保持・転写・整合の 5 軸の語彙を観点に写す。例: edit 指示の実行 / keep 指示外の保持 / transfer 参照の転写 / blend 継ぎ目と光の整合）。`benchmarks/i2i/NN-*.md` に `pairwise:` を追記する
2. `pairwise_build.py` に `--mode` の i2i 版を足す: 上段に元画像と参照画像、下段に候補 2 枚。画像の探し方は `run_i2i.py` の命名に合わせる
3. `results/<model-slug>/i2i.md` を後継書式に置き換え、`benchmarks/README.md` から i2i の 5 軸ルーブリックを外す
4. qwen-image-2-1 と基準モデルの i2i で 1 セッション回し、判定シートを書き直す

## 受け入れ条件

- Given i2i の問題用紙、When build する、Then 元画像・参照画像・候補 2 枚が 1 画面に収まり、t2i と同じ JSON 書式で保存できる
- Given 1 セッションの結果、When 集計する、Then `pairwise_report.py` が t2i と同じ表を出し、`results/qwen-image-2-1/i2i.md` が後継書式で埋まる

## Comments
