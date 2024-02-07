﻿# quot.py
#    
# Locate the Scripture in OT quoted from an NT verse
#
# Copyright (c) 2022-2024 WordTM Project 
# Author: Johnny Cheng <drjohnnycheng@gmail.com>
#
# Updated: 28 January 2024
#
# URL: https://github.com/drjohnnycheng/wordtm.git
# For license information, see LICENSE.TXT

import warnings
warnings.filterwarnings("ignore")

import re
import jieba

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from wordtm import util

# List of Chinese stopwords
chinese_stopwords = ["、","。","〈","〉","《","》","一","一些","一何","一切","一則","一方面","一旦","一來","一樣","一般","一轉眼","七","萬一","三","上","上下","下","不","不僅","不但","不光","不單","不只","不外乎","不如","不妨","不盡","不儘然","不得","不怕","不惟","不成","不拘","不料","不是","不比","不然","不特","不獨","不管","不至於","不若","不論","不過","不問","與","與其","與其說","與否","與此同時","且","且不說","且說","兩者","個","個別","中","臨","為","為了","為什麼","為何","為止","為此","為著","乃","乃至","乃至於","麼","之","之一","之所以","之類","烏乎","乎","乘","九","也","也好","也罷","了","二","二來","於","於是","於是乎","云云","雲爾","五","些","亦","人","人們","人家","什","什麼","什麼樣","今","介於","仍","仍舊","從","從此","從而","他","他人","他們","他們們","以","以上","以為","以便","以免","以及","以故","以期","以來","以至","以至於","以致","們","任","任何","任憑","會","似的","但","但凡","但是","何","何以","何況","何處","何時","餘外","作為","你","你們","使","使得","例如","依","依據","依照","便於","俺","俺們","倘","倘使","倘或","倘然","倘若","借","借儻然","假使","假如","假若","做","像","兒","先不先","光是","全體","全部","八","六","兮","共","關於","關於具體地說","其","其一","其中","其二","其他","其餘","其它","其次","具體地說","具體說來","兼之","內","再","再其次","再則","再有","再者","再者說","再說","冒","沖","況且","幾","幾時","凡","凡是","憑","憑藉","出於","出來","分","分別","則","則甚","別","別人","別處","別是","別的","別管","別說","到","前後","前此","前者","加之","加以","即","即令","即使","即便","即如","即或","即若","卻","去","又","又及","及","及其","及至","反之","反而","反過來","反過來說","受到","另","另一方面","另外","另悉","只","只當","只怕","只是","只有","只消","只要","只限","叫","叮咚","可","可以","可是","可見","各","各個","各位","各種","各自","同","同時","後","後者","向","向使","向著","嚇","嗎","否則","吧","吧噠","含","吱","呀","呃","嘔","唄","嗚","嗚呼","呢","呵","呵呵","呸","呼哧","咋","和","咚","咦","咧","咱","咱們","咳","哇","哈","哈哈","哉","哎","哎呀","哎喲","嘩","喲","哦","哩","哪","哪個","哪些","哪兒","哪天","哪年","哪怕","哪樣","哪邊","哪裡","哼","哼唷","唉","唯有","啊","啐","啥","啦","啪達","啷當","喂","喏","喔唷","嘍","嗡","嗡嗡","呵","嗯","噯","嘎","嘎登","噓","嘛","嘻","嘿","嘿嘿","四","因","因為","因了","因此","因著","因而","固然","在","在下","在於","地","基於","處在","多","多麼","多少","大","大家","她","她們","好","如","如上","如上所述","如下","如何","如其","如同","如是","如果","如此","如若","始而","孰料","孰知","甯","寧可","寧願","寧肯","它","它們","對","對於","對待","對方","對比","將","小","爾","爾後","爾爾","尚且","就","就是","就是了","就是說","就算","就要","盡","儘管","儘管如此","豈但","己","已","已矣","巴","巴巴","年","並","並且","庶乎","庶幾","開外","開始","歸","歸齊","當","當地","當然","當著","彼","彼時","彼此","往","待","很","得","得了","怎","怎麼","怎麼辦","怎麼樣","怎奈","怎樣","總之","總的來看","總的來說","總的說來","總而言之","恰恰相反","您","惟其","慢說","我","我們","或","或則","或是","或曰","或者","截至","所","所以","所在","所幸","所有","才","才能","打","打從","把","抑或","拿","按","按照","換句話說","換言之","據","據此","接著","故","故此","故而","旁人","無","無寧","無論","既","既往","既是","既然","日","時","時候","是","是以","是的","更","曾","替","替代","最","月","有","有些","有關","有及","有時","有的","望","朝","朝著","本","本人","本地","本著","本身","來","來著","來自","來說","極了","果然","果真","某","某個","某些","某某","根據","歟","正值","正如","正巧","正是","此","此地","此處","此外","此時","此次","此間","毋寧","每","每當","比","比及","比如","比方","沒奈何","沿","沿著","漫說","焉","然則","然後","然而","照","照著","猶且","猶自","甚且","甚麼","甚或","甚而","甚至","甚至於","用","用來","由","由於","由是","由此","由此可見","的","的確","的話","直到","相對而言","省得","看","眨眼","著","著呢","矣","矣乎","矣哉","離","秒","竟而","第","等","等到","等等","簡言之","管","類如","緊接著","縱","縱令","縱使","縱然","經","經過","結果","給","繼之","繼後","繼而","綜上所述","罷了","者","而","而且","而況","而後","而外","而已","而是","而言","能","能否","騰","自","自個兒","自從","自各兒","自後","自家","自己","自打","自身","至","至於","至今","至若","致","般的","若","若夫","若是","若果","若非","莫不然","莫如","莫若","雖","雖則","雖然","雖說","被","要","要不","要不是","要不然","要麼","要是","譬喻","譬如","讓","許多","論","設使","設或","設若","誠如","誠然","該","說","說來","請","諸","諸位","諸如","誰","誰人","誰料","誰知","賊死","賴以","趕","起","起見","趁","趁著","越是","距","跟","較","較之","邊","過","還","還是","還有","還要","這","這一來","這個","這麼","這麼些","這麼樣","這麼點兒","這些","這會兒","這兒","這就是說","這時","這樣","這次","這般","這邊","這裡","進而","連","連同","逐步","通過","遵循","遵照","那","那個","那麼","那麼些","那麼樣","那些","那會兒","那兒","那時","那樣","那般","那邊","那裡","都","鄙人","鑒於","針對","阿","除","除了","除外","除開","除此之外","除非","隨","隨後","隨時","隨著","難道說","零","非","非但","非徒","非特","非獨","靠","順","順著","首先","︿","！","＃","＄","％","＆","（","）","＊","＋","，","０","１","２","３","４","５","６","７","８","９","：","；","＜","＞","？","＠","［","］","｛","｜","｝","～","￥"]


