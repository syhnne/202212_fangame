
screen developer_time_set():
    zorder 100
    frame:
        xpos 1700 ypos 20
        vbox:
            textbutton '切换视角' action Show('pov_toggle',dissolve)
            textbutton 'jumpending'action Jump('developer_90')
            textbutton 'p03' action SelectedIf(ToggleDict(persistent.lores, 'p03_read'))
            textbutton 'p05' action SelectedIf(ToggleDict(persistent.lores, 'p05_read'))
            textbutton 'p08' action SelectedIf(ToggleDict(persistent.lores, 'p08_read'))
            textbutton 'p08' action SelectedIf(ToggleDict(persistent.lores, 'p10_read'))
            textbutton 'nightlore' action SelectedIf(ToggleVariable('nightlore'))

label developer_90:
    $ time = 90
    jump expression 'turn' + str(persistent.playthrough)




## 持久化数据 ############################
## 要补充的时候，别忘了去game utter restart函数里面加东西！！！！！！！！！
default persistent.playthrough = 1
## 注：只有在整个游戏流程进行到结尾的时候，才往这个字典中写入剧情信息。
default persistent.lores = {'p03_read':False, 'p05_read':False, 'p08_read':False, 'p10_read':False, 'z09_read':False}
default persistent.unlock_gallery = False




## 定义角色和变量 ###############################################################

default pov_enable_c = True
default pov_enable_z = True
default p03_read = False
default p05_read = False
default p08_read = False
default p10_read = False
default z09_read = False

default z_name = '钟离'
default c_name = '达达利亚'
default npc1_name = '叶卡捷琳娜'
default npc2_name = '???'
default npc3_name = '??'
define test = Character('test')
define narrator = Character('', ctc = 'ctc')
define z = Character('z_name', dynamic = True, ctc = 'ctc') ## 搞立绘的时候加个callback，那个角色回调函数，作出说话人高亮的效果
define c = Character('c_name', dynamic = True, ctc = 'ctc')
define t = Character('旅行者', ctc = 'ctc')
define p = Character('派蒙', ctc = 'ctc')
define npc1 = Character('npc1_name', dynamic = True, ctc = 'ctc')
define npc2 = Character('npc2_name', dynamic = True, ctc = 'ctc')
define npc3 = Character('npc3_name', dynamic = True, ctc = 'ctc')


default pov = None ##方便起见，这东西是个布尔值，True是钟离视角，False是公子视角，一般理性而言，只有一周目开始前和四周目才会出现None
default time = 0 ## 由于时间那个dict不能用list作为value，只好把它做成一个整数，需要判断日期或者时间（指的是上午，下午，晚上那个时间），要用一个函数
default c08_saved = False
default nightlore = True ## 某些特殊剧情里面，晚上最好不要显示一天结束了睡个好觉那种画面，就把这个关掉。

define wanmintangmenu = ['香嫩椒椒鸡','凉拌薄荷','来来菜','扣三丝','四方和平','兽肉薄荷卷','龙须面','米窝窝'] ## 鱼应该不算在钟离讨厌的那种海鲜范围内吧…算了，保险起见，天知道奥赛尔扔没扔过鱼（






## 部分主控流程需要用到的东西，我懒得整理了 ######################################      


