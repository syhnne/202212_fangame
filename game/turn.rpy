
screen developer_time_set():
    zorder 100
    frame:
        xpos 1700 ypos 120
        has vbox
        textbutton '切换视角' action Show('pov_toggle',dissolve)
        textbutton 'time=90'action Jump('developer_90')
        textbutton 'p03' action SelectedIf(ToggleDict(persistent.lores, 'p03_read'))
        textbutton 'p05' action SelectedIf(ToggleDict(persistent.lores, 'p05_read'))
        textbutton 'p08' action SelectedIf(ToggleDict(persistent.lores, 'p08_read'))
        textbutton 'p10' action SelectedIf(ToggleDict(persistent.lores, 'p10_read'))
        textbutton '好感+100' action Function(favp, 100, 'magic')
        # textbutton 'z09' action SelectedIf(ToggleDict(persistent.lores, 'z09_read'))
        textbutton 'night' action SelectedIf(ToggleVariable('nightlore'))



label developer_90:
    python:
        time = 90
        listnumber = time-len(choice_history)
        for i in range(listnumber):
            choice_history.append('magic')
    jump turn

screen developer_time():
    zorder 101
    frame:
        xpos -30 ypos 120
        hbox:
            spacing 30
            $ x=len(choice_history)
            text '       len ch:[x]'
            text 'time:[time]'
            text '好感度:[fav]'

init python:
    if config.developer:
        config.overlay_screens.append("developer_time")


# define config.character_id_prefixes = [ ]
# 该项指定了一个可以用于 Character() 对象的样式特性(property)前缀列表。当某个样式前缀与列表中的前缀匹配，带有那个前缀的可视组件就会应用对应的样式。
# 例如，给默认GUI添加“namebox”前缀。当某个角色给定了namebox_background特性时，它会将带有id“namebox”的可视组件设置为say界面的 background。
# define config.load_failed_label = None
# 如果配置为一个字符串，表示一个脚本标签(label)。脚本修改过多导致Ren’Py无法恢复产生读档失败的情况下，将跳转到该脚本标签。 在执行读档前，Ren’Py将主控流程切换为最后执行语句开头，并清空调用栈。
# 也可以配置为一个函数。该函数没有入参，返回值需要是一个脚本标签(label)。




## 部分主控流程需要用到的东西，我懒得整理了 ######################################


screen pov_toggle(stage=0):
    ## stage：0为主界面，其他数字对应几周目
    tag quick_menu ## 别在这种时候显示quick menu啊，我是不打算让观众在这会儿保存的
    modal True
    if stage==0:
        roll_forward True
    zorder 100
    window:
        align (0,0)
        background 'gui/pov_toggle/bg.png'
            ## 如何做到按钮的遮挡效果：你先写谁，renpy就先渲染哪个按钮，后来的会挡在先来的前面
        if pov_enable_z:
            imagebutton:
                
                idle 'pov_toggle_c_i'
                hover 'pov_toggle_c_h'
                selected_idle 'pov_toggle_c_si'
                selected_hover 'pov_toggle_c_sh'
                insensitive 'gui/pov_toggle/bg_insensitive_c.png'
                action SetVariable('pov',False)
                selected pov == False
                sensitive pov_enable_c
                focus_mask True
        imagebutton:
            idle 'pov_toggle_z_i'
            hover 'pov_toggle_z_h'
            selected_idle 'pov_toggle_z_si'
            selected_hover 'pov_toggle_z_sh'
            insensitive 'gui/pov_toggle/z_insensitive.png'
            action SetVariable('pov',True)
            selected pov
            sensitive pov_enable_z
            focus_mask True
        if not pov_enable_z:
            imagebutton:
                idle 'pov_toggle_c_i'
                hover 'pov_toggle_c_h'
                selected_idle 'pov_toggle_c_si'
                selected_hover 'pov_toggle_c_sh'
                insensitive 'gui/pov_toggle/bg_insensitive_c.png'
                action SetVariable('pov',False)
                selected pov == False
                sensitive pov_enable_c
                focus_mask True
        vbox:
            xalign 0.5 ypos 30
            if stage != 0:
                text '请选择游戏视角…'
            textbutton '确认':
                xalign 0.5
                if stage==0:
                    action ToggleScreen('pov_toggle',dissolve)
                elif stage==4:
                    action Return()
                else:
                    action Return()
                    sensitive pov!=None
                
screen beginner_guide():
    zorder 110
    modal True
    default textline = 1
    window:
        background 'solidblackbg' align (0,0) xysize(1920,1080)
        frame:
            xpos 500 yalign 0.3 padding (30,30,30,30)
            vbox:
                spacing 20
                text ' 操作提示：'
                if textline == 1:
                    use beginner_guide1
                    textbutton '下一条(1/2)' action SetScreenVariable('textline', 2) 
                elif textline == 2:
                    use beginner_guide2
                    hbox:
                        textbutton '上一条(2/2)  ' action SetScreenVariable('textline', 1)
                        textbutton '  确认' action Hide('beginner_guide')

