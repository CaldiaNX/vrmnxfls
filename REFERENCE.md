# VRMNXファイル連携システム 仕様

## readFile関数
「read」フォルダにテキストファイルがあると`readFile`関数がファイルを読み込み、命令を実行します。  
ファイルはダブルクオーテーション無し、改行無し、タブ区切りの1行Shift-JISテキスト形式です。  
ファイル名は年月日時分秒「yyyymmddhhmmssfff.txt」です。  
読み込み対象は「＊.txt」で検出します。  
年月日時分秒の命名規則はFIFO（先入れ先出し）を遵守するためのルールです。  

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
|T |ID|[AutoSpeedCTRL](AutoSpeedCTRL)|0.0～1.0(最高速度の割合)|
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
編成別に処理したい場合は```setPower```関数を利用します。

## sendSettingFile関数
「send」フォルダがある状態で`sendSettingFile`関数を実行するとレイアウトファイルから編成リストとポイントリストをID順でタブ区切りのShift_JISテキストファイルとして`send\yyyymmddhhmmssffffff.txt`へ出力します。  
主に「ネットワークコントローラー」等の設定情報として利用できます。  

出力に成功すると
```
sendフォルダにレイアウト情報ファイルを出力しました。
```
と表示します。  

出力例：
```
t	10	TRAIN_10	2028.6000053961689	6.0	1096.0780848595002	0.0
t	25	TRAIN_25	1297.874999999999	6.0	1400.0000223802317	0.0
t	54	TRAIN_54	1291.4000003714773	6.0	1163.484177169418	0.0
t	64	TRAIN_64	2028.6000027358723	6.0	1332.593930070314	0.0

p	675	B線上駅C渡り線XL	2108.00009006219	0.0	411.48450518271034	0
p	676	C線上駅B渡り線XL	2364.0000885889813	0.0	445.18758033766994	0
p	677	C線上駅B渡り線XL	2108.000088588982	0.0	445.18756914755403	0
p	678	B線上駅C渡り線XR	2364.0000900621894	0.0	411.4845163728262	0
```

### (1) 編成一覧
| 列 | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | t(固定文字) | Object識別子 |
| 2 | ObjectID    | GetID() |
| 3 | ObjectNAME  | GetNAME() |
| 4 | X座標(横)   | GetPosition()[0] |
| 5 | Y座標(高さ) | GetPosition()[1] |
| 6 | Z座標(縦)   | GetPosition()[2] |
| 7 | 速度(電圧0.0～1.0) | GetVoltage() |

### (2) ポイント一覧
| 列 | 内容 | 詳細 |
| ---- | ---- | ---- |
| 1 | p(固定文字) | Object識別子 |
| 2 | ObjectID    | GetID() |
| 3 | ObjectNAME  | GetNAME() |
| 4 | X座標(横)   | GetPosition()[0] |
| 5 | Y座標(高さ) | GetPosition()[1] |
| 6 | Z座標(縦)   | GetPosition()[2] |
| 7 | 分岐状態(0,1) | GetBranch() |

## 履歴
- 2021/09/05 v1.7
  - エラーファイルで無限ループに陥る症状を「ERR_*.txt」で出力して抜け出すように修正。
  - 「PlayHorn」「SplitTrain」を実装。
  - 履歴をこちらへ移動。実装命令一覧を追記。
- 2021/06/05 v1.6
  - 呼び出し方法を変更。※既存レイアウトは修正が必要
  - 細部の記述を修正
- 2020/11/14 v1.5
  - 複数分岐操作で負数の場合に逆方向とする機能を追加
- 2020/10/24 v1.4
  - 編成の電源を制御する「setPower」「setPowerAll」追加
- 2020/09/27 v1.3
  - アンダーバー区切りによるポイント一括設定に対応
- 2020/09/23 v1.2
  - レイアウト情報出力「sendSettingFile」追加
- 2020/09/14 v1.1
  - 方向転換「Turn」命令追加
- 2019/12/29 v1.0
  - 公開
