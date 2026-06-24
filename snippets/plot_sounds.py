# (PC에서 실행) sounds.csv를 Plotly 3D 산점도로 보기
# 처음 한 번만:  pip install plotly pandas
import pandas as pd
import plotly.express as px

df = pd.read_csv("sounds.csv")          # 피코에서 내려받은 파일
fig = px.scatter_3d(
    df, x="rms", y="zcr", z="crest", color="label",
    title="내가 모은 소리들 (3D)",
    labels={"rms": "크기", "zcr": "높낮이", "crest": "들쭉날쭉", "label": "소리"},
)
fig.update_traces(marker=dict(size=5))
fig.show()                              # 브라우저가 열리고, 마우스로 빙글빙글 돌려보기!
