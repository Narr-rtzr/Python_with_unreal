# py automise script by Minomi 
## run with python 2.7 in UE4

#######################################import modules from here#################################
import unreal 
#######################################import modules end#######################################



#######################################functions from here#######################################
def get_selected_asset_dir() -> str :
    ar_asset_lists = unreal.EditorUtilityLibrary.get_selected_assets() 

    if len(ar_asset_lists) > 0 :
        str_selected_asset = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(ar_asset_lists[0])
        path = str_selected_asset.rsplit('/', 1)[0]

    else : 
        path = '' 

    return path


def get_anim_list (__path: str) -> list :
    seq_list = unreal.EditorAssetLibrary.list_assets(__path, True, False)
    return seq_list


def check_animseq_by_name_in_list (__anim_name: str, __list: list ) -> str :
    if len(__list) > 0 :
        for each in __list :
            name = each.rsplit('.', 1)[1]
            found_name = name.find(__anim_name)
            if found_name != -1 :
                break 
        return each
    else :
        return ''


def set_bs_sample (__animation, __axis_x: float, __axis_y: float) : # returns [BlendSample] unreal native type 
    bs_sample = unreal.BlendSample()
    vec_sample = unreal.Vector(__axis_x, __axis_y, 0.0) #do not use 3D BlendSampleVector
    bs_sample.set_editor_property('animation', __animation)
    bs_sample.set_editor_property('sample_value', vec_sample)
    bs_sample.set_editor_property('rate_scale', 1.0)
    bs_sample.set_editor_property('snap_to_grid', True)
    return bs_sample



def set_blendSample_to_bs (__blendspace, __blendsample) : #returns [BlendSpace] unreal loaded asset
    __blendspace.set_editor_property('sample_data', __blendsample)
    return 0

def set_blendParameter (__min: float , __max: float) :
    bs_parameter = unreal.BlendParameter()
    bs_parameter.set_editor_property('display_name', 'none')
    bs_parameter.set_editor_property('grid_num', 4)
    bs_parameter.set_editor_property('min', __min)
    bs_parameter.set_editor_property('max', __max)
    return bs_parameter

def set_square_blendSpace (__blendspace, __blendparameter) :
    __blendspace.set_editor_property('blend_parameters', [__blendparameter,__blendparameter,__blendparameter])
#######################################functions end#######################################


#######################################class from here######################################

class wrapedBlendSpaceSetting:
    
    main_dir: str = ''
    bs_dir: str = '/Animation/BlendSpace' #blend space relative path 
    post_fix: str = '' #edit this if variation
    pre_fix: str = '' #edit this if variation
    custom_input: str = pre_fix + '/Animation' + post_fix

    bs_names: list = [
        "IdleRun_BS_Peaceful", 
        "IdleRun_BS_Battle", 
        "Down_BS", 
        "Groggy_BS", 
        "Airborne_BS",
        "LockOn_BS"
        ]

    seq_names: list = [
        '_Idle01',
        '_Walk_L',
        '_BattleIdle01',
        '_Run_L',
        '_KnockDown_L',
        '_Groggy_L',
        '_Airborne_L',
        '_Caution_Cw',
        '_Caution_Fw',
        '_Caution_Bw',
        '_Caution_Lw',
        '_Caution_Rw'
    ]

    
#######################################class end#######################################

#######################################run from here#######################################
wraped = wrapedBlendSpaceSetting()
wraped.main_dir = get_selected_asset_dir()

seek_anim_path = wraped.main_dir + wraped.custom_input
bs_path = wraped.main_dir + wraped.bs_dir

anim_list = get_anim_list(seek_anim_path)
name_list : list = []


for each in wraped.seq_names :
    anim_name = check_animseq_by_name_in_list(each, anim_list)
    name_list.append(anim_name)
    print(anim_name)

found_list: list = []
for each in name_list :
    loaded_seq = unreal.EditorAssetLibrary.load_asset(each)
    found_list.append(loaded_seq)


bs_sample_for_idle_peace = [set_bs_sample(found_list[0], 0.0, 0.0), set_bs_sample(found_list[1], 100.0, 0.0)]
bs_sample_for_idle_battle = [set_bs_sample(found_list[2], 0.0, 0.0), set_bs_sample(found_list[3], 0.0, 0.0)]
bs_sample_for_down = [set_bs_sample(found_list[4], 0.0, 0.0)]
bs_sample_for_groggy = [set_bs_sample(found_list[5], 0.0, 0.0)]
bs_sample_for_airborne = [set_bs_sample(found_list[6], 0.0, 0.0)]
bs_sample_for_lock_on = [
    set_bs_sample(found_list[7], 0.0, 0.0), 
    set_bs_sample(found_list[8], 0.0, 1.0), 
    set_bs_sample(found_list[9], 0.0, -1.0), 
    set_bs_sample(found_list[10], 1.0, 0.0), 
    set_bs_sample(found_list[11], -1.0, 0.0)
]

bs_param_idle = set_blendParameter(0.0, 100.0)
bs_param_lock_on = set_blendParameter(-1.0, 1.0)

bs_idle_peaceful = unreal.EditorAssetLibrary.load_asset ( bs_path + '/' + wraped.bs_names[0] )
bs_idle_battle = unreal.EditorAssetLibrary.load_asset ( bs_path + '/' + wraped.bs_names[1] )
bs_idle_down = unreal.EditorAssetLibrary.load_asset ( bs_path + '/' + wraped.bs_names[2] )
bs_idle_groggy = unreal.EditorAssetLibrary.load_asset ( bs_path + '/' + wraped.bs_names[3] )
bs_idle_airborne = unreal.EditorAssetLibrary.load_asset ( bs_path + '/' + wraped.bs_names[4] )
bs_idle_lockon = unreal.EditorAssetLibrary.load_asset ( bs_path + '/' + wraped.bs_names[5] )


set_square_blendSpace( bs_idle_peaceful, bs_param_idle)
set_square_blendSpace( bs_idle_battle, bs_param_idle)
set_square_blendSpace( bs_idle_down, bs_param_idle)
set_square_blendSpace( bs_idle_groggy, bs_param_idle)
set_square_blendSpace( bs_idle_airborne, bs_param_idle)
set_square_blendSpace( bs_idle_lockon, bs_param_lock_on)

#######################################run end here#######################################