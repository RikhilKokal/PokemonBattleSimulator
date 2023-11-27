from time import sleep
from random import randint
from copy import deepcopy

# =============================================================================
# def pokeprint
#
# Prints one character at a time from a string
#
# Arguments -
# msg:	the string to print
#
# Returns - None
#
def pokeprint(msg):
	for letter in msg:
		print(letter, end = "", flush = True)
		sleep(0.05)
	print()
# end: def pokeprint


# List of types that are super effective against other types
superEffective = {
	"normal"	:	[],
	"fire"		:	["grass", "ice", "bug", "steel"],
	"water"		:	["fire", "ground", "rock"],
	"electric"	:	["water", "flying"],
	"grass"		:	["water", "ground", "rock"],
	"ice"		:	["grass", "ground", "flying", "dragon"],
	"fighting"	:	["normal", "ice", "rock", "dark", "steel"],
	"poison"	:	["grass", "fairy"],
	"ground"	:	["fire", "electric", "poison", "steel"],
	"flying"	:	["grass", "fighting", "bug"],
	"psychic"	:	["fighting", "poison"],
	"bug"		:	["grass", "psychic", "dark"],
	"rock"		:	["fire", "ice", "fly", "bug"],
	"ghost"		:	["psychic", "ghost"],
	"dragon"	:	["dragon"],
	"dark"		:	["psychic", "ghost"],
	"steel"		:	["ice", "rock", "fairy"],
	"fairy"		:	["fighting", "dragon", "dark"],
}
# List of types that are not effective against other types
notVeryEffective = {
	"normal"	:	["rock", "steel"],
	"fire"		:	["fire", "water", "rock", "dragon"],
	"water"		:	["water", "grass", "dragon"],
	"electric"	:	["electric", "grass", "dragon"],
	"grass"		:	["fire", "grass", "poison", "fly", "bug", "dragon", "steel"],
	"ice"		:	["fire", "water", "ice", "steel"],
	"fighting"	:	["poison", "fly", "psychic", "bug", "fairy"],
	"poison"	:	["poison", "ground", "rock", "ghost"],
	"ground"	:	["grass", "bug"],
	"flying"	:	["electric", "rock", "steel"],
	"psychic"	:	["psychic", "steel"],
	"bug"		:	["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"],
	"rock"		:	["fighting", "ground", "steel"],
	"ghost"		:	["dark"],
	"dragon"	:	["steel"],
	"dark"		:	["figthing", "dark", "fairy"],
	"steel"		:	["fire", "water", "electric", "steel"],
	"fairy"		:	["fire", "poison", "steel"]
}
# List of types that have no effect against other types
noEffect = {
	"normal"	:	["ghost"],
	"fire"		:	[],
	"water"		:	[],
	"electric"	:	["ground"],
	"grass"		:	[],
	"ice"		:	[],
	"fighting"	:	["ghost"],
	"poison"	:	["steel"],
	"ground"	:	["flying"],
	"flying"	:	[],
	"psychic"	:	["dark"],
	"bug"		:	[],
	"rock"		:	[],
	"ghost"		:	["normal"],
	"dragon"	:	["fairy"],
	"dark"		:	[],
	"steel"		:	[],
	"fairy"		:	[]
}

# =============================================================================
# class Move
#
class Move:

	# =============================================================================
	# def __init__
	#
	# init function for Move class
	#
	# Arguments -
	# self - the representation of the instance of the Move class
	# name - the name of the move
	# basePower - base power of the move
	# category - category (physical/special) of the move
	# accuracy - chance that the move will hit
	# powerPoints - how many times the move can be used
	#
	# Returns - None
	#

	def __init__(self, name, category, moveType, basePower, accuracy, powerPoints, critRate = 24):
		self.name = name
		self.category = category
		self.type = moveType
		self.basePower = basePower
		self.accuracy = accuracy
		self.powerPoints = powerPoints
		self.critRate = critRate
	# end: def __init__

# end: class Move

stages = [1/4, 57/200, 1/3, 2/5, 1/2, 2/3, 1, 1.5, 2, 2.5, 3, 3.5, 4]

