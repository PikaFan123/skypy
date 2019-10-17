from sb import Skyblock


skyblock = Skyblock('4ba41725-11ee-44d9-969a-cc57ec771da8')
uuid = skyblock.uname_resolver('Technoblade')

profiles = skyblock.get_player_profiles(uuid)

