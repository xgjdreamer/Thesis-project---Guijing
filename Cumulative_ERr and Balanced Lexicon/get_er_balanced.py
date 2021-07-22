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

def get_er_dic(speaker1_dialogue, speaker2_dialogue):
    expressions = {}

    for x,value_x in speaker1_dialogue.items():
        for y,value_y in speaker2_dialogue.items():
            string = get_er_one_with_u(value_x,value_y, False)

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


def get_er_dic_group(speaker, speaker_dic):
    n = len(speaker)
    expression_n = []
    fit_ex_in_dic = [[]*n]
    sum_dic = {}

    for i in range(0,n-1):
        for j in range(i+1, n):
            ex = get_er_dic(speaker_dic[i],speaker_dic[j])
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