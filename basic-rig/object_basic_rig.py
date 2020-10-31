import maya.cmds as cmds
from random import randint


objetos = cmds.ls( selection=True )
print objetos

new_shapes = []
full_size = 0
axis = ['x', 'y', 'z']
attrs = ['t', 'r', 's']
rand_num = 0

for item in objetos:

    size = cmds.xform(item, q=1, bb=1)
    finalsize = size[0] - size[3]
    full_size +=finalsize
    print "name: {} xsize: {} bb: {}".format(item, finalsize, size)
    circle_01,circle_01_his = cmds.circle( nr=(0, 0, 1), c=(0, 0, 0), r=finalsize)
    print circle_01
    new_shapes.append(circle_01)
    cmds.select(circle_01)
    shape_circle = cmds.listRelatives(circle_01, shapes=True)
    rand_num = randint(0,31)
    shape = cmds.listRelatives(item, shapes=True)
    cmds.setAttr(shape_circle[0]+'.overrideEnabled', 1)
    cmds.setAttr(shape[0]+'.overrideEnabled', 1)
    cmds.setAttr(shape_circle[0]+'.overrideColor', rand_num)
    cmds.setAttr('{0}.overrideColor'.format(shape[0]), rand_num)
    cmds.rotate( '90deg', 0, 0, r=True )
    ctrl = cmds.pointConstraint( item, circle_01)
    cmds.delete(ctrl)
    cmds.parent(item, circle_01)
    cmds.select(circle_01)
    cmds.FreezeTransformations
    cmds.makeIdentity(apply = True, t=1, r=1, s=1, n=0, pn=1)
    cmds.DeleteHistory()
    cmds.delete(ch=True)
    
    for ax in axis:
        for attr in attrs:
            cmds.setAttr(item+'.'+attr+ax, lock=1)
    
general_ctrl = cmds.circle( nr=(0, 0, 1), c=(0, 0, 0), n=u'ctrl_general', r=full_size*1.3)
cmds.select(general_ctrl[0])
shape_general_ctrl = cmds.listRelatives(general_ctrl, shapes=True)
cmds.setAttr('{0}.overrideEnabled'.format(shape_general_ctrl[0]), 1)
cmds.setAttr('{0}.overrideColor'.format(shape_general_ctrl[0]), 13)

for num in range(0,7):

    if num%2 == 0:

        cmds.select('{0}.cv[{1}]'.format(general_ctrl[0], num),tgl=True)
        
cmds.scale(0.196501, 0.196501, 1, r=1, p=(0, 0, 0))
temporal_grp = cmds.group(new_shapes, n='Temp')
cmds.CenterPivot
cmds.xform(cpc=True)
ctrl_Const = cmds.pointConstraint( temporal_grp, general_ctrl[0] )
cmds.delete(ctrl_Const)
cmds.select(general_ctrl[0])
cmds.FreezeTransformations
cmds.makeIdentity(apply = True, t=1, r=1, s=1, n=0, pn=1)
cmds.DeleteHistory
cmds.delete(ch=True)
cmds.parent(new_shapes, general_ctrl[0])
cmds.delete(temporal_grp)

#for shape in new_shapes:
    
