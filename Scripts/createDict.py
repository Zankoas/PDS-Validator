from os import listdir
from openFile import open_file



def search_effects(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs):
    originalpath = path
    path = originalpath + "\\events"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings,thingstripped, **kwargs)
    path = originalpath + "\\common\\national_focus"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs)
    path = originalpath + "\\common\\scripted_effects"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings,thingstripped, **kwargs)
    path = originalpath + "\\common\\decisions"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs)
    return maindict, linedict, filedict

def create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs):
    filterstrings.append('#') #ignore comments
    focussearch = False
    eventsearch = False
    techsearch = False
    skipfiles = []
    try:
        skipfiles = kwargs.get('skipfiles')
        for name in skipfiles:
            break
        filterfiles = True
    except:
        filterfiles = False
    if thingstripped == 'lockey':
        if "id =" in searchstrings:
            focussearch = True
        elif 'events' in path:
            eventsearch = True
        elif 'technologies' in path:
            techsearch = True
    for filename in listdir(path):
        shouldcontinue = False
        if ".txt" in filename: #this makes sure it's not a folder
            if filterfiles: #checking to make sure it's not in a file we're not supposed to check
                for name in skipfiles:
                    if name == filename:
                        #print("in should continue for " + filename)
                        shouldcontinue = True
            if shouldcontinue == True:
                continue
            hasoccured = False
            eventyes = False
            current_line = 0
            file = open_file(path + '\\' + filename)
            line = file.readline()
            current_line += 1
            eventdeep = 0
            nextline = False
            while line:
                i = 0
                isin = False
                while i < len(searchstrings):
                    if focussearch == True or techsearch == True:
                        if 'event' in line:
                            eventyes = True
                        if '{' in line:
                            eventdeep = eventdeep + 1
                    if searchstrings[i] in line:
                        try:
                            searchstrings2 = kwargs.get('searchstrings2')
                            for item in searchstrings2:
                                if item in line:
                                    isin = True
                        except TypeError:
                            isin = True #checking to see if it has stuff that means it should be checked
                    if focussearch == True or techsearch == True:
                        if '}' in line:
                            eventdeep = eventdeep -1
                        if focussearch == True:
                            if eventyes == True:
                                isin = False
                            if eventdeep == 0:
                                eventyes = False
                        elif techsearch == True:
                            if eventdeep != 3:
                                isin = False
                            if nextline == True:
                                isin = True
                    i = i+1
                i = 0
                while i < len(filterstrings):
                    if filterstrings[i] in line:
                        isin = False #checking to see if it's being filtered for one reason or another
                    i = i+1
                if isin:
                    #this means line is a thing being called, so we need to add it to the dictionary
                    if thingstripped == 'lockey':
                        if focussearch == True:
                            if hasoccured == True:
                                maintext = eventlocstrip(line)
                                if (maintext in maindict) == False and maintext != 'yes' and maintext != 'no':
                                    #print(maintext)
                                    maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                                    maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext+"_desc", current_line, filename, path)
                            else:
                                hasoccured = True
                        elif eventsearch == True:
                            maintext = line.split(' = ')[1].strip()
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                        elif techsearch == True:
                            if nextline == False:
                                #print("nextline to true")
                                nextline = True
                            else:
                                maintext = line.strip()
                                #print(maintext)
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                                maintext = maintext + "_desc"
                                #print(maintext)
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                                nextline = False
                    if thingstripped == 'oob':
                        maintext = stripOOB(line)
                        #print(maintext)
                        if maintext != 'empty' and maintext != "" and (maintext in maindict) == False:
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                    elif thingstripped == 'general':
                        maintext = stripGeneral(line)
                        if maintext != 'empty' and maintext != "" and (maintext in maindict) == False:
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                    elif thingstripped == '=no':
                        maindict, linedict, filedict = insertdict(maindict, linedict, filedict, line, current_line, filename, path)
                    elif thingstripped == 'focus':
                        if 'has_completed_focus' in line:
                            maintext = strip_focus(line, 1, 'has_completed_focus =')
                            if (maintext in maindict) == False and maintext != "":
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                        else:
                            linelist = line.split(' focus =')
                            for posfocus in linelist:
                                maintext = strip_focus(posfocus, 0, '=')
                                if (maintext in maindict) == False and maintext != "":
                                    maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                line = file.readline()
                current_line += 1
    return maindict, linedict, filedict

def eventlocstrip(line):
    maintext = line.split("id =")[1].strip()
    maintext = maintext.split(" ")[0].strip()
    return maintext

def insertdict(maindict, linedict, filedict, maintext, current_line, filename, path):
    maindict[maintext] = False
    linedict[maintext] = current_line
    filedict[maintext] = path + '\\' + filename
    return maindict, linedict, filedict

def stripOOB(line):
    #if 'OTT' in line: Debug related code, ignore this
    #    print(line)
    if ("load_oob" in line):
        foundline = line.split("load_oob = ")[1].strip()
    elif ("OOB = " in line):
        foundline = line.split("OOB = ")[1].strip()
    else:
        foundline = line.split("oob = ")[1].strip()
    anewline = foundline.replace("load_oob = ", "")
    newline = anewline.replace("OOB = ","")
    newline = newline.replace("oob = ","")
    nextline = newline.replace("\"","")
    tfinalline = nextline.replace("\n","")
    removeeffect1 = tfinalline.replace("hidden_effect = { ", "")
    afinalline = removeeffect1.replace("}", "")
    mfinalline = afinalline.replace("add_equipment_to_stockpile = {", "")
    threefinalline = mfinalline.split("add_ideas")[0].strip()
    finalline = threefinalline.split("= {")[0].strip()
    lastline = finalline.strip()
    reallastline = lastline.split(" ")[0].strip()
    return reallastline

def stripGeneral(line):
    if ("has_unit_leader" in line):
        foundline = line.split("has_unit_leader = ")[1].strip()
    else:
        foundline = line.split("remove_unit_leader = ")[1].strip()
    if(" }") in foundline:
        foundline = foundline.split(" }")[0].strip()
    return foundline

def strip_focus(focustext, value, splittext):
    #this strips the focus of surrounding text
    #I made it because if I ever copy and paste code, it means I have failed
    finaltext = focustext.split(splittext)[value].strip()
    finaltext = finaltext.split(' ')[0].strip()
    finaltext = finaltext.split('\t')[0].strip()
    finaltext = finaltext.replace("}", "")
    finaltext = finaltext.replace("{", "")
    finaltext = finaltext.strip()
    if (finaltext == "no" or finaltext == "yes" or finaltext == "prerequisite" or finaltext == "if" or finaltext == "avalible" or finaltext == "bypass" or finaltext == "has_completed_focus" or finaltext == "mutually_exclusive" or finaltext == "limit" or finaltext == "focus" or finaltext == "shared_focus"):
        #is this a kludge? Yes. Does it work? Also yes.
        finaltext = ""
    return finaltext