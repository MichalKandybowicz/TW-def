import math
from datetime import datetime, timedelta
from operator import itemgetter
import os

#
SPEED_OF_NOBLE_MAN = 21875 / 10  # s/p
SPEED_OF_RAM = 18750 / 10  # s/p
X = 0  # space for x coordinate
Y = 1  # space for y coordinate

# for all in time type
DAYS = 0
HOURS = 1
MIN = 2
SEC = 3

# for attack list
TYP_ATTACK = 0
ATTACKER_VILLAGE_CORDS = 1
DATE_AND_TIME = 2
ATTACKER_NICK = 3
DEFENDER_VILLAGE_CORDS = 4
DEFENDER_NICK = 5
# added after calculate
WHEN_SENT = 6
DISTANCE = 7
HOW_MANY_ATTACKS = 8


def get_players_list(directory) -> list:
    """

    :param directory: to files where are all txt files
    :return: list off players
    """
    files_list = os.listdir(directory)
    files_name = []
    for i in files_list:
        files_name.append(i[:-5])
    return files_name


def get_how_many_attacks_from_attacker_village(list_of_attacks):
    """

    :param list_of_attacks: all attacks list
    :return: dict {attacker village: int - how many attacks from this village]
    """
    attack_dict = {}

    for attack in list_of_attacks:
        villages_attacks_keys = list(attack_dict.keys())
        if attack[ATTACKER_VILLAGE_CORDS] in villages_attacks_keys:
            attack_dict[attack[ATTACKER_VILLAGE_CORDS]] += 1
        else:
            attack_dict[attack[ATTACKER_VILLAGE_CORDS]] = 1

    return attack_dict


def more_then_one_attack(dict_attacks_from_village):
    """

    :param dict_attacks_from_village:
    :return: list villages under attack more than once
    """
    more_then_one_attack_list = []
    for i in list(dict_attacks_from_village.keys()):
        if dict_attacks_from_village[i] > 1:
            more_then_one_attack_list.append(i)
    return more_then_one_attack_list


def add_sent_time_and_sort_by_this(dict_attacks_from_village, data):
    """

    :param dict_attacks_from_village:
    :param data: list of all attacks
    :return: list sorted by when the attack was sent
    """

    list_with_all_information = []

    for attack in data:

        distance, target, start = distance_counting(attack[ATTACKER_VILLAGE_CORDS],
                                     attack[DEFENDER_VILLAGE_CORDS],
                                     attack)  # return distance a -> b

        attack_travel_time_list = attack_travel_time(distance,
                                                     attack[TYP_ATTACK], attack)  # returns list [D, h, m, s]

        end_time_object = datetime.strptime(attack[DATE_AND_TIME], '%d.%m.%y %H:%M:%S:%f')
        when_sent = end_time_object - timedelta(days=attack_travel_time_list[DAYS],
                                                hours=attack_travel_time_list[HOURS],
                                                minutes=attack_travel_time_list[MIN],
                                                seconds=attack_travel_time_list[SEC])
        when_sent = change_time_object_to_string(when_sent)
        end_time = change_time_object_to_string(end_time_object)
        how_many_attacks = dict_attacks_from_village[attack[ATTACKER_VILLAGE_CORDS]]

        list_with_all_information.append([attack[TYP_ATTACK],
                                          target,
                                          end_time,
                                          attack[ATTACKER_NICK],
                                          start,
                                          attack[DEFENDER_NICK],
                                          when_sent,
                                          str(int(distance)),
                                          how_many_attacks])

    sorted_by_send_time = sort_by_date(list_with_all_information)
    return sorted_by_send_time


def sort_by_date(list_of_attacks):
    """

    :param sort_key: sort key
    :param list_of_attacks: list all of atatcks
    :return: list sorted my key
    """
    sorted_by_send_time = sorted(list_of_attacks, key=itemgetter(DATE_AND_TIME))
    return sorted_by_send_time


def distance_counting(start, target, attacks):
    """

    :param start: attacker village coords
    :param target: defender village coords
    :return: distance 1 -> 2
    """
    try:
        t = target
        s = start
        start = start.split('|')
        target = target.split('|')
        y_dif = math.fabs(int(start[X]) - int(target[X]))
        x_dif = math.fabs(int(start[Y]) - int(target[Y]))
        distance = math.hypot(x_dif, y_dif)
        # print(attacks)
        return distance, s, t
    except ValueError:
        print(attacks)


