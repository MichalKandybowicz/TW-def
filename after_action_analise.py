

def analise(sos_format, defenders_nicks):
    
    attacked = []
    with open("data/attacked/cords.csv") as f:
        for line in f:
            print(line.rstrip())
            attacked.append(line.rstrip())

    ile_attacked = len(attacked)
    ile_spraownaych = 0
    for nick in defenders_nicks:
        if len(sos_format[nick]) > 0:
            for i in sos_format[nick]:
                if i in attacked:
                    ile_spraownaych += 1



