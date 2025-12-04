# import streamlit as st
# import pandas as pd
# import numpy as np
# import time

# st.set_page_config(page_title="⚡️ 加權平均反推計算器（小數分數版）", layout="centered")

# st.title("⚡️ 加權平均反推計算器")
# # st.write("快速反推加權平均，每項分數是整數，最終分數可小數點一位！")

# # 使用者輸入
# target_score = st.number_input("請輸入最終分數（例如 95 或 94.5）", min_value=0.0, max_value=100.0, value=95.0, step=0.1, format="%.1f")
# num_projects = st.number_input("請輸入專案數量", min_value=2, max_value=20, value=4)

# weights = []
# project_names = []

# st.subheader("🔧 請輸入各項目權重")
# for i in range(num_projects):
#     col1, col2 = st.columns(2)
#     name = col1.text_input(f"項目 {i+1} 名稱", value=f"項目{i+1}")
#     weight = col2.number_input(f"項目 {i+1} 權重（%）", min_value=0.0, max_value=100.0, value=round(100.0 / num_projects, 2))
#     project_names.append(name)
#     weights.append(weight)

# # 驗證比重總和
# if sum(weights) != 100:
#     st.error(f"⚠️ 權重總和為 {sum(weights)}%，請確認加起來是 100%")
# else:
#     normalized_weights = [w / 100 for w in weights]
#     max_trials = 50000  # 背後自動設定

#     def random_integer_solution():
#         # === 第一階段：優先找所有分數都在 70~91 的解 ===
#         for _ in range(max_trials):
#             random_scores = np.random.randint(70, 92, size=num_projects - 1)

#             remaining_weight = normalized_weights[-1]
#             weighted_sum_so_far = sum([s * w for s, w in zip(random_scores, normalized_weights[:-1])])
#             last_score = (target_score - weighted_sum_so_far) / remaining_weight

#             # 最後一項也需在 70~91
#             if last_score.is_integer() and 70 <= last_score <= 91:
#                 return list(random_scores) + [int(last_score)]

#         # === 第二階段：若找不到，以原本 1~100 的範圍找解 ===
#         for _ in range(max_trials):
#             random_scores = np.random.randint(1, 101, size=num_projects - 1)

#             remaining_weight = normalized_weights[-1]
#             weighted_sum_so_far = sum([s * w for s, w in zip(random_scores, normalized_weights[:-1])])
#             last_score = (target_score - weighted_sum_so_far) / remaining_weight

#             if last_score.is_integer() and 1 <= last_score <= 100:
#                 return list(random_scores) + [int(last_score)]

#         return None # 沒找到解


#     # def random_integer_solution():
#     #     for _ in range(max_trials):
#     #         # 隨機選 n-1 個分數 (整數)
#     #         random_scores = np.random.randint(1, 101, size=num_projects - 1)
#     #         # 反推最後一個
#     #         remaining_weight = normalized_weights[-1]
#     #         weighted_sum_so_far = sum([s * w for s, w in zip(random_scores, normalized_weights[:-1])])
#     #         last_score = (target_score - weighted_sum_so_far) / remaining_weight

#     #         # ⭐ 檢查：最後一個是整數 AND 1~100 範圍
#     #         if last_score.is_integer() and 1 <= last_score <= 100:
#     #             full_scores = list(random_scores) + [int(last_score)]
#     #             return full_scores
#     #     return None  # 沒找到解

#     if st.button("🚀 開始計算"):
#         start_time = time.time()
#         result = random_integer_solution()
#         elapsed_time = time.time() - start_time

#         if result:
#             st.success(f"✅ 找到解答！計算時間：{elapsed_time:.4f} 秒")
#             df = pd.DataFrame([result], columns=project_names)
#             st.dataframe(df)
#         else:
#             st.warning("😢 在設定的嘗試次數內找不到符合條件的整數解，建議調整比重或最終分數。")

# st.markdown("---")
# st.caption("By Ada 的加權反推小工具 ⚡️你值得擁有 v2.0")


import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="⚡️ 加權平均反推計算器", layout="centered")

st.title("⚡️ 加權平均反推計算器")

# 使用者輸入
target_score = st.number_input(
    "請輸入最終分數（例如 95 或 94.5）",
    min_value=0.0, max_value=100.0, value=95.0, step=0.1, format="%.1f"
)

