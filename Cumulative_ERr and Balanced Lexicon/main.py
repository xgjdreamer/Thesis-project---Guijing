from read_speakers import extract_speakers_n
from read_dialogues import extract_dialogues_dic_n
from get_er_balanced import get_er_dic_group
from get_temporal_err import get_er_ratio_in_time_n, get_er_ratio_temporal_n
from utt_count import number_of_total_u

import pandas as pd
import os, glob





import os

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径


path_sum = ["output_files/group_size_2","output_files/group_size_3","output_files/group_size_4"]
for p in path_sum:
    mkdir(p)

files = glob.glob('S***.tsv')
dl_err_global = [[]for i in range(0,3)]
dl_lexicon_sum = [[]for j in range(0,3)]

for f in files:

    df = pd.read_csv(f, sep=r'\t', header=None)
    speakers = extract_speakers_n(df)

    for sp_num in range(2,5):

        if len(speakers) == sp_num:
            dialogues_dic = extract_dialogues_dic_n(df,speakers)
            er_dic  = get_er_dic_group(speakers,dialogues_dic)
            utt_number = number_of_total_u(dialogues_dic)
            ex_for_each_file = []

            for ex, value in er_dic.items():
                ex_for_each_file.append({'Expression':ex, 'Expression_length': len(ex.split()), 'Expression_established_position':value[0], 'Expression_uttered_position_speaker':value[1],'file':f})

            dl_lexicon_sum[sp_num-2].append({'Expression Lexicon Size': len(er_dic),'file':f})

            err_global = get_er_ratio_in_time_n(speakers,dialogues_dic,er_dic,0,utt_number)
            err_global['file'] = f
            dl_err_global[sp_num-2].append(err_global)
            err_temporal = get_er_ratio_temporal_n(speakers,dialogues_dic,er_dic,50)

            for fx in err_temporal:
                fx['file'] = f

            dl_s = pd.DataFrame(err_temporal)
            dl_s.to_csv(os.path.join(path_sum[sp_num-2],f[0:4] + '_cumulative_err.csv'), index = False)

            dl_ex_for_each_file = pd.DataFrame(ex_for_each_file)
            dl_ex_for_each_file.to_csv(os.path.join(path_sum[sp_num-2],f[0:4] + '_lexicon.csv'), index = False)

i = 0
for dl_err_sum in dl_err_global:
    dl_err_sum_pd = pd.DataFrame(dl_err_sum)
    dl_err_sum_pd.to_csv(os.path.join(path_sum[i],'err_global_' + str(i+2)+ '_speakers.csv'), index = False)
    i = i+1

j = 0
for dl_lexicon in dl_lexicon_sum:
    dl_lexicon_sum_pd = pd.DataFrame(dl_lexicon)
    dl_lexicon_sum_pd.to_csv(os.path.join(path_sum[j],'els_' + str(j+2)+ '_speakers.csv'), index = False)
    j = j+1



    # print(speakers)
    # # print(er_dic)
    # print(len(er_dic))
    # print(utt_number)
    # print(err_global)
    # for x in err_temporal:
    #     print(x['av_er_ratio'])