screen pov_toggle(stage=0):
    ## stage：0为主界面，其他数字对应几周目
    tag quick_menu ## 别在这种时候显示quick menu啊，我是不打算让观众在这会儿保存的
    modal True
    if stage==0:
        roll_forward True
    zorder 100
    ## 等我画好了禁用钟离视角的界面之后再来解决这个问题：现在的代码太长了，最好在禁用某人视角的时候直接把他的图按到window的background里面，而不是特地做一个用不了的按钮
    window:
        align (0,0)
        background 'gui/pov_toggle/bg.png'
            ## 如何做到按钮的遮挡效果：你先写谁，renpy就先渲染哪个按钮，后来的会挡在先来的前面
        if pov_enable_z:
            imagebutton:
                idle 'gui/pov_toggle/c_idle.png'
                hover 'gui/pov_toggle/c_hover.png'
                selected_idle 'gui/pov_toggle/c_selected.png'
                selected_hover 'gui/pov_toggle/c_selected.png'
                insensitive 'gui/pov_toggle/bg_insensitive_c.png'
                action SetVariable('pov',False)
                selected pov == False
                sensitive pov_enable_c
                focus_mask True
        imagebutton:
            idle 'gui/pov_toggle/z_idle.png'
            hover 'gui/pov_toggle/z_hover.png'
            selected_idle 'gui/pov_toggle/z_selected.png'
            selected_hover 'gui/pov_toggle/z_selected.png'
            ## 他奶奶的，问题果然出在这了！因为有selected表达式，所以以上内容必须分开写
            action SetVariable('pov',True)
            selected pov
            sensitive pov_enable_z
            focus_mask True
        if not pov_enable_z:
            imagebutton:
                idle 'gui/pov_toggle/c_idle.png'
                hover 'gui/pov_toggle/c_hover.png'
                selected_idle 'gui/pov_toggle/c_selected.png'
                selected_hover 'gui/pov_toggle/c_selected.png'
                insensitive 'gui/pov_toggle/bg_insensitive_c.png'
                action SetVariable('pov',False)
                selected pov == False
                sensitive pov_enable_c
                focus_mask True
        textbutton '确认':
            
            if stage==0:
                action ToggleScreen('pov_toggle',dissolve)
            elif stage==4:
                action Return()
            else:
                action Return()
                sensitive pov!=None
                
            xalign 0.5 ypos 30




screen map_liyuegang(spot_has_event=False):
    
    zorder 0    
    window:

        ypos 277 xpos 960 ## 我无语了，天知道那个window为什么到处乱飘，只好手搓pos大力出奇迹
        background ConditionSwitch(
        "clock(time)==0", "gui/map/map_liyuegang 0.png",
        "clock(time)==1", "gui/map/map_liyuegang 1.png",
        "clock(time)==2", "gui/map/map_liyuegang 2.png",)
        use days
        if config.developer:
            use developer_time_set

        for key,value in map_liyuegang_dict.items():

            python:
                
                if pov:
                    map_conditionlist = map_liyuegang_z.get(key)
                else:
                    map_conditionlist = map_liyuegang_c.get(key)
                if type(map_conditionlist) == type(True):
                    showspot = map_conditionlist
                elif type(map_conditionlist) == type([]):
                    showspot = map_conditionlist[0]
                    for i in map_conditionlist:
                        ## 两分钟前：你小子不会是他妈的拿着布尔值当数字给我作比较去了吧
                        ## 刚才：卧槽 还真tm是 难怪不报错
                        if type(i) == type(1) and i == time:
                            showspot = not showspot
                            break
                        elif type(i) == type([]):
                            for q in i:
                                if q == time:
                                    showspot = not showspot
            
            if showspot:
                imagebutton:
                    if key != 'outside' and key != 'stay':
                        at hovered_animation
                    xpos value[0] ypos value[1]
                    if key == 'outside' or key == 'stay':
                        idle Text(value[2], xpos=65, ypos=8, color=gui.idle_color)
                        hover Text(value[2], xpos=65, ypos=8)
                        xsize 300
                    else:
                        idle 'gui/map/spot.png'
                        hover 'gui/map/spot_hover.png'
                    if spot_has_event == key:
                        foreground 'gui/map/spot_foreground_event.png'
                    else:
                        foreground 'gui/map/spot_foreground_notevent.png'
                    action Return(key)
                    tooltip value[2]
                    
        $ tooltip = GetTooltip()            
        if tooltip and tooltip!='离开璃月港…' and tooltip!='不出门…':
            nearrect:
                focus "tooltip"
                prefer_top True
                frame:
                    xalign 0.5
                    text tooltip
            

            

screen days():## 测试用,正式版得改个好看点的，并且改个时间单位
    zorder 50
    $ tooltip = GetTooltip('map_liyuegang')
    window:
        background 'gui/map/mapmenu.png'
        xsize 720 ysize 70 xpos 360 ypos 80
        hbox:
            yalign 0.5 xpos 360 spacing 25
            $ dddate=date(time)
            $ ccclock=clocktext(time)
            
            text '第[dddate]天'
            text '[ccclock]'
            null xsize 60
            if tooltip:
                text tooltip
            else:
                text '去哪里看看…'
            if config.developer:
                text '[time]'
            


