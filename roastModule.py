import xlrd
# from paddlenlp.embeddings import TokenEmbedding
import paddlehub as hub
import numpy as np

concernKey1 = ['n', 'nr', 'nz', 'PER', 'ns', 'LOC', 's', 'nt', 'ORG', 'nw']
concernKey2 = ['v']
lac = hub.Module(name="lac")


# test_text = "还记得你之前跟我说，我能及格猪都能上树。可教练我拿到驾照了，猪不仅能上树还能上高速，我再给你来个倒车入库，压线了难受不？以前我不敢顶撞你，现在顶撞你可抗不住。今天是个好日子"


def filt(tagList, wordList):
    nn = []
    vv = []
    for tag, word in zip(tagList, wordList):
        if tag in concernKey1:
            nn.append(word)
        elif tag in concernKey2:
            vv.append(word)
    return nn, vv


def keyOutput(test_text):
    nWord = []
    vWord = []
    result = lac.cut(text=[test_text], use_gpu=False, batch_size=1, return_tag=True)[0]
    # print('results',results)
    # print('result',result)
    tagList = result['tag']
    wordList = result['word']
    nn, vv = filt(tagList, wordList)
    # print(nn,'===',vv)
    nWord = nn
    vWord = vv
    return nWord, vWord


# nnVector,vvVector=keyOutput(test_text)
# print('nnVector,',nnVector)
##
def read_excel_data(fpath):
    ExcelFile = xlrd.open_workbook(fpath)
    num = 1
    personList = []
    sentenceList = []
    classList = []
    nWordList = []
    vWordList = []
    try:
        sheet = ExcelFile.sheet_by_name('Sheet' + str(num))
        num += 1
    except:
        pass
    #     #获取整行或者整列的值
    #    #rows=sheet.row_values(2)#第三行内容
    personList.extend(sheet.col_values(0)[1:])
    sentenceList.extend(sheet.col_values(1)[1:])
    classList.extend(sheet.col_values(2)[1:])
    for sent in sentenceList:
        nWord, vWord = keyOutput(sent)
        nWordList.append(nWord)
        vWordList.append(vWord)
    return personList, sentenceList, classList, nWordList, vWordList


