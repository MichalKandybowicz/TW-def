from datetime import datetime
import logic

# time_s = 5  # odstępy między atakami większe niż podane będą usó∑ane (jako fejki)
# how_many = 10  # >= ilości wysłąnych z 1 wioski będą usówane (jako fejki)
# min_time = "2021/02/06 07:00:00"  # %Y/%m/%d %H:%M:%S
# max_time = "2021/02/06 10:00:00"


def main_filer(stats_all_attacks, data, time, how_many, min_time, max_time):
    how_many_removed = 0
    before_removed = stats_all_attacks
    data, removed, jw, t1, t2, t3 = remove_by_time_period(time, data)
    print("Wywalone bo przekroczyły odstęp:", removed, "sekund, period time:", time,)
    print("wywalone bo juz weszły:", jw)
    print("wywalone bo identyczny odstęp", t1)
    print("wywalone bo identyczny odstęp +/- 1:", t2)
    print("wywalone bo identyczny odstęp +/- 2:", t3)
    print("zostało:", len(data), "\n")
    how_many_removed += removed + jw + t1 + t2 + t3
    # print('test jak liczby są te same to ok:', before_removed, how_many_removed + len(data), "\n")

    data, removed = remove_by_to_many_attacks(data, how_many)
    how_many_removed += removed
    print("wywalone", removed, "bo szło ponad", how_many, "ataków z jednej wioski")
    print("zostało:", len(data), "\n")
    # print('test jak liczby są te same to ok:', before_removed, how_many_removed + len(data), "\n")

    data, removed = remove_by_min_max_time(data, min_time, max_time)
    how_many_removed += removed
    print("Wywalonych", removed, "z powodu wejścia w godzinach innych niż min:", min_time, "max:", max_time)
    print("zostało:", len(data), "\n")
    # print('test jak liczby są te same to ok:', before_removed, how_many_removed + len(data), "\n")
    return data, how_many_removed


def remove_by_min_attack_on_village(sos_format, min_attacks_on_village):
    players_list = sos_format.keys()
    nie_zapisane_wioski = 0
    nie_zapisane_ataki = 0
    end_format = {}
    for nick in players_list:
        end_format[nick] = {}
        villages_this_player = sos_format[nick].keys()
        for village in villages_this_player:
            if len(sos_format[nick][village]) > min_attacks_on_village:
                end_format[nick][village] = sos_format[nick][village]
            else:
                nie_zapisane_wioski += 1
                nie_zapisane_ataki += len(sos_format[nick][village])

    print(nie_zapisane_wioski, "nie zapisanych wiosek bo miały mniej niż:", min_attacks_on_village, "ataków")
    print("w sumie nie zapisanych ataków:", nie_zapisane_ataki)
    return end_format, nie_zapisane_ataki


def remove_by_min_max_time(data, min_time, max_time):
    removed = 0
    new_data = []
    data_time_min = datetime.strptime(min_time, '%Y/%m/%d %H:%M:%S')
    data_time_max = datetime.strptime(max_time, '%Y/%m/%d %H:%M:%S')

    for i in data:
        attack_data = datetime.strptime(i[2], '%Y/%m/%d %H:%M:%S')
        if data_time_min < attack_data < data_time_max:
            new_data.append(i)
        else:
            removed += 1

    return new_data, removed


def get_list_by_attackers(data):
    new_data = {}
    for i in data:
        if i[3] in new_data:
            new_data[i[3]].append(i)
        else:
            new_data[i[3]] = []
            new_data[i[3]].append(i)
    return new_data


def remove_by_time_period(time, data):
    data = get_list_by_attackers(data)
    filtered_data = []
    out = 0
    now = datetime.now()
    now = datetime.strptime('2021/03/04 07:00:00', '%Y/%m/%d %H:%M:%S')
    juz_weszly = 0
    ten_sam_czas = 0
    ten_sam_czas_p1 = 0
    ten_sam_czas_p2 = 0
    for attacker_name in data.keys():
        attacks_list_by_attacker = data[attacker_name]
        for i in range(len(attacks_list_by_attacker)):
            data_time_attack = datetime.strptime(attacks_list_by_attacker[i][2], '%Y/%m/%d %H:%M:%S')
            if now < data_time_attack:

                if (i >= 1) and (i+1 < len(attacks_list_by_attacker)):
                    i_send_time = datetime.strptime(attacks_list_by_attacker[i][6], '%Y/%m/%d %H:%M:%S')
                    pre_send_time = datetime.strptime(attacks_list_by_attacker[i - 1][6], '%Y/%m/%d %H:%M:%S')
                    nex_send_time = datetime.strptime(attacks_list_by_attacker[i + 1][6], '%Y/%m/%d %H:%M:%S')
                    pre_diff = i_send_time - pre_send_time
                    nex_diff = nex_send_time - i_send_time

                    if pre_diff.seconds == nex_diff.seconds:
                        ten_sam_czas += 1

                    elif (pre_diff.seconds + 1 == nex_diff.seconds) or (pre_diff.seconds == nex_diff.seconds + 1):
                        ten_sam_czas_p1 += 1

                    elif (pre_diff.seconds + 2 == nex_diff.seconds) or (pre_diff.seconds == nex_diff.seconds + 2) or \
                            (pre_diff.seconds + 3 == nex_diff.seconds) or (pre_diff.seconds == nex_diff.seconds + 3):
                        ten_sam_czas_p2 += 1

                    elif (pre_diff.seconds < time) and (time > nex_diff.seconds):
                        out += 1

                    else:
                        filtered_data.append(attacks_list_by_attacker[i])
                # elif i >= 1:
                #     i_send_time = datetime.strptime(attacks_list_by_attacker[i][6], '%Y/%m/%d %H:%M:%S')
                #     pre_send_time = datetime.strptime(attacks_list_by_attacker[i - 1][6], '%Y/%m/%d %H:%M:%S')
                #     pre_diff = i_send_time - pre_send_time
                #
                #     if time > pre_diff.seconds:
                #         out += 1
                #
                #     else:
                #         filtered_data.append(attacks_list_by_attacker[i])
                #
                # elif i+1 < len(attacks_list_by_attacker):
                #
                #     i_send_time = datetime.strptime(attacks_list_by_attacker[i][6], '%Y/%m/%d %H:%M:%S')
                #     nex_send_time = datetime.strptime(attacks_list_by_attacker[i + 1][6], '%Y/%m/%d %H:%M:%S')
                #     nex_diff = nex_send_time - i_send_time
                #
                #     if time > nex_diff.seconds:
                #         out += 1
                #     else:
                #         filtered_data.append(attacks_list_by_attacker[i])
                else:
                    filtered_data.append(attacks_list_by_attacker[i])

            else:
                juz_weszly += 1

    return filtered_data, out, juz_weszly, ten_sam_czas, ten_sam_czas_p1, ten_sam_czas_p2


def remove_by_to_many_attacks(data, how_many):
    new_data = []
    how_many_removed = 0
    for i in data:
        # print(i)
        if (len(i[8]) == 3) and (int(i[8][2]) >= how_many):
            how_many_removed += 1

        elif (len(i[8]) == 4) and (int(i[8][-2:]) >= how_many):
            how_many_removed += 1

        elif (len(i[8]) == 5) and (int(i[8][-2:]) >= how_many):
            how_many_removed += 1

        else:
            new_data.append(i)

    return new_data, how_many_removed