init python:
    ## 第一项：布尔值false表示不让你看地图，直接进剧情
    ## 布尔值true表示你可以看地图，但是选哪个都会进一样的剧情
    ## 字符串表示只有你选了这个字符串的地点才能进剧情
    ## 由于我选了这么一种刁钻的方式来触发剧情，想要给进剧情设置条件的时候，就得在另外的地方，往这些dict里面插入内容
    events_z = {
    # 6:['bgyh', 'z01'],
    # 7:['bgyh', 'z01'],
    8:['bgyh', 'p01'],
    10:[False, 'p00'],
    ## events_c[10] = [False, 'p02']
    13:['lygmt','z02'],
    15:['mxjxh', 'z03'],
    16:['mxjxh', 'z03'],
    17:['mxjxh', 'z03'],
    ## events_z[19] = [False, 'p03']
    ## events_z[21] = [False, 'z04']
    ## events_z[24] = ['mxjxh', 'z05']
    32:[False, 'p04'],
    34:['lygmt', 'z06'],
    ## events_z[36] = [False, 'p05']
    42:['wmt', 'p06'],
    48:['wwjs', 'p07'],
    55:[False, 'z08'],
    ## events_z[57] = [False, 'p08']
    ## events_z[60] = [False, 'p09']
    69:['c_home', 'z09'],
    70:['c_home', 'z09'],
    71:['c_home', 'z09'],
    75:['mxjxh', 'z10'], 
    76:['mxjxh', 'z10'], 
    77:['mxjxh', 'z10'], 
    ## events_z[80] = [False, 'p10']
    ## events_z[81] = [False, 'p11']
    87:['outside', 'p12'],
    }

    events_c = {
    0:[True, 'c01'],
    1:[True, 'c01'],
    2:[True, 'c01'],
    4:[False, 'c02'],
    6:[False, 'c03'],
    7:[False, 'c03'],
    8:['stay', 'p01'],
    ## events_z[10] = [False, 'p02']
    13:['lygmt','c04'],
    15:['mxjxh', 'c05'],
    16:['mxjxh', 'c05'],
    17:['mxjxh', 'c05'],
    ## events_c[19] = [False, 'p03']
    ## events_c[21] = [False, 'c06']
    27:['wjt', 'c07'],
    28:['wjt', 'c07'],
    29:['wjt', 'c07'],
    32:[False, 'p04'],
    34:[False, 'c08'],
    36:[False, 'c09'], ## events_c[36] = [False, 'p05']
    ## events_c[37] = [False, 'c10']
    ## events_c[38] = [False, 'c10']
    ## events_c[39] = [True, 'c10']
    ## events_c[40] = [True, 'c10']
    ## events_c[41] = [True, 'c10']
    42:['wmt', 'p06'],
    ## events_c[46] = [False, 'c11']
    48:['wwjs', 'p07'],
    55:['wst', 'c12'],
    56:['wst', 'c12'],
    ## events_c[57] = [False, 'p08']
    ## events_c[60] = [False, 'p09']
    72:['wwjs', 'c15'],
    73:['wwjs', 'c15'],
    74:['wwjs', 'c15'],
    75:['mxjxh', 'c13'], 
    76:['mxjxh', 'c13'], 
    77:['mxjxh', 'c13'], 
    ## events_c[80] = [False, 'p10']
    ## events_c[81] = [False, 'p11']
    86:[False, 'c14'],
    87:['outside', 'p12'],
    }

    ## 这两个map开头的，用来控制地图上的地点在第几天是否显示
    ## 但你要记住一件事，因为你这个做法很烂，所以每次你再list当中塞小list做那种点一次就消失的剧情的时候，必须在那个tag里把这小list删掉
    map_liyuegang_c = {
        'outside':True,
        'stay':True,
        'wmt':True,
        'mxjxh':[False,[15,16,17],[75,76,77],],
        'bgyh':False,
        'wwjs':True,
        'llt':True,
        'xyx':True,
        'yjt':True,
        'lygmt':[False,13],
        'swbgg':[False,range(63,90),],
        'wst':[False,55,56],
        'wjt':[False,[27,28,29]],
        'c_home':False,
        'z_home':[False],
    }

    map_liyuegang_z = {
        'outside':True,
        'stay':True,
        'wmt':True,
        'mxjxh':[False,[15,16,17],27,[75,76,77],],
        'bgyh':[False,6,7,8],
        'wwjs':True,
        'llt':True,
        'xyx':True,
        'yjt':True,
        'lygmt':[False,13,34],
        'swbgg':True,
        'wst':False,
        'wjt':False,
        'c_home':[False,[69,70,71]],
        'z_home':False,  
    }

