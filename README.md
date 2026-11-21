# CompScannedPDF

スキャンPDF専用の圧縮ツールです。処理はすべてPC内で行い、ファイルを外部に送信しません。

- Windows 10 / 11 用
- exe 版は Python や poppler のインストール不要
- 3段階の圧縮モード（品質重視 / バランス / サイズ優先）
- PDF の右クリックメニューから起動可能（任意）

> ⚠️ 対象はスキャンPDFのみです。Word や Excel から作った「文字を選択できるPDF」は小さくならず、逆に大きくなることがあります。

---

## 🚀 使い方（exe 版）

### 1. ダウンロードして配置する

1. 配布された `CompScannedPDF-windows.zip` を解凍する
2. 中のファイルを好きなフォルダにまとめて置く（例：`C:\Tools\CompScannedPDF\`）

```
CompScannedPDF\
├── CompScannedPDF.exe   アプリ本体
├── register.bat         右クリックメニュー登録（任意）
├── unregister.bat       右クリックメニュー解除
└── README.md            この説明書
```

### 2. 起動する

`CompScannedPDF.exe` をダブルクリックします。

初回は次のような警告が出ることがあります。署名のない自作アプリでは通常起きるものです。

- 「Windows によって PC が保護されました」→「詳細情報」→「実行」
- ウイルス対策ソフトが警告した場合は、このファイルを除外に追加してください

起動には数秒かかります（1ファイル形式のため、起動時に内部で展開しています）。

### 3. 圧縮する

1. 上部のエリアをクリックしてPDFを選ぶ
2. 圧縮モードを選ぶ
3. 予想サイズを確認する
4. 「圧縮を開始 →」を押し、保存先を選ぶ

| モード | 解像度 | 画質 | おすすめ用途 |
|---|---|---|---|
| 品質重視 | 200 dpi | 85% | 契約書・公式書類 |
| バランス | 150 dpi | 72% | メール添付・社内共有 |
| サイズ優先 | 100 dpi | 55% | 保管・参照用 |

> 予想サイズは目安です。実際のサイズは原稿によって変わります。

---

## 🖱️ 右クリックメニューに登録する（任意）

1. `register.bat` を `CompScannedPDF.exe` と同じフォルダに置いたまま、ダブルクリックする
2. 「Registered」と表示されれば完了

パスの書き換えや管理者権限は不要です。bat が exe の場所を自動で見つけて登録します。

使い方：PDF を右クリック →「Compress with CompScannedPDF」

> **Windows 11 の場合**：右クリック後に「その他のオプションを確認」を選ぶと表示されます（Shift キーを押しながら右クリックでも可）。

### ⚠️ 注意

- 登録後に exe を別のフォルダへ移動した場合は、移動先で `register.bat` をもう一度実行してください
- 解除するときは `unregister.bat` をダブルクリックします

---

## ❓ よくある質問

**圧縮したら大きくなった**
文字を選択できるPDF（テキストPDF）や、すでに圧縮済みのPDFです。この場合、アプリが警告を表示します。元のファイルをそのままお使いください。

**パスワード付きのPDFは使える？**
対応していません。パスワードを解除してから圧縮してください。

**右クリックメニューに出てこない**
Windows 11 では「その他のオプションを確認」の中にあります。それでも出ない場合は、exe と同じフォルダで `register.bat` を実行し直してください。

**右クリックからエラーが出る**
exe を移動した可能性があります。今ある場所で `register.bat` を実行し直してください。

---

## 🔧 exe の作り方（開発者向け）

### 方法 A：GitHub で自動ビルド（おすすめ）

このリポジトリには GitHub Actions の設定（`.github/workflows/build.yml`）が入っています。Windows PC がなくても exe を作れます。

- **手動で作る**：GitHub の「Actions」タブ →「Build Windows exe」→「Run workflow」。完了後、実行結果のページ下部「Artifacts」から zip をダウンロード
- **リリースとして公開する**：`v1.0.0` のようなタグを push すると、Releases に `CompScannedPDF-windows.zip` が自動で添付されます

### 方法 B：自分の Windows PC で作る

1. Python をインストール（「Add Python to PATH」にチェック）
2. `build.bat` をダブルクリック
3. `dist\CompScannedPDF.exe` が作成されます

ビルドは専用の仮想環境（`.venv-build`）で行うため、PC の Python 環境は汚れません。

### ソースから直接起動する

```powershell
pip install -r requirements.txt
python CompScannedPDF.py
```

---

## 📁 リポジトリ構成

```
CompScannedPDF.py              アプリ本体（ソース）
requirements.txt               依存ライブラリ（PyMuPDF）
build.bat                      exe ビルド用
register.bat / unregister.bat  右クリックメニュー登録・解除
.github/workflows/build.yml    GitHub での自動ビルド設定
```

ファイル名とフォルダ名は英数字のみにしています。日本語を含めると文字化けや動作不良の原因になるため、変更しないでください。
