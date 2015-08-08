# auto_svm.py
## class performance_measure
- json 포맷의 데이터 파일 경로와 List 형식의 feature set을 인자로 받는다.
- play() 메소드로 실행하며, 입력받은 feature set의 모든 조합 중 accuracy가 가장 높게 나오는 조합을 찾아 List 형식으로 result.json 파일에 저장한다.
- 실행 예
`pm = performance_measure("data/data.json", featureList)`
`pm.play()`


## class make_model
- json 포맷의 데이터 파일 경로와 List 형식의 feature set, 그리고 결과로 나온 model을 저장할 파일 경로를 인자로 받는다.
- play() 메소드로 실행하며, svm으로 계산하여 나온 model을 파라미터로 입력된 경로의 파일에 저장한다.
- 실행 예
`mm = make_model("data/data.json", selectedFeatureList, "data/model.txt")`
`mm.play()`

## class predict_label
- json 포맷의 데이터 파일 경로와 List 형식의 feature set, 그리고 make_model에서 저장했던 model 파일 경로를 인자로 받는다.
- play() 메소드로 실행하며, 추측한 label값을 저장하고 있는 List를 return한다.
- 실행 예
`pl = predict_label("data/predictData.json", selectedFeatureList, "data/model.txt")`
`predictLabel = pl.play()`