###############################################################################
## 剧情流程 ####################################################################
###############################################################################

label turn1:

    scene black with dissolve

    while time <= 90:

        ## 特殊剧情判断
        if time == 86:
            if p03_read and persistent.p05_read and persistent.p08_read:
                $ events_c[87]=[False, 'p12']
                $ events_z[87]=[False, 'p12']
        
        if pov:
            $ event = events_z.get(time)
        else:
            $ event = events_c.get(time)

        ## 特殊事件+不允许打开地图
        if event and type(event[0])==type(True) and event[0] == False:
            $ renpy.call(event[1])
            $ time = time + 1 

        ## 允许打开地图
        else:

            if event and type(event[0])==type(''):
                call screen map_liyuegang(event[0]) with dissolve
            else:
                call screen map_liyuegang() with dissolve

            ## 特殊事件，与选项无关
            if event and type(event[0])==type(True) and _return:
                $ renpy.call(event[1])
                $ time = time + 1
            ## 特殊事件，选对才能进
            elif event and type(event[0])==type('') and _return and event[0] == _return:
                $ renpy.call(event[1])
                $ time = time + 1
            ## 无特殊事件
            elif _return:
                $ renpy.call(_return) 
                $ time = time + 1
            
        scene black with dissolve
        if clock(time-1)==2 and time != 0 and _return != False and nightlore and time!=90:
            ## 简单解释上述4个条件。第一个是看你时间是否到晚上。第二个貌似是第一天会卡一些bug，我懒得思考原因，就这样吧。
            ## 第三个是切换视角时需要通过返回一个False快速刷掉不需要的screen，并生成一个新的，但pass语句过后，程序执行到这里会因为符合条件而被拦住。
            ## 如果时间刚好符合，会导致你按切换视角的时候显示“一天结束了”，所以需要此语句判断。
            ## 第四个是手动开关，关了可以不显示这个剧情。
            '又一天结束了…希望晚上能做个好梦。'
        elif time == 90:
            if persistent.playthrough == 1:
                '做了一个梦。'
                '梦中，成千上万的军队向着边境聚集，整装待发，准备听取最后的指令。'
                '他们向亲人与好友告别，为了某个宏大的愿景而聚集在一起，甘愿奉献自己的生命。'
                '可你知道那是徒劳的，在那样的灾难面前，凡人的努力如蚍蜉撼树。'
                '即便如此，仍有人举起手中的武器，愿以凡人的躯体挑战绝对的法则。'
                '正是那样纯粹且炽热的愿望，使神明投下了祂的目光…'
            elif persistent.playthrough == 2:
                '做了一个梦。'
                '梦中，污浊与血迹渗入眼眶，嘶吼和哀嚎刺穿耳膜。'
                '站在已不能被称为家园的这片土地上，任由痛苦与诅咒侵蚀自己的皮肤，思念着永不再归来的平静。'
                '即便是昔日的神明，失去了天空赋予的权柄，也无法再做到什么。'
                '那枚因「愿望」而生的神之眼，便是神明的最后一个「未完成的愿望」…'
            elif persistent.playthrough == 3:
                '做了一个梦。'
                '梦中，世界的法则已尽数崩塌，在混沌和虚无的尽头，万物的界限都变得模糊。'
                '逐渐褪色的视野已无法辨认，眼前那道刺破乌云的光，究竟是拂晓的希望，还是终焉的信号。'
                '只感到记忆飞速流逝，但意识却愈加清醒…'
            

    scene black with dissolve
    if p03_read and persistent.p05_read and persistent.p08_read:
        jump ending1
    elif p03_read or persistent.p05_read or persistent.p08_read:
        jump ending2
    else:
        jump ending3



