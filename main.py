# TODO 요구사항
# - 영화 한글 리뷰 데이터 수집 : 크롤링 (or 데이터셋 사용), 영화 30편 이상
# - 수집한 데이터 전처리 (KoNLPy)
# - 수집한 리뷰 데이터 분류
#
# TODO
# 1) 수집한 리뷰 데이터 긍정/부정 분류(별표가 기준, 텍스트 학습)
# 2) 수집한 리뷰 데이터에서 흥행여부 예측(흥행기준 50만, 영화 개봉: 2000~2010)
# TODO
# 3) 수집한 리뷰 데이터의 아이디 50개 이상 수집하여 선호 장르 분류(별표가 기준, 텍스트 학습)

import requests
from bs4 import BeautifulSoup
import pandas as pd

import reviewDto

def isBoxOffice(visitor) :
    if visitor == 0:
        return 'error'

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
        genre = 'genre is not found'
        movieBaseInfo['genre'] = genre

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

def getReviewInfo(baseUrl, movieIdList):
    whetherMovieBoxOfficeList = {}
    for movieId in movieIdList:
        movieUrl = baseUrl + movieId
        print('Movie url: ', movieUrl)
        response = requests.get(movieUrl)
        sourceType = response.text
        parser = BeautifulSoup(sourceType, 'html.parser')

        # 영화 기본 정보
        movieInfo = movieBaseInfo(parser)

        # 영화 리뷰 리스트
        getReviewList(parser)

        # 흥행 여부
        boxOffice = isBoxOffice(chageDataOnlyNumber(movieInfo['visitor']))
        whetherMovieBoxOfficeList[movieInfo['movieTitle']] = boxOffice

    return whetherMovieBoxOfficeList

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
    print('영화별 흥행 여부 (관람객 50만명 이상)\n', isBoxOfficeList)


if __name__ == '__main__':
    main()
