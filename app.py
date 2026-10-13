import streamlit as st
import requests

sheet_url = st.secrets["sheet_url"]

# -------------------------------------
# タイトル
# -------------------------------------
st.title("⚽　サッカータイプ診断")

st.write("あなたのサッカータイプを診断します。")

name = st.text_input("名前を入力してください。")

if not name.strip():
    st.info("診断を始めるには、名前を入力してください。")


# -------------------------------------
# タイプ名
# -------------------------------------

type_names = {
    "A": "声出し全力応援タイプ",
    "B": "一体感重視サポータータイプ",
    "C": "戦術ガチ分析タイプ",
    "D": "データ・選手分析タイプ",
    "E": "スター選手推しタイプ",
    "F": "推し活全力タイプ",
    "G": "スタジアム満喫タイプ",
    "H": "みんなでワイワイタイプ"
}


# -------------------------------------
# 質問
# -------------------------------------

questions = [
    {
        "question": "スタジアムに到着したとき、一番ワクワクするのは？",
        "answers": [
            ("応援歌やチャントが聞こえてきたとき",{"A":3, "B":1}),
            ("サポーターが集まって盛り上がっている光景",{"B":3, "H":1}),
            ("スタメンやフォーメーションを確認するとき",{"C":3, "D":1}),
            ("推し選手がアップしている姿を見つけたとき",{"E":3, "F":1})
        ]
    },

    {
        "question": "ゴールが決まった瞬間、あなたは？",
        "answers": [
            ("とにかく大声で叫ぶ！",{"A":3, "H":1}),
            ("周りの人とハイタッチする",{"B":3, "H":1}),
            ("「今の崩しうまかったな」とプレーを振り返る",{"C":3, "D":1}),
            ("推し選手が決めたら大興奮！",{"E":3, "F":1})
        ]
    },

    {
        "question": "試合前にチェックするのは？",
        "answers": [
            ("今日の応援歌・チャント",{"A":3, "B":1}),
            ("スタジアムのイベント情報",{"G":3, "H":1}),
            ("スタメン・フォーメーション",{"C":3, "D":1}),
            ("推し選手のコンディション",{"E":3, "D":1})
        ]
    },

    {
        "question": "サッカー観戦で一番大切なのは？",
        "answers": [
            ("チームを全力で応援すること",{"A":3, "B":1}),
            ("サポーターと一緒に盛り上がること",{"B":3, "H":1}),
            ("試合の内容や戦術を楽しむこと",{"C":3, "D":1}),
            ("好きな選手の活躍を見ること",{"E":3, "F":1})
        ]
    },

    {
        "question": "試合中ついつい目で追ってしまうのは？",
        "answers": [
            ("ボールを持っている選手",{"C":3, "D":1}),
            ("推し選手",{"E":3, "F":1}),
            ("サポーターや応援席",{"B":3, "A":1}),
            ("スコアボードやスタッツ",{"D":3, "C":1})
        ]
    },

    {
        "question": "好きな選手を選ぶなら？",
        "answers": [
            ("チームを鼓舞するキャプテン",{"A":3, "B":1}),
            ("戦術を理解してゲームを組み立てる選手",{"C":3, "D":1}),
            ("圧倒的な実績を持つスター選手",{"E":3, "F":1}),
            ("数字に表れない仕事もこなす選手",{"D":3, "C":1})
        ]
    },

    {
        "question": "試合中に気になるには？",
        "answers": [
            ("選手同士のポジショニング",{"C":3, "D":1}),
            ("シュート数やボール支配率",{"D":3, "C":1}),
            ("応援席の盛り上がり",{"B":3, "A":1}),
            ("推し選手がどんなプレーをしているのか",{"E":3, "F":1})
        ]
    },

    {
        "question": "試合後に振り返るなら？",
        "answers": [
            ("あの選手交代が効いた！",{"C":3, "D":1}),
            ("〇〇選手、今日めっちゃよかった！",{"D":3, "E":1}),
            ("今日の応援めちゃくちゃ楽しかった！",{"B":3, "H":1}),
            ("推しがゴール決めてくれて最高！",{"E":3, "F":1})
        ]
    },

    {
        "question": "ＳＮＳでサッカーを見るなら？",
        "answers": [
            ("戦術や試合分析を見る",{"C":3, "D":1}),
            ("選手のスタッツやデータを見る",{"D":3, "C":1}),
            ("推し選手の投稿を見る",{"F":3, "E":1}),
            ("サポーターの盛り上がりを見る",{"B":3, "H":1})
        ]
    },

    {
        "question": "推し選手ができたら？",
        "answers": [
            ("試合でのプレーを徹底的に見る",{"E":3, "D":1}),
            ("グッズを集めたくなる",{"F":3, "E":1}),
            ("ＳＮＳやインタビューも追いかける",{"F":3, "E":1}),
            ("その選手のプレースタイルを分析する",{"D":3, "E":1})
        ]
    },

    {
        "question": "スタジアムで売っていたら嬉しいのは？",
        "answers": [
            ("限定ユニフォーム・タオル",{"F":3, "E":1}),
            ("選手コラボグッズ",{"F":3, "E":1}),
            ("ご当地グルメ",{"G":3, "H":1}),
            ("スタジアム限定メニュー",{"G":3, "F":1})
        ]
    },

    {
        "question": "試合開始まで時間があったら？",
        "answers": [
            ("スタジアムグルメを楽しむ",{"G":3, "H":1}),
            ("グッズショップを見る",{"F":3, "G":1}),
            ("仲間と話しながら待つ",{"H":3, "B":1}),
            ("ピッチを見ながら選手のアップを観察する",{"E":3, "D":1})
        ]
    },

    {
        "question": "観戦に一緒に行くなら？",
        "answers": [
            ("サッカーに詳しい友達",{"C":3, "D":1}),
            ("応援を一緒に全力でできる友達",{"A":3, "B":1}),
            ("サッカーを知らないけど楽しんでくれる友達",{"H":3, "G":1}),
            ("同じ選手を推している友達",{"F":3, "E":1})
        ]
    },

    {
        "question": "応援で好きなのは？",
        "answers": [
            ("大声でチャントを歌う",{"A":3, "B":1}),
            ("スタジアム全体が同じ応援をしている瞬間",{"B":3, "A":1}),
            ("ゴール後にみんなで喜ぶ瞬間",{"H":3, "B":1}),
            ("じっくり試合を見ること",{"C":3, "D":1})
        ]
    },

    {
        "question": "もし負けてしまったら？",
        "answers": [
            ("「次は絶対勝とう！」とすぐ切り替える",{"A":3, "B":1}),
            ("サポーターみんなで選手を励ましたい",{"B":3, "A":1}),
            ("なぜ負けたのか試合内容を分析する",{"C":3, "D":1}),
            ("推し選手の頑張りを思い返す",{"E":3, "F":1})
        ]
    },

    {
        "question": "ハーフタイムにすることは？",
        "answers": [
            ("後半の戦術を考える",{"C":3, "D":1}),
            ("前半のスタッツを確認する",{"D":3, "C":1}),
            ("グッズや写真をチェックする",{"F":3, "E":1}),
            ("フードやドリンクを買いに行く",{"G":3, "H":1})
        ]
    },

    {
        "question": "初めて行くスタジアムなら？",
        "answers": [
            ("応援席の雰囲気が気になる",{"B":3, "A":1}),
            ("スタジアムグルメを調べる",{"G":3, "H":1}),
            ("アクセスや座席を調べる",{"G":3, "C":1}),
            ("推し選手関連のイベントを調べる",{"F":3, "E":1})
        ]
    },{
        "question": "「最高の観戦だった！」と思うのは？",
        "answers": [
            ("最後まで声を出して応援できた日",{"A":3, "B":1}),
            ("スタジアム全体が一つになった日",{"B":3, "H":1}),
            ("戦術的に面白い試合だった日",{"C":3, "D":1}),
            ("推し選手の選手が大活躍した日",{"E":3, "F":1})
        ]
    },

    {
        "question": "試合後についやってしまうのは？",
        "answers": [
            ("試合の戦術について考える",{"C":3, "D":1}),
            ("選手のスタッツを見る",{"D":3, "C":1}),
            ("推し選手のＳＮＳをチェックする",{"F":3, "E":1}),
            ("写真を整理して思い出を振り返る",{"G":3, "F":1})
        ]
    },

    {
        "question": "遠征するとしたら？",
        "answers": [
            ("応援できるなら遠くても行く！",{"A":3, "B":1}),
            ("アウェイサポーターとの雰囲気を楽しみたい",{"B":3, "H":1}),
            ("推し選手を見るためならどこでも行く",{"E":3, "F":1}),
            ("観光もグルメもセットで楽しみたい",{"G":3, "H":1})
        ]
    },

    {
        "question": "試合中、声を出す頻度は？",
        "answers": [
            ("ほぼずっと声を出している",{"A":3, "B":1}),
            ("盛り上がる場面では周りと一緒に声を出す",{"B":3, "H":1}),
            ("重要な場面だけ声を出す",{"H":3, "E":1}),
            ("基本的には静かに試合を見る",{"C":3, "D":1})
        ]
    },

    {
        "question": "サッカー観戦で写真を撮るなら？",
        "answers": [
            ("スタジアムの雰囲気",{"G":3, "B":1}),
            ("サポーターみんなで盛り上がっている瞬間",{"B":3, "H":1}),
            ("推し選手",{"F":3, "E":1}),
            ("試合中の決定的なプレー",{"E":3, "C":1})
        ]
    },

    {
        "question": "もし観戦に丸１日使えるなら？",
        "answers": [
            ("試合前から応援して１日中盛り上がる",{"A":3, "B":1}),
            ("スタジアム周辺を楽しんで、試合も見る",{"G":3, "H":1}),
            ("仲間とご飯を食べたり遊んだりしてから観戦",{"H":3, "G":1}),
            ("試合前から選手や戦術について調べる",{"C":3, "D":1})
        ]
    },

    {
        "question": "あなたにとってサッカー観戦とは？",
        "answers": [
            ("「チームと一緒に戦うもの」",{"A":3, "B":1}),
            ("「みんなで作り上げるもの」",{"B":3, "H":1}),
            ("「試合を読み解くもの」",{"C":3, "D":1}),
            ("「好きな選手を応援するもの」",{"E":3, "F":1})
        ]
    }
]

