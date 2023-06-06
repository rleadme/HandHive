import cv2
import mediapipe as mp
import numpy as np

# image_judge(image_path) : 이미지에 대한 판단
def image_judge(image_data, model_path):
    
    # 인식하는 손 최대 개수 = 1
    max_num_hands = 1
    # 제스쳐 인식하는 
    rps_gesture = {0:'rock', 1:'scissors', 5:'paper', 9:'scissors'}

    # MediaPipe hands model
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=max_num_hands,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    # 학습된 knn 모델 불러오기
    knn_test=cv2.ml.KNearest_load(model_path)

    # 판단할 이미지 불러오기
    # img = cv2.imread(image_path)

    img_array = np.frombuffer(image_data, np.uint8) # 바이트 데이터 -> NumPy 배열로 변환
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR) # 컬러 이미지로 디코딩. 

    # 이미지 전처리
    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


    if result.multi_hand_landmarks is not None: # 손을 인식했다면
        for res in result.multi_hand_landmarks: # 모든 손에 대해서 실행(여기서는 max_num_hands가 1이므로 하나만 생각)
            joint = np.zeros((21, 3)) # 각 조인트(관절 포인트) 좌표 저장을 위한 변수 초기화(21개의 조인트, x,y,z좌표라서 3)
            for j, lm in enumerate(res.landmark): # 각 조인트마다 landmark 저장(x,y,z)
                joint[j] = [lm.x, lm.y, lm.z]

            # 각 조인트끼리의 계산을 통해 벡터를 구함
            # 예) v1[0] 값인 0과 v1[0] 값인 1을 빼면 관절 마디 한 구간에 대한 벡터가 나옴
            # 조인트 번호에 대한 정보는 mediapipe 참고 https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] 
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] 
            v = v2 - v1 # [20,3]

            # 정규화 
            # 각 벡터의 길이로 나누어준다.
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # . 연산의 arccos으로 각도를 구한다.
            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

            # 각도의 결과를 radian에서 degree(도)로 바꾼다.
            angle = np.degrees(angle) 

            # 가위바위보 추론
            data = np.array([angle], dtype=np.float32)
            _, results, _, _ = knn_test.findNearest(data, 3) # k=3 일 때 knn
            idx = int(results[0][0])

            # 가위바위보 추론 결과 반환
            if idx in rps_gesture.keys():
                return rps_gesture[idx]

#print(image_judge('rock.jpeg','knn_model.xml'))