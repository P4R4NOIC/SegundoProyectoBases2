

def mapReduce():
run_cmd(['python3', 'nameMapr.py', '-r', 'hadoop', 'hdfs:///ruta/del/input', '--output-dir', 'outputMapR', '--no-output'])
return


  hdfs dfs -get hdfs:///user/root/outputMapR/part-* /outputMapR

  hdfs dfs -put /dataFromWeb/data.json datajson