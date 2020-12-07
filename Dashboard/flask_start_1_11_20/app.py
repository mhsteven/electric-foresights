from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np
import json
from random import random
from plotly.subplots import make_subplots

###Data

df1 = pd.read_csv('./static/data/monterrey_Total_A.csv')
df1['date'] = pd.to_datetime(df1.Timestamp, dayfirst=True)
df1['Total_fake'] = df1['Total']-300*random()
del df1['Timestamp']
del df1['Unnamed: 0']
df1 = df1[['date','Total','Total_fake']]

df2 = pd.read_csv('./static/data/monterrey_Total_P.csv')
df2['date'] = pd.to_datetime(df2.Timestamp, dayfirst=True)
df2['Total_fake'] = df2['Total']-300*random()
del df2['Timestamp']
del df2['Unnamed: 0']
df2 = df2[['date','Total','Total_fake']]

df3 = pd.read_csv('./static/data/monterrey_feels_like_A.csv')
df3['date'] = pd.to_datetime(df3.Timestamp, dayfirst=True)
del df3['Timestamp']
del df3['Unnamed: 0']
df3 = df3.rename(columns = {'feels_like': 'temp'}, inplace = False)
df3 = df3[['date','temp']]

df4 = pd.read_csv('./static/data/monterrey_feels_like_P.csv')
df4['date'] = pd.to_datetime(df4.Timestamp, dayfirst=True)
del df4['Timestamp']
del df4['Unnamed: 0']
df4 = df4.rename(columns = {'feels_like': 'temp'}, inplace = False)
df4 = df4[['date','temp']]

df5 = pd.read_csv('./static/data/monterrey_Ending_A.csv')
df5['date'] = pd.to_datetime(df5.Timestamp, dayfirst=True)
del df5['Timestamp']
del df5['Unnamed: 0']
df5 = df5.rename(columns = {'Ending': 'oil_p'}, inplace = False)
df5 = df5[['date','oil_p']]

df6 = pd.read_csv('./static/data/monterrey_Ending_P.csv')
df6['date'] = pd.to_datetime(df6.Timestamp, dayfirst=True)
del df6['Timestamp']
del df6['Unnamed: 0']
df6 = df6.rename(columns = {'Ending': 'oil_p'}, inplace = False)
df6 = df6[['date','oil_p']]

df7 = pd.read_csv('./static/data/monterrey_Rate_A.csv')
df7['date'] = pd.to_datetime(df7.Timestamp, dayfirst=True)
del df7['Timestamp']
del df7['Unnamed: 0']
df7 = df7.rename(columns = {'Rate': 'exch_rate'}, inplace = False)
df7 = df7[['date','exch_rate']]

df8 = pd.read_csv('./static/data/monterrey_Rate_P.csv')
df8['date'] = pd.to_datetime(df8.Timestamp, dayfirst=True)
del df8['Timestamp']
del df8['Unnamed: 0']
df8 = df8.rename(columns = {'Rate': 'exch_rate'}, inplace = False)
df8 = df8[['date','exch_rate']]


###Simulator data

cal_data=pd.read_csv('./static/data/sample1.csv')
cal_data['Timestamp']=pd.to_datetime(cal_data['Timestamp'])
cal_data['Day']=cal_data['Timestamp'].map(lambda x:x.day)
cal_data['Hour']=cal_data['Timestamp'].map(lambda x:x.hour)	

app = Flask(__name__)



