TYP_ATTACK = 0
ATTACKER_VILLAGE_CORDS = 1
DATE_AND_TIME = 2
ATTACKER_NICK = 3
DEFENDER_VILLAGE_CORDS = 4
DEFENDER_NICK = 5
WHEN_SENT = 6
DISTANCE = 7
HOW_MANY_ATTACKS = 8


def write_in_sos_format(sos_format):
    with open("data/rezults/sos_for_all.txt", "w", encoding='utf-8') as sos_for_all:
        players_list = sos_format.keys()
        for nick in players_list:
            sos_for_all.write(nick + "\n")
            villages_this_player = sos_format[nick].keys()
            for village in villages_this_player:
                sos_for_all.write("\n" + "\t" + village + "\n")
                for attack in sos_format[nick][village]:
                    sos_for_all.write(
                        "\t\t" +
                        attack[TYP_ATTACK] +
                        ", " +
                        attack[ATTACKER_NICK] +
                        ", " +
                        attack[DISTANCE] +
                        ", " +
                        attack[WHEN_SENT].replace(" ", ",") +
                        ", " +
                        attack[DATE_AND_TIME].replace(" ", ",") +
                        ", ataki: ," +
                        attack[HOW_MANY_ATTACKS].replace("/", ",") +
                        "\n")

    sos_for_all.close()