def extract_quotation(text, quot_marks):
    """Returns the text within a pair of quotation marks.

    :param text: The target text to be extracted, default to None
    :type text: str
    :param quot_marks: A pair of quotation marks, ['"', '"'] for English text
        or ['『', '』'] for Chinese text, default to None
    :type quot_marks: list
    :return: The text within a pair of quotation marks, if any, otherwise,
        an empty string
    :rtype: str
    """

    arr = text.split(quot_marks[0])
    if len(arr) > 1:
        return arr[1].split(quot_marks[1])[0]
    else:
        return ""


def tokenize(sentence):
    """Returns a list of tokens from a Chinese sentence.

    :param sentence: The target text to be tokenized, default to None
    :type sentence: str
    :return: The generator object that storing the list of tokens
        extracted from the sentence
    :rtype: generator
    """

    without_duplicates = re.sub(r'(.)\1+', r'\1\1', sentence)
    without_punctuation = re.sub(r'[^\w]','', without_duplicates)
    # return jieba.lcut(without_duplicates)
    return jieba.cut(without_duplicates)

	
def match_text(target, sent_tokens, lang, threshold, n=5):
    """Returns a list of tuples of the cosine smilarity measure of the OT verse
    with target verse and the index of that OT verse in the DataFrame storing
    the prescribed OT Scripture.

    :param target: The target verse to be matched, default to None
    :type target: str
    :param sent_tokens: The target verse to be matched, default to None
    :type sent_tokens: str
    :param lang: If the value is 'chi' , the processed language is assumed to be
        Chinese, otherwise, it is English, default to None
    :type lang: str
    :param threshold: The threshold value of the cosine similarity measure
        between the target verse and an OT verse, where the cosine similarity measure
        of a matched OT verse and the target verse should be greater this value,
        default to None
    :type threshold: float
    :param n: The upper bound of the number of matched verses, default to 5
    :type n: int, optional
    :return: The list of tuples of the cosine smilarity measure and the index
        of the OT verse
    :rtype: list
    """

    result = ''
    sent_tokens.append(target)
    if lang == 'chi':
        TfidfVec = TfidfVectorizer(tokenizer=tokenize, stop_words=chinese_stopwords)
    else:
        TfidfVec = TfidfVectorizer(analyzer='word', stop_words='english')

    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)

    results = []
    for i in range(n):
        idx = vals.argsort()[0][-2-i]
        flat = vals.flatten()
        flat.sort()
        cos_sim = flat[-2-i]
        if (cos_sim > threshold):
            results.append((cos_sim, idx))

    return results