def create_plot():

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df1['date'], y=df1['Total'],
	                    mode='lines',
	                    name='Monterrey historical',
	                    line=dict(color='firebrick')))
	              
	fig.add_trace(go.Scatter(x=df1['date'], y=df1['Total_fake'],
	                    mode='lines',
	                    name='Other region historical',
	                    line=dict(color='#dde9f4')))

	fig.add_trace(go.Scatter(x=df2['date'], y=df2['Total'],
	                    mode='lines',
	                    name='Monterrey predicted',
	                    line=dict(color='lightsalmon',
	                              dash='dash')))
	              
	fig.add_trace(go.Scatter(x=df2['date'], y=df2['Total_fake'],
	                    mode='lines',
	                    name='Other region predicted',
	                    line=dict(color='#dde9f4',
	                              dash='dash')))

	fig.update_layout(
	    updatemenus=[go.layout.Updatemenu(
	        active=0,
	        x=-0.03,
	        y=1.1,
	        buttons=list(
	            [dict(label = 'All Data',
	                  method = 'update',
	                  args = [{'visible': [True, True, True, True]},
	                          {'title': '<b>All Data</b>',
	                           'showlegend':True}]),
	             dict(label = 'Monterrey',
	                  method = 'update',
	                  args = [{'visible': [True, False, True, False]},
	                          {'title': '<b>Monterrey</b>',
	                           'showlegend':True}]),
	             dict(label = 'Other region',
	                  method = 'update',
	                  args = [{'visible': [False, True, False, True]},
	                          {'title': '<b>Other Region</b>',
	                           'showlegend':True}]),
	            ])
	        )
	    ])

	fig.update_layout(
	    xaxis=dict(
	         rangeslider=dict(
	            visible=True
	        ),
	        type="date"
	    )
	)

	fig.update_layout(
    autosize=False,
    width=1000,
    height=600,
    margin=dict(
        l=10,
        r=10,
        b=30,
        t=50,
        pad=4
    ),
    yaxis=dict(title_text="Electicity Price in Peso"))

	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1),
	    plot_bgcolor = '#dde9f4',
        paper_bgcolor = '#eff5fa')

	fig.update_layout(
	    title={
	        'y':0.99,
	        'x':0.15,
	        'xanchor': 'left',
	        'yanchor': 'top'})

	fig

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

def create_plot_data():

	fig1 = make_subplots(rows=4, cols=1,
	                    shared_xaxes=True,
	                    vertical_spacing=0.05,
	                    subplot_titles=("<b>Crude Oil Price</b>", "<b>Exchange Rate</b>", 
	                                    "<b>Monterrey Temperature</b>", "<b>Electricity Price</b>"))

	fig1.add_trace(go.Scatter(x=df1['date'], y=df1['Total'],
	                    mode='lines',
	                    name='Monterrey historical',
	                    line=dict(color='red')),row=4, col=1)

	fig1.add_trace(go.Scatter(x=df3['date'], y=df3['temp'],
	                    mode='lines',
	                    name='Monterrey hist temperature',
	                    line=dict(color='blue')),row=3, col=1)

	fig1.add_trace(go.Scatter(x=df5['date'], y=df5['oil_p'],
	                    mode='lines',
	                    name='Historical oil price',
	                    line=dict(color='orange')),row=1, col=1)

	fig1.add_trace(go.Scatter(x=df7['date'], y=df7['exch_rate'],
	                    mode='lines',
	                    name='Historical exch rate',
	                    line=dict(color='green')),row=2, col=1)

	fig1.update_layout(
	autosize=False,
	width=1000,
	height=800,
	margin=dict(
	    l=20,
	    r=20,
	    b=30,
	    t=50,
	    pad=4
	))

	fig1.update_layout(showlegend = False,
	    plot_bgcolor = '#dde9f4',
	    paper_bgcolor = '#eff5fa')

	fig1.update_layout(xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness = 0.05)

	graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

