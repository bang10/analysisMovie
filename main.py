import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
import reviewDto

excelWriter = pd.ExcelWriter('final_test_BANGSEONGHWAN.xlsx', engine='openpyxl')

def isBoxOffice(visitor) :
    if visitor == 0:
        return 'Nan'

    return True if visitor > 500000 else False

# 이상한 것도 같이 크롤링 되는 것 방지
def chageDataOnlyNumber(param):
    if param.isdigit():  # 숫자로만 이루어진 경우
        return int(param)
    else:
        # 숫자와 쉼표로 이루어진 경우
        if ',' in param.replace('.', '') and all(char.isdigit() or char == ',' for char in param):
            return param
        # 숫자와 공백으로 이루어진 경우
        elif param.replace(' ', '').isdigit():
            return int(''.join(filter(str.isdigit, param)))
        # 한글과 숫자로 이루어진 경우
        elif any(char.isdigit() for char in param) and any(char.isalpha() for char in param):
            return int(''.join(filter(str.isdigit, param)))
        # 그 외의 경우
        else:
            return float(param) if '.' in param else param


def movieBaseInfo(parser):
    movieBaseInfo = {}
    # 영화 이름 detail_tit > tit_movie > span .txt_tit
    titleTag = parser.find('span', {'class': 'txt_tit'})
    movieTitle = titleTag.text
    movieBaseInfo['movieTitle'] = movieTitle

    # 누적 관람객이 없는 경우 예외처리 하는 김에 모두 예외처리
    try:
        # 장르
        genre = parser.find('dt', text='장르').find_next('dd').get_text(strip=True)
        movieBaseInfo['genre'] = genre
    except:
        movieBaseInfo['genre'] = 'Empty'

    try:
        # 영화 별점
        score = parser.find('dt', text='평점').find_next('dd').get_text(strip=True)
        movieBaseInfo['score'] = score
    except:
        movieBaseInfo['score'] = 0

    # 누적 관람객이 없는 경우가 있는 경우 대비 ex)40778
    try:
        # 누적 관람객
        visitor = parser.find('dt', text='누적관객').find_next('dd').get_text(strip=True)
        movieBaseInfo['visitor'] = visitor
    except:
        movieBaseInfo['visitor'] = 0

    return movieBaseInfo

# TODO 각각의 리뷰 데이터 필요
def getReviewList(parsar):
    reviewList = parsar.find('div', {'class': 'ratings'})
    print('review', reviewList)

# TODO 리뷰 긍정/부정 구분
def isReviewPositive(reviewContent):
    print(reviewContent)

# TODO 해당 ID가 선호하는 장르
def offerGenre(reviewData):
    print(reviewData)

def htmlParsar(movieUrl):
    response = requests.get(movieUrl)
    sourceType = response.text
    parser = BeautifulSoup(sourceType, 'html.parser')

    return parser

def getReviewInfo(baseUrl, movieIdList):
    whetherMovieBoxOfficeList = {}
    for movieId in movieIdList:
        movieUrl = baseUrl + movieId
        parser = htmlParsar(movieUrl)

        # 영화 기본 정보
        movieInfo = movieBaseInfo(parser)

        # 흥행 여부
        boxOffice = isBoxOffice(chageDataOnlyNumber(movieInfo['visitor']))
        whetherMovieBoxOfficeList[movieInfo['movieTitle']] = boxOffice

    return whetherMovieBoxOfficeList

def tranceExcel(division, param):
    if division == 2:
        param.to_excel(excelWriter, sheet_name='boxOffice')
    elif division == 1:
        param.to_excel(excelWriter, sheet_name='divisionIsPositive')
    elif division == 3:
        param.to_excel(excelWriter, sheet_name='preferMovie')
    else:
        print("It was had error when trance excel")


def main():
    print('Start to get movie base information and review analysis!!')
    baseUrl = 'https://movie.daum.net/moviedb/grade?movieId='
    # movieIdList = ['39519', '3791', '35497', '40878', '43729', '44085', '46121', '145342', '1660', '109512',
    #                '160244', '122749', '104209', '43172', '76384', '100237', '89720', '69737', '44832', '139237',
    #                '3649', '62730', '41951', '62708', '43584', '111292', '79544', '163777', '115601', '53080']

    # 테스트 코드, 실제 제출할 때는 위의 리스트로 수정
    movieIdList = ['39519']

    # 2번 흥행 여부
    isBoxOfficeList = getReviewInfo(baseUrl, movieIdList)
    try:
        dfBoxOfficeList = pd.DataFrame(isBoxOfficeList, index=[False])
        tranceExcel(2, dfBoxOfficeList)
    except Exception as e:
        print('error trance to excel')
        print(e)

    print('영화별 흥행 여부 (관람객 50만명 이상)\n', isBoxOfficeList)


if __name__ == '__main__':
    main()
