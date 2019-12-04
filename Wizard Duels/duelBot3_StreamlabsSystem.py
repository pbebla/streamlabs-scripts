#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr
import sys
import json
import os
import random
import ctypes
import codecs
import string

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "Duels v2"
Website = "https://www.twitch.tv/cynaschism"
Creator = "Cynaschism - Murp"
Version = "2.0.0.0"
Description = "Duels v2"

#---------------------------------------
#	Set Variables
#---------------------------------------
dStarter=""
dInvited=""
starterTurn=False
dStage=0
dsBurn=False
diBurn=False
dsBlind=0
diBlind=0
spell=0
reflect=False
dsSkip=0
diSkip=0
HP={}
spells = ["Flipendo","Wingardium","Incendio","Lumos","Skurge","Diffindo","Glacius","Protego","Expelliarmus", "Rictusempra"]

def ScriptToggled(state):
	return

#---------------------------------------
#	[Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	return

#---------------------------------------
#   [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    global dStarter, HP, username, dInvited, starterTurn, dStage, dsBurn, diBurn, dsBlind, diBlind, spell, reflect, dsSkip, diSkip, spells
    username=data.User
    msg=""
    def spellDamage(name,player,redChance):
        random.seed()
        global dsSkip, diSkip, dsBurn, diBurn, dsBlind, diBlind
        num = random.randint(0,100)
        text=""
        if name=="Flipendo" and (num <= (75 - redChance)):
            HP[player]-=20
            text+="Flipendo landed for 20% damage."+ " "
        elif name=="Wingardium" and num <= 70 - redChance:
            d=random.randint(0, 1) * 20 + 10
            HP[player]-=d
            text+="Wingardium landed for " + str(d) + "% damage." + " "
        elif name=="Incendio" and num <= 50 - redChance:
            if(player.lower()==dStarter.lower()):
                dsBurn=True
            else:
                diBurn=True
            text+="Incendio landed burn damage." + " "
        elif name=="Lumos" and num <= 90 - redChance:
            if(player.lower()==dStarter.lower()):
                dsBlind+=3
            else:
                diBlind+=3
            text+= "Lumos successful in blinding for 3 turns." + " "
        elif name=="Rictusempra" and num <= 70 - redChance:
            HP[player]-=25
            text+= "Rictusempra landed for 25% damage." + " "
        elif name=="Skurge" and num <= 70 - redChance:
            if(player.lower()==dStarter.lower()):
                diBlind=0
                diBurn=False
            else:
                dsBlind=0
                dsBurn=False
            text+="Skurge successful in removing effects." + " "
        elif name=="Diffindo" and num <= 60 - redChance:
            HP[player]-=30
            text += "Diffindo landed for 30% damage." + " "
        elif name=="Glacius" and num <= 50 - redChance:
            HP[player]-=10
            if(player.lower()==dStarter.lower()):
                dsSkip+=1
            else:
                diSkip+=1
            text+= "Glacius has landed for 10% damage and a turn skip." + " "
        elif name=="Expelliarmus" and num <= 60 - redChance:
            if(player.lower()==dStarter.lower()):
                dsSkip+=2
            else:
                diSkip+=2
            text+= "Expelliarmus landed for two turn skips." + " "
        else:
            text+=name + " has missed." + " "
        return text
        
    if data.IsChatMessage() and data.GetParam(0).lower()=="!duel":
        parsed = data.Message.split(" ")
        if parsed[1]=="help":
            msg="THIS IS V2. https://pastebin.com/Q2YKtxzb , !duel start <username> to initiate, !duel accept to start, more info in pastebin"
        elif parsed[1]=="start" and len(parsed)>=2 and dStage==0:
            myPoints = Parent.GetPoints(username)
            theirPoints = Parent.GetPoints(parsed[2])
            if myPoints<300 or theirPoints <300:
                msg="Both contestants need 300 points to duel!"
            else:
                dStage=1
                dStarter=username
                dInvited=parsed[2]
                msg="@" + dInvited + " do you hereby accept this duel? [!duel accept]"
        elif parsed[1]=="cancel" and username.lower()==dStarter.lower() and dStage==1:
            msg+="Duel request cancelled."
            dStage=0
            dStarter=""
            dInvited=""
        elif parsed[1]=="accept" and username.lower()==dInvited.lower() and dStage==1:
            dStage=2
            msg+="Duel between " + dStarter + " and " + dInvited + " has begun. It is " + dInvited + "'s turn."
            HP[dStarter]=100
            HP[dInvited]=100
        elif parsed[1]=="end" and (username.lower()==dStarter.lower() or username.lower()==dInvited.lower()):
            msg="Duel between " + dStarter + " and " + dInvited + " has concluded early, no winner determined."
            dStage=0
            del HP[dStarter]
            del HP[dInvited]
            dStarter=""
            dInvited=""
        elif parsed[1]=="cast" and len(parsed)>=3 and dStage==2:
            if len(parsed)>3:
                msg="Can only cast one spell at a time."
            else:
                if username.lower() == dStarter.lower():
                    if starterTurn==False:
                        msg="Not your turn yet."
                    if dsSkip !=0:
                        msg = "Your turn is skipped."
                    if parsed[2] not in spells:
                        msg="That's not a spell."
                    else:
                        redChance=0
                        if dsBlind!=0:
                            dsBlind-=1
                            redChance=30
                        if dsBurn:
                            dsBurn==False
                            HP[dStarter]-=5
                            msg+=dStarter + " has taken 5% burn damage." + " "
                        msg+=spellDamage(parsed[2],dInvited,redChance)
                        if diSkip>0:
                            diSkip-=1
                        else:
                            starterTurn=False
                elif username.lower() == dInvited.lower():
                    if starterTurn==True:
                        msg="Not your turn yet."
                    if diSkip !=0:
                        msg = "Your turn is skipped."
                    if parsed[2] not in spells:
                        msg="That's not a spell."
                    else:
                        if diBlind!=0:
                            diBlind-=1
                            redChance=30
                        if diBurn:
                            diBurn==False
                            HP[dInvited]-=5
                            msg+=dInvited + " has taken 5% burn damage." + " "
                        redChance=0
                        msg+=spellDamage(parsed[2],dStarter,redChance)
                        if dsSkip>0:
                            dsSkip-=1
                        else:
                            starterTurn=True
            msg+=dStarter + ": " + str(HP[dStarter]) + ", " + dInvited + ": " + str(HP[dInvited]) + ". "
            if HP[dStarter]<=0 and HP[dStarter]<HP[dInvited]:
                msg += dInvited + " has defeated " + dStarter + " and has taken 300 sync points." + " "
                Parent.AddPoints(dInvited, 300)
                Parent.RemovePoints(dStarter, 300)
                dStage = 0
                del HP[dStarter]
                del HP[dInvited]
                dStarter = ""
                dInvited = ""
            elif HP[dInvited]<=0 and HP[dInvited]<HP[dStarter]:
                msg += dStarter + " has defeated " + dInvited + " and has taken 300 sync points." + " "
                Parent.AddPoints(dStarter, 300)
                Parent.RemovePoints(dInvited, 300)
                dStage = 0
                del HP[dStarter]
                del HP[dInvited]
                dStarter = ""
                dInvited = ""
            elif HP[dStarter]==HP[dInvited] and HP[dStarter]<=0:
                msg+="We have a tie! How was that possible? Take 150 each for participating I guess."
                Parent.AddPoints(dStarter, 150)
                Parent.AddPoints(dInvited, 150)
                dStage = 0
                del HP[dStarter]
                del HP[dInvited]
                dStarter = ""
                dInvited = ""
            else:
                if starterTurn:
                    msg += "It is " + dStarter + "'s turn." + " "
                else:
                    msg+="It is " + dInvited + "'s turn." + " "
            if msg=="":
                dStage = 0
                del HP[dStarter]
                del HP[dInvited]
                dStarter = ""
                dInvited = ""
                msg+="There was nothing."


    if data.IsFromTwitch():
        Parent.SendStreamMessage(msg)
    if data.IsFromDiscord():
        Parent.SendDiscordMessage(msg)
    return

#---------------------------------------
#   [Required] Tick Function
#---------------------------------------
def Tick():
    return

#SpellName: #Accuracy, #Description
#1Flipendo: 75%, does 20% damage
#2Wingardium: 70%, 10% or 30% damage (50/50Chance)
#3Incendio: 50%, 0% damage, 5% burn damage per turn after (Does not stack)
#4Lumos: 90%, 0% damage, reduces all accuracy by 30% for 3 turns
#5Rictusempra: 70%, 20% damage, gives opponent time to react, +5% damage on rebound
#6Skurge: 70%: 0% damge, removes effects (burn & blindness)
#7Diffindo: 60%, 30% damage
#8Glacius: 50%, 10% damage, causes opponent to lose next turn gives opponent time to react
#9Protego: 85%, reflects certain spells
#10Expelliarmus: 60%, causes opponent to lose next turn
