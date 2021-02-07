# VRMNX-FLS対応コントローラー

## 概要
「VRMNXネットワークコントローラー」は「VRMNXファイル連携システム」対応の「鉄道模型シミュレーターNX」操作プログラムです。  
サーバー・クライアントモードを連携させることでネットワーク越しのビュワーを操作することが出来ます。  

![vrmnxfls-net_controller-about](https://user-images.githubusercontent.com/66538961/107125012-7d5fd300-68ea-11eb-88ab-108202b87697.png)

## ダウンロード
サンプルプログラムがOS機能でブロックされる場合はプロパティから「ブロックの解除」をしてください。  
ウィルス対策ソフトで検出される場合は除外操作をしてください。

- [vrmnxflsNetController.zip](https://github.com/CaldiaNX/vrmnxfls/files/5937275/vrmnxflsNetController.zip)

## 操作方法
![vrmnxfls-net_controller-sample](https://user-images.githubusercontent.com/66538961/107125077-08d96400-68eb-11eb-8efd-3f96e305944f.png)

### 動作モード
- ローカルモード
    - 「VRM-NXファイル連携システム」のみを利用するモードです。
    - 「出力フォルダ」パスに命令用ファイルが生成されます。
- クライアントモード
    - 送信先URL・ポート番号に対して「VRM-NXファイル連携システム」対応のUDPコマンドを発信するモードです。
    - 本モードを利用するには別途サーバーが必要です。
    - 送信先URLに「127.0.0.1」または「localhost」を指定することで自身を対象にすることが出来ます。
    - UDPの発信にはエフェメラルポートが利用されます。（ファイアウォール等の設定不要）
    - 「;」で区切ることで複数サーバーに送信します。（※v2.3以降、テスト実装）
- サーバーモード
    - 「VRM-NXファイル連携システム」対応のクライアントから発信されたUDPコマンドを自身の出力フォルダにファイル出力するモードです。
    - 本機能を利用する際はファイアウォールの解除が必要です。通常は「実行」タイミングでファイアウォールからポップアップが表示されるので解除してください。（ポップアップでキャンセルを押した場合「コントロールパネル」→「Windows Defender ファイアウォール」→「Windows Defender ファイアウォールを介したアプリまたは機能を許可」でチェックを入れてください）
    - グローバルネットワークから通信を受け付けるときはルータのポート開放などを行ってください。

### 実行・停止
- 「実行」ボタンを押すと命令出力可能になります。
- 実行中はラジオボタンにロックが掛かります。
- 停止中は分岐制御と編成制御の設定やログ確認が可能ですが命令出力されません。  
  ログには「未出力」と表示されます。
- 「ローカルモード」ではファイル出力、「クライアントモード」ではUDP送信、「サーバーモード」ではUDP受信と、受信パケットのファイル出力が有効になります。

### データグリッド共通操作
- 「ID」列にVRMNXのオブジェクトIDを入力して対象オブジェクトを操作します。  
- 「名前」は任意です。
- 「ID」「名前」ヘッダーをクリックして表示順をソートできます。
- 左端をクリックした行選択モード時に「Del」キーを押すことで行を削除できます。
- 「サーバーモード」ではクライアントから受信した命令内容が表示に反映されます。

### ポイント制御(左)
- 「直」「曲」列をクリックするとポイントを「直進方向」「分岐方向」に切り替えます。
- アンダーバー「_」で複数のIDを繋げて一括制御することが可能です。（例：675_678）
- 負数で「直」「曲」を反転させることが出来ます。渡り線の制御で便利です。（例：675_-678）

### 編成制御(右)
- 「減速」「加速」ボタンで編成の速度を操作します。
- 速度は「AutoSpeedCTRL」関数で変更します。移動距離は速度によって自動調整されます。
- 速度は編成最高速度の0～100％で10％刻みに設定されます。（電圧0.0～1.0に相当）
- 「反転」を押すと編成の向きを反転します。速度は0になります。
- 「Pw」を押すと編成の電装を切り替えます。電装の対象は電灯・効果音・蒸気機関車の煙・パンタグラフです。

### 設定保存
- 「設定保存」ボタンを押すと動作モードの文字列と分岐制御、編成制御のID・名前を`vrmnxflsNetController.txt`にShift_JIS形式のテキストファイルで保存します。
- 保存されたファイルは次回起動時に読み込まれます。
- テキストファイルなので手作業で編集することも可能です。
  - タブ区切りのためタブ文字は利用しないでください。
  - 例外処理などは細かく実装していないのでご注意ください。
- 運転制御盤が有効な場合、表示位置も保存されます。

ファイルサンプル：
```
textBoxPath	C:\VRM-NX\FLS\read
textBoxUrl	127.0.0.1
textBoxSendPort	5200
textBoxReadPort	5200

p	645	A-1
p	635	A-2
p	145	A-3	120	540
p	138	A-4	520	540

t	25	A1_787系_にちりん
t	708	A2_883系_ソニック
t	64	B1_683系_サンダーバード
```

## 運転制御盤
運転制御盤はポイント制御をグラフィカルに操作できるサブコントローラーです。  
「VRMNXネットワークコントローラー」と同階層に「vrmnxflsNetController.png」ファイルを置くと、画像ファイルを透過PNGファイルとして読み込んで別フォームで表示します。

![vrmnxfls-net_controller-controlpanel](https://user-images.githubusercontent.com/66538961/107125172-987f1280-68eb-11eb-8fee-d1a87f6f2f68.png)

設定ファイルでポイント情報に位置情報が登録されている場合、数値を読み込んでポイント操作可能なチェックボックスコントロールを生成します。  
チェック無しが直進、チェックありが分岐方向を示します。  
運転制御盤の配線図作成は作図に特化したWebサービスの [Diagrams.net](https://app.diagrams.net/ "diagrams.net") が便利です。  

## 履歴
- 2020/10/24 v2.5
    - 編成電源スイッチ「Pw」を追加（vrmnxfls.py v1.4以降）
    - 複数ポイントを含んだ状態で設定を保存するとエラーとなる不具合を修正
- 2020/09/27 v2.4
    - アンダーバー区切りによるポイント一括設定に対応（vrmnxfls.py v1.3以降）
- 2020/09/23 v2.3
    - 運転制御盤を実装
    - 列車コントロールボタン配置を入替え
    - クライアントモード時のURLを「;」で区切ることで複数サーバー送信に対応（※暫定）
    - クライアントモード時の不正URLエラー処理を実装
- 2020/09/17 v2.2 （ビルドのみ）
    - DataGridViewのチラツキを低減(DoubleBuffered)
    - DataGridViewの全体サイズ調整、列ヘッダーの幅・高さの変更禁止
    - サーバーモード時にクライアントからの命令をコントロールに反映
    - UDPクラスをサーバーモードとクライアントモードで分離
- 2020/09/16 v2.1
    - 設定保存機能を実装
    - UDPサーバ・クライアントを連続して使う場合にエラーとなる処理を修正
    - 機能ボタン画像を置き換え
    - 速度0及び100の時でも出力されるように変更
- 2020/09/14 v2.0
  - ネットワーク機能搭載。GUIフルチェンジ
- 2019/12/28 v1.0
  - ネットワーク機能のないローカルコントローラーを作成

## 今後の実装予定
- 操作オブジェクトと命令種類の増加
- 双方向通信（uPnP）
- ユーザー識別やアクセスレベル制御
- 複数サーバー・クライアント同期機能