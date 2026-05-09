# CompScannedPDF

> スキャンPDF専用 圧縮ツール — ローカル処理・外部送信なし・完全無料

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Free](https://img.shields.io/badge/Price-Free-brightgreen)

---

## 📌 このツールについて

複合機やスキャナーで作成した**スキャンPDF**を、PC上だけで圧縮できるデスクトップアプリです。

| 項目 | 内容 |
|------|------|
| 🔒 プライバシー | ファイルは一切外部に送信されません |
| 💰 コスト | 完全無料（Adobe Acrobat・iLovePDF 不要） |
| 💻 動作環境 | Windows 10 / 11 |
| 🗜️ 圧縮率 | スキャンPDFで最大約90%削減 |

> ⚠️ **対象はスキャンPDFのみです**
> Word・Excelから作成したテキストPDFには効果がありません。
> PDFの文字をマウスで選択できる → テキストPDF（対象外）
> PDFの文字を選択できない → スキャンPDF（対象 ✅）

---

## 📦 ファイル構成

```
CompScannedPDF/
├── CompScannedPDF.pyw          # メインアプリ本体
├── CompScannedPDF-register.reg # 右クリックメニュー登録用（オプション）
├── README.md                   # このファイル
└── CompScannedPDF-manual.txt   # 詳細マニュアル
```

---

## ⚠️ フォルダ・ファイル名に関する重要な注意事項

> **必ず守ってください。守らないと正常に動作しません。**

### ❌ パスに日本語を使わない

```
✅ 良い例：  C:\Tools\CompScannedPDF.pyw
✅ 良い例：  C:\Users\john\Documents\CompScannedPDF.pyw

❌ 悪い例：  C:\Users\山田\Documents\CompScannedPDF.pyw
❌ 悪い例：  C:\ツール\CompScannedPDF.pyw
```

Windowsのユーザー名が日本語の場合は `C:\Tools\` など別の場所に置いてください。

### ❌ ファイル名を変更しない（大文字・小文字も区別されます）

```
✅ 正しい：  CompScannedPDF.pyw
❌ 誤り：    compscannedpdf.pyw   （大文字・小文字が違う）
❌ 誤り：    CompScannedPDF.py    （拡張子が違う）
```

### ⚠️ フォルダ名にスペースを含めない（推奨）

```
✅ 推奨：   C:\Tools\CompScannedPDF.pyw
⚠️ 非推奨： C:\My Tools\CompScannedPDF.pyw
```

---

## 🔧 セットアップ手順

### Step 1 — ツールファイルの配置

`CompScannedPDF.pyw` を任意のフォルダに置いてください。

```
推奨場所： C:\Tools\CompScannedPDF.pyw
```

`C:\Tools\` が存在しない場合はエクスプローラーで作成してください。

---

### Step 2 — Python のインストール

1. [python.org](https://www.python.org/downloads/) からインストーラーをダウンロード
2. インストール時に **「Add Python to PATH」に必ずチェックを入れる**
3. インストール確認：

```powershell
python --version
# Python 3.xx.x と表示されれば成功
```

---

### Step 3 — 必要ライブラリのインストール

PowerShell を開いて以下を実行：

```powershell
pip install pdf2image Pillow pypdf reportlab img2pdf
```

`Successfully installed ...` と表示されれば成功。

---

### Step 4 — poppler のインストール

1. [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases) から最新の `Release-xx.xx.x-0.zip` をダウンロード
2. 解凍して以下の場所に配置・リネーム：

```
C:\Tools\poppler\
```

正しく配置できると `C:\Tools\poppler\Library\bin\` が存在する状態になります。

3. PowerShell で PATH に追加：

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\poppler\Library\bin", "User")
```

4. PowerShell を再起動して動作確認：

```powershell
pdftoppm -v
# pdftoppm version xx.xx.x と表示されれば成功
```

---

### Step 5 — .pyw ファイルの関連付け設定

`.pyw` ファイルをダブルクリックで起動できるよう設定します。

**① Python の実行ファイルの場所を確認する**

```powershell
python -c "import sys; print(sys.executable)"
# 例） C:\Users\john\AppData\Local\Python\pythoncore-3.14-64\python.exe
```

表示されたパスをメモしておく。（末尾の `python.exe` を `pythonw.exe` に変えて使います）

**② コマンドプロンプトを管理者として開く**

スタートメニューで `cmd` と検索 → 右クリック →「管理者として実行」

**③ 以下の2行を順番に実行する**

`YourName` の部分を①で確認したパスに合わせて書き換えてください。

```cmd
ftype Python.NoConFile=C:\Users\YourName\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe "%1" %*
assoc .pyw=Python.NoConFile
```

`.pyw=Python.NoConFile` と表示されれば成功。

**④ `CompScannedPDF.pyw` をダブルクリックしてアプリが起動すれば完了 ✅**

---

## 🖱️ 右クリックメニューへの登録（オプション）

PDFファイルを右クリック →「**Compress with CompScannedPDF**」から直接起動できるようになります。

### 手順

1. `CompScannedPDF-register.reg` をメモ帳で開く
2. 以下の行の2箇所のパスを書き換える：

```
@="\"C:\\Users\\YourName\\...\\pythonw.exe\" \"C:\\Tools\\CompScannedPDF.pyw\" \"%1\""
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
         pythonw.exe のフルパス                    CompScannedPDF.pyw のフルパス
```

**書き換えのルール：**
- バックスラッシュ `\` は必ず `\\` と2つ書く
- 引用符 `"` はそのまま残す

**書き換え例（ユーザー名が `john`、ツールを `C:\Tools\` に置いた場合）：**

```
# 書き換え前
@="\"C:\\Users\\pikum\\AppData\\Local\\Python\\pythoncore-3.14-64\\pythonw.exe\" \"C:\\Tools\\CompScannedPDF.pyw\" \"%1\""

# 書き換え後
@="\"C:\\Users\\john\\AppData\\Local\\Python\\pythoncore-3.14-64\\pythonw.exe\" \"C:\\Tools\\CompScannedPDF.pyw\" \"%1\""
```

3. 上書き保存して `CompScannedPDF-register.reg` をダブルクリック →「はい」
4. PDFを右クリックして「Compress with CompScannedPDF」が表示されれば完了 ✅

### 登録解除

`regedit` を開いて以下のキーを削除：

```
HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\CompScannedPDF
```

---

## 📖 使い方

| ステップ | 操作 |
|----------|------|
| 1️⃣ PDFを選択 | 上部エリアをクリックしてスキャンPDFを選択 |
| 2️⃣ モードを選択 | 用途に合わせて3種類から選ぶ |
| 3️⃣ 予想サイズを確認 | 圧縮後の予想サイズが自動表示される |
| 4️⃣ 圧縮を開始 | 「圧縮を開始 →」をクリックして保存先を選択 |

### 圧縮モード

| モード | 解像度 | 画像品質 | おすすめ用途 |
|--------|--------|----------|-------------|
| 品質重視 | 200 dpi | 85% | 契約書・公式書類 |
| バランス | 150 dpi | 72% | メール添付・社内共有（推奨） |
| サイズ優先 | 100 dpi | 55% | アーカイブ・参照用 |

---

## ❓ よくある質問

<details>
<summary>圧縮後にファイルサイズが大きくなった</summary>

テキストPDF（Wordなどで作成）が対象になっている可能性があります。
PDFの文字をマウスで選択できる場合はテキストPDFです。
このツールはスキャンPDFのみ有効です。

</details>

<details>
<summary>ダブルクリックすると「アプリを選択してください」と出る</summary>

Step 5 の `.pyw` 関連付け設定が完了していません。Step 5 の手順をやり直してください。

</details>

<details>
<summary>右クリックメニューに「Compress with CompScannedPDF」が出ない</summary>

`CompScannedPDF-register.reg` のパスが実際の場所と違う可能性があります。
メモ帳でファイルを開いてパスを確認・修正後、再度ダブルクリックして登録し直してください。

</details>

<details>
<summary>右クリックから起動するとPDFが読み込まれない</summary>

reg ファイル内の `pythonw.exe` のパスが間違っている可能性があります。
PowerShell で以下を実行してパスを再確認してください：

```powershell
python -c "import sys; print(sys.executable)"
```

表示されたパスの `python.exe` を `pythonw.exe` に変えて reg ファイルを書き直して再登録してください。

</details>

<details>
<summary>処理が遅い・途中で止まっているように見える</summary>

ページ数が多いほど時間がかかります。15ページで1〜3分程度が目安です。
プログレスバーで進捗を確認しながらお待ちください。

</details>

---

## 📄 License

MIT License
