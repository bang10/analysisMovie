import requests
from bs4 import BeautifulSoup
import pandas as pd

import reviewDto
movieReviewList = []

# README 2번 흥행 여부
def isBoxOffice(visitor) :
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


def getReviewInfo(baseUrl, movieIdList):
    for movieId in movieIdList:
        movieUrl = baseUrl + movieId
        response = requests.get(movieUrl)
        sourceType = response.text
        parser = BeautifulSoup(sourceType, 'html.parser')

        # 영화 이름 detail_tit > tit_movie > span .txt_tit
        titleTag = parser.find('span', {'class': 'txt_tit'})
        movieTitle = titleTag.text

        # 영화 평점 info_detail > detail_cont > list_cont >> dd
        movieScoreTag = parser.select('.list_cont dd')
        movieScore = float(chageDataOnlyNumber(movieScoreTag[6].text))
        # 관람객 수
        visitor = chageDataOnlyNumber(movieScoreTag[7].text)
        # 흥행 여부
        boxOffice = isBoxOffice(int(visitor))

        # 관람객 ID 정보
        # TODO
        visitorTag = parser.select('ul', {'class': 'list_comment'})
        print(visitorTag)
        # 관람객 아이디 당 평점

        # 관람평


def main():
    baseUrl = 'https://movie.daum.net/moviedb/grade?movieId='
    # movieIdList = ['39519', '3791', '35497', '40878', '43729', '44085', '46121', '145342', '1660', '109512',
    #                '160244', '122749', '104209', '43172', '76384', '100237', '89720', '69737', '44832', '139237',
    #                '3649', '40778', '41951', '62708', '43584', '111292', '79544', '163777', '115601', '53080']

    # 테스트 코드, 실제 제출할 때는 위의 리스트로 수정
    movieIdList = ['39519']

    getReviewInfo(baseUrl, movieIdList)


if __name__ == '__main__':
    main()
