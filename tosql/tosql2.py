import warnings
warnings.filterwarnings('ignore')

import pandas as pd

def clean_data(data_dir, out_dir):
	for f in sorted(os.listdir(data_dir)):
		print(f)
		if f.endswith(".csv"):
			df = pd.read_csv(os.path.join(data_dir, f))
			outfile = os.path.join(out_dir, f)
			
			df.VIDEO_DURATION = df.VIDEO_DURATION.fillna(0)
			values = df.VIDEO_DURATION.unique()

			if "Infinity" in values:
				print("with infinity")
				df.loc[df.VIDEO_DURATION == 'Infinity', 'VIDEO_DURATION'] = 0

			df.to_csv(outfile, index = False)
			print("Number of rows: ", len(df))

def mainClean():
	clean_data("../../events/2nd_implem/2019/02", "../../events/2nd_sql/02")
	clean_data("../../events/2nd_implem/2019/03", "../../events/2nd_sql/03")
	clean_data("../../events/2nd_implem/2019/04", "../../events/2nd_sql/04")
	clean_data("../../events/2nd_implem/2019/05", "../../events/2nd_sql/05")
	clean_data("../../events/2nd_implem/2019/06", "../../events/2nd_sql/06")
	clean_data("../../events/2nd_implem/2019/07", "../../events/2nd_sql/07")
	clean_data("../../events/2nd_implem/2019/08", "../../events/2nd_sql/08")

def loadMultData(cursor, file, connection):
	load = '''LOAD DATA LOCAL INFILE %s INTO TABLE events_data_new
	       FIELDS TERMINATED BY ','
	       OPTIONALLY ENCLOSED BY '\"'
	       LINES TERMINATED BY '\n'
	       IGNORE 1 ROWS (CALID, PROPERTYID, SRC, ACTIVITY, USERID, PRIMARY_FINGERPRINT, USER_BROWSER, USER_BROWSER_VERSION, USER_OS, USER_OS_VERSION, USER_HOSTADDRESS, SESSIONID, ORIGINAL_VIDEO_CONTENT_ID, VIDEO_CONTENT_ID, VIDEO_CONTENT_TITLE, ORIGINAL_VIDEO_CATEGORY_ID, VIDEO_CATEGORY_ID, VIDEO_CATEGORY_TITLE, VIDEO_TYPE, VIDEO_DURATION, SESSION_STARTDT, SESSION_ENDDT, CLICK_COUNT, ADPLAY_COUNT, PLAY_COUNT, PAUSE_COUNT, RESUME_COUNT, AB_FLAG, SEEK_COUNT, BUFFER_COUNT, TOTAL_BUFFER_TIME, MAX_BUFFER_TIME, USR_TOT_WATCHING_DUR, USR_ACT_TOT_WATCHING_DUR, ISP_PROVIDER, ISMOBILE, MOBILE_DEVICE, ISP_TAG, NUMBER_USED, CURRENCY, AMOUNT, FREE_ACCESS_TAG, PRODUCTTYPE, PRODUCTNAME, PARTNER, MOBILETYPE, SESSION_STARTDT_YEAR, SESSION_STARTDT_MONTH, SESSION_STARTDT_DAY, APP_TAG, THREE_G_TAG, CONTENT_TYPE, VERIFIED, IPCOUNTRY, SUBDIVISION_1, SUBDIVISION_2, IPCITY, SOURCESCRIPT, IS_KNOWN, APP_VERSION, MODIFIEDDATE)
	   '''
	cursor.execute(load, (file))
	connection.commit()
	print('Added rows: ', cursor.rowcount)
	print('Successfully imported file {}'.format(file))

def importToSQL(data_dir, cursor, connection):
	s = time.time()
	for f in sorted(os.listdir(data_dir)):
		if f.endswith('.csv'):
			file = os.path.join(data_dir, f)
			loadMultData(cursor, file, connection)
	e = time.time()
	total_time = time.strftime('%H:%M:%S', time.gmtime(e-s))
	print('Finish importing {} in {}'.format(data_dir, total_time))

def mainImport():
	connection = pymysql.connect(host = 'localhost', user = 'rigi', password = 'pwd@rigi', db = 'events_db', local_infile = True)
	cursor = connection.cursor()
	# vloadMultData(cursor, '../../events/2nd_sql/02/IWantVideoEvent-20190201.csv', connection)
	importToSQL("../../events/2nd_sql/01", cursor, connection)
	importToSQL("../../events/2nd_sql/02", cursor, connection)
	importToSQL("../../events/2nd_sql/03", cursor, connection)
	importToSQL("../../events/2nd_sql/04", cursor, connection)
	importToSQL("../../events/2nd_sql/05", cursor, connection)
	importToSQL("../../events/2nd_sql/06", cursor, connection)
	importToSQL("../../events/2nd_sql/07", cursor, connection)
	importToSQL("../../events/2nd_sql/08", cursor, connection)
	cursor.close()

if __name__ == '__main__':
	mainClean()
	mainImport()
