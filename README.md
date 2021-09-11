# VRMNXファイル連携システム

## 概要
「VRMNXファイル連携システム」（VRMNX File linkege System：VRMNX FLS）は「[鉄道模型シミュレーターNX](http://www.imagic.co.jp/hobby/products/vrmnx/ "鉄道模型シミュレーターNX")」（VRMNX）のビュワーオブジェクトを外部から制御するためのシステムです。  

タイマーイベント(既定は0.1秒毎)でレイアウトファイルと同階層にある「readフォルダ」の「オブジェクト命令ファイル」を読み込み、テキストで記述されている命令をVRMNXで実行します。  
オプション機能で命令実行後に「sendフォルダ」へ「レイアウト情報ファイル」を出力することもできます。

![vrmfls](https://user-images.githubusercontent.com/66538961/132936559-80d0a686-aac4-408e-b33d-89f28801c467.png)

## ダウンロード
- [vrmnxfls.py](https://raw.githubusercontent.com/CaldiaNX/vrmnxfls/main/vrmnxfls.py)

## 利用方法
レイアウトファイルと同じフォルダ階層に「vrmnxfls.py」ファイルと「read」「read_end」フォルダを配置します。  

フォルダ構成例：
```
C:\VRMNX
├ \read
├ \read_end
├ \send  (任意：レイアウト情報ファイル出力用）
├ vrmnxfls.py
└ VRMNXレイアウトファイル.vrmnx
```

対象レイアウトのレイアウトスクリプトに以下の★内容を追記します。  

```py
#LAYOUT
import vrmapi
import vrmnxfls # ★インポート

def vrmevent(obj,ev,param):
    vrmnxfls.vrmevent(obj,ev,param) # ★メイン処理
    if ev == 'init':
        dummy = 1
    elif ev == 'broadcast':
        dummy = 1
    elif ev == 'timer':
        dummy = 1
    elif ev == 'time':
        dummy = 1
    elif ev == 'after':
        dummy = 1
    elif ev == 'frame':
        dummy = 1
    elif ev == 'keydown':
        dummy = 1
```

ファイル読み込みに成功すると、ビューワー起動時のスクリプトログに

```
load VRMNXファイル連携システム Ver.x.x
```

が表示されます。  

## 使い方
「readフォルダ」に「オブジェクト命令ファイル」を置くことでビュワーを操作します。  
読み込んだファイルは「read_end」フォルダへ移動します。  
対応命令や詳細仕様は下記のリファレンスを参照ください。

## 関連資料
- [VRMNXファイル連携システム リファレンス](REFERENCE.md)
- [VRMNXネットワークコントローラー](vrmnxflsNetController.md)
- [VRMNXネットワークコントローラー対応レイアウト](vrmnxflsSampleLayout.md)

## 本システムを使って実現したいこと
- VRMNX以外の外部プログラムや市販コントローラを使った運転や、独自システムとの連携
- ネットワークを介した疑似オンライン運転会

## 今後の実装予定
- 対象オブジェクト・命令セットの拡充
- イベントドリブン（SetEvent～）の追加
