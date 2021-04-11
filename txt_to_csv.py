from docx import Document

ATTACK_TYPE = 0
ATTACKER_VILLAGE = 1
ATTACK_TIME = 2
ATTACKER_NICK = 3
DEFENDER_VILLAGE = -1  # last element form defender village list
DEFENDER_NICK = -1  # last element frm defender nick list


def get_data_from_docx(PLAYERS_LIST, players_data_files):
    end_data = {}
    for nick in PLAYERS_LIST:

        document = Document(players_data_files+"/"+nick+'.docx')
        data = []
        end_data[nick] = []
        for para in document.paragraphs:
            data.append(para.text)

        for line in data:

            line = line.replace("[b]Wioska:[/b] ", "")
            line = line.replace("[b]Poparcie:[/b] 100", "")
            line = line.replace("    ", "")

            if "[b]Po" in line:
                line = ""
            elif "[b]Ob" in line:
                line = ""

            elif len(line) > 25:
                line = line.replace("\t", "")
                line = line.replace("nd] [co", "nd] nieOpisany [co")
                line = line.replace("[command]attack[/command] ", "")
                line = line.replace("[command]attack_small[/command] ", "")
                line = line.replace(" [coord]", "!@!")
                line = line.replace("[/coord] --> Czas przybycia: ", "!@!")
                line = line.replace(" [player]", "!@!")
                line = line.replace("[/player]", "")
                line = line.split("!@!")

                # line = [item[::-1] for item in line[::-1].split('-', 4)][::-1]
                end_data[nick].append(line)

            elif len(line) > 5:
                line = line.replace("[coord]", "")
                line = line.replace("[/coord]", "")
                end_data[nick].append([line])

    end_data = change_format_to_list_of_list(end_data)
    return end_data


def change_format_to_list_of_list(data_dict_form):
    data_list_attacks = []
    nicks_list = data_dict_form.keys()
    for nick in nicks_list:
        records = data_dict_form[nick]
        cord_list = []
        for record in records:
            if len(record) == 1:
                cord_list.append(record[0])
            else:
                # print(nick)
                # print(record)
                one_attack = [record[ATTACK_TYPE],  # ATTACK_TYPE
                              record[ATTACKER_VILLAGE],  # ATTACKER_VILLAGE
                              record[ATTACK_TIME],  # ATTACK_TIME
                              record[ATTACKER_NICK],  # ATTACKER_NICK
                              cord_list[DEFENDER_VILLAGE],  # DEFENDER_VILLAGE
                              nick,  # DEFENDER_NICK
                              ]
                data_list_attacks.append(one_attack)

    return data_list_attacks
