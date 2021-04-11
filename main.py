"""
format for players
    nick 1 (defender)
        XXX|YYY - defender village cords
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]

        XXX|YYY - defender village cords
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]

    nick 2 (defender)
        XXX|YYY - defender village cords
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]

        XXX|YYY - defender village cords
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]
            [ aggressor village, which is the attack from this village , Attack type, aggressor name, attack sent time]


"""

from txt_to_csv import get_data_from_docx
import data_connection
import logic
import filters
import after_action_analise

TYP_ATTACK = 0
ATTACKER_VILLAGE_CORDS = 1
DATE_AND_TIME = 2
ATTACKER_NICK = 3
DEFENDER_VILLAGE_CORDS = 4
DEFENDER_NICK = 5
WHEN_SENT = 6
DISTANCE = 7
HOW_MANY_ATTACKS = 8


def load_and_data_preparation():
    players_list = logic.get_players_list(players_data_files)
    data = get_data_from_docx(players_list, players_data_files)
    dict_attacks_from_village = logic.get_how_many_attacks_from_attacker_village(data)
    list_of_attacks = logic.add_sent_time_and_sort_by_this(dict_attacks_from_village, data)
    return list_of_attacks


def print_stats(stats_all_attacks, removed, stats_how_many_by_name, sos_format):
    # print("wyjebane bo idą z defówek: 0")
    # print("wyjebane bo idą z z wiosek gdzie off padł mniej niż 3 dni temu: 0")

    print("\nwszystkie ataki przed filtrowaniem:", stats_all_attacks)

    print("w sumie uznanych za fejki:", removed)

    print("wszystkie ataki po filtrowaniu:", stats_all_attacks - removed, '\n')

    defenders_nicks = sos_format.keys()
    atakowanych_wiosek = 0
    for nick in defenders_nicks:
        if len(sos_format[nick]) >= 1:
            atakowanych_wiosek += len(sos_format[nick])
            print(len(sos_format[nick]), "atakowanych wiosek", nick)

    after_action_analise.analise(sos_format, defenders_nicks)

    print("atakowanych wiosek wszystkich graczy:", atakowanych_wiosek)

    print('')
    how_many_by_name = dict(sorted(stats_how_many_by_name.items(), key=lambda item: item[1]))
    for i in how_many_by_name:
        if how_many_by_name[i] > 10:
            print(i, "wysła:", how_many_by_name[i], "ataków")


def main():
    data = load_and_data_preparation()

    data = logic.add_information_send_no(data)
    stats_all_attacks = len(data)

    sorted_data = logic.sort_by_sent_time(
        data,
    )

    filtered_data, removed = filters.main_filer(  # filters
        stats_all_attacks=stats_all_attacks, data=sorted_data, time=time_s, how_many=how_many, min_time=min_time, max_time=max_time
    )

    stats_how_many_by_name = logic.how_many_attacks_by(  # stats
        filtered_data
    )

    sos_format, removed_1 = filters.remove_by_min_attack_on_village(
        logic.get_sos_format(filtered_data)
        , min_attacks_on_village
    )

    data_connection.write_in_sos_format(sos_format)

    print_stats(stats_all_attacks, removed+removed_1, stats_how_many_by_name, sos_format)


try:
    from local_settings import *
except ImportError:
    print("Please create local file 'local_settings.py' ", end="")


if __name__ == '__main__':
    main()
