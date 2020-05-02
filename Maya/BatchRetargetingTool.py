
# import os
# # from maya import OpenMaya
from maya import cmds
from maya import mel
import pymel.core as pm
import os

from PySide2.QtCore import SIGNAL, QObject, QDir, QFileInfo

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
                           QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# 加载HumanIK控制代码
MAYA_LOCATION = os.environ['MAYA_LOCATION']
# 执行对应的mel代码
mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikGlobalUtils.mel"')
mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikCharacterControlsUI.mel"')
mel.eval('source "'+MAYA_LOCATION +
         '/scripts/others/hikDefinitionOperations.mel"')


class Ui_Form(object):
    def setupUi(self, Form):
        # if not Form.objectName():
        #     Form.setObjectName(u"Form")
        self.resize(593, 545)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_animationFilePath = QPushButton(Form)
        self.pushButton_animationFilePath.setObjectName(
            u"pushButton_animationFilePath")

        self.gridLayout.addWidget(
            self.pushButton_animationFilePath, 2, 1, 1, 1)

        self.pushButton_targetSkin = QPushButton(Form)
        self.pushButton_targetSkin.setObjectName(u"pushButton_targetSkin")

        self.gridLayout.addWidget(self.pushButton_targetSkin, 0, 1, 1, 1)

        self.lineEdit_sourceSkin = QLineEdit(Form)
        self.lineEdit_sourceSkin.setObjectName(u"lineEdit_sourceSkin")

        self.gridLayout.addWidget(self.lineEdit_sourceSkin, 1, 0, 1, 1)

        self.lineEdit_targetSkin = QLineEdit(Form)
        self.lineEdit_targetSkin.setObjectName(u"lineEdit_targetSkin")

        self.gridLayout.addWidget(self.lineEdit_targetSkin, 0, 0, 1, 1)

        self.lineEdit_animationFilePath = QLineEdit(Form)
        self.lineEdit_animationFilePath.setObjectName(
            u"lineEdit_animationFilePath")

        self.gridLayout.addWidget(self.lineEdit_animationFilePath, 2, 0, 1, 1)

        self.pushButton_sourceSkin = QPushButton(Form)
        self.pushButton_sourceSkin.setObjectName(u"pushButton_sourceSkin")

        self.gridLayout.addWidget(self.pushButton_sourceSkin, 1, 1, 1, 1)

        self.lineEdit_outputFilePath = QLineEdit(Form)
        self.lineEdit_outputFilePath.setObjectName(u"lineEdit_outputFilePath")

        self.gridLayout.addWidget(self.lineEdit_outputFilePath, 3, 0, 1, 1)

        self.pushButton_outputFilePath = QPushButton(Form)
        self.pushButton_outputFilePath.setObjectName(
            u"pushButton_outputFilePath")

        self.gridLayout.addWidget(self.pushButton_outputFilePath, 3, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.plainTextEdit = QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_start = QPushButton(Form)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.horizontalLayout.addWidget(self.pushButton_start)

        self.pushButton_stop = QPushButton(Form)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.horizontalLayout.addWidget(self.pushButton_stop)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(
            u"HumanIK\u6279\u91cf\u91cd\u5b9a\u5411\u5de5\u5177")
        self.pushButton_animationFilePath.setText(
            u"\u52a8\u753b\u6587\u4ef6\u8def\u5f84")
        self.pushButton_targetSkin.setText(
            u"\u76ee\u6807\u8499\u76ae\u6587\u4ef6")
        self.pushButton_sourceSkin.setText(u"\u6e90\u8499\u76ae\u6587\u4ef6")
        self.pushButton_outputFilePath.setText(u"\u5bfc\u51fa\u8def\u5f84")
        self.pushButton_start.setText(u"\u5f00\u59cb")
        self.pushButton_stop.setText(u"\u505c\u6b62")
    # retranslateUi


class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)    # 执行父类的__init__()
        self.setupUi(self)  # 调用 ui.Ui_Form 的 setupUi()
        # 绑定按键事件
        self.pushButton_targetSkin.clicked.connect(self.slotTargetSkinClicked)
        self.pushButton_animationFilePath.clicked.connect(
            self.slotAnimationFilePathClicked)
        self.pushButton_outputFilePath.clicked.connect(
            self.slotOutputFilePathClicked)
        self.pushButton_sourceSkin.clicked.connect(self.slotSourceSkinClicked)
        self.pushButton_start.clicked.connect(self.slotStartClicked)
        self.pushButton_stop.clicked.connect(self.slotStopClicked)
        # 定义属性
        self.bTermination = False
        self.AnimationFileList = []

    def slotSourceSkinClicked(self):
        sourceSkinFilePath = QFileDialog.getOpenFileName(self,
                                                         u"源蒙皮文件", "/home/jana", u"maya Files (*.ma *.mb)")
        self.lineEdit_sourceSkin.setText(sourceSkinFilePath[0])

    def slotTargetSkinClicked(self):
        targetSkinFilePath = QFileDialog.getOpenFileName(self,
                                                         u"目标蒙皮文件", "/home/jana", u"maya Files (*.ma *.mb)")
        self.lineEdit_targetSkin.setText(targetSkinFilePath[0])

    def slotAnimationFilePathClicked(self):
        animationFilePath = QFileDialog.getExistingDirectory(self,
                                                             u"选择动画文件路径", "/home/jana", QFileDialog.ShowDirsOnly
                                                             | QFileDialog.DontResolveSymlinks)
        self.lineEdit_animationFilePath.setText(animationFilePath)

    def slotOutputFilePathClicked(self):
        outputFilePath = QFileDialog.getExistingDirectory(self,
                                                          u"选择输出文件路径", "/home/jana", QFileDialog.ShowDirsOnly
                                                          | QFileDialog.DontResolveSymlinks)
        self.lineEdit_outputFilePath.setText(outputFilePath)

    def slotStartClicked(self):
        self.bTermination = False
        if(len(self.lineEdit_animationFilePath.text()) == 0 | len(self.lineEdit_outputFilePath.text()) == 0 | len(self.lineEdit_sourceSkin.text()) == 0 | len(self.lineEdit_targetSkin.text()) == 0):
            return
        self.findFile(self.lineEdit_animationFilePath.text())

        complete = 0
        for animfilePath in self.AnimationFileList:
            if(self.bTermination):
                break
            outputFilePath = animfilePath.replace(
                self.lineEdit_animationFilePath.text(), self.lineEdit_outputFilePath.text())
            # 检查目录是否存在，不存在则创建
            self.generateDirectorys(outputFilePath)

            # 新建场景
            cmds.file(new=True, force=True)
            # cmds.file(self.lineEdit_sourceSkin.text(), o=True)

            # 导入蒙皮文件
            cmds.file(self.lineEdit_sourceSkin.text(), i=True, renameAll=True, mergeNamespacesOnClash=True,
                      namespace=":")
            # 导入动画文件
            cmds.file(animfilePath, i=True, renameAll=True, type='fbx', mergeNamespacesOnClash=True,
                      namespace=":", options="fbx", importFrameRate=True, importTimeRange='override')

            # 导入蒙皮文件
            cmds.file(self.lineEdit_targetSkin.text(), i=True, renameAll=True, mergeNamespacesOnClash=False,
                      namespace="target")

            # 设置Character与Source
            # 判断是否存在HumanIK界面，不存在则创建
            mel.eval('hikCreateCharacterControlsDockableWindow()')

            # 查询指定名称的下拉菜单控件并且设置选项
            allCharacter = cmds.optionMenuGrp(
                "hikCharacterList", query=True, itemListLong=True)

            i = 1
            for item in allCharacter:
                # This is the name of the option menu that lives in the HIK window globally
                optMenu = "hikCharacterList|OptionMenu"
                sourceChar = cmds.menuItem(item, query=True, label=True)
                if sourceChar.find("target", 0, len(sourceChar)) != -1:
                    cmds.optionMenu(optMenu, edit=True, select=i)
                    mel.eval('hikUpdateCurrentCharacterFromUI()')
                    mel.eval('hikUpdateContextualUI()')
                    mel.eval('hikUpdateCharacterMenu()')
                    # 位于hikCallbackOperations.mel
                    mel.eval('hikUpdateCharacterControlsUICallback()')
                    break

                i += 1

            allSource = cmds.optionMenuGrp(
                "hikSourceList", query=True, itemListLong=True)
            i = 1
            for item in allSource:
                # This is the name of the option menu that lives in the HIK window globally
                optMenu = "hikSourceList|OptionMenu"
                sourceChar = cmds.menuItem(item, query=True, label=True)

                # 注意source选项前面有空格
                if sourceChar == " Character1":
                    cmds.optionMenu(optMenu, edit=True, select=i)
                    mel.eval('hikUpdateCurrentSourceFromUI()')
                    mel.eval('hikUpdateContextualUI()')
                    # 位于hikCallbackOperations.mel
                    mel.eval('hikControlRigSelectionChangedCallback()')
                    break

                i += 1

            # 选中骨骼并导出文件
            cmds.select('target:root')

            mel.eval('FBXExportBakeComplexAnimation -v true;')
            mel.eval('FBXExport -f "'+outputFilePath+'" -s')
            # 显示输出结果
            complete += 1
            self.progressBar.setValue(
                complete*100.0/len(self.AnimationFileList))
            self.plainTextEdit.appendPlainText(outputFilePath)
            self.update()

    def slotStopClicked(self):
        self.bTermination = True

    def findFile(self, _filePath):
        # 通过递归的方式，遍历所有动画文件
        animationFilePath = QDir(_filePath)
        animationFilePath.setFilter(
            QDir.Dirs | QDir.Files | QDir.NoDotAndDotDot)
        animationFilePath.setSorting(QDir.DirsFirst)

        list = animationFilePath.entryInfoList()
        if(len(list) < 1):
            return

        i = 0
        # 采用递归算法
        while(i < len(list)):
            fileInfo = list[i]
            bisDir = fileInfo.isDir()
            if(bisDir):
                self.findFile(fileInfo.filePath())
            else:
                self.AnimationFileList.append(fileInfo.filePath())
            i += 1

    def generateDirectorys(self, _dir):
        sourceDir = QFileInfo(_dir).dir()
        if (sourceDir.exists()):
            return

        tempDir = ''
        directorys = sourceDir.path().split("/")

        for i in range(0, len(directorys), 1):
            tempDir += directorys[i] + "/"

            dir = QDir(tempDir)
            if (dir.exists() == False):
                dir.mkdir(tempDir)


def main():
    global win
    try:
        win.close()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    except:
        pass

    win = MainWindow()
    win.show()


if __name__ == "__main__":
    main()
