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