def create_table():

	part_df = partitioning(df2,df2.date[0],df2.date[len(df2.date)-1])

	datap1 = part_df.groupby('dayofyear#').apply(lambda x: x.sort_values('Total',ascending=False)).reset_index(drop = True)

	index_list = []

	for i in datap1.index:
	    if i%24 in [0,1,2,3]:# 24 will change depending on the values slected
	        index_list.append(i)

	datap2 = datap1.loc[index_list].reset_index(drop = True)

	price = pd.DataFrame(np.reshape(list(datap2.Total),(7,4)),columns=['top1_hour_price','top2_hour_price',\
                                                               'top3_hour_price','top4_hour_price'])
	date = pd.DataFrame(np.reshape(list(datap2.date),(7,4)),columns=['top1_hour_date','top2_hour_date',\
	                                                               'top3_hour_date','top4_hour_date'])
	final_dataset = pd.concat([date, price], axis = 1)
	final_dataset = final_dataset[['top1_hour_date', 'top1_hour_price','top2_hour_date', 'top2_hour_price',\
	                               'top3_hour_date', 'top3_hour_price','top4_hour_date', 'top4_hour_price']]
	final_dataset.insert(0,'date',[d.date() for d in final_dataset['top1_hour_date']])
	final_dataset.insert(1,'top1_time',[d.time() for d in final_dataset['top1_hour_date']])
	final_dataset.insert(4,'top2_time',[d.time() for d in final_dataset['top2_hour_date']])
	final_dataset.insert(7,'top3_time',[d.time() for d in final_dataset['top3_hour_date']])
	final_dataset.insert(10,'top4_time',[d.time() for d in final_dataset['top4_hour_date']])
	del final_dataset['top1_hour_date']
	del final_dataset['top2_hour_date']
	del final_dataset['top3_hour_date']
	del final_dataset['top4_hour_date']

	df_av = df2

	df_av['date1'] = [d.date() for d in df_av['date']]
	df_av['time'] = [d.time() for d in df_av['date']]

	df_av =  df2.groupby('date1')['Total'].mean()
	df_av = df_av.round(2)
	df_av['date'] = df_av.index
	df_av= df_av.reset_index()
	df_av = df_av.drop([len(df_av)-1])
	df_av = df_av.sort_values('date1',ascending=True)

	final_dataset.insert(1, "average", df_av['Total']) 

	final_dataset = final_dataset.round(2)

	fig_t = go.Figure()

	date_col = '#74a7d2'
	av_col = '#b7d2eB'
	col = 'LightSkyBlue'

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Top 1 Hours','Top 1 Price','Top 2 Hours','Top 2 Price',
	                        'Top 3 Hours','Top 3 Price','Top 4 Hours','Top 4 Price'],
	                fill_color='blue',
					font=dict(color='white'),
					align='center',
					height = 30),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price,final_dataset.top2_time, 
	                       final_dataset.top2_hour_price,final_dataset.top3_time, final_dataset.top3_hour_price,
	                       final_dataset.top4_time, final_dataset.top4_hour_price],
	               fill_color=[date_col,av_col,'white','white',col,col,'white','white',col,col],
	               align='left')))

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Top 1 Hours','Top 1 Price','Top 2 Hours','Top 2 Price',
	                        'Top 3 Hours','Top 3 Price'],
	                fill_color='blue',
	               	align='center',
					font=dict(color='white'),
					height = 50),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price,final_dataset.top2_time, 
	                       final_dataset.top2_hour_price,final_dataset.top3_time, final_dataset.top3_hour_price],
	               fill_color=[date_col,av_col,'white','white',col,col,'white','white'],
	               align='left')))

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Top 1 Hours','Top 1 Price','Top 2 Hours','Top 2 Price'],
	                fill_color='blue',
	               	align='center',
					font=dict(color='white'),
					height = 50),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price,
	    					final_dataset.top2_time,final_dataset.top2_hour_price],
	               fill_color=[date_col,av_col,'white','white',col,col],
	               align='left')))

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Top 1 Hours','Top 1 Price'],
	                fill_color='blue',
	               	align='center',
					font=dict(color='white'),
					height = 50),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price],
	               fill_color=[date_col,av_col,'white','white'],
	               align='left')))


	fig_t.update_layout(
	    updatemenus=[go.layout.Updatemenu(
	        active=0,
	        x=-0.005,
	        y=1.0,
	        buttons=list(
	            [dict(label = 'Top 1',
	                  method = 'update',
	                  args = [{'visible': [False,False,False,True]}]),
	             dict(label = 'Top 2',
	                  method = 'update',
	                  args = [{'visible': [False,False,True,False]}]),
	             dict(label = 'Top 3',
	                  method = 'update',
	                  args = [{'visible': [False, True, False, False]}]),
	            dict(label = 'Top 4',
	                  method = 'update',
	                  args = [{'visible': [True, False, False, False]}]),
	            ])
	        )
	    ])

	fig_t.update_layout(
		    autosize=False,
		    width=1000,
		    height=250,
		    margin=dict(
		        l=10,
		        r=10,
		        b=30,
		        t=20,
		        pad=4
		    ),
		    plot_bgcolor = '#dde9f4',
		    paper_bgcolor = '#eff5fa')

	tableJSON = json.dumps(fig_t, cls=plotly.utils.PlotlyJSONEncoder)

	return tableJSON


