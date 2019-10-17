from sb import Skyblock


skyblock = Skyblock('')
uuid = skyblock.uname_resolver('Technoblade')

profiles = skyblock.get_player_profiles(uuid)

