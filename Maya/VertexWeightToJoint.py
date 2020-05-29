from maya import cmds
from maya import mel
import pymel.core as pm

# 初始化变量
parentJoint = 'joint5'
jointRadius = 0.3
# VertexToJointMap = {"one": 1, "two": 2, "three": 3, "four": 4}
VertexToJointMap = {}
# 假设选择若干顶点
selected = cmds.ls(selection=True, flatten=True)
# 取得蒙皮Mesh对象
skinMesh = selected[0].split('.')[0]


for vertex in selected:
    vertexPosition = cmds.xform(vertex, query=True, ws=True, t=True)

    # 绝对坐标创建并创建父子关系(其他参数：name、)
    cmds.select(parentJoint, r=True)
    createJoint = cmds.joint(p=vertexPosition, radius=jointRadius, a=True)
    cmds.joint(parentJoint, e=True, zso=True, oj="xyz", sao="yup")

    VertexToJointMap[vertex] = createJoint

# 取得根骨骼
rootJointName = pm.selected()[0].root().name()

# 创建Smooth蒙皮
cmds.skinCluster(rootJointName, skinMesh, dr=4.0)

# 设置蒙皮值
for vertex in VertexToJointMap:
    cmds.skinPercent('skinCluster1', vertex, transformValue=[
                     (VertexToJointMap[vertex], 1.0)])
