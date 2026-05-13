import requests, json, os, sys, pick

def ClrHome():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

options = ["Minecraft", "Luanti", "SRB2", "Ring Racers", "SRB2Kart"]
serv_type = pick.pick(options, "Choose a server to check", indicator="*")
serv_type = serv_type[0]

ClrHome()
print("Philooxy's Server Status Checker!!")
print("v1.2")
print(" ")

# defining functions

def mc_get():
	global serv_ip
	URL = "https://api.mcsrvstat.us/3/" + serv_ip # change api used later
	r = requests.get(url=URL)
	print(" ")
	if r.status_code == 200:
		print("Succesfully got data.")
	mc_data = r.json()
	ClrHome()

	try:
		mc_version_number = str(mc_data["version"])
	except KeyError:
		print("Invalid server address!")
		print("Note: this may not be 100% accurate!")
		print("For 100% accuracy, open the server list on the official Minecraft client.")
		sys.exit()

	if mc_data["debug"]["ping"] == True:
		print("Successfully pinged server.")
	else:
		print("Couldn't ping server.")

	print(" ")
	print("["+serv_ip+"]")
	print("----------")

	if mc_data["online"] == True:
		serv_online = "Online!! :D"
	else:
		serv_online = "Offline :("
	print("Status: " + serv_online)

	print("IP Address: " + str(mc_data["ip"]) + ":" + str(mc_data["port"]))

	try:
		print("Hostname: " + str(mc_data["hostname"]))
	except KeyError:
		print("Hostname: N/A")

	print("MOTD: [" + mc_data["motd"]["clean"][0] + "]")

	if mc_data["debug"]["bedrock"] == False:
		mc_version = "Java"
	else:
		mc_version = "Bedrock"

	mc_version_num = str(mc_data["version"])

	print("Version: " + mc_version + " | " + mc_version_num)

	print("Players online: " + str(mc_data["players"]["online"]) + " / " + str(mc_data["players"]["max"]))
	
	mc_plist = ""
	try:
		for i in range(len(mc_data["players"]["list"])):
			mc_plist += mc_data["players"]["list"][i]["name"]
			print(len(mc_data["players"]["list"]))
			if i < len(mc_data["players"]["list"]) - 1:
				mc_plist += ", "
	except KeyError:
			if mc_data["players"]["online"] == 0:
				mc_plist = "No one online."
			else:
				mc_plist = "Unable to retrieve player list."
	print("Player list: " + mc_plist)

def ring_get():
	global serv_ip
	r = requests.get(url="https://ms.kartkrew.org/cc.json")
	ring_data = r.json()
	r = requests.get(url="https://ms.kartkrew.org/list.json")
	ring_data2 = r.json()
	#print(ring_data.keys())
	#print(ring_data2.keys())
	
	ring_ipcheck = ""
	for i in range(len(ring_data2["servers"])):
		ring_ipcheck = ""
		ring_ipcheck = ring_data2["servers"][i]["address"][0]
		if ":" in serv_ip:
			ring_ipcheck += ":" + str(ring_data2["servers"][i]["address"][1])
			#print(ring_ipcheck)
		if serv_ip == ring_ipcheck:
			ring_index = i
			break
	try:
		ring_data3 = ring_data2["servers"][ring_index]
	except UnboundLocalError:
		print("Address not detected in server list.")
		sys.exit()
	ClrHome()
	print("["+ ring_data3["server_name"] +"]") # clean up server name (remove color codes)
	if ring_data3["dedicated"] == True:
		print("Dedicated server")
	else:
		print("Self-hosted server")
	print("----------")
	print("Server address: " + ring_data3["address"][0] + ":" + str(ring_data3["address"][1]))
	print("Server contact: " + ring_data3["contact"])
	print("Players online: " + str(ring_data3["num_humans"]) + " / " + str(ring_data3["max_connections"]))
	print("Country code: " + ring_data["mapping"][ring_data3["address"][0]]["iso3166"])
	print("Gametype: " + ring_data3["gametype"])
	print("Gear: " + ring_data3["speed"])
	print("Current zone: " + ring_data3["map_title"])