screen beginner_guide1():
    text '每天有3次机会，可以在地图上选择要去的地点，触发不同的剧情。\n也可以点击左上角，选择不出门。\n有些地点会触发特殊的事件，有些则不会每天都显示。' 
screen beginner_guide2():
    text '另外，在游戏中做出的选项不仅会影响当前存档的剧情推进，\n还可能{u}在其他的游戏视角中{/u}触发新的事件……\n请善用存档功能，在不同的游戏视角中尽可能触发更多的事件吧。'


screen map_options():
    zorder 51
    frame:
        xsize 500 ysize 80 xpos 1400 ypos 20
        hbox:
            spacing 20 yalign 0.5
            textbutton '好感度 : [fav]' action CaptureFocus("options_drop")
            bar value fav range 100 yalign 0.5
    if GetFocusRect("options_drop"):
        dismiss action ClearFocus("options_drop")
        nearrect:
            xoffset -15 yoffset 20
            focus "options_drop"
            frame:
                modal True
                has vbox
                textbutton "（操作提示，还没写）" action [ ClearFocus("options_drop") ]

screen days():
    zorder 50
    $ tooltip = GetTooltip('map_liyuegang')
    frame:
        xysize (350,80) xpos -34 ypos 20
    frame:
        xysize (472,80) xpos 328 ypos 20
        hbox:
            yalign 0.5 xpos 20 spacing 25
            $ dddate=date(time)
            $ ccclock=clocktext(time)
            text '第[dddate]天'
            text '[ccclock]'
            null xsize 60
            if tooltip:
                text tooltip
            else:
                text '去哪里看看…'



init python:
    ## [剧情地点，剧情label名称，进剧情条件，顶替2]
    events_z = {
    8:['bgyh', 'p01'],
    10:[False, 'p00', 'persistent.p01enter', 'p02'],
    13:[False, 'p03', 'persistent.p03enter'],
    15:[False, 'z04', 'choice_history[13]==\'p03\''],
    18:['mxjxh', 'z05', 'choice_history[13]==\'p03\''],
    26:[False, 'p04'],
    28:['lygmt', 'z06'],
    30:[False, 'p05', 'persistent.p05enter'],
    31:['bgyh', 'z07', 'choice_history[36]==\'p05\''],
    ## 38以后也有，但我懒得写，而且我得斟酌一下是不是真的要写
    36:['wmt', 'p06'],
    39:['wwjs', 'p07'],
    49:[False, 'z08'],
    51:[False, 'p08', 'persistent.p08enter'],
    57:[False, 'p09', 'persistent.p08enter'],
    66:['outside', 'p13', 'fav>30'],
    69:['c_home', 'z09'],
    70:['c_home', 'z09'],
    71:['c_home', 'z09'],
    75:['mxjxh', 'z10'], 
    76:['mxjxh', 'z10'], 
    77:['mxjxh', 'z10'], 
    80:[False, 'p10', 'persistent.p10enter'],
    81:[False, 'p11', 'choice_history[13]==\'p03\''],
    87:['outside', 'p12'],
    }

    events_c = {
    0:[True, 'c01'],
    1:[True, 'c01'],
    2:[True, 'c01'],
    4:[False, 'c02'],
    8:[False, 'p01', 'persistent.p01enter'],
    10:[False, 'p02', 'persistent.p01enter' ],
    13:[False, 'p03', 'persistent.p03enter'],
    15:[False, 'c06', 'choice_history[13]==\'p03\''],
    21:['wjt', 'c07'],
    22:['wjt', 'c07'],
    23:['wjt', 'c07'],
    26:[False, 'p04'],
    28:[False, 'c08'],
    30:[False, 'c09'],
    30:[False, 'p05', 'persistent.p05enter'],
    31:[False, 'c10', 'choice_history[13]==\'p03\''],
    32:[True, 'c10', 'choice_history[13]==\'p03\''],
    33:[True, 'c10', 'choice_history[13]==\'p03\''],
    ## 本来也有很多重复的，准备砍，遂删之
    36:['wmt', 'p06'],
    39:['wwjs', 'p07'],
    40:[False, 'c11', 'choice_history[13]==\'p03\''],
    49:['wst', 'c12'],
    50:['wst', 'c12'],
    51:[False, 'p08', 'persistent.p08enter'],
    57:[False, 'p09', 'persistent.p08enter'],
    66:['outside', 'p13', 'fav>30'],
    72:['wwjs', 'c15'],
    73:['wwjs', 'c15'],
    74:['wwjs', 'c15'],
    75:['mxjxh', 'c13'], 
    76:['mxjxh', 'c13'], 
    77:['mxjxh', 'c13'], 
    80:[False, 'p10', 'persistent.p10enter'],
    81:[False, 'p11', 'choice_history[13]==\'p03\''],
    86:[False, 'c14'],
    87:['outside', 'p12'],
    }


    map_liyuegang_dict = {
        'outside':[ True, True,  180,550,'离开璃月港…', ],
        'stay':[ True, True,   10,29,'不出门…', ],
        'wmt':[ True, True,  1565,339,'万民堂', ],
        'mxjxh':[ [False,[15,16,17],[75,76,77],], [False,[15,16,17],24,[75,76,77],],  1478,221,'冒险家协会', ],
        'bgyh':[ False, [False,6,7,8],    1010,441,'北国银行', ],
        'wwjs':[ True, True,   459,660,'万文集舍', ],
        'llt':[ True, True,  637,585,'琉璃亭', ],
        'xyx':[ True, True,  835,538,'新月轩', ],
        'yjt':[ True, True,  1246,785,'玉京台', ],
        'lygmt':[ [False,13], [False,13,34],  1175,218,'璃月港码头', ],
        'swbgg':[ [False,'range(7,62)', range(63,90),], True,    1470,360,'「三碗不过港」', ],
        'wst':[ [False,55,56], False,   1202,496,'往生堂', ],
        'wjt':[ [False,[27,28,29]], False,    1339,366,'「玩具摊」', ],
        'c_home':[ False, [False,[69,70,71]],  510,470,'???', ],
        'z_home':[ [False], False,    200,400,'z_home', ],
    }





