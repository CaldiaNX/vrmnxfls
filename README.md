# VRMNXファイル連携システム

## 概要
「VRMNXファイル連携システム」（VRMNX File linkege System）は「[鉄道模型シミュレーターNX](http://www.imagic.co.jp/hobby/products/vrmnx/ "鉄道模型シミュレーターNX")」（VRMNX）のビュワーオブジェクトを外部から制御するためのPythonで記述されたシステムです。  
タイマーイベント(既定は0.1秒毎)にレイアウトファイルと同階層にある「read」フォルダ内のファイルを読み込み、テキストで記述されている命令をVRMNXの命令に変換して実行します。

![vrmnxfls-about](https://user-images.githubusercontent.com/66538961/107118763-3bbd3100-68c6-11eb-986b-252884227ef3.png)

## ダウンロード
- [vrmnx-fls.py](https://github.com/CaldiaNX/vrmnx-fls/blob/main/vrmnx-fls.py)

## 利用方法
レイアウトファイルと同じフォルダ階層に「vrmnx-fls.py」ファイルと「read」「read_end」フォルダを準備します。  

フォルダ構成：
```
C:\VRMNX（一例）
├ \read
├ \read_end
├ \send (任意)「sendSettingFile」関数出力用
├ vrmnx-fls.py
└ VRMNXレイアウトファイル.vrmnx
```

対象レイアウトのレイアウトスクリプトに以下の★内容を追記します。  
任意関数は必要に応じて利用してください。

```py
import vrmapi
# ★ファイル連携システムをインポート
import vrmnxfls

def vrmevent(obj,ev,param):
    if ev == 'init':
        # ★起動時に0.1秒間隔のタイマーイベントを登録
        obj.SetEventTimer(0.1)
        # (任意)sendフォルダにポイントと編成情報を出力
        vrmnxfls.sendSettingFile()
        # (任意)レイアウト内の全編成の電源を一括設定（0:OFF, 1:ON）
        vrmnxfls.setPowerAll(0)
    elif ev == 'broadcast':
        dummy = 1
    elif ev == 'timer':
        # ★タイマーイベントでフォルダを周期監視
        vrmnxfls.readFile()
    elif ev == 'time':
        dummy = 1
    elif ev == 'after':
        dummy = 1
    elif ev == 'frame':
        dummy = 1
    elif ev == 'keydown':
        dummy = 1
```

ファイル読み込みに成功すると、ビューワー起動時のスクリプトログに `load vrmnx-fls.py` と表示されます。

## readFile関数
テキストファイルが「read」フォルダにあると`readFile`関数がファイルを読み込み、命令を実行します。  
読み込まれたファイルは「read_end」フォルダに移動されます。

### ファイル名
ファイル名は年月日時分秒「yyyymmddhhmmssfff.txt」です。  
読み込み対象は「＊.txt」で検出します。  
年月日時分秒の命名規則はFIFO（先入れ先出し）を遵守するためのルールです。

### 命令ファイル構文
ファイルはダブルクオーテーション無し、改行無し、タブ区切りの1行Shift-JISテキストファイルです。

#### 1. Object識別子

| 識別子 | オブジェクト | 名前 |
| ---- | ---- | ---- |
| T | VRMTrain | 編成 |
| P | VRMPoint | ポイント |
| A | VRMATS | 自動センサー |
| B | VRMBell | 音源 |
| C | VRMCamera | 地上カメラ |
| R | VRMCar | 車輌 |
| X | VRMCrossing | 踏切、ホームドア |
| E | VRMEmitter | エミッター |
| L | VRMLayout | レイアウト |
| M | VRMMotionPath | モーションパス |
| G | VRMSignal | 信号 |
| K | VRMSky | スカイドーム、天候 |
| I | VRMSprite | スプライト |
| S | VRMSystem | システム |
| U | VRMTurntable | ターンターブル |

#### 2. ObjectID(int)
α版は直接参照のみ対応しているため、無効なIDがある場合はエラーとなります。  
データ名での指定や、存在チェックを導入する予定です。

#### 3. 命令関数
VRMNXで定義されている各オブジェクトの命令文字列です。  
文字列が無効なものは命令が無視されます。

#### 4. 引数
命令関数に必要な引数を記載します。  
引数が1つ以上ない場合は命令が無視されます。  
α版は必ず1つ以上を強制していますが、今後は命令セットに応じて要素数をチェックする予定です。

### 構文サンプル
列車の速度を変える（列車ID10の速度を距離50で最高速度の50％に変える）
```
T	10	AutoSpeedCTRL	50	0.5
```

列車の進行方向を変える（0はダミー変数）
```
T	10	Turn	0
```

列車の電装を変える（0:OFF, 1:ON）
```
T	10	SetPower	0
```

ポイントを切り替える（ポイントID11の向きを1側にする）
```
P	11	SetBranch	1
```

複数ポイントを切り替える（ポイントID11と12の向きを1側、13の向きを0側）
```
P	11_12_-13	SetBranch	1
```

## sendSettingFile関数
「send」フォルダがある状態で`sendSettingFile`関数を実行するとレイアウトファイルから編成と列車の一覧をタブ区切りのShift_JISテキストファイルとして`send\yyyymmddhhmmssffffff.txt`へ出力します。  
この情報は「ネットワークコントローラー」等の設定情報として利用可能です。  
いずれのリストもID順で出力します。  
出力に成功すると`sendフォルダにレイアウト情報ファイルを出力しました。`と表示します。  
レイアウトファイルの初回起動時、カレントディレクトリ未登録によりフォルダ読み込みに失敗する場合があります。その場合はVRMNXを再起動してください。

### 1.編成一覧

| 列 | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | t(固定文字) | Object識別子 |
| 2 | ObjectID | GetID() |
| 3 | ObjectNAME | GetNAME() |
| 4 | X座標(横) | GetPosition()[0] |
| 5 | Y座標(高さ) | GetPosition()[1] |
| 6 | Z座標(縦) | GetPosition()[2] |
| 7 | 速度(電圧0.0～1.0) | GetVoltage() |

出力例：
```
t	10	TRAIN_10	2028.6000053961689	6.0	1096.0780848595002	0.0
t	25	TRAIN_25	1297.874999999999	6.0	1400.0000223802317	0.0
t	54	TRAIN_54	1291.4000003714773	6.0	1163.484177169418	0.0
t	64	TRAIN_64	2028.6000027358723	6.0	1332.593930070314	0.0
```

### 2.ポイント一覧

| 列 | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | p(固定文字) | Object識別子 |
| 2 | ObjectID | GetID() |
| 3 | ObjectNAME | GetNAME() |
| 4 | X座標(横) | GetPosition()[0] |
| 5 | Y座標(高さ) | GetPosition()[1] |
| 6 | Z座標(縦) | GetPosition()[2] |
| 7 | 分岐状態(0,1) | GetBranch() |

出力例：
```
p	675	B線上駅C渡り線XL	2108.00009006219	0.0	411.48450518271034	0
p	676	C線上駅B渡り線XL	2364.0000885889813	0.0	445.18758033766994	0
p	677	C線上駅B渡り線XL	2108.000088588982	0.0	445.18756914755403	0
p	678	B線上駅C渡り線XR	2364.0000900621894	0.0	411.4845163728262	0
```

## 想定される利用シーン
- 外部プログラムの運転盤や自動運転システムとの連携
- DCCコントローラを使ったマスコン制御（COM連携・命令変換）
- レイアウト同士の連携させた疑似オンライン運転会

## 履歴
- v1.5 2020/11/14 複数分岐操作で負数の場合に逆方向とする機能を追加
- v1.4 2020/10/24 編成の電源を制御する「setPower」「setPowerAll」追加
- v1.3 2020/09/27 アンダーバー区切りによるポイント一括設定に対応
- v1.2 2020/09/23 レイアウト情報出力「sendSettingFile」追加
- v1.1 2020/09/14 方向転換「Turn」命令追加
- v1.0 2019/12/29 公開

## 今後の実装予定
- 対象オブジェクト・命令セットの拡充
- イベントドリブン（SetEvent～）の追加
- エラー制御
- VRMNX側からの出力対応
