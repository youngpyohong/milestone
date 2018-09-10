from flask import Flask,render_template,request,redirect
import numpy as np
import bokeh
import quandl
from bokeh import plotting
from bokeh.plotting import figure,output_file, show,save
from bokeh.models import DatetimeTickFormatter
import os


quandl.ApiConfig.api_key = "_Sjg3Zgvo6CxWitjj-2P"



app_lulu = Flask(__name__)



@app_lulu.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
    app_lulu.i=0
    if request.method == 'GET':
        return render_template('userinfo_young.html')
    else:
        #request was a POST

        app_lulu.tickername = request.form['tickersym']

        
        app_lulu.oc1=request.form.get('close_lulu')
        app_lulu.oc2=request.form.get('adj_close_lulu')
        app_lulu.oc3=request.form.get('open_lulu')
        app_lulu.oc4=request.form.get('adj_open_lulu')
        
        '''
        app_lulu.vars['name'] = request.form['name_lulu']
        app_lulu.vars['age'] = request.form['age_lulu']
        '''
        return redirect('/main_lulu')

@app_lulu.route('/main_lulu')
def main_lulu2():
    
   
    p=bokeh.plotting.figure(title='Quandl WIKI EOD Stock Prices - 2017')
    
    print app_lulu.tickername
    
    app_lulu.data = quandl.get_table('WIKI/PRICES', ticker = [app_lulu.tickername], 
                        qopts = { 'columns': ['ticker', 'date', 'adj_open','open','adj_close','close'] }, 
                        date = { 'gte': '2015-12-31', 'lte': '2016-12-31' }, 
                        paginate=True)
    if app_lulu.oc1 != None:
        p.line(app_lulu.data['date'],app_lulu.data['close'],color='firebrick',legend=app_lulu.tickername+':close')
  
    if app_lulu.oc2 != None:
        p.line(app_lulu.data['date'],app_lulu.data['adj_close'],color="#B3DE69",legend=app_lulu.tickername+':adj_close')

    if app_lulu.oc3 != None:  
        p.line(app_lulu.data['date'],app_lulu.data['open'],color='navy',legend=app_lulu.tickername+':open')

    if app_lulu.oc4 != None:
        p.line(app_lulu.data['date'],app_lulu.data['adj_open'],color='olive',legend=app_lulu.tickername+':adj_open')

       
    p.xaxis.formatter=DatetimeTickFormatter(
            months=["%b %Y"],
            years=["%b %Y"],
    )

    p.xaxis.axis_label = "date"
    fileexist=True
    
    while fileexist:
        app_lulu.filename = './templates/myplot'+str(app_lulu.i)+'.html'
        if os.path.exists(app_lulu.filename):
            app_lulu.i+=1
        else:
            break
    output_file(app_lulu.filename,title=app_lulu.tickername+" stock prices-2017")
    save(p)
    
    return redirect('/next_lulu')

#####################################
## IMPORTANT: I have separated /next_lulu INTO GET AND POST
## You can also do this in one function, with If and Else.

@app_lulu.route('/next_lulu',methods=['GET'])
def next_lulu():  

    return render_template('myplot'+str(app_lulu.i)+'.html')

@app_lulu.route('/next_lulu',methods=['POST'])
def next_lulu2():  

    return render_template('myplot.html')

if __name__ == "__main__":
    app_lulu.run()
