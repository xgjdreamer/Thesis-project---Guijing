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

def get_er_one_with_u(x,y, exclude_stops):
    record=[[0 for i in range(len(y)+1)]  for j in range(len(x)+1)]
    dic_record_s1 = {}
    dic_record_s2 = {}
    expression_list_1 = []
    # expression_list_2 = []
    expression_list_1_token = []
    # expression_list_2_token = []
    for i in range(0,len(x)):
        for j in range(0,len(y)):
            if x[i] == y[j]:
                record[i+1][j+1] = record[i][j] + 1
                if record[i+1][j+1] > 0:
                        if i not in dic_record_s1.keys():
                            dic_record_s1[i] = record[i+1][j+1]
                        elif i in dic_record_s1.keys():
                            if (dic_record_s1[i]<record[i+1][j+1]):
                                dic_record_s1[i] = record[i+1][j+1]

                        if j not in dic_record_s2.keys():
                            dic_record_s2[j] = record[i+1][j+1]
                        elif j in dic_record_s2.keys():
                            if (dic_record_s2[j]<record[i+1][j+1]):
                                dic_record_s2[j] = record[i+1][j+1]

    if dic_record_s1== {}:
        return []

    else:
        i = max(dic_record_s1.values())


    if dic_record_s2== {}:
        return []

    else:
        j = max(dic_record_s2.values())

    while i>0:
        for key in dic_record_s1:
            if dic_record_s1[key] == i:
            #expression_repitition_record = expression_repitition_record+1
                expression = x[key+1-i : key+1]
                expression_string = ' '.join(expression)

                for k in range(0,i):
                    dic_record_s1[key - k] = 0

                if exclude_stops == True:
                    if expression_string not in stops:
                        if expression_string not in expression_list_1:
                            expression_list_1.append(expression_string)
                            expression_list_1_token.append(expression)

                else:
                    if expression_string not in expression_list_1:
                        expression_list_1.append(expression_string)
                        expression_list_1_token.append(expression)

        i = i-1

    while j>0:
        for key in dic_record_s2:
            if dic_record_s2[key] == j:
                expression_2 = y[key+1-j : key+1]
                expression_string_2 = ' '.join(expression_2)

                for k in range(0,j):
                    dic_record_s2[key - k] = 0



                if exclude_stops == True:
                    if expression_string_2 not in stops:
                        if expression_string_2 not in expression_list_1:
                            expression_list_1.append(expression_string_2)
                            expression_list_1_token.append(expression_2)

                else:
                    if expression_string_2 not in expression_list_1:
                        expression_list_1.append(expression_string_2)
                        expression_list_1_token.append(expression_2)

        j = j-1

    return expression_list_1

# def get_er_dic(speaker1_dialogue, speaker2_dialogue, exclude_stops):
#     expressions = {}
#
#     for x,value_x in speaker1_dialogue.items():
#         for y,value_y in speaker2_dialogue.items():
#             string = get_er_one_with_u(value_x,value_y, exclude_stops)
#
#             for s in string:
#
#                 if s not in expressions.keys():
#
#                     pos = max(x,y)
#                     expressions[s] = [pos,[x],[y]]
#
#                 elif s in expressions.keys():
#                     if (x in expressions[s][1]) and (y not in expressions[s][2]):
#                         expressions[s][2].append(y)
#                         expressions[s][0] = max(min(expressions[s][2]),min(expressions[s][1]))
#
#                     elif (y in expressions[s][2]) and (x not in expressions[s][1]):
#                         expressions[s][1].append(x)
#                         expressions[s][0] = max(min(expressions[s][2]),min(expressions[s][1]))
#
#     return expressions

def get_er_dic_in_window(speaker1_dialogue, speaker2_dialogue, u_low, u_high, exclude_stops):
    expressions = {}

    for x,value_x in speaker1_dialogue.items():
        for y,value_y in speaker2_dialogue.items():
            if (x<u_high) and (x>= u_low) and (y<u_high) and (y>= u_low):
                string = get_er_one_with_u(value_x,value_y, exclude_stops)

                for s in string:

                    if s not in expressions.keys():

                        pos = max(x,y)
                        expressions[s] = [pos,[x],[y]]

                    elif s in expressions.keys():
                        if (x in expressions[s][1]) and (y not in expressions[s][2]):
                            expressions[s][2].append(y)
                            expressions[s][0] = max(min(expressions[s][2]),min(expressions[s][1]))

                        elif (y in expressions[s][2]) and (x not in expressions[s][1]):
                            expressions[s][1].append(x)
                            expressions[s][0] = max(min(expressions[s][2]),min(expressions[s][1]))

    return expressions