def lnt_get():
	global serv_ip
	r = requests.get(url="https://servers.luanti.org/list")
	lnt_data = r.json()
	ClrHome()
	print(" ")
	#print(lnt_data.keys())
	lnt_data2 = lnt_data["list"]
	for i in range(len(lnt_data2)):
		if lnt_data2[i]["address"] == serv_ip:
			lnt_index = i
			break
	try:
		lnt_data3 = lnt_data2[lnt_index]
	except UnboundLocalError:
		print("Address not detected in server list!")
		sys.exit()
	#print(lnt_data3)
	print("[" + lnt_data3["name"] + "]")
	print("-----------")
	print("Description")
	print("-----------")
	print(lnt_data3["description"])
	print("-----------")
	print("Server address: " + lnt_data3["address"] + ":" + str(lnt_data3["port"]))
	print("Country code: " + lnt_data3["geo_continent"])
	print("Game ID: " + lnt_data3["gameid"])

	if lnt_data3["creative"] == False:
		lnt_gamemode = "Survival"
	else:
		lnt_gamemode = "Creative"

	print("Gamemode: " + lnt_gamemode)

	print("Players online: " + str(lnt_data3["clients"]) + " / " + str(lnt_data3["clients_max"]))

	if lnt_data3["clients"] == 0:
		print("Player list: No one online.")
	else:
		lnt_plist = ""
		for i in range(lnt_data3["clients"]):
			lnt_plist += lnt_data3["clients_list"][i]
			if i < lnt_data3["clients"] - 1:
				lnt_plist += ", "
	print("Player list: " + lnt_plist)

def srb2_get():
	global serv_ip # yes this is copied from ring_get because its essentially the same game
	r = requests.get(url="https://ms.srb2.org/cc.json")
	srb2_data = r.json()
	srb2_data = srb2_data["mapping"]
	r = requests.get(url="https://ms.srb2.org/list.json")
	srb2_data2 = r.json()

	srb2_ipcheck = ""
	for i in range(len(srb2_data2["servers"])):
		srb2_ipcheck = ""
		srb2_ipcheck = srb2_data2["servers"][i]["address"][0]
		if ":" in serv_ip:
			srb2_ipcheck += ":" + str(srb2_data2["servers"][i]["address"][1])
		if serv_ip == srb2_ipcheck:
			srb2_index = i
			break
	try:
		srb2_data3 = srb2_data2["servers"][srb2_index]
	except UnboundLocalError:
		print("Address not detected in server list.")
		sys.exit()

	ClrHome()
	print("[" + srb2_data3["server_name"] + "]")
	if srb2_data3["dedicated"] == True:
		print("Dedicated server")
	else:
		print("Self-hosted server")
	print("----------")
	print("Server address: " + srb2_data3["address"][0] + ":" + str(srb2_data3["address"][1]))
	print("Players online: " + str(srb2_data3["num_humans"]) + " / " + str(srb2_data3["max_connections"]))
	
	if srb2_data3["num_humans"] == 0:
		print("Player list: No one online.")
	else:
		srb2_plist = ""
		for i in range(srb2_data3["num_humans"]):
			srb2_plist += str(srb2_data3["players"][i]["name"])
			if i < srb2_data3["num_humans"] - 1:
				srb2_plist += ", "
	print("Player list: " + srb2_plist)

	print("Country code: " + srb2_data[srb2_data3["address"][0]]["iso3166"])
	print("Gametype: " + srb2_data3["gametype"])
	print("Current zone: " + srb2_data3["map_title"])
	if srb2_data3["modified"] == True:
		print("Mods: Yes")
	else:
		print("Mods: No")
	if srb2_data3["cheats"] == True:
		print("Cheats: Yes")
	else:
		print("Cheats: No")

print("Checking: " + serv_type)
serv_ip = input("Server Address: ")
print(" ")
print("Loading...")

if serv_type == "Minecraft":
	mc_get()
elif serv_type == "Ring Racers":
	ring_get()
elif serv_type == "Luanti":
	lnt_get()
elif serv_type == "SRB2":
	srb2_get()
elif serv_type == "SRB2Kart":
	print("not yet")