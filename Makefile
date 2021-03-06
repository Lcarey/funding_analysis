W = wget --continue 

dl_abs:
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2019.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2018.zip 
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2017.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2016.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2015.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2014.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2013.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2012.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2011.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2010.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2009.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2008.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2007.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2006.zip 
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2005.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2004.zip &
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2003.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2002.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2001.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJABS_C_FY2000.zip

dl_data:
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2019.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2018.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2017.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2016.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2015.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2014.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2013.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2012.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2011.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2010.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2009.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2008.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2007.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2006.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2005.zip
	$W https://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2004.zip

unzip:
	parallel unzip -f :::  *.zip
	parallel dos2unix :::  *.csv