def create_table_bot():

	part_df = partitioning(df2,df2.date[0],df2.date[len(df2.date)-1])

	datap1 = part_df.groupby('dayofyear#').apply(lambda x: x.sort_values('Total',ascending=True)).reset_index(drop = True)

	index_list = []

	for i in datap1.index:
	    if i%24 in [0,1,2,3]:# 24 will change depending on the values slected
	        index_list.append(i)

	datap2 = datap1.loc[index_list].reset_index(drop = True)

	price = pd.DataFrame(np.reshape(list(datap2.Total),(7,4)),columns=['top1_hour_price','top2_hour_price',\
                                                               'top3_hour_price','top4_hour_price'])
	date = pd.DataFrame(np.reshape(list(datap2.date),(7,4)),columns=['top1_hour_date','top2_hour_date',\
	                                                               'top3_hour_date','top4_hour_date'])
	final_dataset = pd.concat([date, price], axis = 1)
	final_dataset = final_dataset[['top1_hour_date', 'top1_hour_price','top2_hour_date', 'top2_hour_price',\
	                               'top3_hour_date', 'top3_hour_price','top4_hour_date', 'top4_hour_price']]
	final_dataset.insert(0,'date',[d.date() for d in final_dataset['top1_hour_date']])
	final_dataset.insert(1,'top1_time',[d.time() for d in final_dataset['top1_hour_date']])
	final_dataset.insert(4,'top2_time',[d.time() for d in final_dataset['top2_hour_date']])
	final_dataset.insert(7,'top3_time',[d.time() for d in final_dataset['top3_hour_date']])
	final_dataset.insert(10,'top4_time',[d.time() for d in final_dataset['top4_hour_date']])
	del final_dataset['top1_hour_date']
	del final_dataset['top2_hour_date']
	del final_dataset['top3_hour_date']
	del final_dataset['top4_hour_date']

	df_av = df2

	df_av['date1'] = [d.date() for d in df_av['date']]
	df_av['time'] = [d.time() for d in df_av['date']]

	df_av =  df2.groupby('date1')['Total'].mean()
	df_av = df_av.round(2)
	df_av['date'] = df_av.index
	df_av= df_av.reset_index()
	df_av = df_av.drop([len(df_av)-1])
	df_av = df_av.sort_values('date1',ascending=True)

	final_dataset.insert(1, "average", df_av['Total']) 

	final_dataset = final_dataset.round(2)

	fig_t = go.Figure()

	date_col = '#74a7d2'
	av_col = '#b7d2eB'
	col = 'LightSkyBlue'

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Bottom 1 Hours','Bottom 1 Price','Bottom 2 Hours','Bottom 2 Price',
	                        'Bottom 3 Hours','Bottom 3 Price','Bottom 4 Hours','Bottom 4 Price'],
	                fill_color='blue',
					font=dict(color='white'),
					align='center',
					height = 30),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price,final_dataset.top2_time, 
	                       final_dataset.top2_hour_price,final_dataset.top3_time, final_dataset.top3_hour_price,
	                       final_dataset.top4_time, final_dataset.top4_hour_price],
	               fill_color=[date_col,av_col,'white','white',col,col,'white','white',col,col],
	               align='left')))

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Bottom 1 Hours','Bottom 1 Price','Bottom 2 Hours','Bottom 2 Price',
	                        'Bottom 3 Hours','Bottom 3 Price'],
	                fill_color='blue',
	               	align='center',
					font=dict(color='white'),
					height = 50),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price,final_dataset.top2_time, 
	                       final_dataset.top2_hour_price,final_dataset.top3_time, final_dataset.top3_hour_price],
	               fill_color=[date_col,av_col,'white','white',col,col,'white','white'],
	               align='left')))

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Bottom 1 Hours','Bottom 1 Price','Bottom 2 Hours','Bottom 2 Price'],
	                fill_color='blue',
	               	align='center',
					font=dict(color='white'),
					height = 50),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price,
	    					final_dataset.top2_time,final_dataset.top2_hour_price],
	               fill_color=[date_col,av_col,'white','white',col,col],
	               align='left')))

	fig_t.add_trace(go.Table(
	    header=dict(values=['Date','Average Price','Bottom 1 Hours','Bottom 1 Price'],
	                fill_color='blue',
	               	align='center',
					font=dict(color='white'),
					height = 50),
	    cells=dict(values=[final_dataset.date, final_dataset.average, final_dataset.top1_time, final_dataset.top1_hour_price],
	               fill_color=[date_col,av_col,'white','white'],
	               align='left')))


	fig_t.update_layout(
	    updatemenus=[go.layout.Updatemenu(
	        active=0,
	        x=-0.005,
	        y=1.0,
	        buttons=list(
	            [dict(label = 'Bot 1',
	                  method = 'update',
	                  args = [{'visible': [False,False,False,True]}]),
	             dict(label = 'Bot 2',
	                  method = 'update',
	                  args = [{'visible': [False,False,True,False]}]),
	             dict(label = 'Bot 3',
	                  method = 'update',
	                  args = [{'visible': [False, True, False, False]}]),
	            dict(label = 'Bot 4',
	                  method = 'update',
	                  args = [{'visible': [True, False, False, False]}]),
	            ])
	        )
	    ])

	fig_t.update_layout(
		    autosize=False,
		    width=1000,
		    height=250,
		    margin=dict(
		        l=10,
		        r=10,
		        b=30,
		        t=20,
		        pad=4
		    ),
		    plot_bgcolor = '#dde9f4',
		    paper_bgcolor = '#eff5fa')

	tableJSON = json.dumps(fig_t, cls=plotly.utils.PlotlyJSONEncoder)

	return tableJSON
	