# -------------------------------------
# 1問ずつ表示する診断画面
# -------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * len(questions)

if "finished" not in st.session_state:
    st.session_state.finished = False


# 診断スタート
if not st.session_state.started:
    if st.button(
        "診断スタート",
        key="start_diagnosis",
        disabled=not name.strip()
    ):
        st.session_state.started = True
        st.rerun()


# 質問画面
if st.session_state.started and not st.session_state.finished:

    i = st.session_state.current_question
    q = questions[i]

    st.progress((i + 1) / len(questions))
    st.write(f"質問 {i + 1} / {len(questions)}")

    st.subheader(f"Q{i + 1}. {q['question']}")

    # 前に選んだ回答を復元する
    saved_answer = st.session_state.user_answers[i]

    default_index = (
        q["answers"].index(saved_answer)
        if saved_answer is not None else 0
    )

    answer = st.radio(
        "回答を選んでください",
        q["answers"],
        format_func=lambda x: x[0],
        index=default_index,
        key=f"question_{i}"
    )

    # 戻る・次へボタン
    col1, col2 = st.columns(2)

    with col1:
        if i > 0:
            if st.button("← 前の質問"):
                st.session_state.user_answers[i] = answer
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if i < len(questions) - 1:
            if st.button("次の質問 →"):
                st.session_state.user_answers[i] = answer
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("診断結果を見る 🎉"):
                st.session_state.user_answers[i] = answer
                st.session_state.finished = True
                st.rerun()


