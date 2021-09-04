__title__ = "VRMNXファイル連携システム Ver.1.7"
__author__ = "Caldia"
__update__  = "2021/09/05"

import vrmapi
import shutil
import os.path
from datetime import datetime
from pathlib import Path

# ファイル読み込みの確認用
vrmapi.LOG("import " + __title__)

# main
def vrmevent(obj,ev,param):
    if ev == 'init':
        # フォルダチェック
        dir = vrmapi.SYSTEM().GetLayoutDir()
        if(os.path.exists(dir + "\\read") == False):
            vrmapi.LOG(dir + "\\read フォルダがありません。")
            return
        if(os.path.exists(dir + "\\read_end") == False):
            vrmapi.LOG(dir + "\\read_end フォルダがありません。")
            return
        # 起動時に0.1秒間隔のタイマーイベントを登録
        obj.SetEventTimer(0.1)
        # (任意)レイアウト内の全編成の電源を一括設定(0:OFF, 1:ON)
        #setPowerAll(0)
        # (任意)sendフォルダにポイントと編成情報を出力
        #sendSettingFile()
    elif ev == 'timer':
        # タイマーイベントでフォルダを周期監視
        readFile()


# readフォルダのファイル読み込み
def readFile():
    # Pathオブジェクトを生成
    p = Path(vrmapi.SYSTEM().GetLayoutDir() + "\\read")
    l = list(p.glob("*.txt"))
    for item in l:
        try:
            #withでテキスト読み込みモード使用
            with open(item, 'r') as text:
                # 文字列を全て読み込む
                t = text.read()
                # タブで分割
                line = t.split()
                # 要素が0:Object種別、1:ID、2:命令、3:Paramの4つ以上
                if len(line) >= 4:
                    readFileLine(line)
                #vrmapi.LOG(str(t))
            # 読み込んだファイルは別フォルダへ移動
            re = vrmapi.SYSTEM().GetLayoutDir() + "\\read_end\\" + item.name
            #vrmapi.LOG(str(re))
            shutil.move(item, re)
        except Exception as e:
            # エラーファイルは名前を変えて別フォルダへ移動
            re = vrmapi.SYSTEM().GetLayoutDir() + "\\read_end\\ERR_" + item.name
            vrmapi.LOG(str(e))
            vrmapi.LOG(str(re))
            shutil.move(item, re)



# ファイルの命令を解析して実行
def readFileLine(line):
    # 種別T＝列車オブジェクト
    if line[0] == "T":
        #vrmapi.LOG(line[1])
        train = vrmapi.LAYOUT().GetTrain(int(line[1]))
        if line[2] == "AutoSpeedCTRL":
            #vrmapi.LOG(line[2])
            train.AutoSpeedCTRL(int(line[3]), float(line[4]))
        elif line[2] == "Turn":
            train.Turn()
        elif line[2] == "PlayHorn":
            train.PlayHorn(int(line[3]))
        elif line[2] == "SplitTrain":
            spl = train.SplitTrain(int(line[3]))
            vrmapi.LOG("Train[{}].SplitTrain({})->Train[{}]".format(line[1], line[3], spl))
        elif line[2] == "SetPower":
            setPower(train, int(line[3]))
    # 種別P＝ポイントオブジェクト
    elif line[0] == "P":
        vrmapi.LOG(line[1])
        # 向き
        d = int(line[3])
        # アンダーバーで複数あり(カンマは運転盤のcheckbox.Nameでエラーのため使えず)
        if ('_') in line[1]:
            # アンダーバーで分割
            pAry = line[1].split('_')
            # 複数ポイント処理
            for p in pAry:
                pid = int(p)
                # 負数の場合
                if pid < 0:
                    # 整数に戻す
                    pid = -pid
                    # 方向反転
                    if d == 0:
                        d = 1
                    else:
                        d = 0
                # ID検索
                point = vrmapi.LAYOUT().GetPoint(pid)
                vrmapi.LOG("SetBranch:" + str(pid) + " " + str(d))
                if line[2] == "SetBranch":
                    point.SetBranch(d)
        else:
            # ID検索
            point = vrmapi.LAYOUT().GetPoint(int(line[1]))
            if line[2] == "SetBranch":
                point.SetBranch(d)

# 指定編成の車両電装を制御
def setPower(tra, sw):
    # サウンド変更
    if sw == 0:
        # 再生停止
        tra.SetSoundPlayMode(0)
    else:
        # 常時再生
        tra.SetSoundPlayMode(2)
    #車両数を取得
    len = tra.GetNumberOfCars()
    #車両ごとに処理
    for i in range(0, len):
        #ダミーは対象外
        if tra.GetDummyMode():
            vrmapi.LOG(tra.GetNAME() + " ダミースキップ")
        else:
            # 車両を取得
            car = tra.GetCar(i)
            # 方向幕
            car.SetRollsignLight(sw)
            # 室内灯
            car.SetRoomlight(sw)
            # LED
            car.SetLEDLight(sw)
            # 運転台室内灯
            car.SetCabLight(sw)
            # パンダグラフ個数確認
            for j in range(0, car.GetCountOfPantograph()):
                # パンタグラフ
                car.SetPantograph(j,sw)
            # 先頭車両処理(ifを外して中間連結車も含む)
            #if i == 0:
            # ヘッドライト
            car.SetHeadlight(sw)
            # 最後尾車両処理(ifを外して中間連結車も含む)
            #if i == len - 1:
            # テールライト
            car.SetTaillight(sw)
            # 運転台室内灯
            car.SetCabLight(sw)
            # 蒸気機関車用（テンダーも対象）
            if car.GetCarType() == 1:
                # 煙
                car.SetSmoke(sw)

# 全編成の電源を一括操作
def setPowerAll(sw):
    # 編成リストを取得
    tList = vrmapi.LAYOUT().GetTrainList()
    # 編成ごとに処理
    for tra in tList:
        setPower(tra, sw)


# レイアウト情報を「send」フォルダへファイル出力
def sendSettingFile():
    dir = vrmapi.SYSTEM().GetLayoutDir()
    if(os.path.exists(dir + "\\send") == False):
        vrmapi.LOG(dir + "\\send フォルダがありません。")
        return

    s = list()

    #編成リストを新規編成リストに格納
    tList = vrmapi.LAYOUT().GetTrainList()
    #新規編成リストから編成を繰り返し取得
    for t in tList:
        pos = t.GetPosition()
        s.append('t\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(t.GetID(), t.GetNAME(), pos[0], pos[1], pos[2], t.GetVoltage()))
    s.append('\n')

    #新規ポイントリストを作成
    pList=list()
    #ポイントリストを新規ポイントリストに格納
    vrmapi.LAYOUT().ListPoint(pList)
    #新規ポイントリストからポイントを繰り返し取得
    for p in pList:
        pos = p.GetPosition()
        s.append('p\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(p.GetID(), p.GetNAME(), pos[0], pos[1], pos[2], p.GetBranch()))
    s.append('\n')

    # 結合
    text = ''.join(s)
    # ファイル出力
    timeText = datetime.now().strftime('%Y%m%d%H%M%S%f')
    path_w = dir + "\\send\\" + timeText + '.txt'
    with open(path_w, mode='w') as f:
        f.write(text)
        vrmapi.LOG(dir + "\\send フォルダにレイアウト情報ファイルを出力しました。")