screen map_liyuegang(spot_has_event=False):
    
    zorder 0    
    window:
        ## window是一款高血压神器，他诞生之初就是为了做对话框，所以一旦把它拿去做别的东西，他就会满屏乱飘逼你手搓pos，于是弃之用frame
        ypos 277 xpos 960
        background 'map_bg'
        use days
        if persistent.unlock_gallery:
            use map_options
        if config.developer:
            use developer_time_set

        for key,value in map_liyuegang_dict.items():

            python:
                
                x = map_liyuegang_dict.get(key)
                map_clist = x[int(pov)]
                if type(map_clist) == type(True):
                    showspot = map_clist
                elif type(map_clist) == type([]):
                    showspot = map_clist[0]
                    for i in map_clist:
                        if type(i) == type(1) and i == time:
                            showspot = not showspot
                            break
                        elif type(i) == type([]):
                            for q in i:
                                if q == time:
                                    showspot = not showspot
                        elif type(i) == type(''):
                            l=eval(i)
                            for q in l:
                                if q == time:
                                    if rand==3:
                                        showspot = not showspot

            if showspot:
                imagebutton:
                    if key != 'stay':
                        at hovered_animation
                    xpos value[2] ypos value[3]
                    if key == 'stay':
                        idle Text(value[4], xpos=65, ypos=8, color=gui.idle_color)
                        hover Text(value[4], xpos=65, ypos=8)
                        xsize 300
                    else:
                        idle 'gui/map/spot.png'
                        hover 'gui/map/spot_hover.png'
                    if spot_has_event == key:
                        foreground 'gui/map/spot_foreground_event.png'
                    else:
                        foreground 'gui/map/spot_foreground_notevent.png'
                    action Return(key)
                    tooltip value[4]
                    
        $ tooltip = GetTooltip()            
        if tooltip and tooltip!='不出门…':
            nearrect:
                focus "tooltip"
                prefer_top True
                frame:
                    xalign 0.5
                    text tooltip
            


            
            




 

###############################################################################
## 剧情流程 ####################################################################
###############################################################################


