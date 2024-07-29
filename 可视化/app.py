from flask import Flask, render_template, jsonify
import read_data
import pandas as pd

app = Flask(__name__, template_folder='htmls')


def word_cloud():
    read_mysql = read_data.Read()
    sql = "select * from label"
    result = read_mysql.source_mysql(sql)
    data = " ".join([" ".join(i) for i in result]).split(" ")
    df = pd.DataFrame(data, columns=['标签'])
    df_group_count = df.value_counts()
    data = []
    for key, value in df_group_count.items():
        data.append({"name": key[0], "value": value})

    return data


def china_map():
    read_mysql = read_data.Read()
    sql = "select * from province_sum"
    result = read_mysql.source_mysql(sql)
    data = []
    for key, value in dict(result).items():
        data.append({"name": key, "value": value})

    return data


def rating_pie():
    read_mysql = read_data.Read()
    sql = "select * from rating_count"
    result = read_mysql.source_mysql(sql)
    data = []
    for key, value in dict(result).items():
        data.append({"name": key, "value": value})

    return data


def sale_price_scatter():
    read_mysql = read_data.Read()
    sql = "select price,sale from sale_price"
    result = read_mysql.source_mysql(sql)
    df = pd.DataFrame(result, columns=["price", "sale"]).value_counts()
    data = []
    for key, value in df.items():
        a = []
        [a.append(i) for i in key]
        a.append(value)
        data.append(a)

    return data


def score_count_pie():
    read_mysql = read_data.Read()
    sql = "select * from score_count"
    result = read_mysql.source_mysql(sql)
    df = pd.DataFrame(result, columns=["score", "count"])
    count_sum = df.sort_values("count", ascending=False)[5:]['count'].sum()
    df2 = df.sort_values("count", ascending=False) \
        .head(5) \
        .append({"score": "其他评分", "count": count_sum}, ignore_index=True)
    data = []
    for key, value in df2.values:
        data.append({"name": key, "value": value})

    return data


def supplier_count_bar():
    read_mysql = read_data.Read()
    sql = "select * from supplier_count"
    result = read_mysql.source_mysql(sql)
    df = pd.DataFrame(result, columns=["supplier", "count"])
    df2 = df.sort_values("count", ascending=False).head(10)
    data = [df2['supplier'].tolist(), df2['count'].tolist()]

    return data


def title_sale_bar():
    read_mysql = read_data.Read()
    sql = "select * from title_sale"
    result = read_mysql.source_mysql(sql)
    df = pd.DataFrame(result, columns=["title", "sale"])
    df2 = df.sort_values("sale", ascending=False).head(10)
    data = [df2['title'].tolist(), df2['sale'].tolist()]

    return data


def title_supplier_card():
    read_mysql = read_data.Read()
    sql = "select * from title_supplier_count order by title desc limit 1"
    result = read_mysql.source_mysql(sql)
    data = [result[0][0], result[0][1]]

    return data


@app.route('/data1', methods=['GET', 'POST'])
def data1():
    return jsonify(word_cloud())


@app.route('/data2', methods=['GET', 'POST'])
def data2():
    return jsonify(china_map())


@app.route('/data3', methods=['GET', 'POST'])
def data3():
    return jsonify(rating_pie())


@app.route('/data4', methods=['GET', 'POST'])
def data4():
    return jsonify(sale_price_scatter())


@app.route('/data5', methods=['GET', 'POST'])
def data5():
    return jsonify(score_count_pie())


@app.route('/data6', methods=['GET', 'POST'])
def data6():
    return jsonify(supplier_count_bar())


@app.route('/data7', methods=['GET', 'POST'])
def data7():
    return jsonify(title_sale_bar())


@app.route('/data8', methods=['GET', 'POST'])
def data8():
    return jsonify(title_supplier_card())


@app.route('/')
def index1():
    return render_template('index1.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
