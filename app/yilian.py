# 导入必要的库
from flask import Flask, request, render_template
import numpy as np 

# 创建 Flask 应用
#app = Flask(__name__)
app = Flask(__name__, static_url_path='')

# 量表题目
questions = [
    "我发现与人亲近比较容易。",
    "我发现要我去依赖别人很困难。",
    "我时常担心情侣并不真心爱我。",
    "我发现别人并不愿像我希望的那样亲近我。",
    "能依赖别人让我感到很舒服。",
    "我不在乎别人太亲近我。",
    "我发现当我需要别人帮助时，没人会帮我。",
    "和别人亲近使我感到有些不舒服。",
    "我时常担心情侣不想和我在一起。",
    "当我对别人表达我的情感时，我害怕他们与我的感觉会不一样。",
    "我时常怀疑情侣是否真正关心我。",
    "我对别人建立亲密的关系感到很舒服。",
    "当有人在情感上太亲近我时，我感到不舒服。",
    "我知道当我需要别人帮助时，总有人会帮我。",
    "我想与人亲近，但担心自己会受到伤害。",
    "我发现我很难完全信赖别人。",
    "情侣想要我在情感上更亲近一些，这常使我感到不舒服。",
    "我不能肯定，在我需要时，总找得到可以依赖的人。"
]

# 量表选项
options = [
    "完全不符合",
    "较不符合",
    "不能确定",
    "较符合",
    "完全符合"
]

# 量表分量表
subscales = {
    "亲近": [1, 6, 8, 12, 13, 17],
    "依赖": [2, 5, 7, 14, 16, 18],
    "焦虑": [3, 4, 9, 10, 11, 15]
}

# 反向计分条目
reverse_items = [2, 7, 8, 13, 16, 17, 18]

# 路由装饰器，用于处理网页请求
@app.route("/survey", methods=["GET", "POST"])
def attachment_survey():
    # 如果是 GET 请求，则渲染量表调查页面
    if request.method == "GET":
        # return render_template("survey.html", questions=questions, options=options)
        # return render_template("survey.html", questions=enumerate(questions), options=enumerate(options))
        return render_template("survey.html", questions=enumerate(questions), options=options)

    # 如果是 POST 请求，则处理量表调查结果
    elif request.method == "POST":
        # 获取用户输入
        responses = []
        for key in request.form:
            response = int (request.form[key])  
            responses.append(response) 
        # return str(responses)
        # responses = [int(response) for response in request.form.getlist("response")]

        # 计算分量表得分
        subscale_scores = {}
        for subscale, items in subscales.items():
            subscale_scores[subscale] = np.mean([responses[i - 1] for i in items])

        # 计算亲近依赖复合维度得分
        intimacy_dependency_score = np.mean([subscale_scores["亲近"], subscale_scores["依赖"]])

        # 计算焦虑得分
        anxiety_score = subscale_scores["焦虑"]

        # 依恋类型划分
        attachment_type = ""
        if intimacy_dependency_score > 3 and anxiety_score < 3:
            attachment_type = "安全型"
        elif intimacy_dependency_score > 3 and anxiety_score > 3:
            attachment_type = "先占型"
        elif intimacy_dependency_score < 3 and anxiety_score < 3:
            attachment_type = "拒绝型"
        elif intimacy_dependency_score < 3 and anxiety_score > 3:
            attachment_type = "恐惧型"

        # 渲染结果页面
        return render_template("result.html", attachment_type=attachment_type)

# 运行 Flask 应用
if __name__ == "__main__":

    app.run(debug=True)
    #app.run()