# def get_er_dic_group(speaker, speaker_dic,exclude_stops):
#     n = len(speaker)
#     expression_n = []
#     fit_ex_in_dic = [[]*n]
#     sum_dic = {}
#
#     for i in range(0,n-1):
#         for j in range(i+1, n):
#             ex = get_er_dic(speaker_dic[i],speaker_dic[j],exclude_stops)
#             expression_n.append(ex)
#
#     for split_dic in expression_n:
#         for k, v in split_dic.items():
#             v_sum = []
#             pos = v[0]
#
#             for v1 in v[1]:
#                 v_sum.append(v1)
#             for v2 in v[2]:
#                 v_sum.append(v2)
#
#             if k not in sum_dic.keys():
#                 sum_dic[k] = [pos,v_sum]
#             else:
#                 for vs in v_sum:
#                     if vs not in sum_dic[k][1]:
#                         sum_dic[k][1].append(vs)
#                         sum_dic[k][0] = min(pos, sum_dic[k][0])
#
#
#     for key, value in sum_dic.items():
#         sum_dic[key][1] = sorted(sum_dic[key][1])
#
#     return sum_dic
#
# def get_er_window_n(speaker_dic, ex_group, u_high):
#     ex_in_window = {}
#     for k,v in ex_group.items():
#         if v[0] <= u_high:
#             ex_in_window[k] = v
#
#
#     return ex_in_window

def get_er_dic_group_in_window(speaker, speaker_dic,u_low, u_high,exclude_stops):
    n = len(speaker)
    expression_n = []
    fit_ex_in_dic = [[]*n]
    sum_dic = {}

    for i in range(0,n-1):
        for j in range(i+1, n):
            ex = get_er_dic_in_window(speaker_dic[i],speaker_dic[j],u_low, u_high,exclude_stops)
            expression_n.append(ex)

    for split_dic in expression_n:
        for k, v in split_dic.items():
            v_sum = []
            pos = v[0]

            for v1 in v[1]:
                v_sum.append(v1)
            for v2 in v[2]:
                v_sum.append(v2)

            if k not in sum_dic.keys():
                sum_dic[k] = [pos,v_sum]
            else:
                for vs in v_sum:
                    if vs not in sum_dic[k][1]:
                        sum_dic[k][1].append(vs)
                        sum_dic[k][0] = min(pos, sum_dic[k][0])


    for key, value in sum_dic.items():
        sum_dic[key][1] = sorted(sum_dic[key][1])

    return sum_dic


def get_er_ratio_in_time_n(speaker, speaker_dic, u_low, u_high,exclude_stops):
    ex_in_window = get_er_dic_group_in_window(speaker, speaker_dic,u_low, u_high,exclude_stops)
#     print(ex_in_window.keys())
    n = len(speaker)
    sum_token = [0 for i in range(0,n)]
    max_len = 0
    speaker_dic_string = [{} for i in range(0,n)]
    sum_er = [0 for i in range(0,n)]
    sum_er_token = [0 for i in range(0,n)]
    er_ratio = [0 for i in range(0,n)]