# =============================================================================
# class Pokemon
#
class Pokemon:

	# =============================================================================
	# def __init__
	#
	# Init function for Pokemon class
	#
	# Arguments -
	# self - the representation of the instance of the Pokemon class
	# name - the Pokemon's name
	# type1 - the Pokemon's first typing
	# type2 - the Pokemon's second typing, or an empty string if not applicable
	# EVs - A dictionary containing the EVs for the Pokemon
	# moves - A list containing four instances of the Move class as the learned moves for that pokemon
	#
	# Returns - None
	#
	def __init__(self, name, type1, type2, level, EVs, moves):
		self.name = name
		self.type1 = type1
		self.type2 = type2
		self.level = level
		self.hp = EVs["HP"]
		self.maxHP = EVs["HP"]
		self.atk = EVs["ATK"]
		self.defense = EVs["DEF"]
		self.spA = EVs["SPATK"]
		self.spD = EVs["SPDEF"]
		self.spe = EVs["SPE"]
		self.moves = moves
		self.flinch = False
	# end: def __init__

	# =============================================================================
	# def fight
	#
	# Actual fight
	#
	# Arguments -
	# self - the representation of the instance of the Pokemon class
	# move - the move that the pokemon is using
	# pokemon2 - the Pokemon that the user fights
	# opposing - whether or not to print opposing
	#
	# Returns - None
	#
	def fight(self, move, pokemon2, opposing):
		miss = False
		hit = randint(1, 100)

		if self.flinch is False:
			pokeprint("The {0}{1} used {2}!".format("opposing " if opposing else "", self.name, move.name))

			if hit > move.accuracy:
				if opposing is True:
					pokeprint(f"{pokemon2.name} avoided the attack!")
				else:
					pokeprint(f"The opposing {pokemon2.name} avoided the attack!")
				miss = True

			elif move.basePower != 0:
				damage = (((2 * self.level)/5) + 2) * move.basePower

				if move.category == "physical":
					damage *= self.atk/pokemon2.defense
				elif move.category == "special":
					damage *= self.spA/pokemon2.spD

				if randint(1, move.critRate) == move.critRate: crit = 1.5
				else: crit = 1

				damage /= 50
				damage += 2

				modifier = (randint(85,100)/100) * crit
				if move.type == self.type1 or move.type == self.type2:
					modifier *= 1.5

				effective = 1
				if pokemon2.type1 in superEffective[move.type]:
					effective *= 2
				elif pokemon2.type1 in notVeryEffective[move.type]:
					effective *= 1/2
				elif pokemon2.type1 in noEffect[move.type]:
					effective *= 0

				if pokemon2.type2 in superEffective[move.type]:
					effective *= 2
				elif pokemon2.type2 in notVeryEffective[move.type]:
					effective *= 1/2
				elif pokemon2.type2 in noEffect[move.type]:
					effective *= 0

				if effective > 1:
					pokeprint("It's super effective!")
				elif effective == 0:
					if opposing is True:
						pokeprint(f"It doesn't affect {pokemon2.name}.")
					else:
						pokeprint(f"It doesn't affect the opposing {pokemon2.name}")
				elif effective < 1:
					pokeprint("It's not very effective...")

				if crit == 1.5:
					pokeprint("A critical hit!")

				modifier *= effective
				damage = round(damage * modifier)
				if (pokemon2.hp - damage) < 0:
					damage = pokemon2.hp

				if opposing is True:
					pokeprint(f"({pokemon2.name} lost {round((damage / pokemon2.maxHP) * 100)}% of its health!)")
				else:
					pokeprint(f"(The opposing {pokemon2.name} lost {round((damage / pokemon2.maxHP) * 100)}% of its health!)")
				
				pokemon2.hp -= damage



			if miss is True and move.name == "High Jump Kick":
				self.hp -= (self.maxHP // 2)
				if opposing is True:
					pokeprint(f"The opposing {self.name} kept going and crashed!")
				else:
					pokeprint(f"{self.name} kept going and crashed!")
		
			elif move.name == "Meteor Mash" and miss is False:
				if randint(1, 100) <= 20:
					self.attack *= 1.5
					if opposing is True:
						pokeprint(f"The opposing {self.name}'s Attack rose!")
					else:
						pokeprint(f"{self.name}'s Attack rose!")

			elif move.name == "Wild Charge":
				self.hp -= damage // 4
				if opposing is True:
					pokeprint(f"The opposing {self.name} was damaged by the recoil!")
				else:
					pokeprint(f"{self.name} was damaged by the recoil!")

			elif move.name == "Psychic":
				if randint(1, 100) <= 10:
					pokemon2.spD = round(pokemon2.spD * 2/3)
					if opposing is True:
						pokeprint(f"{self.name}'s Special Defense fell!")
					else:
						pokeprint(f"The opposing {self.name}'s Special Defense fell!")
			
			elif move.name == "Iron Tail" and miss is False:
				if randint(1, 100) <= 30:
					pokemon2.defense = round(pokemon2.spD * 2/3)
					if opposing is True:
						pokeprint(f"{self.name}'s Defense fell!")
					else:
						pokeprint(f"The opposing {self.name}'s Defense fell!")

			elif move.name == "Calm Mind":
				self.spA = round(self.spA * 1.5)
				self.spD = round(self.spD * 1.5)
				if opposing is True:
					pokeprint(f"The opposing {self.name}'s Special Attack rose!")
					pokeprint(f"The opposing {self.name}'s Special Defense rose!")
				else:
					pokeprint(f"{self.name}'s Special Attack rose!")
					pokeprint(f"{self.name}'s Special Defense rose!")

			elif move.name == "Iron Head":
				if randint(1, 100) <= 30 and self.spe > pokemon2.spe:
					pokemon2.flinch = True

			elif move.name == "Swords Dance":
				self.atk *= 2
				if opposing is True:
					pokeprint(f"The opposing {self.name}'s Attack rose sharply!")
				else:
					pokeprint(f"{self.name}'s Attack rose sharply!")
			
			print()

		elif self.flinch is True:
			if opposing is True:
				print(f"The opposing {self.name} flinched and couldn't move!\n")
			else:
				print(f"{self.name} flinched and couldn't move!\n")
			
			self.flinch = False

		move.powerPoints -= 1

	# end: def fight
# end: class Pokemon


# List of moves
moves = {
	"highJumpKick": Move("High Jump Kick", "physical", "fighting", 130, 90, 16), # lose 50% HP if miss
	"earthquake": Move("Earthquake", "physical", "ground", 100, 100, 16),
	"meteorMash": Move("Meteor Mash", "physical", "steel", 90, 90, 16), # 20% chance to raise atk
	"shadowClaw": Move("Shadow Claw", "physical", "ghost", 70, 100, 24, 8),
	"crossChop": Move("Cross Chop", "physical", "fighting", 100, 80, 8, 8),
	"wildCharge": Move("Wild Charge", "physical", "electric", 90, 100, 24), # 1/4 recoil
	"surf": Move("Surf", "special", "water", 90, 100, 24),
	"psychic": Move("Psychic", "special", "psychic", 90, 100, 16), # 10% chance to lower target's SPDEF
	"iceBeam": Move("Ice Beam", "special", "ice", 90, 100, 16),
	"calmMind": Move("Calm Mind", "status", "psychic", 0, 100, 32), # Raises user's SPA and SPDEF
	"dragonClaw": Move("Dragon Claw", "physical", "dragon", 80, 100, 24),
	"ironTail": Move("Iron Tail", "physical", "steel", 100, 75, 24), # 30% chance to lower target's DEF
	"nightSlash": Move("Night Slash", "physical", "dark", 70, 100, 24, 8),
	"ironHead": Move("Iron Head", "physical", "steel", 80, 100, 24), # 30% chance to make target flinch
	"swordsDance": Move("Swords Dance", "status", "normal", 0, 100, 32), # Raises user's attack by 2 stages
}

# List of the user's pokemon
userPokemon = [
	Pokemon(
		"Lucario", "fighting", "steel", 100,
		{"HP": 281, "ATK": 256, "DEF": 176, "SPATK": 266, "SPDEF": 176, "SPE": 216},
		[moves["highJumpKick"], moves["earthquake"], moves["meteorMash"], moves["shadowClaw"]]
	),

	Pokemon(
		"Electivire", "electric", "", 100,
		{"HP": 291, "ATK": 251, "DEF": 170, "SPATK": 226, "SPDEF": 206, "SPE": 226},
		[moves["wildCharge"], moves["crossChop"], moves["ironTail"], moves["earthquake"]]
	),

	Pokemon(
		"Slowbro", "water", "psychic", 100,
		{"HP": 331, "ATK": 186, "DEF": 256, "SPATK": 236, "SPDEF": 196, "SPE": 96},
		[moves["surf"], moves["psychic"], moves["iceBeam"], moves["calmMind"]]
	),

	Pokemon(
		"Garchomp", "dragon", "ground", 100,
		{"HP": 357, "ATK": 296, "DEF": 226, "SPATK": 196, "SPDEF": 206, "SPE": 240},
		[moves["earthquake"], moves["shadowClaw"], moves["dragonClaw"], moves["ironTail"]]
	),

	Pokemon(
		"Bisharp", "dark", "steel", 100,
		{"HP": 271, "ATK": 286, "DEF": 236, "SPATK": 156, "SPDEF": 176, "SPE": 176},
		[moves["nightSlash"], moves["ironHead"], moves["shadowClaw"], moves["swordsDance"]]
	),
]

# List of computer's pokemon
CPUPokemon = []
for mon in userPokemon:
	CPUPokemon.append(deepcopy(mon))

# Get a pokemon from the user
whichMon = None
while whichMon not in range(1, len(userPokemon) + 1):
	# Ask the user for their choice of pokemon
	print("Which Pokemon would you like to use?")
	for mon in range(len(userPokemon) - 1):
		print(f"[{mon + 1}] {userPokemon[mon].name}")
	whichMon = input(f"[{len(userPokemon)}] {userPokemon[-1].name}\n\n")
	
	# See if the user's input is valid
	try:
		whichMon = int(whichMon)
	except:
		print("Your input must be a number.\n") # Return an error for invalid inputs
		continue # Ask for a new input

	# If the user entered an invalid pokemon number
	if whichMon not in range(1, len(userPokemon) + 1):
		print(f"Your input must be a number between 1 and {len(userPokemon)}.\n")

# Give the user their chosen pokemon
chosenMon = userPokemon[whichMon - 1]
# Give the computer a random pokemon
CPUMon = CPUPokemon[randint(0, len(CPUPokemon) - 1)]

print()

if chosenMon.spe < CPUMon.spe:
	pokeprint(f"CPU sent out {CPUMon.name}!")
	pokeprint(f"Go! {chosenMon.name}!")
else:
	pokeprint(f"Go! {chosenMon.name}!")
	pokeprint(f"CPU sent out {CPUMon.name}!")

print("\nYour moves are:")
for move in range(len(chosenMon.moves)):
	print(f"[{move + 1}] {chosenMon.moves[move].name}")

print()
# Make sure both pokemon are still alive
while chosenMon.hp > 0 and CPUMon.hp > 0:
	pokeprint(f"{chosenMon.name} HP: {round((chosenMon.hp / chosenMon.maxHP) * 100)}%")
	pokeprint(f"The opposing {CPUMon.name} HP: {round((CPUMon.hp / CPUMon.maxHP) * 100)}%\n")
	# Asks the player what move they would like to use
	whichMove = None
	while whichMove not in [1, 2, 3, 4]:
		for letter in f"What will {chosenMon.name} do?":
			print(letter, end = "", flush = True)
			sleep(0.05)
		whichMove = input("\n")

		try:
			whichMove = int(whichMove)
		except:
			print("You input must be a number.")
			continue
		
		if whichMove not in [1, 2, 3, 4]:
			print("Your input must be a number between one and four.\n")
		
		if chosenMon.moves[whichMove - 1].powerPoints == 0:
			pokeprint("You can't use that move!")
			whichMove = None

	print()

	# Choose who goes first based on speed
	whoGoesFirst = 0
	# If attack speeds are the same, choose a random player to go first
	if chosenMon.spe == CPUMon.spe:
		whoGoesFirst = randint(1, 2)

	# If the user has superior attack speed, they go first
	if chosenMon.spe > CPUMon.spe or whoGoesFirst == 1:
		chosenMon.fight(chosenMon.moves[whichMove - 1], CPUMon, False)
		
		# If the computer pokemon is still alive after the player's attack, they go
		if chosenMon.hp > 0 and CPUMon.hp > 0:
			CPUMon.fight(CPUMon.moves[randint(0,3)], chosenMon, True)
	
	# If the computer has superior attack speed, they go first
	elif chosenMon.spe < CPUMon.spe or whoGoesFirst == 2:
		CPUMon.fight(CPUMon.moves[randint(0,3)], chosenMon, True)
		
		# If the player pokemon is still alive, the player goes
		if chosenMon.hp > 0 and CPUMon.hp > 0:
			chosenMon.fight(chosenMon.moves[whichMove - 1], CPUMon, False)

if chosenMon.hp <= 0:
	pokeprint(f"{chosenMon.name} fainted!")
else:
	pokeprint(f"The opposing {CPUMon.name} fainted!")