def create_table_week():

	part_df = partitioning(df2,df2.date[0],df2.date[len(df2.date)-1])

	datap1 = part_df.groupby('dayofyear#').apply(lambda x: x.sort_values('Total',ascending=True)).reset_index(drop = True)

	index_list = []

	for i in datap1.index:
	    if i%24 in [0,1,2,3]:# 24 will change depending on the values slected
	        index_list.append(i)

	datap2 = datap1.loc[index_list].reset_index(drop = True)

	price = pd.DataFrame(np.reshape(list(datap2.Total),(7,4)),columns=['top1_hour_price','top2_hour_price',\
                                                               'top3_hour_price','top4_hour_price'])
	date = pd.DataFrame(np.reshape(list(datap2.date),(7,4)),columns=['top1_hour_date','top2_hour_date',\
	                                                               'top3_hour_date','top4_hour_date'])
	final_dataset = pd.concat([date, price], axis = 1)
	final_dataset = final_dataset[['top1_hour_date', 'top1_hour_price','top2_hour_date', 'top2_hour_price',\
	                               'top3_hour_date', 'top3_hour_price','top4_hour_date', 'top4_hour_price']]
	final_dataset.insert(0,'date',[d.date() for d in final_dataset['top1_hour_date']])
	final_dataset.insert(1,'top1_time',[d.time() for d in final_dataset['top1_hour_date']])
	final_dataset.insert(4,'top2_time',[d.time() for d in final_dataset['top2_hour_date']])
	final_dataset.insert(7,'top3_time',[d.time() for d in final_dataset['top2_hour_date']])
	final_dataset.insert(10,'top4_time',[d.time() for d in final_dataset['top2_hour_date']])
	del final_dataset['top1_hour_date']
	del final_dataset['top2_hour_date']
	del final_dataset['top3_hour_date']
	del final_dataset['top4_hour_date']

	weekly_avg_rec = part_df.groupby('dayofyear#').mean().sort_values(by ='Total').reset_index(drop = True)
	weekly_dict = {0.0:'Monday',1.0:'Tuesday',2.0:'Wednesday',3.0:'Thursday',4.0:'Friday',5.0:'Saturday',6.0:'Sunday'}

	weekly_list = [weekly_dict[weekly_avg_rec['dayofweek#'][i]] for i in range(len(weekly_dict))]
	weekly_avg_rec.insert(5, "Week_day", weekly_list, True)
	weekly_avg_rec['Avg_price'] = weekly_avg_rec['Total']
	weekly_avg_rec = weekly_avg_rec[['Week_day','Avg_price']]
	weekly_avg_rec = weekly_avg_rec.T 
	weekly_avg_rec.columns = ['Daily_Average_Price_1','Daily_Average_Price_2','Daily_Average_Price_3',\
	                          'Daily_Average_Price_4','Daily_Average_Price_5','Daily_Average_Price_6',\
	                          'Daily_Average_Price_7']

	fig_t = go.Figure()

	date_col = '#74a7d2'
	av_col = '#b7d2eB'
	col = 'LightSkyBlue'

	fig_t.add_trace(go.Table(
	    header=dict(values=[weekly_avg_rec.Daily_Average_Price_1[0],weekly_avg_rec.Daily_Average_Price_2[0],weekly_avg_rec.Daily_Average_Price_3[0],
	    					weekly_avg_rec.Daily_Average_Price_4[0],weekly_avg_rec.Daily_Average_Price_5[0],weekly_avg_rec.Daily_Average_Price_6[0],
	    					weekly_avg_rec.Daily_Average_Price_7[0]],
	                fill_color='blue',
					font=dict(color='white'),
					align='center',
					height = 30),
	    cells=dict(values=[round(weekly_avg_rec.Daily_Average_Price_1[1],2),
	    					round(weekly_avg_rec.Daily_Average_Price_2[1],2),
	    					round(weekly_avg_rec.Daily_Average_Price_3[1],2),
	    					round(weekly_avg_rec.Daily_Average_Price_4[1],2),
	    					round(weekly_avg_rec.Daily_Average_Price_5[1],2),
	    					round(weekly_avg_rec.Daily_Average_Price_6[1],2),
	    					round(weekly_avg_rec.Daily_Average_Price_7[1],2)],
	               fill_color=[col,'white',col,'white',col,'white',col],
	               align='left')))

	fig_t.update_layout(
		    autosize=False,
		    width=1000,
		    height=100,
		    margin=dict(
		        l=10,
		        r=10,
		        b=30,
		        t=20,
		        pad=4
		    ),
		    plot_bgcolor = '#dde9f4',
		    paper_bgcolor = '#eff5fa')

	tableJSON = json.dumps(fig_t, cls=plotly.utils.PlotlyJSONEncoder)

	return tableJSON

