# from read_speakers import extract_speakers_n
# from read_dialogues import extract_dialogues_dic_n
# from get_er_balanced import get_er_dic_group
# from get_temporal_err import get_er_ratio_in_time_n, get_er_ratio_temporal_n
# from utt_count import number_of_total_u

from nltk.corpus import stopwords
stops = set(stopwords.words('english'))
# print(len(stops))
filled_p = ['ah','oh','eh','er','erm','mm','mhm','huh','uhu']
for p in filled_p:
    stops.add(p)
# print(stops)
# print(len(stops))


def extract_speakers_n(df1):
    dataC = df1
    speaker = [dataC[0][0]]

    for row in range(0,len(dataC)):
        if dataC[0].iloc[row] not in speaker:
            speaker.append(dataC[0].iloc[row])

    return speaker

def number_of_total_u(speaker_dic):
    number_of_u = 0
    for s_d in speaker_dic:
        number_of_u = number_of_u + len(s_d)

    return number_of_u

def extract_dialogues_dic_n(rdd1, speaker):
    n = len(speaker)
    dataC = rdd1
    speaker_dic = [{} for x in range(0,n)]

    for i in range(0,len(dataC)):
        if dataC[0].iloc[i] in speaker:
            p = speaker.index(dataC[0].iloc[i])
            if dataC[1].iloc[i]!=None:
                speaker_dic[p][i] = dataC[1].iloc[i].split()

    return speaker_dic


def number_of_slot_n(speaker_dic,length_u):
    number_of_u = 0
    for s_d in speaker_dic:
        number_of_u = number_of_u + len(s_d)

    number_slot = int(number_of_u - number_of_u%length_u)/length_u
    return int(number_slot)

def number_of_total_u(speaker_dic):
    number_of_u = 0
    for s_d in speaker_dic:
        number_of_u = number_of_u + len(s_d)

    return number_of_u

def get_vo_average_speaker(speaker, speaker_dic, ex_stop):
    n = len(speaker)
    voand = []
    voor = []
    speaker_vo = [[] for x in range(0,n)]
    vo_group = {}
    token_n = 0

    for i in range(0,n):
        for k,tokens in speaker_dic[i].items():
            token_n = token_n + len(tokens)
            for token in tokens:
#                 token_n = token_n+1
                if token not in voor:
                    voor.append(token)
                if token not in speaker_vo[i]:
                    speaker_vo[i].append(token)

    if n==2:
        voand_2 = []

        if ex_stop == True:
            for s0 in speaker_vo[0]:
                if s0 in speaker_vo[1]:
                    if (s0 not in voand_2) and (s0 not in stops):
                        voand_2.append(s0)

        else:
            for s0 in speaker_vo[0]:
                if s0 in speaker_vo[1]:
                    if (s0 not in voand_2):
                        voand_2.append(s0)

        countand = len(voand_2)
        # print(countand)
        countor = len(voor)
        overlap = countand/countor

        vo_group = {"speaker_number": n, "vo_overlap": countand, "vo_total": countor, "total_token_number":token_n, "overlap": overlap}
        return vo_group

    if n>2:
        countand_list = [[] for j in range(0,len(speaker))]
        x = 0

        if ex_stop == True:
            for s_i in range(0,n):
                for s_j in range(0,n):
                    if s_j != s_i:
                        for token in speaker_vo[s_i]:
                            if token in speaker_vo[s_j]:
                                if (token not in countand_list[x]) and (token not in stops):
                                    countand_list[x].append(token)
                x = x+1

        else:
            for s_i in range(0,n):
                for s_j in range(0,n):
                    if s_j != s_i:
                        for token in speaker_vo[s_i]:
                            if token in speaker_vo[s_j]:
                                if token not in countand_list[x]:
                                    countand_list[x].append(token)
                x = x+1

        countand = 0
        for c in range(0,len(speaker)):
            countand = countand + len(countand_list[c])

        countor = len(voor)
        overlap = countand/(len(speaker)*countor)

        vo_group = {"speaker_number": n, "vo_overlap": countand, "vo_total": countor, "total_token_number":token_n, "overlap": overlap}

        for sp in range(0,len(speaker)):
            vo_group["s" + str(sp+1)+ "_and_other"] = len(countand_list[sp])

        return vo_group

def get_vo_average_speaker_in_window(speaker, speaker_dic, start, end, ex_stop):
    n = len(speaker)
    voand = []
    voor = []
    speaker_vo = [[] for x in range(0,n)]
    vo_group = {}
    token_n = 0

    for i in range(0,n):
        for k,tokens in speaker_dic[i].items():
            if k>=start and k<end:
                token_n = token_n + len(tokens)
                for token in tokens:
#                 token_n = token_n+1
                    if token not in voor:
                        voor.append(token)
                    if token not in speaker_vo[i]:
                        speaker_vo[i].append(token)

    if n==2:
        voand_2 = []

        if ex_stop == True:
            for s0 in speaker_vo[0]:
                if s0 in speaker_vo[1]:
                    if (s0 not in voand_2) and (s0 not in stops):
                        voand_2.append(s0)

        else:
            for s0 in speaker_vo[0]:
                if s0 in speaker_vo[1]:
                    if (s0 not in voand_2):
                        voand_2.append(s0)

        countand = len(voand_2)
        countor = len(voor)
        overlap = countand/countor

        vo_group = {"speaker_number": n, "vo_overlap": countand, "vo_total": countor, "total_token_number":token_n, "overlap": overlap, "begin":start, "end":end}

        return vo_group

    if n>2:
        countand_list = [[] for j in range(0,len(speaker))]
        x = 0
        if ex_stop == True:
            for s_i in range(0,n):
                for s_j in range(0,n):
                    if s_j != s_i:
                        for token in speaker_vo[s_i]:
                            if token in speaker_vo[s_j]:
                                if (token not in countand_list[x]) and (token not in stops):
                                    countand_list[x].append(token)
                x = x+1

        else:
            for s_i in range(0,n):
                for s_j in range(0,n):
                    if s_j != s_i:
                        for token in speaker_vo[s_i]:
                            if token in speaker_vo[s_j]:
                                if token not in countand_list[x]:
                                    countand_list[x].append(token)
                x = x+1

        countand = 0
        for c in range(0,len(speaker)):
            countand = countand + len(countand_list[c])

        countor = len(voor)
        overlap = countand/(len(speaker)*countor)

        vo_group = {"speaker_number": n, "vo_overlap": countand, "vo_total": countor, "total_token_number":token_n, "overlap": overlap}

        for sp in range(0,len(speaker)):
            vo_group["s" + str(sp+1)+ "_and_other"] = len(countand_list[sp])

        vo_group['begin'] = start
        vo_group['end'] = end


        return vo_group

def get_vo_average_speaker_temporal_n(speaker, speaker_dic, length, exclude_stops):
    slot_number = number_of_slot_n(speaker_dic, length)
    vo_dic_list = []
    total_u = 0

    for s in speaker_dic:
        total_u = total_u + len(s)

    for i in range(0,slot_number):
        vo_dic = get_vo_average_speaker_in_window(speaker,speaker_dic, 0, length*(i+1), exclude_stops)
        vo_dic_list.append(vo_dic)

    vo_dic_end = get_vo_average_speaker_in_window(speaker, speaker_dic, 0, total_u, exclude_stops)
    vo_dic_list.append(vo_dic_end)

    return vo_dic_list



import pandas as pd
import os, glob


import os

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)            #makedirs




input_path = input('Enter Input Folder Path:')
output_path = input('Enter Desired Output Folder Path:')
window_length = input('Enter Desired Window Length:')
input_exclude_stops = input('Whether or not to exclude stopwords (y/n):')

if input_exclude_stops == 'y':
    para_exclude_stops = True
else:
    para_exclude_stops = False


files = glob.glob(os.path.join(input_path,'S***.tsv'))
dl_vo_global = [[]for i in range(0,12)]
# dl_lexicon_sum = [[]for j in range(0,12)]

# path_sum = [output_path + "/group_size_2", output_path + "/group_size_3", output_path + "/group_size_4"]
# for p in path_sum:
#     mkdir(p)

for f in files:

    df = pd.read_csv(f, sep=r'\t', header=None)
    speakers = extract_speakers_n(df)

    for sp_num in range(2,12):

        if len(speakers) == sp_num:
            path2 = output_path + "/group_size_" + str(sp_num)
            mkdir(path2)
            dialogues_dic = extract_dialogues_dic_n(df,speakers)
            df_vo_temporal = get_vo_average_speaker_temporal_n(speakers,dialogues_dic,int(window_length), para_exclude_stops)
            for d in df_vo_temporal:
                d['file'] = f

            vo_global = get_vo_average_speaker(speakers,dialogues_dic, para_exclude_stops)
            vo_global['file'] = f
            dl_vo_global[sp_num-2].append(vo_global)

            dl_s = pd.DataFrame(df_vo_temporal)
            dl_s.to_csv(os.path.join(path2,f[len(f)-8:len(f)-4] + '_cumulative_vo.csv'), index = False)


for i in range(0,len(dl_vo_global)):
    if dl_vo_global[i]!=[]:
        dl_err_sum_pd = pd.DataFrame(dl_vo_global[i])
        dl_err_sum_pd.to_csv(os.path.join(output_path,'global_vo_summary' + str(i+2)+ '_speakers.csv'), index = False)
        # dl_err_sum_pd.to_csv(os.path.join(output_path + "/group_size_" + str(i+2),'summary_err_global_' + str(i+2)+ '_speakers.csv'), index = False)





    # print(speakers)
    # # print(er_dic)
    # print(len(er_dic))
    # print(utt_number)
    # print(err_global)
    # for x in err_temporal:
    #     print(x['av_er_ratio'])


