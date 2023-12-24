# wave лист заполняется по типу: кол-во легких, кол-во средних, кол-во тяжелых

WAVES = {'1':[3,1,0],'2':[5,2,0],'3':[8,5,1],'4':[12,7,2],'5':[15,10,3]}
DATA = {
    "light": {
    "health": 10,
    "speed": 2
  },
    "medium": {
    "health": 15,
    "speed": 3
  },
    "strong": {
    "health": 20,
    "speed": 4
  }
}

enemyesalive = 0
for i in WAVES:
    enemyesalive = sum(WAVES[i])
    print(enemyesalive)
