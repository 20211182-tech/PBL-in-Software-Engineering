# 문제1. 여러개의 눈

## 문제 요약
- OpenCV로 이미지/영상/카메라를 다루고, 단축키로 캡처/녹화를 제어하는 멀티미디어 처리 문제입니다.

## 핵심 파일
- `multiple_eyes.py`: 이미지 표시, 영상 재생, 카메라, 단축키 녹화 기능
- `test_multiple_eyes.py`: 키 매핑/경로 생성/디렉터리 생성 유틸 검증
- `requirements.txt`: `opencv-python`

## 풀이에 필요한 정보
1. 주요 단축키: ESC(종료), Ctrl+Z(캡처), Ctrl+X(녹화 시작), Ctrl+C(녹화 종료)
2. 캡처 파일은 `captures/`, 녹화 파일은 `recordings/`에 저장됩니다.
3. 실행 예시: `python multiple_eyes.py --video <파일경로> --shortcuts --codec mp4v`
4. 테스트 실행: `python test_multiple_eyes.py`