def simulatorchart():

	fig3 = go.Figure()

	fig3.add_trace(go.Scatter(x=cal_data['Timestamp'], y=cal_data['Prediction'],name='Forecast',mode='markers'))
	fig3.add_trace(go.Scatter(x=cal_data['Timestamp'], y=cal_data['Actual'],name='Actual'))
	fig3.update_yaxes(title_text='Local Marginal Cost in Peso')
	fig3.update_xaxes(automargin=True)
	fig3.update_yaxes(rangemode="tozero")
	fig3.update_layout(title={'text':"<b> Local Marginal Cost:</b> <i>Prediction vs Actual</i>",
	                        'y':0.99,
					        'x':0.05,
					        'xanchor': 'left',
					        'yanchor': 'top'})
	
	fig3.update_layout(
    autosize=False,
    width=1000,
    height=400,
    margin=dict(
        l=10,
        r=10,
        b=50,
        t=30,
        pad=4
    ))

	fig3.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1),
	    plot_bgcolor = '#dde9f4',
        paper_bgcolor = '#eff5fa')


	simulatorchart = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

	return simulatorchart

def partitioning(dataset, start_date, end_date): # choose what start and end date you want for you dataframe 
     principio =   int(dataset[dataset['date']== start_date].index.values[0])
    
     fin = int(dataset[dataset['date']== end_date].index.values[0])+1
     
     dataset = dataset[principio:fin].reset_index(drop=True)
     
     dataset['Timestamp'] = pd.DatetimeIndex(dataset['date'])#prophet readable datetime format

     #      dataset = dataset.rename(columns={'DATE_TIME': 'ds','DEMAND': 'y'})
    
     dataset['week#'] = dataset['date'].dt.week
     
     dataset['day#'] = dataset['date'].dt.day
     
     dataset['dayofweek#'] = dataset['date'].dt.dayofweek
     
     dataset['dayofyear#'] = dataset['date'].dt.dayofyear
    
     dataset['hour#'] = dataset['date'].dt.hour
     
    
     return dataset

