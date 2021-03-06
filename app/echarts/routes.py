from app.echarts import bp
from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from flask import render_template, flash, redirect, url_for, request
from random import randrange
from pyecharts import options as opts
from pyecharts.charts import Bar

@bp.route("/echarts")
def echarts():
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 85, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 80])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return Markup(c.render_embed())

@bp.route('/getdata')
def get_data():
	language = ['python', 'java', 'c', 'c++', 'c#', 'php']
	value = ['100', '150', '100', '90', '80', '90']
	return json.dumps({'language':language,'value':value},ensure_ascii=False)