label turn2:

    scene black with dissolve

    python:
        events_z[34] = ['mxjxh', 'z06_2']

        map_liyuegang_z = {
        'outside':[False,87],
        'stay':False,
        'wmt':False,
        'mxjxh':False,
        'bgyh':[False,8,],
        'wwjs':False,
        'llt':False,
        'xyx':False,
        'yjt':False,
        'lygmt':[False,34,],
        'swbgg':False,
        'wst':False,
        'wjt':False,
        'c_home':False,
        'z_home':False,  
    }

    
    if persistent.lores['p03_read']:

        $ time=8
        call screen map_liyuegang with dissolve
        call p01 from _call_p01
        scene black with dissolve

        $ time=10
        call p02_2 from _call_p02_2
        scene black with dissolve

        $ time=19
        call p03_2 from _call_p03_2
        scene black with dissolve

        $ time=21
        call z04_2 from _call_z04_2
        scene black with dissolve

    if persistent.lores['p05_read']:
        
        $ time=32
        call p04_2 from _call_p04_2
        scene black with dissolve

        $ time=34
        call screen map_liyuegang with dissolve
        call z06_2 from _call_z06_2
        scene black with dissolve

        $ time=36
        call p05_2 from _call_p05_2
        scene black with dissolve

    if persistent.lores['p08_read']:
        
        $ time=57
        call p08_2 from _call_p08_2
        scene black with dissolve

        $ time=60
        call p09_2 from _call_p09_2
        scene black with dissolve

    if persistent.lores['p10_read']:

        $ time=80
        call p10_2 from _call_p10_2
        scene black with dissolve

    python:
        for key,value in persistent.lores:
            if not value:
                all_events_unlocked = False
                break
            else:
                all_events_unlocked = True

    $ time=87
    if not all_events_unlocked:
        call screen map_liyuegang with dissolve
    call p12_2 from _call_p12_2
    scene black with dissolve

    $ time=91
    if all_events_unlocked:
        jump ending4
    else:
        jump ending5




label turn3:

    $ map_liyuegang_c = {
        'outside':True,
        'stay':False,
        'wmt':False,
        'mxjxh':False,
        'bgyh':False,
        'wwjs':False,
        'llt':False,
        'xyx':False,
        'yjt':False,
        'lygmt':False,
        'swbgg':False,
        'wst':False,
        'wjt':False,
        'c_home':False,
        'z_home':False,
    }

    if persistent.lores['p03_read']:

        $ time=10
        call p02_3 from _call_p02_3
        scene black with dissolve

        $ time=19
        call p03_3 from _call_p03_3
        scene black with dissolve

    if persistent.lores['p05_read']:

        $ time=34
        call c08 from _call_c08
        call c09_2 from _call_c09_2
        scene black with dissolve

    if persistent.lores['p08_read']:

        $ time=57
        call screen map_liyuegang with dissolve
        call p08_3 from _call_p08_3
        scene black with dissolve

    $ time=80
    call p10_3 from _call_p10_3
    scene black with dissolve

    $ time=91
    jump ending6






label start:
    ## 「」

    $ _dismiss_pause = False
    # $ _dismiss_pause = config.developer
    if persistent.playthrough == 2:
        $ pov_enable_c = False
        $ pov_enable_z = True
    elif persistent.playthrough == 3:
        $ pov_enable_c = True
        $ pov_enable_z = False
    elif persistent.playthrough == 4:
        $ pov_enable_c = False
        $ pov_enable_z = False
    elif persistent.playthrough == 5:
        $ time = -1
        menu:
            '您已经通关。是否重启游戏并从头开始？这会删除您的存档，但不会清除游戏数据。'
            '是，从头开始':
                $ game_utter_restart()
            '否，返回主界面':
                return
    else:
        $ z_name = '钟离'
        $ c_name = '达达利亚'
        $ pov_enable_c = True
        $ pov_enable_z = True

    
    scene black with dissolve
    call screen pov_toggle(persistent.playthrough) with dissolve

    if persistent.playthrough == 2:
        call start_z from _call_start_z_1
    elif persistent.playthrough == 3:
        $ z_name = glitchtext(10)
        call start_c_3 from _call_start_c_3
    elif persistent.playthrough == 4:
        jump full_ending
    else:
        if pov:
            call start_z from _call_start_z_2
        else:
            call start_c from _call_start_c
    

    scene black with dissolve
    # '提示：地图上某些地点不是每天都会出现的，请留意这些地方的突发事件。'
    ## 这句话写到新手提示里罢
    
    jump expression 'turn' + str(persistent.playthrough)
    return