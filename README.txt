A first person dungeon crawler with easily editable maps, items, and enemies.
Objective is to find gold key and exit the dungeon through the gold door.

COTNROLS
------------------------------
Arrow keys to move, up and down for forward and back, left and right to turn.
I opens inventory
-Z uses/equips item
-X exits Inventory
When fighting
-Z attacks
-X defends
-Enemies attack after certain intervals, defend to learn when to attack and when to defend

MAPS
------------------------------
Currently use map should be named 'map.txt'
Maps are made up of a series of letters and spaces, like below:
X X X X X X X X X X
X C X E - - D - - X
X - X - X X X X - X
X - X - X K X - - X
X - X - X - X - X X
X G - - - - - P X
X L X X X X X X X
X X X

X=Wall
-=Empty space
C=Chest
G=Gold key
L=Gold door
E=Enemy
D=Door
K=Key
P=Player starting position

All corners must be filled,
  X
X - X
  X
would cause an error.

ITEMS
------------------------------
There are 3 kinds of items, Weapons, Armors, and Consumables
Weapons increase attack damage, Armors subtract from damage recieved, Consumables add to current health value
in the text file, the first number shows what the item is,
1=Consumable
-Second number is amount of health added
2=Armor
-Second number is damage prevented
3=Weapon
-Second number is total attack

ENEMIES
------------------------------
First number is health
Second is damage
Third is how many FRAMES between attacks (game at 30 FPS)
Image should have same name as text file