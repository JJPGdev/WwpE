import subprocess


def execute_cmd(cmd):
    return subprocess.run(cmd,capture_output=True,shell=True)


def get_profiles():
    profiles = []
    profiles_unfiltered = execute_cmd("netsh wlan show profile").stdout
    getNameMode = False
    profile_name =  ""
    for char in profiles_unfiltered:
        if ord(chr(char)) == 13 and getNameMode == True:
            getNameMode = False
            profiles.append(profile_name)
            profile_name = ""

        if getNameMode == True and chr(char) != " ":
            profile_name += chr(char)

        if chr(char) == ':' and getNameMode == False:
            getNameMode = True

    return profiles


def get_password(profile):
    cmd = "netsh wlan show profile " + profile +  " key=clear"
    result = execute_cmd(cmd)
    password_unfiltered = str(result.stdout)
    start = int(password_unfiltered.find("Key Content")) + 11
    password = ""
    for i in range(start,len(password_unfiltered)):
        if password_unfiltered[i] == " ":
            continue
        if ord(password_unfiltered[i]) == 92 and ord(password_unfiltered[i+1]) == 114:
            break
        password += password_unfiltered[i]
    password_final = password[1:]
    return password_final


def mode1():
    profiles = get_profiles()
    print("We found the following profiles:")
    index = 1
    profiles.pop(0)
    for prof in profiles:
        print(prof + " - " + str(index))
        index+=1
    getPassFrom = 0
    #print("I want to get the password from(index):")
    getPassFrom = input()
    if ord(getPassFrom[0]) > 57 or ord(getPassFrom[0]) < 48 or len(getPassFrom) > 1:
        print("Please enter a valid value!")    
        return
    else:
        getPassFrom = int(getPassFrom)
    print("The password I found is: " + get_password(profiles[getPassFrom-1]))
    
print("Welcome to WwpE (Windows wlan password extractor)")
menu = '''I want to: Get wlan password - 1'''
while(1):   
    print("\n")
    print(menu)
    action = input()
    print("\n")
    if ord(action[0]) > 57 or ord(action[0]) < 48 or len(action) > 1:
        print("Please enter a valid value!")    
        continue
    else:
        action = int(action)

    if action == 1:
        mode1()