#     print(speaker_dic[2])

    for key,value in ex_in_window.items():
        max_len = max(max_len, len(key.split()))

    for i in range(0,n):
        for k,v in speaker_dic[i].items():
            if k<u_high and k>=u_low:
                sum_token[i] = sum_token[i]+len(speaker_dic[i][k])
                speaker_dic_string[i][k] = ' '.join(speaker_dic[i][k])

    m = max_len

    while m>1:
        for k,v in ex_in_window.items():
            if (len(k.split())==m):
                for u in ex_in_window[k][1]:
                    if u<u_high and u>= u_low:
                        for j in range(0,len(speaker_dic_string)):
                            if u in speaker_dic_string[j].keys():
                                c = speaker_dic_string[j][u].count(k)
                                speaker_dic_string[j][u] = speaker_dic_string[j][u].replace(k, '0'*len(k))
                                if u>= ex_in_window[k][0]:
                                    sum_er[j] = sum_er[j]+ c
                                    sum_er_token[j] = sum_er_token[j] + c*len(k.split())
        m = m-1

    for k,v in ex_in_window.items():
        if (len(k.split())==1):
            for u in ex_in_window[k][1]:
                if u<u_high and u>= u_low:
                    for j in range(0,len(speaker_dic_string)):
                        if u in speaker_dic_string[j].keys():
                            c = speaker_dic_string[j][u].split().count(k)
                            if u>= ex_in_window[k][0]:
                                sum_er[j] = sum_er[j]+ c
                                sum_er_token[j] = sum_er_token[j]+c

    for c in range(0,len(sum_token)):
        if sum_token[c]!=0:
            er_ratio[c] = sum_er_token[c]/sum_token[c]
        else:
            er_ratio[c] = 0

    total_token_number = 0
    for tn in sum_token:
        total_token_number = total_token_number + tn

    total_er_token_number = 0
    for en in sum_er_token:
        total_er_token_number = total_er_token_number + en

    total_er_number = 0
    for er_n in sum_er:
        total_er_number = total_er_number + er_n

    if total_token_number!=0:
        av_er_ratio = total_er_token_number/total_token_number
    else:
        av_er_ratio = 0

    result_dic = {}
    for s in range(0, len(speaker)):
        result_dic['speaker' + str(s+1)]  = speaker[s]
        result_dic['speaker' + str(s+1) + '_token_number']  = sum_token[s]
        result_dic['speaker' + str(s+1) + '_expression_token_number']  = sum_er_token[s]
        result_dic['speaker' + str(s+1) + '_expression_number']  = sum_er[s]
        result_dic['speaker' + str(s+1) + '_er_ratio'] = er_ratio[s]

    result_dic['total_token_number'] = total_token_number
    result_dic['total_er_token_number'] = total_er_token_number
    result_dic['total_er_number'] = total_er_number
    result_dic['av_er_ratio'] = av_er_ratio

    return result_dic

    # if n==2:
    #     result_dic = {'speaker1': speaker[0], 'speaker1_token_number': sum_token[0], 'speaker1_expression_token_number':sum_er_token[0],
    #                   'speaker1_expression_number':sum_er[0],'speaker1_er_ratio':er_ratio[0],
    #                   'speaker2': speaker[1], 'speaker2_token_number': sum_token[1], 'speaker2_expression_token_number':sum_er_token[1],
    #                   'speaker2_expression_number':sum_er[1],'speaker2_er_ratio':er_ratio[1],
    #                   # 'speaker3': speaker[2], 'speaker3_token_number': sum_token[2], 'speaker3_expression_token_number':sum_er_token[2],
    #                   # 'speaker3_expression_number':sum_er[2],'speaker3_er_ratio':er_ratio[2],
    #                   'total_token_number': total_token_number, 'total_er_token_number' : total_er_token_number, 'av_er_ratio':av_er_ratio,
    #                   'total_er_number': total_er_number}
    #
    # if n==3:
    #     result_dic = {'speaker1': speaker[0], 'speaker1_token_number': sum_token[0], 'speaker1_expression_token_number':sum_er_token[0],
    #                   'speaker1_expression_number':sum_er[0],'speaker1_er_ratio':er_ratio[0],
    #                   'speaker2': speaker[1], 'speaker2_token_number': sum_token[1], 'speaker2_expression_token_number':sum_er_token[1],
    #                   'speaker2_expression_number':sum_er[1],'speaker2_er_ratio':er_ratio[1],
    #                   'speaker3': speaker[2], 'speaker3_token_number': sum_token[2], 'speaker3_expression_token_number':sum_er_token[2],
    #                   'speaker3_expression_number':sum_er[2],'speaker3_er_ratio':er_ratio[2],
    #                   'total_token_number': total_token_number, 'total_er_token_number' : total_er_token_number, 'av_er_ratio':av_er_ratio,
    #                   'total_er_number': total_er_number}
    # if n==4:
    #     result_dic = {'speaker1': speaker[0], 'speaker1_token_number': sum_token[0], 'speaker1_expression_token_number':sum_er_token[0],
    #                   'speaker1_expression_number':sum_er[0],'speaker1_er_ratio':er_ratio[0],
    #                   'speaker2': speaker[1], 'speaker2_token_number': sum_token[1], 'speaker2_expression_token_number':sum_er_token[1],
    #                   'speaker2_expression_number':sum_er[1],'speaker2_er_ratio':er_ratio[1],
    #                   'speaker3': speaker[2], 'speaker3_token_number': sum_token[2], 'speaker3_expression_token_number':sum_er_token[2],
    #                   'speaker3_expression_number':sum_er[2],'speaker3_er_ratio':er_ratio[2],
    #                   'speaker4': speaker[3], 'speaker4_token_number': sum_token[3], 'speaker4_expression_token_number':sum_er_token[3],
    #                   'speaker4_expression_number':sum_er[3],'speaker4_er_ratio':er_ratio[3],
    #                   'total_token_number': total_token_number, 'total_er_token_number' : total_er_token_number, 'av_er_ratio':av_er_ratio,
    #                   'total_er_number': total_er_number}