def match_verse(i, ot_list, otdf, df, book, chap, verse, lang, threshold):
    """Returns whether the target NT verse (book, chap, verse) can match a particular verse
    in the list of OT verses (ot_list), and prints the matched OT versed.

    :param i: The number of matched verses so far, default to None
    :type i: int
    :param ot_list: The list of OT verses (str) to be matched, default to None
    :type ot_list: list
    :param otdf: The DataFrame storing the prescribed OT verses to be matched,
        default to None
    :type otdf: pandas.DataFrame
    :param df: The DataFrame storing the collection of the target NT verses
        to be matched, default to None
    :type df: pandas.DataFrame
    :param book: The Bible book short name (3 characters) of the target NT verse
        to be matched, default to None
    :type book: str
    :param chap: The chapter number of the target NT verse to be matched,
        default to None
    :type chap: int
    :param verse: The verse number of the target NT verse to be matched,
        default to None
    :type verse: int
    :param lang: If the value is 'chi' , the processed language is assumed to be Chinese
        otherwise, it is English, default to None
    :type lang: str
    :param threshold: The threshold value of the cosine similarity measure
        between the target verse and an OT verse, where that measure for successful match
        should be greater this value, default to None
    :type threshold: float
    :return: True if the target verse matched an OT verse, False otherwise
    :rtype: bool
    """

    book_cat = util.load_word('book_categories.csv')

    if lang == 'en':
        book_sname = book
        quot_marks = ['"', '"']
    else:
        book_sname = book_cat[book_cat.book_s == book].book_chi.iloc[0]
        quot_marks=['『', '』']

    averse = util.extract(df, book=book, chapter=chap, verse=verse)
    vtext = util.get_text(averse)

    quot = extract_quotation(vtext, quot_marks)
    if quot == "": return False

    nt_str = book_sname + ' ' + str(chap) + ':' + str(verse)
    print("(%2d) %-6s %s" %(i+1, nt_str, vtext))  # NT Verse

    results = match_text(quot, ot_list, lang, threshold)
    ot_list.remove(quot)

    for cos_sim, idx in results:
        sv = otdf.iloc[idx]

        if lang == 'en':
            book_sname = book
        else:
            book_sname = book_cat[book_cat.book_s == sv.book].book_chi.iloc[0]

        ot_str = book_sname + ' ' + str(sv.chapter) + ':' + str(sv.verse)
        print("     -> %.4f %-9s %s" %(cos_sim, ot_str, sv.text))  # OT Verse

    return True


def show_quot(target, source='ot', lang='en', threshold=0.5):
    """Shows a collection of matched OT verses, if any, based on the prescribed
    collection of target NT verse and the threshold value.

    :param target: The collection of target NT verses to be matched, default to None
    :type target: pandas.DataFrame
    :param source: The string representing the collection of all or subset of OT verses
        to be matched, default to 'ot'
    :type source: str, optional
    :param lang: If the value is 'en', the processed language is assumed to be English
        otherwise, it is Chinese, default to 'en
    :type lang: str, optional
    :param threshold: The threshold value of the cosine similarity measure
        between the target verse and an OT verse, where that measure for successful match
        should be greater this value, default to 0.5
    :type threshold: str, optional
    :return: The list of tuples of the cosine smilarity measure and the index
        of the OT verse
    :rtype: list
    """

    util.set_lang(lang)
    ot_cat = ['tor', 'oth', 'ket', 'map', 'mip']

    if lang == 'en':
        df = util.load_word()
    else:
        df = util.load_word('cuv.csv')
        # df.text = df.text.apply(lambda x: x.replace('\u3000', ''))

    if source in ot_cat:
        otdf = util.extract(df, category=source)
    else:
        otdf = util.extract(df, testament=0)

    ot_list = util.get_text_list(otdf)

    i = 0
    for _, row in target.iterrows():
        if match_verse(i, ot_list, otdf, target, row.book, row.chapter, row.verse, lang, threshold):
            i += 1
