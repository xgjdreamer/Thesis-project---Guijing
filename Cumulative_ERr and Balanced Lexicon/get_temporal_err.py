def get_er_window_n(speaker_dic, ex_group, u_high):
    ex_in_window = {}
    for k,v in ex_group.items():
        if v[0] <= u_high:
            ex_in_window[k] = v


    return ex_in_window

def get_er_ratio_in_time_n(speaker, speaker_dic, ex_group, u_low, u_high):
    ex_in_window = get_er_window_n(speaker_dic, ex_group, u_high)
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

    if n==2:
        result_dic = {'speaker1': speaker[0], 'speaker1_token_number': sum_token[0], 'speaker1_expression_token_number':sum_er_token[0],
                      'speaker1_expression_number':sum_er[0],'speaker1_er_ratio':er_ratio[0],
                      'speaker2': speaker[1], 'speaker2_token_number': sum_token[1], 'speaker2_expression_token_number':sum_er_token[1],
                      'speaker2_expression_number':sum_er[1],'speaker2_er_ratio':er_ratio[1],
                      # 'speaker3': speaker[2], 'speaker3_token_number': sum_token[2], 'speaker3_expression_token_number':sum_er_token[2],
                      # 'speaker3_expression_number':sum_er[2],'speaker3_er_ratio':er_ratio[2],
                      'total_token_number': total_token_number, 'total_er_token_number' : total_er_token_number, 'av_er_ratio':av_er_ratio,
                      'total_er_number': total_er_number}

    if n==3:
        result_dic = {'speaker1': speaker[0], 'speaker1_token_number': sum_token[0], 'speaker1_expression_token_number':sum_er_token[0],
                      'speaker1_expression_number':sum_er[0],'speaker1_er_ratio':er_ratio[0],
                      'speaker2': speaker[1], 'speaker2_token_number': sum_token[1], 'speaker2_expression_token_number':sum_er_token[1],
                      'speaker2_expression_number':sum_er[1],'speaker2_er_ratio':er_ratio[1],
                      'speaker3': speaker[2], 'speaker3_token_number': sum_token[2], 'speaker3_expression_token_number':sum_er_token[2],
                      'speaker3_expression_number':sum_er[2],'speaker3_er_ratio':er_ratio[2],
                      'total_token_number': total_token_number, 'total_er_token_number' : total_er_token_number, 'av_er_ratio':av_er_ratio,
                      'total_er_number': total_er_number}
    if n==4:
        result_dic = {'speaker1': speaker[0], 'speaker1_token_number': sum_token[0], 'speaker1_expression_token_number':sum_er_token[0],
                      'speaker1_expression_number':sum_er[0],'speaker1_er_ratio':er_ratio[0],
                      'speaker2': speaker[1], 'speaker2_token_number': sum_token[1], 'speaker2_expression_token_number':sum_er_token[1],
                      'speaker2_expression_number':sum_er[1],'speaker2_er_ratio':er_ratio[1],
                      'speaker3': speaker[2], 'speaker3_token_number': sum_token[2], 'speaker3_expression_token_number':sum_er_token[2],
                      'speaker3_expression_number':sum_er[2],'speaker3_er_ratio':er_ratio[2],
                      'speaker4': speaker[3], 'speaker4_token_number': sum_token[3], 'speaker4_expression_token_number':sum_er_token[3],
                      'speaker4_expression_number':sum_er[3],'speaker4_er_ratio':er_ratio[3],
                      'total_token_number': total_token_number, 'total_er_token_number' : total_er_token_number, 'av_er_ratio':av_er_ratio,
                      'total_er_number': total_er_number}


    return result_dic


def number_of_slot_n(speaker_dic,length_u):
    number_of_u = 0
    for s_d in speaker_dic:
        number_of_u = number_of_u + len(s_d)

    number_slot = int(number_of_u - number_of_u%length_u)/length_u
    return int(number_slot)


def get_er_ratio_temporal_n(speaker, speaker_dic, ex_group, length):
    slot_number = number_of_slot_n(speaker_dic, length)
    er_dic_list = []
    total_u = 0

    for s in speaker_dic:
        total_u = total_u+len(s)

    for i in range(0,slot_number):
        er_dic = get_er_ratio_in_time_n(speaker,speaker_dic, ex_group , length*i, length*(i+1))
        er_dic['begin'] = length*i
        er_dic['end'] = length*(i+1)
        er_dic_list.append(er_dic)

    er_dic_end = get_er_ratio_in_time_n(speaker, speaker_dic, ex_group , slot_number*length, total_u)
    er_dic_end['begin'] = slot_number*length
    er_dic_end['end'] = total_u
    er_dic_list.append(er_dic_end)

    return er_dic_list



