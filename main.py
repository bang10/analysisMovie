import requests
from bs4 import BeautifulSoup
import pandas as pd

import reviewDto
whetherMovieBoxOfficeList = {}

# README 2번 흥행 여부
def isBoxOffice(visitor) :
    if visitor == 0:
        return 'Movie Error'

    return True if visitor > 500000 else False

# 이상한 것도 같이 크롤링 되는 것 방지
def chageDataOnlyNumber(param):
    if param.isdigit():  # 숫자로만 이루어진 경우
        return int(param)
    else:
        # 숫자와 쉼표(,)로 이루어진 경우
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

    # 누적 관람객이 없는 김에 모두 예외처리
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
        score = 0
        movieBaseInfo['score'] = score

    # 누적 관람객이 없는 경우가 있는 경우 대비 ex)40778
    try:
        # 누적 관람객
        visitor = parser.find('dt', text='누적관객').find_next('dd').get_text(strip=True)
        movieBaseInfo['visitor'] = visitor
    except:
        visitor = 0
        movieBaseInfo['visitor'] = visitor

    return movieBaseInfo

def getReviewInfo(baseUrl, movieIdList):
    for movieId in movieIdList:
        movieUrl = baseUrl + movieId
        response = requests.get(movieUrl)
        sourceType = response.text
        parser = BeautifulSoup(sourceType, 'html.parser')

        # 영화 기본 정보
        movieInfo = movieBaseInfo(parser)

        # 영화 리뷰 리스트

        # 흥행 여부
        boxOffice = isBoxOffice(chageDataOnlyNumber(movieInfo['visitor']))
        whetherMovieBoxOfficeList[movieInfo['movieTitle']] = boxOffice

        # 관람객 ID 정보
        # TODO
        # visitorTag = parser.select('p')




def main():
    baseUrl = 'https://movie.daum.net/moviedb/grade?movieId='
    # movieIdList = ['39519', '3791', '35497', '40878', '43729', '44085', '46121', '145342', '1660', '109512',
    #                '160244', '122749', '104209', '43172', '76384', '100237', '89720', '69737', '44832', '139237',
    #                '3649', '62730', '41951', '62708', '43584', '111292', '79544', '163777', '115601', '53080']

    # 테스트 코드, 실제 제출할 때는 위의 리스트로 수정
    movieIdList = ['39519']

    # 2번 흥행 여부
    getReviewInfo(baseUrl, movieIdList)
    print('영화별 흥행 여부 (관람객 50만명 이상)\n', whetherMovieBoxOfficeList)


if __name__ == '__main__':
    main()
