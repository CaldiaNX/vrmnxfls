# VRMNXファイル連携システム 仕様

## readFile関数
「readフォルダ」内のテキストファイルを検知すると「readFile関数」がファイルを読み込み、命令を実行します。  
ファイルはダブルクオーテーション無し、改行無し、タブ区切りの1行Shift-JISテキスト形式です。  
ファイル名は年月日時分秒「yyyymmddhhmmssfff.txt」です。  
年月日時分秒の命名規則はFIFO（先入れ先出し）を遵守するためのルールです。  
読み込み対象は「＊.txt」で0.1秒ごとのポーリングで検出します。  

### (1) Object識別子
| 識別子 | オブジェクト | 名前 |
| ------ | ---- | ---- |
| T | VRMTrain  | 編成 |
| P | VRMPoint  | ポイント |
| A | VRMATS    | 自動センサー |
| B | VRMBell   | 音源 |
| C | VRMCamera | 地上カメラ |
| R | VRMCar    | 車輌 |
| X | VRMCrossing   | 踏切、ホームドア |
| E | VRMEmitter    | エミッター |
| L | VRMLayout     | レイアウト |
| M | VRMMotionPath | モーションパス |
| G | VRMSignal | 信号 |
| K | VRMSky    | スカイドーム、天候 |
| I | VRMSprite | スプライト |
| S | VRMSystem | システム |
| U | VRMTurntable  | ターンターブル |

### (2) ObjectID(int)
操作対象のオブジェクトIDを指定します。  
無効なIDはエラーになります。  

### (3) 命令関数名
VRMNXファイル連携システムで実装されている命令文字列を記載します。  
文字列が無効なものは無視されます。

### (4) 命令引数
命令関数に必要な引数を記載します。  
引数が1つ以上ない場合は命令が無視されます。  
現行版は1つ以上を強制しています。（今後、命令セットに応じて要素数をチェック予定）