class WordVector():
    def __init__(self, sim_thershold=0.8, fpath='resource/roast1.xls'):
        # self.wordemb = hub.Module(name='w2v_weibo_target_word-word_dim300')
        self.wordemb = None
        if self.wordemb is not None:

            self.personList, self.sentenceList, _, self.nWordList, self.vWordList = read_excel_data(fpath)
            print('self.nWordList', len(self.nWordList))



            self.sim_thershold = sim_thershold
            self.UNK = self.wordemb.get_idx_from_word('UNK')

            self.nWordIndexList = self.wordList2indexList(self.nWordList)
            self.vWordIndexList = self.wordList2indexList(self.vWordList)
            print('nWordIndexList', len(self.nWordIndexList), self.nWordIndexList[:5], self.nWordList[:5])
            print('self.vWordIndexList', len(self.vWordIndexList), self.vWordIndexList[:5], self.vWordList[:5])

    def index_cosine_sim(self, xIndex, yIndex):
        x = self.wordemb.search(xIndex)
        y = self.wordemb.search(yIndex)
        return self.cosine_sim(x, y)

    def cosine_sim(self, x, y):

        chushu = (np.sqrt(np.dot(x, x.T)) * np.sqrt(np.dot(y, y.T)))
        if chushu == 0:
            sim = 0
        else:
            sim = np.dot(x, y.T) / chushu
            sim = sim[0, 0]
        # print('sim',sim)
        # sim=self.wordemb.cosine_sim(x, y)
        return sim

    def get_vector(self, query):
        #
        if self.wordemb.get_idx_from_word(query) == self.UNK:
            # not in vector dict use char vector
            queryVector = self.wordemb.search(query[0])
            if len(query) > 1:
                for index in range(1, len(query)):
                    queryVector += self.wordemb.search(query[0])
        else:
            queryVector = self.wordemb.search(query)
        return queryVector

    def wordList2indexList(self, wordList):
        indexList = []
        for words in wordList:
            indexs = []
            for word in words:
                indexs.append(self.word2index(word))
            indexList.append(indexs)
            ##双层list
        return indexList

    def word2index(self, word):
        wordIndex = []
        if self.wordemb.get_idx_from_word(word) == self.UNK:
            # not in vector dict use char vector

            for index in range(0, len(word)):
                wordIndex.append(self.wordemb.get_idx_from_word(word[index]))
        else:
            wordIndex.append(self.wordemb.get_idx_from_word(word))
        return wordIndex

    def index2vector(self, aIndexs):
        # 所有lac后单词组合的wordvec

        vectorList = []
        for ai in aIndexs:
            vectorList.append(self.wordemb.search(ai))
        return vectorList

    def indexList2vectorList(self, indexsList):
        vectorsList = []
        for indexs in indexsList:
            vectorsList.append(self.index2vector(indexs))
        return vectorsList

    def cosine_sim_lac(self, vectorList1, vectorList2):

        combineVector1 = np.sum(np.array(vectorList1), 0)
        combineVector2 = np.sum(np.array(vectorList2), 0)

        return self.cosine_sim(combineVector1, combineVector2)

    def vectorList2sentenceVector(self, sVectorList):
        wordVectorList = []
        for vl in sVectorList:  # vl 每个word的 vector list
            # print(type(vl))
            # print(vl)
            wordVectorList.append(np.sum(np.array(vl), 0))
        return np.sum(np.array(wordVectorList), 0)

    def cosine_sim_sentence(self, sVectorList, qVectorList):
        storeVector = self.vectorList2sentenceVector(sVectorList)
        queryVector = self.vectorList2sentenceVector(qVectorList)
        return self.cosine_sim(storeVector, queryVector)

    def cal_simList(self, queryIndexList, storeIndexList):
        simList = []
        sentenceSimList = []
        charSimList = []
        # query中每个key word的indexlist，n个key word或char组成wordIndexList

        for sIndexList in storeIndexList:  # sIndexList-》每一句吐槽= [[],[]]
            simValue = 0
            sVectorList = self.indexList2vectorList(sIndexList)
            qVectorList = self.indexList2vectorList(queryIndexList)
            # print('sVectorList', len(sVectorList[0]), 'qVectorList', len(qVectorList[0]))
            sentenceSimValue = self.cosine_sim_sentence(sVectorList, qVectorList)
            # print('sentenceSimValue', sentenceSimValue)
            if sentenceSimValue < self.sim_thershold:
                for qvs in qVectorList:  # 每一个word的vector list
                    for svs in sVectorList:  # 每一句吐槽中的每个字的vector list

                        # 先计算
                        temp = self.cosine_sim_lac(qvs, svs)
                        if temp > simValue:
                            simValue = temp

            #
            sentenceSimList.append(sentenceSimValue)
            charSimList.append(simValue)
        # print('simList',len(charSimList))
        return sentenceSimList, charSimList

    def query2index(self, query):
        queryIndexList = []
        for word in query:
            queryIndexList.append(self.word2index(word))
        return queryIndexList

    def simSentenceIndex(self, qnWord, qvWord, vWordMatch=False):
        if self.wordemb is None: return ''
        index = -1
        qnIndexList = []
        qnIndexList = self.query2index(qnWord)
        # print('qnIndex',qnIndexList)
        nSenSimList, nCharSimList = self.cal_simList(qnIndexList, self.nWordIndexList)
        if max(nSenSimList) >= self.sim_thershold:  # caculate n word combine sentence
            index = nSenSimList.index(max(nSenSimList))
        elif max(nCharSimList) >= self.sim_thershold:  # caculate n word
            index = nCharSimList.index(max(nCharSimList))
        else:
            if vWordMatch:
                ##caculate the v word
                vnIndexList = self.query2index(qvWord)
                vSenSimList, vCharSimList = self.cal_simList(vnIndexList, self.vWordIndexList)
                if max(vSenSimList) >= self.sim_thershold:
                    index = vSenSimList.index(max(vSenSimList))

                elif max(vCharSimList) >= self.sim_thershold:
                    index = vCharSimList.index(max(vCharSimList))
        return index

    def simSentence(self, query):
        try:
            qnWord, qvWord = keyOutput(query)
            # try:
            index = self.simSentenceIndex(qnWord, qvWord)
            if index >= 0:
                return self.sentenceList[index]
        except:
            pass
        return ''
        # except Exception as e:
        #     print(e)
        #     return ''


wv = WordVector()
ans = wv.simSentence('娘娘腔，不会唱歌不会跳舞')
print(ans)