def peakshave(dataset,days,rate,hour_con,hours,shave_hour,spead_hour):
    num=len(hours)
    dataset=dataset[dataset['Day'].isin(days)]
    dataset=dataset.sort_values(['Day','Prediction']).reset_index()
    dataset['shave_cost']=0
    choices=len(days)
    for n in range(choices*num):
        if n%num<spead_hour:
            dataset.at[n,'shave_cost']=dataset.at[n,'Actual']*hour_con*(1+rate*shave_hour/spead_hour)
        elif n%num>num-shave_hour-1:
            dataset.at[n,'shave_cost']=dataset.at[n,'Actual']*hour_con*(1-rate)
        else:
            dataset.at[n,'shave_cost']=dataset.at[n,'Actual']*hour_con
    return dataset

def simulation(dataset,hour_con,ori_days,shave_rate,hours,shave_hour,spead_hour):
    dataset=dataset[dataset['Hour'].isin(hours)]
    temp1=dataset.copy(deep=True)
    temp1=temp1[temp1['Day'].isin(ori_days)]
    temp1['cost']=temp1['Actual']*hour_con
    ori_cost=temp1['cost'].sum()
    temp1=temp1.groupby(['Day'])['cost'].sum().reset_index()
    temp1=temp1.rename(columns={'cost':'ori_cost'})
    
    temp2=dataset.copy(deep=True)
    temp2=temp2.groupby('Day')['Prediction'].sum().reset_index()
    temp2=temp2.sort_values('Prediction',ascending=True)
    least_days=temp2['Day'].to_list()
    choice=len(ori_days)
    least_days=least_days[:choice]
    temp2=dataset.copy(deep=True)
    temp2=temp2[temp2['Day'].isin(least_days)]
    temp2['cost']=temp2['Actual']*hour_con
    flexi_cost=temp2['cost'].sum()
    temp2=temp2.groupby(['Day'])['cost'].sum().reset_index()
    temp2=temp2.rename(columns={'cost':'flexi_cost'})
    
    temp3=peakshave(dataset,ori_days,shave_rate,hour_con,hours,shave_hour,spead_hour)
    temp3=temp3.groupby(['Day'])['shave_cost'].sum().reset_index()
    shave_only=temp3['shave_cost'].sum()
    temp4=peakshave(dataset,least_days,shave_rate,hour_con,hours,shave_hour,spead_hour)
    temp4=temp4.groupby(['Day'])['shave_cost'].sum().reset_index()
    flexi_shave=temp4['shave_cost'].sum()
    
    flexi_save=ori_cost-flexi_cost
    shave_save=ori_cost-shave_only
    both_save=ori_cost-flexi_shave
    
    
    fig = go.Figure()

    fig.add_trace(go.Bar(x=temp1['Day'], y=temp1['ori_cost'],width=0.15,name='Original Cost',marker=dict(color='grey',opacity=0.95)))
    fig.add_trace(go.Bar(x=temp2['Day'], y=temp2['flexi_cost'],width=0.15,name='Alternative Schedule Only',marker=dict(color='orange',opacity=0.95)))
    fig.add_trace(go.Bar(x=temp3['Day'], y=temp3['shave_cost'],width=0.15,name='Peak-shaving Only',marker=dict(color='lightgreen',opacity=0.95)))
    fig.add_trace(go.Bar(x=temp4['Day'], y=temp4['shave_cost'],width=0.15,name='Applying Both Measures',marker=dict(color='purple',opacity=0.95)))
    fig.update_yaxes(title_text='Local Marginal Cost in Peso')
    fig.update_xaxes(automargin=True)  

    fig.update_layout(title={'text':"<b>Illustration of Cost-Saving Measures Enabled by the Forecast</b>",
	                        'y':0.99,
					        'x':0.05,
					        'xanchor': 'left',
					        'yanchor': 'top'}, 
                      height=500,
                      width=1100,
                          margin=dict(
								        l=10,
								        r=10,
								        b=50,
								        t=30,
								        pad=4
								    ),
                      legend=dict(
								orientation="h",
								yanchor="bottom",
								y=0.95,
								xanchor="right",
								x=1
                            ),
                      plot_bgcolor = '#dde9f4',
                      paper_bgcolor = '#eff5fa')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return {'chart':graphJSON,'ori_cost':ori_cost,'flexi_cost':flexi_cost,'shave_only_cost':shave_only,
           'both_cost':flexi_shave,'flexi_save':flexi_save,'shave_save':shave_save,'both_save':both_save}