num_projects = st.number_input(
    "請輸入專案數量",
    min_value=2, max_value=20, value=4
)

project_names = []
weights = []
score_inputs = []

st.subheader("🛠️ 請輸入各項目資料（名稱｜權重｜已知分數）")

for i in range(num_projects):
    col1, col2, col3 = st.columns([2, 1, 1])

    # 名稱
    name = col1.text_input(f"項目 {i+1} 名稱", value=f"項目{i+1}")

    # 權重
    weight = col2.number_input(
        f"權重（%）",
        min_value=0.0, max_value=100.0,
        value=round(100.0 / num_projects, 2),
        key=f"weight_{i}"
    )

    # 已知分數（可留空）
    known_score = col3.number_input(
        f"已知分數",
        min_value=0, max_value=100,
        value=0,
        step=1,
        key=f"score_{i}"
    )

    project_names.append(name)
    weights.append(weight)
    score_inputs.append(known_score if known_score != 0 else None)


# 檢查權重總和
if sum(weights) != 100:
    st.error(f"⚠️ 權重總和為 {sum(weights)}%，請確認加起來是 100%")
else:
    normalized_weights = [w / 100 for w in weights]
    max_trials = 50000

    # --------------------------
    # 搜尋解答主函式
    # --------------------------
    def random_integer_solution():
        known_indices = [i for i, v in enumerate(score_inputs) if v is not None]
        unknown_indices = [i for i, v in enumerate(score_inputs) if v is None]

        # 已知項目的加權和
        known_weighted_sum = sum(
            score_inputs[i] * normalized_weights[i] for i in known_indices
        )

        # 若全部已知 → 直接檢查
        if len(unknown_indices) == 0:
            if abs(known_weighted_sum - target_score) < 1e-6:
                return score_inputs
            return None

        # ========== 第一階段：優先找 70～91 ==========
        for _ in range(max_trials):
            trial_scores = {}

            # 除最後一個外，先隨機產生分數
            for idx in unknown_indices[:-1]:
                trial_scores[idx] = np.random.randint(70, 92)

            last_idx = unknown_indices[-1]
            remaining_weight = normalized_weights[last_idx]

            weighted_sum_so_far = known_weighted_sum + \
                sum(trial_scores[i] * normalized_weights[i] for i in unknown_indices[:-1])

            last_score = (target_score - weighted_sum_so_far) / remaining_weight

            if last_score.is_integer() and 70 <= last_score <= 91:
                trial_scores[last_idx] = int(last_score)

                final_scores = []
                for i in range(num_projects):
                    if i in known_indices:
                        final_scores.append(score_inputs[i])
                    else:
                        final_scores.append(trial_scores[i])
                return final_scores

        # ========== 第二階段：找 1～100 ==========
        for _ in range(max_trials):
            trial_scores = {}

            for idx in unknown_indices[:-1]:
                trial_scores[idx] = np.random.randint(1, 101)

            last_idx = unknown_indices[-1]
            remaining_weight = normalized_weights[last_idx]

            weighted_sum_so_far = known_weighted_sum + \
                sum(trial_scores[i] * normalized_weights[i] for i in unknown_indices[:-1])

            last_score = (target_score - weighted_sum_so_far) / remaining_weight

            if last_score.is_integer() and 1 <= last_score <= 100:
                trial_scores[last_idx] = int(last_score)

                final_scores = []
                for i in range(num_projects):
                    final_scores.append(score_inputs[i] if i in known_indices else trial_scores[i])
                return final_scores

        return None

    # --------------------------
    # 按鈕觸發
    # --------------------------
    if st.button("🚀 開始計算"):
        start_time = time.time()
        result = random_integer_solution()
        elapsed_time = time.time() - start_time

        if result:
            st.success(f"✅ 找到解答！計算時間：{elapsed_time:.4f} 秒")
            df = pd.DataFrame([result], columns=project_names)
            st.dataframe(df)
        else:
            st.warning("😢 找不到符合條件的整數解，請調整權重或分數。")

st.markdown("---")
st.caption("By Ada 的加權反推小工具 ⚡️ 你值得擁有 v3.0")