label turn:

    scene black with dissolve
        
    while time <= 90:
        # if config.developer:
        #     $ renpy.profile_screen('map_liyuegang', predict=False, show=True, update=False, request=False, time=True, debug=True, const=True)
        #     $ renpy.profile_memory(fraction=1.0, minimum=0, skip_constants=False)
        
        $ rand=renpy.random.randint(1,6)
        $ d = '（第'+str(date(time))+'天  '+clocktext(time)+'）'
        $ add_history(d)
        

        ## 特殊剧情判断
        if time == 9 and pov and choice_history[-1] != 'p01':
            $ persistent.p01enter = False
            $ persistent.p03enter = False
        elif time == 30 and not pov and not 'c07' in choice_history[-3:]:
            $ persistent.p04enter = False
        
        ## 获得列表中特殊事件
        if pov:
            $ event = events_z.get(time)
        else:
            $ event = events_c.get(time)

        ## 分配给变量
        if event:
            $ event_label_name = event[1]
            

            ## 判定是否满足触发的条件。这个条件需要是个字符串，并且返回一个布尔值
            if len(event)>2:
                $ cond = eval(event[2])
                if cond != True:
                    $ event = None
                elif len(event)>3:
                    $ event_label_name = event[3]

        ## 特殊事件+不允许打开地图
        if event and type(event[0])==type(True) and event[0] == False:
            $ choice_history.append(event_label_name)
            call expression event_label_name
            $ time = time + 1 
            

        ## 允许打开地图
        else:
            
            ## 新手教程
            if persistent.seen_beginner_guide == False:
                show screen beginner_guide
                $ persistent.seen_beginner_guide = True

            ## 打开地图
            $ in_map = True
            if event and type(event[0])==type(''):
                call screen map_liyuegang(event[0]) with dissolve
            else:
                call screen map_liyuegang() with dissolve
            $ in_map = False

            if _return:

                ## 加入历史记录
                $ choice=map_liyuegang_dict.get(_return)
                $ narrator.add_history('adv', '', choice[4])

                ## 特殊事件，与选项无关
                if event and type(event[0])==type(True):
                    $ choice_history.append(event_label_name)
                    call expression event_label_name
                    $ time = time + 1
                    
                ## 特殊事件，选对才能进
                elif event and type(event[0])==type('') and event[0] == _return:
                    $ choice_history.append(event_label_name)
                    call expression event_label_name
                    $ time = time + 1
                    
                ## 无特殊事件
                else:
                    if _return:
                        $ choice_history.append(_return)
                    call expression _return
                    $ time = time + 1
                    
                    
            
        scene black with dissolve
        if clock(time-1)==2 and time != 0 and _return != False and nightlore :
            call night from _call_night
        

    scene black with dissolve
    
    if persistent.playthrough == 1:
        if fav>50:
            jump ending1
        else:
            jump ending2
    elif persistent.playthrough == 2:
        jump ending3
    elif persistent.playthrough == 3:
        jump ending4








# label turn2:

#     scene black with dissolve

#     python:
#         events_z[34] = ['mxjxh', 'z06_2']
    
#     if persistent.lores['p03_read']:

#         $ time=8
#         call screen map_liyuegang with dissolve
#         call p01 from _call_p01
#         scene black with dissolve

#         $ time=10
#         call p02_2 from _call_p02_2
#         scene black with dissolve

#         $ time=13
#         call p03_2 from _call_p03_2
#         scene black with dissolve

#         $ time=15
#         call z04_2 from _call_z04_2
#         scene black with dissolve

#     if persistent.lores['p05_read']:
        
#         $ time=32
#         call p04_2 from _call_p04_2
#         scene black with dissolve

#         $ time=34
#         call screen map_liyuegang with dissolve
#         call z06_2 from _call_z06_2
#         scene black with dissolve

#         $ time=36
#         call p05_2 from _call_p05_2
#         scene black with dissolve

#     if persistent.lores['p08_read']:
        
#         $ time=57
#         call p08_2 from _call_p08_2
#         scene black with dissolve

#         $ time=60
#         call p09_2 from _call_p09_2
#         scene black with dissolve

#     if persistent.lores['p10_read']:

#         $ time=80
#         call p10_2 from _call_p10_2
#         scene black with dissolve


#     $ time=87
#     $ e = events_unlocked()
#     if e<2:
#         call screen map_liyuegang with dissolve
#     call p12_2 from _call_p12_2
#     scene black with dissolve

#     $ time=91
#     if e==2:
#         jump ending3
#     else:
#         jump ending4




# label turn3:

#     if persistent.lores['p03_read']:

#         $ time=10
#         call p02_3 from _call_p02_3
#         scene black with dissolve

#         $ time=13
#         call p03_3 from _call_p03_3
#         scene black with dissolve

#     if persistent.lores['p05_read']:

#         $ time=34
#         call c08 from _call_c08
#         call c09_2 from _call_c09_2
#         scene black with dissolve

#     if persistent.lores['p08_read']:

#         $ time=57
#         call screen map_liyuegang with dissolve
#         call p08_3 from _call_p08_3
#         scene black with dissolve

#     $ time=80
#     call p10_3 from _call_p10_3
#     scene black with dissolve

#     $ time=91
#     jump ending5





################################################

label start:
    $ playthrough = persistent.playthrough
    $ _dismiss_pause = False
    if persistent.playthrough == 2:
        $ pov_enable_c = False
        $ pov_enable_z = True
    elif persistent.playthrough == 3:
        $ pov_enable_c = True
        $ pov_enable_z = False
    elif persistent.playthrough == 4:
        $ pov_enable_c = False
        $ pov_enable_z = False
        $ pov = None
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

    call before_start from _call_before_start
    scene black with dissolve
    call screen pov_toggle(persistent.playthrough) with dissolve
    if config.developer:
        show screen developer_time

    if not persistent.playthrough == 1:
        call test

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
    
    # jump expression 'turn' + str(persistent.playthrough)
    jump turn
    return