def get_hours(text):
    hours=[]
    text=text.replace(' ','')
    text=text.split(',')
    for item in text:
        if '-'in item:
            temp=item.split('-')
            start=int(temp[0])
            end=int(temp[1])
            for n in range(start,end+1):
                hours.append(n)
        else:
            hours.append(int(item))
    return hours


@app.route('/')
def about():

    return render_template('about.html',title = 'About', plot=create_plot_data())
    
@app.route('/first')
def graph_1():
    return render_template('graph_1.html', title = 'Forecast', plot=create_plot(), table = create_table(), tb = create_table_bot(),
    						tbw = create_table_week(), value="./static/data/monterrey_Total_P.csv" )

@app.route('/simulator')
def simulator():
    
    return render_template('simulator.html',plot=simulatorchart())

@app.route('/simulator/simulation', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    
    feature = feature.replace('/','')
    feature = feature.split('|')
    
    if feature[-1]=='':
        feature=feature[:-1]
    
    rate=float(feature[0])
    hour_con=float(feature[1])
    hours_selected=feature[2]
    hours_selected=get_hours(hours_selected)
    shave_hour=int(feature[3])
    spead_hour=int(feature[4])
    ori_days=feature[5:]
    num=len(ori_days)
    js_output=simulation(cal_data,hour_con,ori_days,rate,hours_selected,shave_hour,spead_hour)
    msg= "<i>By implementing flexible work schedule only, you save </i>"+str(int(js_output['flexi_save'])) + \
    "<i> PESO a week; By implementing peak shaving only, you save </i>"+str(int(js_output['shave_save']))+\
    "<i> PESO a week; By implementing both measures, you save </i>" +str(int(js_output['both_save']))+\
    "<i> PESO a week; It translates to annual savings of </i>"+str(int(js_output['flexi_save']/num*365))+\
    "<i> PESO, </i>" + str(int(js_output['shave_save']/num*365))+'<i> PESO, and </i>'+\
    str(int(js_output['both_save']/num*365))+'<i> PESO, respectively!</i>'
    outputdata='{"chart":'
    outputdata+=js_output['chart'] +',"msg":' + '"'+msg+'"'+'}'
    
    return outputdata


if __name__ == '__main__':
    app.run()