from sb import Skyblock


skyblock = Skyblock('') # tfw you forget to remove ur api key and have to regenerate it
uuid = skyblock.uname_resolver('Technoblade')

profiles = skyblock.get_player_profiles(uuid)