# -------------------------------------
# 診断結果
# -------------------------------------

if st.session_state.finished:

    scores = {
        t: 0 for t in type_names
    }

    # 点数計算
    for answer in st.session_state.user_answers:
        for type_name, point in answer[1].items():
            scores[type_name] += point

    # 一番点数が高いタイプ
    result = max(scores, key=scores.get)
    result_name = type_names[result]

    data = {
        "name": name,
        "result": result_name,
        **scores
    }

    # Googleスプレッドシートへ記録
    if not st.session_state.get("sent_to_sheet", False):
        try:
            response = requests.post(
                sheet_url,
                data=data,
                timeout=15
            )
            response.raise_for_status()
            st.session_state.sent_to_sheet = True
        except requests.RequestException:
            st.error("記録に失敗しました。通信状況を確認してください。")

    # 結果表示
    st.success("🎉 診断結果！")
    st.write(f"あなたは【{result_name}】です！")

    st.subheader("📊 あなたの診断スコア")

    max_score = max(scores.values())

    for type_name, score in sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        st.write(f"**{type_names[type_name]}** {score}点")
        st.progress(score / max_score if max_score else 0)

    if st.button("もう一度診断する"):
        st.session_state.started = False
        st.session_state.current_question = 0
        st.session_state.user_answers = [None] * len(questions)
        st.session_state.finished = False
        st.session_state.sent_to_sheet = False
        st.rerun()