## 実装命令一覧
|識別子|ID|命令関数名|命令引数|
|--|--|--|--|
|T |ID|[AutoSpeedCTRL](https://vrmcloud.net/nx/script/script/train/AutoSpeedCTRL.html)|0.0～1.0(最高速度の割合)|
|T |ID|[Turn](https://vrmcloud.net/nx/script/script/train/Turn.html)|0(ダミー)|
|T |ID|[PlayHorn](https://vrmcloud.net/nx/script/script/train/PlayHorn.html)|0(標準), 1(組込み)|
|T |ID|[SplitTrain](https://vrmcloud.net/nx/script/script/train/SplitTrain.html)|1以上(切り離す車両位置)|
|T |ID|SetPower|0,1（0:OFF, 1:ON）|
|P |ID|[SetBranch](https://vrmcloud.net/nx/script/script/point/SetBranch.html)|0,1（ポイント方向）|

## 命令構文例
列車［10］の速度を距離50(固定)で最高速度の50％に変える
```
T	10	AutoSpeedCTRL	50	0.5
```
列車［10］の進行方向を変える
```
T	10	Turn	0
```
列車［10］の電装をOFF
```
T	10	SetPower	0
```
ポイント［11］を向き［1］側に切り替える
```
P	11	SetBranch	1
```
ポイント[11］［12］の向きを［1］側、［13］の向きを［0］側に切り替える
```
P	11_12_-13	SetBranch	1
```

## setPowerAll関数
「VRMNXファイル連携システム」と関係性の無い便利関数です。  
レイアウトにある全編成の電装系をONにします。  
主に起動時の初期設定として利用しますが、単体でも実行できます。  
編成別に処理したい場合は「setPower関数」を利用します。

## sendSettingFile関数
「sendフォルダ」がある状態で「sendSettingFile関数」を実行すると「レイアウト情報ファイル」を出力します。  
レイアウトの編成リストとポイントリストをID順でタブ区切りのShift_JISテキストファイルとして「send\yyyymmddhhmmssffffff.txt」へ出力します。  
「ネットワークコントローラー」等の設定情報として利用できます。

出力に成功すると
```
sendフォルダにレイアウト情報ファイルを出力しました。
```
と表示します。

出力例：
```
t	10	TRAIN_A	1001N	1138	814	6	180	5
t	64	TRAIN_B	2001N	1912	848	6	0	3	dummy

p	12	A2	0	1537	814	0	180
p	20	A1	0	2513	814	0	0
p	55	B1	1	2513	848	0	0
p	63	B2	1	1537	848	0	180
```
浮動小数点型は整数値で出力されます。

### (1) 編成一覧
| 列   | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | t (固定文字) | 識別文字 |
| 2 | 列車ID | [GetID()](https://vrmcloud.net/nx/script/script/data/GetID.html) |
| 3 | 列車名 | [GetNAME()](https://vrmcloud.net/nx/script/script/data/GetNAME.html) |
| 4 | 列車番号 | [GetTrainNumber()](https://vrmcloud.net/nx/script/script/train/GetTrainNumber.html) |
| 5 | X座標(横)   | [GetPosition()](https://vrmcloud.net/nx/script/script/data/GetPosition.html)[0] |
| 6 | Z座標(縦)   | GetPosition()[2] |
| 7 | Y座標(高さ) | GetPosition()[1] |
| 8 | 角度 | [GetRotate()](https://vrmcloud.net/nx/script/script/data/GetRotate.html) |
| 9 | 車両数 | len([GetCarList()](https://vrmcloud.net/nx/script/script/train/GetCarList.html)) |
| 10 | ダミーフラグ | [GetDummyMode()](https://vrmcloud.net/nx/script/script/train/GetDummyMode.html) |

### (2) ポイント一覧
| 列   | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | p (固定文字) | 識別文字 |
| 2 | ポイントID    | [GetID()](https://vrmcloud.net/nx/script/script/data/GetID.html) |
| 3 | ポイント名  | [GetNAME()](https://vrmcloud.net/nx/script/script/data/GetNAME.html) |
| 4 | 分岐状態(0,1) | [GetBranch()](https://vrmcloud.net/nx/script/script/point/GetBranch.html) |
| 5 | X座標(横)   | [GetPosition()](https://vrmcloud.net/nx/script/script/data/GetPosition.html)[0] |
| 6 | Z座標(縦)   | GetPosition()[2] |
| 7 | Y座標(高さ) | GetPosition()[1] |

## sendStateFile関数
オプション機能で命令実行後に「sendフォルダ」へ「レイアウト情報ファイル」を出力することができます。  
「sendSettingFile関数」と動作が似ていますが出力内容が異なります。  

利用する場合は以下のフラグを「True」にします。  
「readFile関数」が実行されるたびにファイルを作成します。

```py
# 出力機能(True…有効、False…無効)
_sendState = False
```

「sendフォルダ」がある状態で「sendStateFile」関数を実行するとレイアウトファイルから編成リストとポイントリストをID順でタブ区切りのShift_JISテキストファイルとして「send\yyyymmddhhmmssffffff.txt」へ出力します。  
「sendフォルダ」が無い場合は起動時のフォルダチェックでエラーとなり、機能が無効になります。  
ダミー編成、および頭文字が「dummy」のポイントは除外されます。

出力例：
```
t	10	0.0
t	64	0.0

p	12	0
p	20	1
p	55	0
p	63	0
```

### (1) 編成一覧
| 列   | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | t (固定文字) | 識別文字 |
| 2 | 列車ID | [GetID()](https://vrmcloud.net/nx/script/script/data/GetID.html) |
| 3 | 速度(電圧0.0～1.0) | [GetVoltage()](https://vrmcloud.net/nx/script/script/train/GetVoltage.html) |

### (2) ポイント一覧
| 列   | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | p (固定文字) | 識別文字 |
| 2 | ポイントID    | [GetID()](https://vrmcloud.net/nx/script/script/data/GetID.html) |
| 3 | 分岐状態(0,1) | [GetBranch()](https://vrmcloud.net/nx/script/script/point/GetBranch.html) |
