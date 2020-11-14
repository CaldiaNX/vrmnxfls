# -*- coding: utf-8 -*-
"""
VRM-NX ファイル連携システム
"""
__author__ = "Caldia"
__status__ = "production"
__version__ = "1.3"
__date__    = "2020/09/27"

import vrmapi
import shutil
import os.path
from datetime import datetime
from pathlib import Path

#ファイル読み込みの確認用
vrmapi.LOG(vrmapi.SYSTEM().GetLayoutPath())
vrmapi.LOG(vrmapi.SYSTEM().GetLayoutDir())
#p = Path(vrmapi.SYSTEM().GetLayoutDir())
#vrmapi.LOG(str(p.cwd()))
#vrmapi.LOG(str(p.home()))
vrmapi.LOG("load vrmnxfls.py")

def readFile():
    """
    「read」フォルダのファイルを読み込みます。
    レイアウトファイルと同じディレクトリに「read」フォルダと「read_end」フォルダを作成してください。
    """
    # Pathオブジェクトを生成
    p = Path(vrmapi.SYSTEM().GetLayoutDir() + "\\read")
    l = list(p.glob("*.txt"))
    for item in l:
        #vrmapi.LOG(str(item))
        #withでテキスト読み込みモード使用
        with open(item, 'r') as text:
            # 文字列を全て読み込む
            t = text.read()
            # タブで分割
            line = t.split()
            # 要素が0:Object種別、1:ID、2:命令、3:Paramの4つ以上
            if len(line) >= 4:
                readFileLine(line)
            vrmapi.LOG(str(t))
        # 読み込んだファイルは別フォルダへ移動
        re = vrmapi.SYSTEM().GetLayoutDir() + "\\read_end\\" + item.name
        #vrmapi.LOG(str(re))
        shutil.move(item, re)

def readFileLine(line):
    """
    ファイルの命令を解析して実行します。
    """
    #vrmapi.LOG(line[0])
    # 種別T＝列車オブジェクト
    if line[0] == "T":
        #vrmapi.LOG(line[1])
        train = vrmapi.LAYOUT().GetTrain(int(line[1]))
        if line[2] == "AutoSpeedCTRL":
            #vrmapi.LOG(line[2])
            train.AutoSpeedCTRL(int(line[3]), float(line[4]))
        elif line[2] == "Turn":
            train.Turn()
    # 種別P＝ポイントオブジェクト
    elif line[0] == "P":
        vrmapi.LOG(line[1])
        # アンダーバーで複数あり(カンマは運転盤のcheckbox.Nameでエラーのため使えず)
        if ('_') in line[1]:
            # アンダーバーで分割
            pAry = line[1].split('_')
            # 複数ポイント処理
            for p in pAry:
                # ID検索
                point = vrmapi.LAYOUT().GetPoint(int(p))
                #vrmapi.LOG("Search:" + p)
                if line[2] == "SetBranch":
                    point.SetBranch(int(line[3]))
                    #vrmapi.LOG("Hit:" + p)
        else:
            # ID検索
            point = vrmapi.LAYOUT().GetPoint(int(line[1]))
            if line[2] == "SetBranch":
                point.SetBranch(int(line[3]))

def sendSettingFile():
    """
    レイアウト情報を「send」フォルダへファイル出力します。
    """
    if(os.path.exists(vrmapi.SYSTEM().GetLayoutDir() + "\\send") == False):
        #vrmapi.LOG("vrmnxfls.sendSettingFile is no find send\\ folder.")
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
    path_w = vrmapi.SYSTEM().GetLayoutDir() + "\\send\\" + timeText + '.txt'
    with open(path_w, mode='w') as f:
        f.write(text)
        vrmapi.LOG("sendフォルダにレイアウト情報ファイルを出力しました。")
