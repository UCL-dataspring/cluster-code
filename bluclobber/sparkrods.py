import pyspark
import requests

def get_streams(downsample=1, source="oids.txt", app="iRodsSpark"):


    sc = pyspark.SparkContext(appName=app)

    oids = map(lambda x: x.strip(), list(open('oids.txt')))

    rddoids = sc.parallelize(oids)
    down = rddoids.sample(False, 1.0 / downsample )

    streams = down.map(lambda x:
                       requests.get('http://arthur.rd.ucl.ac.uk/objects/'+x,
                       stream=True).raw)
    return streams
