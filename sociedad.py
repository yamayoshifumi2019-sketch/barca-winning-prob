import pandas as pd

file_path = r"C:\Users\yoshi\Downloads\barca data\laliga2425.csv"
df_all=pd.read_csv(file_path)

#バルセロナの全試合
df_barca=df_all[(df_all["HomeTeam"] == "Barcelona") | (df_all["AwayTeam"] == "Barcelona")]

#ソシエダの全試合
df_sociedad=df_all[(df_all["HomeTeam"] == "Sociedad") | (df_all["AwayTeam"] == "Sociedad")]

# --- バルセロナの平均得点 ---
barca_goals = df_barca.apply(lambda x: x['FTHG'] if x['HomeTeam'] == 'Barcelona' else x['FTAG'], axis=1)
barca_avg_goals = barca_goals.mean()

# --- ソシエダの平均得点 --- 
sociedad_goals = df_sociedad.apply(lambda x: x['FTHG'] if x['HomeTeam'] == 'Sociedad' else x['FTAG'], axis=1)
sociedad_avg_goals = sociedad_goals.mean()

# --- バルセロナの平均失点 ---
barca_conceded = df_barca.apply(lambda x: x['FTAG'] if x['HomeTeam'] == 'Barcelona' else x['FTHG'], axis=1)
barca_avg_conceded = barca_conceded.mean()

# --- ソシエダの平均失点 ---
sociedad_conceded = df_sociedad.apply(lambda x: x['FTAG'] if x['HomeTeam'] == 'Sociedad' else x['FTHG'], axis=1)
sociedad_avg_conceded = sociedad_conceded.mean()

# --- バルセロナの枠内シュート決定率 ---
barca_total_goals = df_barca.apply(lambda x: x['FTHG'] if x['HomeTeam'] == 'Barcelona' else x['FTAG'], axis=1).sum()
barca_total_shots_on = df_barca.apply(lambda x: x['HST'] if x['HomeTeam'] == 'Barcelona' else x['AST'], axis=1).sum()
barca_efficiency = (barca_total_goals / barca_total_shots_on) * 100

# --- ソシエダの枠内シュート決定率 ---
soc_total_goals = df_sociedad.apply(lambda x: x['FTHG'] if x['HomeTeam'] == 'Sociedad' else x['FTAG'], axis=1).sum()
soc_total_shots_on = df_sociedad.apply(lambda x: x['HST'] if x['HomeTeam'] == 'Sociedad' else x['AST'], axis=1).sum()
soc_efficiency = (soc_total_goals / soc_total_shots_on) * 100

#バルセロナのアウェイ勝率
df_barca_away = df_all[df_all['AwayTeam'] == 'Barcelona']
barca_away_wins = (df_barca_away['FTR'] == 'A').sum()
barca_away_total = len(df_barca_away)
barca_away_win_rate = (barca_away_wins / barca_away_total) * 100

# ソシエダのホーム勝率
df_soc_home = df_all[df_all['HomeTeam'] == 'Sociedad']
soc_home_wins = (df_soc_home['FTR'] == 'H').sum()
soc_home_total = len(df_soc_home)
soc_home_win_rate = (soc_home_wins / soc_home_total) * 100 if soc_home_total > 0 else 0

# --- バルセロナの直近5試合の勝率 ---
recent_5_barca = df_barca.tail(5)
barca_recent_wins = recent_5_barca.apply(lambda x: 1 if (x['HomeTeam'] == 'Barcelona' and x['FTR'] == 'H') or (x['AwayTeam'] == 'Barcelona' and x['FTR'] == 'A') else 0, axis=1).sum()
barca_recent_win_rate = (barca_recent_wins / 5) * 100

# --- ソシエダの直近5試合の勝率 ---
recent_5_soc = df_sociedad.tail(5)
soc_recent_wins = recent_5_soc.apply(lambda x: 1 if (x['HomeTeam'] == 'Sociedad' and x['FTR'] == 'H') or (x['AwayTeam'] == 'Sociedad' and x['FTR'] == 'A') else 0, axis=1).sum()
soc_recent_win_rate = (soc_recent_wins / 5) * 100

import pandas as pd
import glob
import os

# 1. フォルダパスを指定
folder_path = r"C:\Users\yoshi\Downloads\barca data"

# 2. 13/14から23/24までの全CSVファイルを取得
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

list_df = []
for file in all_files:
    # 今シーズンのデータ(2425)は「今季の実力」として別で考えたいので、相性（過去データ）からは除外
    if "2425" not in file:
        tmp_df = pd.read_csv(file)
        list_df.append(tmp_df)

# 全シーズン分を1つに合体
df_all_years = pd.concat(list_df, ignore_index=True)

# 3. 「ソシエダ(Home) vs バルセロナ(Away)」の試合だけを抽出
h2h_matches = df_all_years[
    (df_all_years['HomeTeam'] == 'Sociedad') & (df_all_years['AwayTeam'] == 'Barcelona')
].copy()

# 簡単な集計
wins = (h2h_matches['FTR'] == 'A').sum()
draws = (h2h_matches['FTR'] == 'D').sum()
losses = (h2h_matches['FTR'] == 'H').sum()

# 相性勝率の計算（バルサがアウェイで勝った確率）
total_h2h = len(h2h_matches)
barca_h2h_wins = (h2h_matches['FTR'] == 'A').sum()
compatibility_score = (barca_h2h_wins / total_h2h) * 100 if total_h2h > 0 else 0

# バルセロナの総合スコア計算 ---
# 失点は「少ないほど良い」ので (3 - 失点) で計算し、得点と失点は10倍して勝率と桁を合わせます
barca_final_score = (
    (barca_avg_goals * 10 * 0.15) + 
    ((3 - barca_avg_conceded) * 10 * 0.15) + 
    (barca_efficiency * 0.1) + 
    (barca_away_win_rate * 0.25) + 
    (barca_recent_win_rate * 0.25) + 
    (compatibility_score * 0.1)
)

# --- ソシエダの総合スコア計算 ---
# 相性はバルサの裏返し (100 - 相性)
soc_comp_score = 100 - compatibility_score

sociedad_final_score = (
    (sociedad_avg_goals * 10 * 0.15) + 
    ((3 - sociedad_avg_conceded) * 10 * 0.15) + 
    (soc_efficiency * 0.1) + 
    (soc_home_win_rate * 0.25) + 
    (soc_recent_win_rate * 0.25) + 
    (soc_comp_score * 0.1)
)
# --- 3. 割合（％）に変換 ---
total_point = barca_final_score + sociedad_final_score
barca_percent = (barca_final_score / total_point) * 100
espanol_percent = (sociedad_final_score / total_point) * 100

# --- 4. 結果をシンプルに表示 ---
print(f"  勝敗予想結果 (Win Rate)")
print("="*30)
print(f"Barcelona : {barca_percent:.1f} %")
print(f"Espanol   : {espanol_percent:.1f} %")
print("="*30)