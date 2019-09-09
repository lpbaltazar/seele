import warnings
warnings.filterwarnings("ignore")

import os
import re
import time
import pandas as pd
import pymysql.cursors


cols = ["VIDEO_CONTENT_TITLE", "VIDEO_CATEGORY_TITLE", "ISP_TAG", "IPCOUNTRY", "SUBDIVISION_1", "SUBDIVISION_2",
       "IPCITY", "MOBILE_DEVICE", "USERID", "PRIMARY_FINGERPRINT", "USER_BROWSER", "USER_OS", "USER_OS_VERSION", "USER_BROWSER_VERSION", "SESSIONID",
       "ORIGINAL_VIDEO_CONTENT_ID", "ORIGINAL_VIDEO_CATEGORY_ID", "VIDEO_CONTENT_ID", "VIDEO_CATEGORY_ID"]


def clean_data(data_dir, out_dir):
	for f in sorted(os.listdir(data_dir)):
		print(f)
		if f.endswith(".csv"):
			df = pd.read_csv(os.path.join(data_dir, f))
			outfile = os.path.join(out_dir, f)
			dfcols = df.columns
			for col in cols:
				if col in dfcols:
				df[col] = df[col].astype(str)
				df[col] = df[col].apply(lambda x: x.replace(",", ""))
			df.to_csv(outfile, index = False)

def mainClean(data_dir, out_dir):
	clean_data("events/2018/12", "events/december")
	clean_data("events/2019/01", "events/january")
	clean_data("events/2019/02", "events/february")
	clean_data("events/2019/03", "events/march")
	clean_data("events/2019/04", "events/april")
	clean_data("events/2019/06", "events/june")

def loadMultData(cursor, file):
	load = '''LOAD DATA LOCAL INFILE %s INTO TABLE events_data2
	       FIELDS TERMINATED BY ','
	       LINES TERMINATED BY '\n'
	       IGNORE 1 ROWS (CALID, PROPERTYID, SRC, ACTIVITY, USERID, PRIMARY_FINGERPRINT, USER_BROWSER, USER_BROWSER_VERSION, USER_OS, USER_OS_VERSION, USER_HOSTADDRESS, SESSIONID, ORIGINAL_VIDEO_CONTENT_ID, VIDEO_CONTENT_ID, VIDEO_CONTENT_TITLE, ORIGINAL_VIDEO_CATEGORY_ID, VIDEO_CATEGORY_ID, VIDEO_CATEGORY_TITLE, VIDEO_TYPE, VIDEO_DURATION, SESSION_STARTDT, SESSION_ENDDT, CLICK_COUNT, ADPLAY_COUNT, PLAY_COUNT, PAUSE_COUNT, RESUME_COUNT, AB_FLAG, SEEK_COUNT, BUFFER_COUNT, TOTAL_BUFFER_TIME, MAX_BUFFER_TIME, USR_TOT_WATCHING_DUR, USR_ACT_TOT_WATCHING_DUR, ISP_PROVIDER, ISMOBILE, MOBILE_DEVICE, ISP_TAG, NUMBER_USED, CURRENCY, AMOUNT, FREE_ACCESS_TAG, PRODUCTTYPE, PRODUCTNAME, PARTNER, MOBILETYPE, SESSION_STARTDT_YEAR, SESSION_STARTDT_MONTH, SESSION_STARTDT_DAY, APP_TAG, THREE_G_TAG, CONTENT_TYPE, VERIFIED, IPCOUNTRY, SUBDIVISION_1, SUBDIVISION_2, IPCITY, SOURCESCRIPT, IS_KNOWN, APP_VERSION, MODIFIEDDATE)
	   '''
	cursor.execute(load, (file))
	connection.commit()
	print('Added rows: ', cursor.rowcount)
	print('Successfully imported file {}'.format(file))

def importToSQL(data_dir, cursor):
	s = time.time()
	for f in sorted(os.listdir(data_dir)):
	if f.endswith('.csv'):
		file = os.path.join(data_dir, f)
		loadMultData(cursor, file)
	e = time.time()
	total_time = time.strftime('%H:%M:%S', time.gmtime(e-s))
	print('Finish importing {} in {}'.format(data_dir, total_time))

def mainImport(data_dir):
	connection = pymysql.connect(host = 'localhost', user = 'rigi', password = 'pwd@rigi', db = 'events_db', local_infile = True)
	cursor = connection.cursor()
	# loadMultData(cursor, 'events/december/IWantVideoEvent-20181201.csv')
	# importToSQL('events/december', cursor)
	# importToSQL('events/january', cursor)
	# importToSQL('events/february', cursor)
	# importToSQL('events/march', cursor)
	# importToSQL('events/april', cursor)
	importToSQL('events/may', cursor)
	cursor.close()
	

	
	