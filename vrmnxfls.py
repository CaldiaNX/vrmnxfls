# -*- coding: utf-8 -*-
"""
@author: Caldia
"""

import vrmapi
import shutil
from pathlib import Path

#ファイル読み込みの確認用
vrmapi.LOG("load vrmnxfls.py")

# ファイル連携システム
# レイアウトファイルのフォルダに「read」フォルダと「read_end」フォルダを作成してください
def readFile():
        #vrmapi.LOG(str(p.cwd()))
        #vrmapi.LOG(str(p.home()))
        #vrmapi.LOG(vrmapi.SYSTEM().GetLayoutPath())
        #vrmapi.LOG(vrmapi.SYSTEM().GetLayoutDir())
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

# ファイル連携システム命令セット
def readFileLine(line):
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
        #vrmapi.LOG(line[1])
        point = vrmapi.LAYOUT().GetPoint(int(line[1]))
        if line[2] == "SetBranch":
            point.SetBranch(int(line[3]))
