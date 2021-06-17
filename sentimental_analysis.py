import pandas as pd
from konlpy.tag import Kkma
kkma = Kkma()

topic1_data = list(pd.read_csv('/Users/boralim/Desktop/capstone/topic(0)_review.csv', encoding='utf-8').description)
topic2_data = list(pd.read_csv('/Users/boralim/Desktop/capstone/topic(1)_review.csv', encoding='utf-8').description)
topic3_data = list(pd.read_csv('/Users/boralim/Desktop/capstone/topic(2)_review.csv', encoding='utf-8').description)
topic4_data = list(pd.read_csv('/Users/boralim/Desktop/capstone/topic(3)_review.csv', encoding='utf-8').description)
topic5_data = list(pd.read_csv('/Users/boralim/Desktop/capstone/topic(4)_review.csv', encoding='utf-8').description)
topic6_data = list(pd.read_csv('/Users/boralim/Desktop/capstone/topic(5)_review.csv', encoding='utf-8').description)
rawdata = list(pd.read_csv('/Users/boralim/Desktop/capstone/crawling_naver_iphone.csv', encoding='utf-8').description)

print("number of sentence of topic 1: ", len(topic1_data))
print("number of sentence of topic 2: ", len(topic2_data))
print("number of sentence of topic 3: ", len(topic3_data))
print("number of sentence of topic 4: ", len(topic4_data))
print("number of sentence of topic 5: ", len(topic5_data))
print("number of sentence of topic 6: ", len(topic6_data))
print("number of sentence of topic 6: ", len(rawdata))

#감성사전 불러오기
#우선 KOSAC(Korean Sentiment Analysis Corpus) 코드로 감성 분석 해본다.
f = open("lexicon/polarity.csv", encoding="utf-8")
for line in f.read().split("\n")[:10]:
    line = line.strip().split(",")
    #print(line)
f.close()

#KOSAC 감성사전을 딕셔너리에 저장
sentiment = {}
f = open("lexicon/polarity.csv", encoding="utf-8")
for line in f:
    col = line.strip().split(",")
    pos = col[0]
    polarity = col[7]
    score = col[8]
    # 극성이 POS인 경우 +, NEG인 경우 -를 곱해 스코어(score)를 계산합니다.
    if polarity == "POS":
        score = float(score)
    elif polarity == "NEG":
        score = -float(score)
    else:
        # 긍정 또는 부정인 경우만 취급합니다.
        continue
    # 세미콜론(;)을 띄어쓰기로 바꿔 딕셔너리에 스코어와 함께 저장합니다.
    sentiment[pos.replace(";", " ")] = score
f.close()

#문장을 형태소 단위로 분리하기 샘플
#print(kkma.pos(topic1_data[10]))

def sentimental_analysis(data_ls):
    # 형태소 분석
    tag_data = []

    now = 0
    for desc in data_ls:
        now += 1
        print(now, end="\r")  # 오.. 진행상황을 카운트다운처럼 프린트로 찍어주는 코드!
        tag_list = kkma.pos(desc)
        tag_desc = []
        for word, pos in tag_list:
            tag_desc.append(word + "/" + pos)
        tag_data.append(tag_desc)

    # 감성분석 결과를 긍정과 부정 리뷰로 각각 저장할 리스트를 생성합니다.
    positive_sentence = []
    negative_sentence = []

    for tag_sentence, review in zip(tag_data, data_ls):
        # 스코어를 0점으로 초기화합니다.
        score = 0.0
        # 형태소분석된 문장 안에서 최대 7개까지 결합된 형태소가 감성사전 안에 있는지 확인합니다.
        for i in range(len(tag_sentence)):
            max_n = 7
            for n in range(1,max_n+1):
                # ngram = ""
                # ngrams = []
                for j in range(len(tag_sentence) - n):
                    # j  ngram starting position
                    # I am a boy.
                    ngram = (" ".join(tag_sentence[j:j+n])).strip()
                    # ngrams.append((" ".join(tag_sentence[j:j+n])).strip())

                    ngram = ngram.strip()
                    if ngram in sentiment.keys():
                        score += sentiment[ngram]
        # 감성스코어로 긍정 또는 부정을 판단하기위한 임계값을 지정합니다.
        limit = 0
        if score > limit:
            positive_sentence.append(["POSITIVE", str(review)])
        elif score < -limit:
            negative_sentence.append(["NEGATIVE", str(review)])

    # 감성분석 결과를 감성스코어를 기준으로 정렬합니다.
    positive_sentence.sort(reverse=True)
    negative_sentence.sort()

    print("긍정판별 문장 개수 :", len(positive_sentence))
    positive_sentence[:10]
    print("부정판별 문장 개수 :", len(negative_sentence))
    negative_sentence[:10]
    print("\r")

print(" ")
print("---감성분석 실시---")
print(" ")

"""
i=1
for data_ls in [topic1_data, topic2_data, topic3_data, topic4_data, topic5_data, topic6_data]:
    print(i, "번째 토픽 감성분석 결과: ")
    sentimental_analysis(data_ls)
    i=i+1
"""
sentimental_analysis(rawdata)