def number_of_slot_n(speaker_dic,length_u):
    number_of_u = 0
    for s_d in speaker_dic:
        number_of_u = number_of_u + len(s_d)

    number_slot = int(number_of_u - number_of_u%length_u)/length_u
    return int(number_slot)


def get_er_ratio_temporal_n(speaker, speaker_dic, length,exclude_stops):
    slot_number = number_of_slot_n(speaker_dic, length)
    er_dic_list = []
    total_u = 0

    for s in speaker_dic:
        total_u = total_u+len(s)

    for i in range(0,slot_number):
        er_dic = get_er_ratio_in_time_n(speaker,speaker_dic, length*i, length*(i+1),exclude_stops)
        er_dic['begin'] = length*i
        er_dic['end'] = length*(i+1)
        er_dic_list.append(er_dic)

    er_dic_end = get_er_ratio_in_time_n(speaker, speaker_dic, slot_number*length, total_u,exclude_stops)
    er_dic_end['begin'] = slot_number*length
    er_dic_end['end'] = total_u
    er_dic_list.append(er_dic_end)

    return er_dic_list

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
dl_err_global = [[]for i in range(0,12)]
dl_lexicon_sum = [[]for j in range(0,12)]

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
            # er_dic = get_er_dic_group(speakers,dialogues_dic, para_exclude_stops)
            utt_number = number_of_total_u(dialogues_dic)
            # ex_for_each_file = []
            #
            # for ex, value in er_dic.items():
            #     ex_for_each_file.append({'Expression':ex, 'Expression_length': len(ex.split()), 'Expression_established_position':value[0], 'Expression_uttered_position_speaker':value[1],'file':f})
            #
            # dl_lexicon_sum[sp_num-2].append({'Expression Lexicon Size': len(er_dic),'file':f})
            #
            # err_global = get_er_ratio_in_time_n(speakers,dialogues_dic,er_dic,0,utt_number)
            # err_global['file'] = f
            # dl_err_global[sp_num-2].append(err_global)
            err_temporal_local = get_er_ratio_temporal_n(speakers,dialogues_dic,int(window_length),para_exclude_stops)

            for fx in err_temporal_local:
                fx['file'] = f

            dl_s = pd.DataFrame(err_temporal_local)
            dl_s.to_csv(os.path.join(path2,f[len(f)-8:len(f)-4] + '_local_err.csv'), index = False)

            # dl_ex_for_each_file = pd.DataFrame(ex_for_each_file)
            # dl_ex_for_each_file.to_csv(os.path.join(path2,f[len(f)-8:len(f)-4] + '_lexicon.csv'), index = False)


# for i in range(0,len(dl_err_global)):
#     if dl_err_global[i]!=[]:
#         dl_err_sum_pd = pd.DataFrame(dl_err_global[i])
#         dl_err_sum_pd.to_csv(os.path.join(output_path,'global_err_summary' + str(i+2)+ '_speakers.csv'), index = False)
#         # dl_err_sum_pd.to_csv(os.path.join(output_path + "/group_size_" + str(i+2),'summary_err_global_' + str(i+2)+ '_speakers.csv'), index = False)
#
#
# for j in range(0,len(dl_lexicon_sum)):
#     if dl_lexicon_sum[j]!=[]:
#         dl_lexicon_sum_pd = pd.DataFrame(dl_lexicon_sum[j])
#         dl_lexicon_sum_pd.to_csv(os.path.join(output_path,'balanced_els_summary' + str(j+2)+ '_speakers.csv'), index = False)
#         # dl_lexicon_sum_pd.to_csv(os.path.join(output_path + "/group_size_" + str(j+2),'summary_els_' + str(j+2)+ '_speakers.csv'), index = False)
#         #



    # print(speakers)
    # # print(er_dic)
    # print(len(er_dic))
    # print(utt_number)
    # print(err_global)
    # for x in err_temporal:
    #     print(x['av_er_ratio'])


