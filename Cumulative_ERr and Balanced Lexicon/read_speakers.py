def extract_speakers_n(df1):
    dataC = df1
    speaker = [dataC[0][0]]

    for row in range(0,len(dataC)):
        if dataC[0].iloc[row] not in speaker:
            speaker.append(dataC[0].iloc[row])

    return speaker