def attack_travel_time(distance, attack_type, data):
    """

    :param distance:
    :param attack_type:
    :return: attack travel time for Szlachcic, zwiad and all others like "taran"
    """
    if attack_type == "Szlachcic":
        duration = distance * SPEED_OF_NOBLE_MAN
        time_list = seconds_to_datetime(duration)
        return time_list
    else:
        duration = distance * SPEED_OF_RAM
        time_list = seconds_to_datetime(duration)
        return time_list


def seconds_to_datetime(secs):
    """

    :param secs: time travel in seconds
    :return: list [days, hours, minutes, seconds]
    """
    days = secs // 86400
    hours = (secs - days * 86400) // 3600
    minutes = (secs - days * 86400 - hours * 3600) // 60
    seconds = secs - days * 86400 - hours * 3600 - minutes * 60
    time_list = [days, hours, minutes, seconds]
    return time_list


def sort_by_sent_time(list_of_list):
    """
    Sorting data by sent time
    :param list_of_list: list of attacks
    :return: list of list (sorted by sent time)
    """
    sorted_by_send_time = sorted(list_of_list, key=itemgetter(WHEN_SENT))
    return sorted_by_send_time


def get_list_of_keys_from_list(list_of_list, key):
    """

    :param list_of_list:
    :param key:
    :return:
    """
    attacked_villages_list = []
    for attack in list_of_list:
        if attack[key] in attacked_villages_list:
            pass
        else:
            attacked_villages_list.append(attack[key])

    return attacked_villages_list


def add_information_send_no(list_of_list):
    """
    change information [how many attacks from attacker_village to with one
    :param list_of_list:
    :return:
    """
    data = get_key_attack_dict(list_of_list, ATTACKER_VILLAGE_CORDS)
    data_keys_list = list(data.keys())
    for key in data_keys_list:
        attack_list = data[key]
        for attack_no in range(len(attack_list)):
            how_many = attack_list[attack_no][HOW_MANY_ATTACKS]
            new_information = str(attack_no + 1) + "/" + str(how_many)
            attack_list[attack_no][HOW_MANY_ATTACKS] = new_information

    list_of_list = dict_to_list_of_list(data)

    return list_of_list


def dict_to_list_of_list(dict_with_list):
    """
    change to list of the list from format dict {key: attack list, key: attack list}
    :param dict_with_list: key is one part of list
    for example {attack_type : [[attack type, 1, 2, 3], [attack type, 2, 2, 3], [attack type, 2, 2, 3]]
    :return: return list of the list
    for example [[attack type, 1, 2, 3], [attack type, 2, 2, 3], [attack type, 2, 2, 3]]
    """

    list_of_list = []
    for key in dict_with_list:
        attacks_list = dict_with_list[key]
        for attack in attacks_list:
            list_of_list.append(attack)
    return list_of_list


def get_key_attack_dict(list_of_list, key):
    """

    :param list_of_list:
    :param key:
    :return:
    """
    attacked_villages_list = get_list_of_keys_from_list(list_of_list, key)
    attacks_dict = {}
    for i in attacked_villages_list:
        attacks_dict[i] = []

    for attack in list_of_list:
        attacks_dict_keys_list = list(attacks_dict.keys())
        if attack[key] in attacks_dict_keys_list:
            list_for_def = attacks_dict[attack[key]]
            list_for_def.append(attack)
            attacks_dict[attack[key]] = list_for_def
        else:
            attacks_dict[attack[key]] = [[attacks_dict[attack]]]
    return attacks_dict


def change_time_object_to_string(time_object):
    """
    convert datetime object to str
    :param time_object: date in time object
    :return: string Y/M/D H:M:S
    """
    return time_object.strftime("%Y/%m/%d %H:%M:%S")


def get_sos_format(list_of_list):
    """

    :param list_of_list: list of all attacks
    :return: conver list off atacks to sos format
    """
    end_format = {}
    list_of_list = sort_by_date(list_of_list)
    defenders_nicks_list = get_list_of_keys_from_list(list_of_list, DEFENDER_NICK)
    for nick in defenders_nicks_list:
        end_format[nick] = {}
        for attack in list_of_list:
            if attack[DEFENDER_NICK] == nick:
                end_format[nick][attack[DEFENDER_VILLAGE_CORDS]] = []

    for attack in list_of_list:
        end_format[attack[DEFENDER_NICK]][attack[DEFENDER_VILLAGE_CORDS]].append(attack)

    return end_format


def how_many_attacks_by(data):
    """
    :param data: list of attacks
    :return: dict K:nick - V: how many attack send
    """
    attackers_dict = {}
    for i in data:
        if i[3] in attackers_dict:
            attackers_dict[i[3]] += 1
        else:
            attackers_dict[i[3]] = 1

    return attackers_dict
